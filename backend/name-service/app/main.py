from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
from typing import Optional
from .generator import NameGenerator

app = FastAPI(
    title="Name Generator Service",
    description="Service for generating unique usernames",
    version="1.0.0"
)

class GenerateNameRequest(BaseModel):
    prefix: Optional[str] = None
    style: Optional[str] = "default"  # default, funny, serious

class GenerateNameResponse(BaseModel):
    username: str
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate", response_model=GenerateNameResponse)
async def generate_name(request: GenerateNameRequest):
    try:
        generator = NameGenerator()
        username = generator.generate(
            prefix=request.prefix,
            style=request.style
        )
        return GenerateNameResponse(username=username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
