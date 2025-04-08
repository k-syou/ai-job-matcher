from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig, chain

import os, json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
index_name = "job-postings"
# embedding_llm = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

vector_store = PineconeVectorStore(
    pinecone_api_key=PINECONE_API_KEY,
    index_name=index_name,
    embedding=embeddings_model,
)
# read_json = open("app/text_data/job_posting.json", "r", encoding="utf-8")
# job_postings = json.load(read_json)
# vector_db = Chroma(collection_name="job_postings", embedding_function=embeddings_model, persist_directory="db/job_postings")
# print(job_postings[0])
# vector_store.from_texts(
#     index_name=index_name,
#     texts=[job_postings[0]["content"]],
#     metadatas=[
#         {"job_id": job_postings[0]["job_id"], "title": job_postings[0]["title"]}
#     ],
#     embedding=embeddings_model,
# )
existing_job = vector_store.similarity_search(
    query="",
    filter={"job_id": "job001"},
    k=1,
)
# print(existing_job)


@tool
def search_job_posting(job_id: str) -> str:
    """Search for a job posting by job ID"""
    job_posting = vector_store.similarity_search(
        query="",
        filter={"job_id": job_id},
        k=1,
    )
    if len(job_posting) > 0:
        return job_posting[0].page_content
    return [Document(page_content=f"해당 id({job_id})의 채용 공고가 없습니다.")]


prompt = ChatPromptTemplate(
    [
        ("system", f"You are a helpful assistant that can search for job postings."),
        ("human", "job posting: {job_posting}"),
        ("human", "user info: {user_info}"),
        ("human", "answer in korean"),
        ("human",
            "Please analyze the above job posting based on the provided user information. "
        ),
        ("human",
            "Identify the matching qualifications, missing qualifications, and suggest at least three ways to improve skills. "
        ),
        ("human", "Also, provide a brief summary (within 300 characters)."),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
llm_with_tools = llm.bind_tools([search_job_posting])
llm_chain = prompt | llm_with_tools


@chain
def job_matching_chain(inputs: dict, config: RunnableConfig) -> str:
    job_posting = inputs.get("job_posting")
    user_info = inputs.get("user_info")
    user_info_str = json.dumps(user_info)
    input_ = {"job_posting": job_posting, "user_info": user_info_str}
    ai_msg = llm_chain.invoke(input_, config)

    tool_messages = []
    for tool_call in ai_msg.tool_calls:
        if tool_call["name"] == "search_job_posting":
            tool_message = search_job_posting.invoke(tool_call, config=config)
            tool_messages.append(tool_message)
    # print(tool_messages)
    return llm_chain.invoke(
        {**input_, "messages": [ai_msg, *tool_messages]}, config=config
    )


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
response = job_matching_chain.invoke(
    {"job_posting": "job001", "user_info": sample_user_info}
)
print(response)
