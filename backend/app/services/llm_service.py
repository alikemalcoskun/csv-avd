# https://python.langchain.com/docs/integrations/chat/openai/
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/json/
from langchain_core.output_parsers import JsonOutputParser

import logging
from dotenv import load_dotenv
import os



class LLMService:
    def __init__(self):
        self.model = self._build_model()
        self.json_output_parser = JsonOutputParser()

    def _build_model(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=OPENAI_API_KEY,
        )

    def invoke(self, prompt: ChatPromptTemplate, is_response_json=False, **kwargs):
        messages = prompt.invoke(**kwargs)
        response = self.model.invoke(messages)
        response_content = response.content

        if is_response_json:
            return self.json_output_parser.parse(response_content)
        return response_content




class LLMServiceMock:
    def __init__(self):
        pass

    def invoke(self, prompt: ChatPromptTemplate, is_response_json=False, **kwargs):
        logging.info(f"Mocking LLMService invoke with kwargs: {kwargs} and is_response_json: {is_response_json}")
        return {
            "type": "mock",
        }