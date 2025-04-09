import faiss
print(faiss.__version__)
print(faiss.get_num_gpus())  # Nếu trả về 0 thì Faiss đang chạy bản CPU
