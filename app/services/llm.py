from abc import ABC, abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings


# contract that any LLM implementation must follow
class BaseLLMService(ABC):

    # return the LangChain LLM object used inside chains
    @abstractmethod
    def get_llm(self):
        pass

    # send a prompt string, get a plain text answer back
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


# Gemini implementation using LangChain
class GeminiLLMService(BaseLLMService):

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=get_settings().gemini_model_name)

    # returns the LLM object for use in LangChain chains
    def get_llm(self):
        return self.llm

    # sends a prompt to Gemini and returns the text response
    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content
