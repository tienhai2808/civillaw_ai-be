from fastapi import APIRouter, HTTPException, Depends
from schemas.question import Question
from schemas.response import Response
from services.rag_service import find_relevant_laws
from services.ai_service import get_gemini_response
from controllers.chat import *
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/api/chat", response_model=Response)
async def ask_question(question: Question, user=Depends(get_current_user)):
    if not question.message.strip():
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống!")

    save_question(user.id, question.message)
    
    relevant_laws = find_relevant_laws(question.message)
    answer = get_gemini_response(question.message, relevant_laws)
    
    answer_relevant_laws = [
            {
                "article": law["article"],
                "content": law["content"],
                "similarity_score": round(law["similarity"], 2)
            }
            for law in relevant_laws
        ]

    save_answer(user.id, answer, answer_relevant_laws)
    
    response = {
        "question": question.message,
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
