from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Legal QA API", description="API trả lời câu hỏi luật dân sự")
app.include_router(router)