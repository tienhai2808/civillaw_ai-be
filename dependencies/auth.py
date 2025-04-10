from fastapi import Header, HTTPException
from middleware.security import verify_token

def get_current_user(authorization: str = Header(...)):
  if not authorization.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="Invalid auth header")
  token = authorization.split(" ")[1]
  return verify_token(token)