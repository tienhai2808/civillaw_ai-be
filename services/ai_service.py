import google.generativeai as genai
from typing import List
from core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
ai_model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)

def get_gemini_response(question: str, relevant_laws: List[dict]) -> str:
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
        "Giả sử bạn tên là Luật, một luật sư chuyên về luật dân sự Việt Nam với hơn 5 năm kinh nghiệm, hãy trả lời câu hỏi dựa trên các điều luật được tôi cung cấp dưới đây và không cần phải chào tôi hay giới thiệu về bạn. "
        "Cung cấp câu trả lời chính xác, ngắn gọn, dễ hiểu, đúng trọng tâm và chỉ dựa vào các điều luật liên quan. "
        "Nếu cần, giải thích ngắn gọn cách áp dụng điều luật vào câu hỏi.\n\n"
        f"Câu hỏi: {question}\n\n"
        f"Điều luật liên quan:\n{laws_text}\n\n"
        "Trả lời:"
    )
    
    try:
        response = ai_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Có lỗi xảy ra khi tạo câu trả lời, vui lòng thử lại sau."