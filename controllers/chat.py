from db.supabase import supabase

def save_question(user_id: str, message: str):
  data = {"user": user_id, "message": message}
  response = supabase.table("questions").insert(data).execute()
  return response

def save_answer(user_id: str, message: str, relevant_laws):
  data = {"user": user_id, "message": message, "relevant_laws": relevant_laws}
  response = supabase.table("answers").insert(data).execute()  
  return response