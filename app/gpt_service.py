from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.settings import OPENAI_API_KEY

llm = ChatOpenAI(temperature=0.2, model="gpt-4", openai_api_key=OPENAI_API_KEY)


def analyze_job_with_llm(prompt: str) -> str:
    messages = [
        SystemMessage(content="너는 채용공고와 사용자 정보를 분석하는 전문가야."),
        HumanMessage(content=prompt),
    ]
    response = llm(messages)
    return response.content
