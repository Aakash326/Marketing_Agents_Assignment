"""
OpenAI LLM client configuration using LangChain.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.7) -> ChatOpenAI:
    """
    Get an OpenAI LLM client instance.

    Args:
        model: OpenAI model name (default: gpt-4o-mini)
        temperature: Sampling temperature (default: 0.7)

    Returns:
        ChatOpenAI instance configured with API key
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key
    )


def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Simple function to call the LLM with a prompt.

    Args:
        prompt: The text prompt to send to the LLM
        model: OpenAI model name (default: gpt-4o-mini)

    Returns:
        The LLM's response as a string
    """
    llm = get_llm(model=model)
    response = llm.invoke(prompt)
    return response.content
