# FastAPI chatbot API
from fastapi import APIRouter
from app.services.job_matcher_service import llm_search, JobMatchingRequest

router = APIRouter()


@router.post("/")
def job_matching(request: JobMatchingRequest):
    response = llm_search(request)
    return {"message": "v1 job_matching", "response": response}
