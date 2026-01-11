from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.rountes import router
from database import engine, Base

# This line creates the database tables automatically if they don't exist
# It uses the definitions found in your database.py file
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Khmer POS Tagging API",
    description="A BiLSTM-powered API for Khmer Word Segmentation and POS Tagging",
    version="1.0.0"
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    """Root endpoint to check if the service is alive."""
    return {
        "message": "Khmer POS API is running",
        "docs": "/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    # When running locally without Docker:
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)