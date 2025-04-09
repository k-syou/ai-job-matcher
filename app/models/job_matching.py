# Pydantic 모델 (요청/응답)
from pydantic import BaseModel

class JobMatchingRequest(BaseModel):
    job_id: str
    user_info: dict

class JobMatchingResponse(BaseModel):
    """
        3가지 질문에 대한 답변을 각각 answer1, answer2, answer3 키값으로 json 형식으로 반환합니다.
    """
    answer1: str
    answer2: str
    answer3: str

__all__ = ["JobMatchingRequest", "JobMatchingResponse"]