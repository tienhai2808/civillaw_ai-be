from decouple import config

class Settings:
  GEMINI_API_KEY = config("GEMINI_API_KEY")
  GEMINI_MODEL_NAME = config("GEMINI_MODEL_NAME")
  SUPABASE_URL = config("SUPABASE_URL")
  SUPABASE_ROLE_KEY = config("SUPABASE_ROLE_KEY")
  EMBEDDING_MODEL_NAME = config("EMBEDDING_MODEL_NAME")

settings = Settings()