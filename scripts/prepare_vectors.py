import os
import json
import torch
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import InMemoryDocstore
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)
from utils.embeddings import TransformersEmbeddings

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

embedding = TransformersEmbeddings()


laws_json_path = os.path.join(project_root, "data", "laws.json")
vector_store_path = os.path.join(project_root, "vector_store")

with open(laws_json_path, "r", encoding="utf-8") as f:
  laws_data = json.load(f)

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=256,
  chunk_overlap=64,
  separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
)

documents = []
for law in tqdm(laws_data, desc="Processing laws"):
  full_text = f"{law['article']}: {law['content']}"
  chunks = text_splitter.split_text(full_text)
  for chunk in chunks:
    documents.append(Document(page_content=chunk, metadata={"article": law["article"]}))

dimension = 1024 
index = faiss.IndexHNSWFlat(dimension, 32)
index.hnsw.efConstruction = 200
index.hnsw.efSearch = 100

batch_size = 16
vector_store = None
for i in tqdm(range(0, len(documents), batch_size), desc="Building FAISS index"):
  batch_docs = documents[i:i + batch_size]
  batch_texts = [doc.page_content for doc in batch_docs]
  batch_metadatas = [doc.metadata for doc in batch_docs]
  embeddings = embedding.embed_documents(batch_texts)

  if i == 0:
    vector_store = FAISS(
      embedding_function=embedding,
      index=index,
      docstore=InMemoryDocstore({}),
      index_to_docstore_id={}
    )
    vector_store.add_embeddings(
      text_embeddings=list(zip(batch_texts, embeddings)),
      metadatas=batch_metadatas
    )
  else:
    # Thêm các batch tiếp theo
    vector_store.add_embeddings(
      text_embeddings=list(zip(batch_texts, embeddings)),
      metadatas=batch_metadatas
    )
  torch.cuda.empty_cache() if torch.cuda.is_available() else None

# Lưu index
vector_store.save_local(vector_store_path)
print(f"✅ Đã lưu FAISS index vào thư mục {vector_store_path}")