from fastapi import FastAPI
from app.schemas import UserInfo
from app.job_fetcher import fetch_job_posting
from app.prompt_builder import build_prompt
from app.gpt_service import analyze_job_with_llm

app = FastAPI()


@app.post("/analyze-job")
def analyze_job(user: UserInfo):
    job_posting = fetch_job_posting(user.job_id)
    prompt = build_prompt(job_posting, user.model_dump())
    result = analyze_job_with_llm(prompt)
    return {"result": result}
