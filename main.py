import json
import os
import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
import google.generativeai as genai
import logging
from underthesea import word_tokenize
from rag.embeddings import TransformersEmbeddings
from decouple import config

GEMINI_API_KEY = config('GEMINI_API_KEY')
GEMINI_MODEL_NAME = config('GEMINI_MODEL_NAME')

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Thêm biến môi trường để tránh lỗi OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

genai.configure(api_key=GEMINI_API_KEY) 
ai_model = genai.GenerativeModel(GEMINI_MODEL_NAME)

embedding = TransformersEmbeddings()

current_dir = os.path.dirname(os.path.abspath(__file__))
vector_store = FAISS.load_local(
  os.path.join(current_dir, "rag/faiss"), 
  embedding,
  allow_dangerous_deserialization=True
)

laws_json_path = os.path.join(current_dir, "rag/data", "laws.json")
if not os.path.exists(laws_json_path):
  raise FileNotFoundError(f"laws.json not found at {laws_json_path}")

with open(laws_json_path, "r", encoding="utf-8") as f:
  laws_data = json.load(f)
    
laws_dict = {law["article"]: law["content"] for law in laws_data}  

app = FastAPI(title="Legal QA API", description="API trả lời câu hỏi luật dân sự")

class Question(BaseModel):
  text: str

def find_relevant_laws(question: str, min_similarity: float = 0.8, top_k: int = 3) -> List[dict]:
  tokenized_question = word_tokenize(question, format="text")
  logger.info(f"Tokenized question: {tokenized_question}")
    
  docs_with_scores = vector_store.similarity_search_with_score(tokenized_question, k=top_k)
  if not docs_with_scores:
    logger.warning(f"No relevant laws found for question: {question}")
    return []

  relevant_laws = []
  seen_articles = set()  # Tránh trùng lặp điều luật
  for doc, distance in docs_with_scores:
    similarity = 1 - (distance / 2)  # Chuyển distance L2 thành similarity
    article = doc.metadata["article"]
    if similarity >= min_similarity and article not in seen_articles:
      seen_articles.add(article)
      full_content = laws_dict.get(article, doc.page_content) 
      relevant_laws.append({
        "article": article,
        "content": full_content,
        "similarity": similarity
      })
    else:
      logger.debug(f"Skipping law {article} - similarity {similarity} < {min_similarity}")
    
  logger.info(f"Found {len(relevant_laws)} relevant laws for question: {question}")
  return relevant_laws

def get_gemini_response(question: str, relevant_laws: List[dict]) -> str:
  """Tạo câu trả lời từ Gemini với các điều luật liên quan."""
  if not relevant_laws:
    return (
      "Rất tiếc, tôi không tìm thấy điều luật nào liên quan đến câu hỏi của bạn trong dữ liệu hiện tại. "
      "Bạn có thể tham khảo thêm tại https://thuvienphapluat.vn/van-ban/Quyen-dan-su/Bo-luat-dan-su-2015-296215.aspx"
    )
    
  laws_text = "\n".join(
    [f"- {law['article']}: {law['content']} (độ tương đồng: {law['similarity']:.2f})" 
        for law in relevant_laws]
  )

  prompt = (
    "Giả sử bạn tên là Luật, một luật sư chuyên về luật dân sự Việt Nam với hơn 5 năm kinh nghiệm, hãy trả lời câu hỏi dựa trên các điều luật được tôi cung cấp dưới đây."
    "Cung cấp câu trả lời chính xác, ngắn gọn, dễ hiểu, đúng trọng tâm và chỉ dựa vào các điều luật liên quan."
    "Nếu cần, giải thích ngắn gọn cách áp dụng điều luật vào câu hỏi.\n\n"
    f"Câu hỏi: {question}\n\n"
    f"Điều luật liên quan:\n{laws_text}\n\n"
    "Trả lời:"
  )
    
  logger.debug(f"Prompt sent to Gemini:\n{prompt}")
  try:
    response = ai_model.generate_content(prompt)
    return response.text.strip()
  except Exception as e:
    logger.error(f"Error calling Gemini API: {str(e)}")
    return "Có lỗi xảy ra khi tạo câu trả lời, vui lòng thử lại sau."

@app.post("/ask", response_model=dict)
async def ask_question(question: Question):
  """API endpoint để trả lời câu hỏi pháp luật."""
  try:
    if not question.text.strip():
      raise HTTPException(status_code=400, detail="Câu hỏi không được để trống!")
    
    logger.info(f"Received question: {question.text}")
    relevant_laws = find_relevant_laws(question.text, min_similarity=0.8, top_k=3)
    answer = get_gemini_response(question.text, relevant_laws)
    
    response = {
      "question": question.text,
      "answer": answer,
      "relevant_laws": [
        {
          "article": law["article"],
          "content": law["content"],
          "similarity_score": round(law["similarity"], 2)
        }
        for law in relevant_laws
      ]
    }
    return response
  except Exception as e:
    logger.error(f"Error processing question: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")