import os
import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Import the predictor and the database session getter
from inference.predictor import POSPredictor
from database import get_db, PredictionHistory  # We will define these in a separate file

router = APIRouter()

# --- 1. Define Request/Response Schemas ---
class TextRequest(BaseModel):
    text: str

class WordTag(BaseModel):
    word: str
    tag: str

class PredictionResponse(BaseModel):
    tokens: List[WordTag]

# --- 2. Initialize the Predictor (Singleton Pattern) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    predictor = POSPredictor(
        model_path=os.path.join(BASE_DIR, "model", "model1_POS.pt"),
        char_map=os.path.join(BASE_DIR, "model", "char2idx.json"),
        pos_map=os.path.join(BASE_DIR, "model", "pos2idx.json")
    )
except Exception as e:
    print(f"CRITICAL ERROR: Could not initialize model. {e}")
    predictor = None

# --- 3. Define the Endpoint ---
@router.post("/predict", response_model=PredictionResponse)
async def predict_pos(request: TextRequest, db: Session = Depends(get_db)):
    """
    Receives raw text, runs BiLSTM inference, saves to DB, and returns results.
    """
    if not predictor:
        raise HTTPException(status_code=500, detail="Model not loaded on server.")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        # 1. Run inference
        raw_results = predictor.predict(request.text)

        results = []
        for r in raw_results:
            results.append({
                "word": r["word"],
                "tag": r["tag"] or "O"
            })
        
        # 2. Save to Database (PostgreSQL)
        # results is a list of dicts, we store it as a JSON string
        new_history = PredictionHistory(
            input_text=request.text,
            prediction_output=json.dumps(results) 
        )
        db.add(new_history)
        db.commit()
        
        # 3. Return results to Frontend
        return {"tokens": results}
    
    except Exception as e:
        db.rollback() # Undo DB changes if something fails
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    """Optional: Fetch the last 10 predictions from the database."""
    history = db.query(PredictionHistory).order_by(PredictionHistory.id.desc()).limit(10).all()
    return history

@router.get("/health")
async def health_check():
    return {"status": "online", "model_loaded": predictor is not None}