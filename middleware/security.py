from fastapi import HTTPException
from db.supabase import supabase

def verify_token(token: str):
  try:
    response = supabase.auth.get_user(token)
    return response.user
  except Exception as e:
    print("Error:", str(e))  
    raise HTTPException(status_code=401, detail="Invalid token")