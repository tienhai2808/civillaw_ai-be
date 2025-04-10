from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="Legal QA API", description="API trả lời câu hỏi luật dân sự")

origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép các origin này
    allow_credentials=True,
    allow_methods=["*"],    # Cho phép tất cả các phương thức (GET, POST, OPTIONS, v.v.)
    allow_headers=["*"],    # Cho phép tất cả các header
)

app.include_router(router)