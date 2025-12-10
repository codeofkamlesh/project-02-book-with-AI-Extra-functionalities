from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Physical AI & Humanoid Robotics RAG API",
    description="API for RAG chatbot, authentication, and personalization services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Physical AI & Humanoid Robotics RAG API"}

@app.get("/api/v1/status")
def health_check():
    return {"status": "healthy", "service": "rag-backend"}

# Include API routes
from api.v1.query import router as query_router
from api.v1.ingest import router as ingest_router
from api.v1.auth import router as auth_router

app.include_router(query_router, prefix="/api/v1", tags=["query"])
app.include_router(ingest_router, prefix="/api/v1", tags=["ingest"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))