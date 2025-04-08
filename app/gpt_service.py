from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage
# from app.settings import OPENAI_API_KEY
from langchain_chroma import Chroma
import json, os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.2, model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY
)
# embedding_llm = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
embedding_llm = OllamaEmbeddings(model="nomic-embed-text")
def analyze_job_with_llm(prompt: str) -> str:
    messages = [
        SystemMessage(content="너는 채용공고와 사용자 정보를 분석하는 전문가야."),
        HumanMessage(content=prompt),
    ]
    response = llm(messages)
    return response.content


def analyze_job_with_llm(
    job_posting: str, user_info: dict, request_message: str
) -> str:
    system_message = SystemMessage(
        content="You are an AI expert who provides consulting on recruiting new and experienced developers. You must analyze job postings based on the user's capabilities and desired conditions, identify the conditions that are met and those that are lacking, and suggest appropriate career growth directions. In the case of new recruits, they may lack practical experience, so please structure your feedback considering their growth potential and willingness to learn. Your answers must be written in Korean."
    )
    job_posting_message = HumanMessage(content="Job Posting Data:\n" + job_posting)
    formatted_user_info = "\n".join([f"{key}: {value}" for key, value in user_info.items()])
    user_info_message = HumanMessage(content="User Info:\n" + formatted_user_info)
    request_message = HumanMessage(content=request_message)

    messages = [system_message, job_posting_message, user_info_message, request_message]
    response = llm.invoke(messages)
    return response.content


def initialize_vector_store(job_postings: list[dict]):
    embedding_llm = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    vector_db = Chroma(embedding_function=embedding_llm, persist_directory="db/job_postings")
    # 기존 vector_db가 존재하는지 확인
    if os.path.exists("db/job_postings"):
        for job in job_postings:
            add_job_posting_if_not_exists(vector_db, job)
    else:
        vector_db = Chroma.from_texts(
            texts=[job['content'] for job in job_postings],
            embedding=embedding_llm,
            metadatas=[{'job_id': job['job_id'], 'title': job['title']} for job in job_postings],
            collection_name="job_postings",
            persist_directory="db/job_postings",
        )
    
    return vector_db


def get_job_posting_text(vector_db:Chroma, job_id: str):
    results = vector_db.similarity_search(query="", k=1, filter={"job_id": job_id})
    if results:
        return results[0].page_content
    else:
        return None


def add_job_posting_if_not_exists(vector_db: Chroma, job_posting: dict):
    job_id = job_posting['job_id']
    existing_job = vector_db.similarity_search(query="", k=1, filter={"job_id": job_id})
    
    if not existing_job:
        print("새로운 데이터 추가")
        # 새로운 데이터 추가
        vector_db.add_texts(
            texts=[job_posting['content']],
            metadatas=[{'job_id': job_id, 'title': job_posting['title']}]
        )


if __name__ == "__main__":
    read_json = open("app/text_data/job_posting.json", "r", encoding="utf-8")
    job_postings = json.load(read_json)
    vector_db = initialize_vector_store(job_postings)
    job_posting_text = get_job_posting_text(vector_db, "job001")
    sample_user_info = {
        "skills": "Python, Django 경험",
        "experience_years": "3",
        "entry_label": "경력",
        "salary": "5000만원",
        "location": "서울",
        "benefits": "식대, 복지포인트",
        "target_position": "백엔드 개발자",
        "certifications": "정보처리기사, SQLD",
        "languages": "영어"
    }
    job_id = "job001"
    english_request_text = (
        "Please analyze the above job posting based on the provided user information. "
        "Identify the matching qualifications, missing qualifications, and suggest at least three ways to improve skills. "
        "Also, provide a brief summary (within 300 characters)."
    )
    result = analyze_job_with_llm(job_posting_text, sample_user_info, english_request_text)
    print(result)
