"""
Azure OpenAI client setup using Azure Identity for authentication.
"""

import os

import azure.identity
import openai


def get_client() -> openai.OpenAI:
    """
    Create an Azure OpenAI client using DefaultAzureCredential.
    
    Requires environment variables:
    - AZURE_OPENAI_ENDPOINT: The Azure OpenAI endpoint URL
    - AZURE_OPENAI_CHAT_DEPLOYMENT: The deployment name for chat completions
    """
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )
    
    client = openai.AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21",
    )
    
    return client


def get_model_name() -> str:
    """Get the deployment name from environment."""
    return os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]


def chat_completion(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 8000,
) -> str:
    """
    Send a chat completion request to Azure OpenAI.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
        
    Returns:
        The assistant's response text
    """
    client = get_client()
    model = get_model_name()
    
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
    )
    
    return response.choices[0].message.content
