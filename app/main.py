from fastapi import FastAPI
from app.api import job_matcher_router
from app.services.job_matcher_service import llm_search, JobMatchingRequest

app = FastAPI()

app.include_router(job_matcher_router, prefix="/api/v1/job_matcher")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    