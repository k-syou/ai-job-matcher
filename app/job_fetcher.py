import requests
from app.settings import JOB_API_BASE

def fetch_job_posting(job_id: str):
    url = f"{JOB_API_BASE}{job_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("채용공고를 불러오지 못했습니다.")
    
