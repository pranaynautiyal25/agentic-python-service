from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pipeline import run_pipeline, human_input_pipeline
from app.schemas.input_models import UserRequest, HumanInputRequest
from app.schemas.output_models import FinalResponse

app = FastAPI(
    title="Meeting Agent API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Meeting Agent API is running"}


@app.post("/run", response_model=FinalResponse)
def run_agent(payload: UserRequest):
    try:
        return run_pipeline(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/human-input", response_model=FinalResponse)
def human_input_agent(payload: HumanInputRequest):
    try:
        return human_input_pipeline(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))