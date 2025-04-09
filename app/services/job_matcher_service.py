# 직업 매칭 서비스
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import OllamaEmbeddings
from app.core.config import settings
from app.models import JobMatchingRequest, JobMatchingResponse

# from ..core import settings
# from ..models import JobMatchingRequest, JobMatchingResponse
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnableConfig
import json

llm = ChatOpenAI(
    model=settings.openai.model,
    temperature=settings.openai.temperature,
    api_key=settings.openai.api_key,
)

embeddings = OllamaEmbeddings(
    model=settings.ollama_embedding.model,
    temperature=settings.ollama_embedding.temperature,
)
prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a professional career consultant specialized in job matching analysis. Provide clear and concise evaluations. IMPORTANT: All your answers must be written in Korean."
        ),
        ("human", "Job Posting: {retrieved_data}"),
        ("human", "Candidate Information: {user_info}"),
        (
            "human",
            "NOTE: If the Candidate Information contains a 'name' field, refer to the candidate using that name followed by '님'. For example, if 'name' is 'John', address as 'John님' instead of a generic term."
        ),
        (
            "human",
            "Based on the job posting and the candidate's information, please answer the following questions:"
        ),
        (
            "human",
            "Q1. Provide a concise summary of the candidate's strengths, along with the percentage of overall requirements that are met."
        ),
        (
            "human",
            "Q2. Provide a concise summary of the candidate's weaknesses, along with the percentage of overall requirements that are not met."
        ),
        (
            "human",
            "Q3. Summarize your recommendations for improvements and the areas the candidate should prepare for, within 300 characters."
        ),
    ]
)


def llm_search(request: JobMatchingRequest):
    """
    채용 공고 ID 와 개인 정보가 주어지면,
    채용 공고에 적합한 사람인지 분석해서 결과를 반환합니다.
    """

    # Pinecone 클라이언트 및 인덱스 초기화
    pc = Pinecone(api_key=settings.pinecone.api_key)
    index = pc.Index(settings.pinecone.index_name)
    vector_db = PineconeVectorStore(index=index, embedding=embeddings)

    # request에서 전달된 특정 키값(job_id)을 사용하여 데이터 검색
    job_key = request.job_id  # JobMatchingRequest에 job_id 필드가 있다고 가정
    search_kwargs = {"k": 1, "filter": {"job_id": job_key}}
    results = vector_db.similarity_search(query="", **search_kwargs)

    # 검색 결과가 있으면 첫 번째 결과의 컨텐츠 활용, 없으면 빈 문자열 사용
    retrieved_data = results[0].page_content if results else ""

    # runnable_config = RunnableConfig()
    structured_llm = llm.with_structured_output(JobMatchingResponse)
    # 프롬프트와 LLM을 연결한 체인을 이용해 응답 생성
    chain = prompt | structured_llm

    str_user_info = '\n'.join(f"{k}: {v}" for k, v in request.user_info.items())
    response_text = chain.invoke(
        {"user_info": str_user_info, "retrieved_data": retrieved_data}
    )
    return response_text


if __name__ == "__main__":
    user_info = """
    sample_user_info = {
    "skills": "Python, Django 경험",
    "experience_years": "3",
    "entry_label": "경력",
    "salary": "5000만원",
    "location": "서울",
    "benefits": "식대, 복지포인트",
    "target_position": "백엔드 개발자",
    "certifications": "정보처리기사, SQLD",
    "languages": "영어",
}
    """
    request = JobMatchingRequest(user_info=user_info, job_id="job001")
    response = llm_search(request)
    print(response)
