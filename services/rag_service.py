import os
import json
from typing import List
from langchain_community.vectorstores import FAISS
from utils.embeddings import TransformersEmbeddings
from underthesea import word_tokenize

embedding = TransformersEmbeddings()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
vector_store_path = os.path.join(project_root, "vector_store")
laws_json_path = os.path.join(project_root, "data", "laws.json")
vector_store = FAISS.load_local(
  vector_store_path, 
  embedding,
  allow_dangerous_deserialization=True
)

with open(laws_json_path, "r", encoding="utf-8") as f:
  laws_data = json.load(f)
    
laws_dict = {law["article"]: law["content"] for law in laws_data}  

def find_relevant_laws(question: str, min_similarity: float = 0.8, top_k: int = 3) -> List[dict]:
  tokenized_question = word_tokenize(question, format="text")  
  docs_with_scores = vector_store.similarity_search_with_score(tokenized_question, k=top_k)
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
  return relevant_laws