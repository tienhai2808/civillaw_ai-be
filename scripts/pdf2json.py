import fitz 
import json
import re
import os

def extract_articles_from_pdf(pdf_path):
  doc = fitz.open(pdf_path)
  full_text = ""

  for page in doc:
    full_text += page.get_text("text") + "\n"

  articles = []
  lines = full_text.splitlines()  # Tách thành từng dòng
  current_article = None
  current_content = []

  for line in lines:
    line = line.strip()
    if not line:  # Bỏ qua dòng trống
      continue
    
    # Kiểm tra xem dòng có bắt đầu bằng "Điều" không
    if re.match(r'^Điều \d+\.', line):
      # Nếu đã có điều luật trước đó, lưu lại
      if current_article:
        articles.append({
          "article": current_article,
          "content": "\n".join(current_content).strip()
        })
      # Bắt đầu điều luật mới
      current_article = line
      current_content = []
    else:
      # Nếu đang trong tiêu đề (chưa gặp dấu chấm cuối)
      if current_article and not current_article.endswith('.'):
        current_article += " " + line
      # Nếu đã qua tiêu đề, thêm vào nội dung
      elif current_article:
        current_content.append(line)

  # Lưu điều luật cuối cùng
  if current_article and current_content:
    articles.append({
      "article": current_article,
      "content": "\n".join(current_content).strip()
    })

  return articles

def save_to_json(articles, output_path):
  with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
  current_dir = os.path.dirname(os.path.abspath(__file__))
  data_dir = os.path.join(current_dir, "..", "data")

  pdf_path = os.path.join(data_dir, "legal_dansu_2.pdf")
  output_path = os.path.join(data_dir, "laws.json")
    
  articles = extract_articles_from_pdf(pdf_path)
  save_to_json(articles, output_path)
  print("Đã trích xuất xong, file JSON lưu tại:", output_path)