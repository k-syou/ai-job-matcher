# 설정 파일
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class OpenAIConfig(BaseSettings):
    api_key: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float


class OllamaEmbeddingConfig(BaseSettings):
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float


class PineconeConfig(BaseSettings):
    api_key: str
    environment: str
    index_name: str


class Settings(BaseSettings):
    openai: OpenAIConfig
    ollama_embedding: OllamaEmbeddingConfig
    pinecone: PineconeConfig


settings = Settings()

__all__ = ["settings"]
