from abc import ABC, abstractmethod
from urllib import response
from openai import OpenAI, AzureOpenAI
import os
from dotenv import load_dotenv



class Provider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def call(self, *args, **kwargs):
        """Abstract method to call the LLM provider."""
        pass



class OpenAiProvider(Provider):
    """OpenAI provider implementation."""
    
    def __init__(self):
        """Initialize OpenAI provider by reading credentials from .env."""
        self.client = self.init_openai_object()
    
    def init_openai_object(self) -> OpenAI:
        """Initialize and return OpenAI client object.
        
        Reads OPENAI_API_KEY from .env file.
        
        Returns:
            OpenAI: Initialized OpenAI client
        """
        api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME")
        return OpenAI(api_key=api_key)
    
    def call(self, messages: list) -> str:
        """Call the OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        response = {
            "content": response.choices[0].message.content,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return response



class AzureOpenAiProvider(OpenAiProvider):
    """Azure OpenAI provider implementation."""
    
    def init_openai_object(self) -> OpenAI:

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        
        return OpenAI(
            base_url=endpoint,
            api_key=api_key
        )


def get_provider() -> Provider:
    
    load_dotenv()
    provider_name = os.getenv("PROVIDER")
    if provider_name == "openai":
        return OpenAiProvider()
    elif provider_name == "azure":
        return AzureOpenAiProvider()
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
    
if __name__ == "__main__":
    provider = get_provider()
    print(type(provider))

    msgs=[
        {
            "role": "user",
            "content": "What is the capital of Egypt?",
        }
    ]
    print(provider.call(msgs))