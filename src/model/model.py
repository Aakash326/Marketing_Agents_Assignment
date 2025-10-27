"""
Model client configuration for AutoGen agents.
Provides a centralized way to create and configure OpenAI model clients.
"""

import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
load_dotenv()


def get_model_client(model_name: str = "gpt-4o-mini"):
    """
    Create and return an OpenAI model client for use with AutoGen agents.

    Args:
        model_name: The name of the OpenAI model to use (default: "gpt-4o-mini")

    Returns:
        OpenAIChatCompletionClient: Configured model client

    Raises:
        ValueError: If OPENAI_API_KEY is not set in environment
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it in your .env file or environment."
        )

    return OpenAIChatCompletionClient(
        model=model_name,
        api_key=api_key
    )


# Create a default model client that agents can import directly
try:
    model_client = get_model_client()
except ValueError as e:
    print(f"Warning: Could not create default model client: {e}")
    model_client = None
