# Civil Law AI - Backend

A sophisticated AI-powered legal assistant built with FastAPI that provides intelligent responses to civil law questions. The system uses RAG (Retrieval Augmented Generation) with Google's Gemini model to provide accurate and context-aware legal information.

## 🚀 Features

- **AI-Powered Legal Assistant**: Utilizes Google's Gemini model for generating accurate legal responses
- **RAG Implementation**: Combines retrieval-based and generative approaches for improved accuracy
- **PDF Document Processing**: Converts legal documents to searchable format
- **Vector Search**: Uses FAISS for efficient similarity search in legal documents
- **Authentication**: Secure API endpoints with user authentication
- **Cross-Origin Support**: Configured CORS for frontend integration

## 🛠️ Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A Supabase account for database services
- Google AI API key for Gemini model access

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/civillaw_ai.git
   cd civillaw_ai/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=your_supabase_url
   SECRET_KEY=your_secret_key
   GOOGLE_API_KEY=your_google_ai_api_key
   ```

## 📚 Project Structure

```
backend/
├── api/               # API endpoints and route definitions
├── controllers/       # Business logic controllers
├── core/             # Core configurations and settings
├── data/             # Legal document storage (PDFs, JSON)
├── db/               # Database connection and models
├── dependencies/     # Authentication and dependency injection
├── middleware/       # Security and request/response middleware
├── schemas/          # Pydantic models for request/response
├── services/         # AI and RAG service implementations
├── utils/           # Utility functions and helpers
├── vector_store/    # FAISS index storage
└── scripts/         # Data processing scripts
```

## 🚀 Running the Application

### Development Server
```bash
uvicorn main:app --reload
```
The server will be available at http://127.0.0.1:8000

### Production Deployment
For production, use a production-grade ASGI server:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 📋 API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧪 Testing

Run the test suite:
```bash
cd test
pytest
```

## 📦 Dependencies

Key dependencies include:
- FastAPI: Web framework
- LangChain: RAG implementation
- Google Generative AI: Gemini model integration
- FAISS: Vector similarity search
- Supabase: Database and authentication
- Underthesea: Vietnamese text processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.