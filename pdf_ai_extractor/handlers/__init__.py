from typing import Optional, Union, Dict
from .base_handler import BaseHandler
from .local_handler import LocalHandler
from .openai_handler import OpenAIHandler
from .xai_handler import XAIHandler
from .huggingface_handler import HuggingFaceHandler

__all__ = [
    "BaseHandler",
    "LocalHandler",
    "OpenAIHandler",
    "XAIHandler",
    "HuggingFaceHandler",
    "create_handler"
]

def create_handler(
    handler_type: str = "local",
    config: Optional[Dict] = None
) -> BaseHandler:
    """
    Factory function: Create a handler instance based on the specified type.

    Args:
        handler_type (str): Handler type, can be "local", "openai", "xai", "huggingface"
        config (Dict, optional): Configuration parameters for the handler

    Returns:
        BaseAIProvider: Handler instance

    Raises:
        ValueError: When the specified handler type does not exist
    """
    config = config or {}
    
    handlers = {
        "local": lambda: LocalHandler(),
        "openai": lambda: OpenAIHandler(api_key=config.get("api_key")),
        "xai": lambda: XAIHandler(api_key=config.get("api_key")),
        "huggingface": lambda: HuggingFaceHandler(
            model_name=config.get("model_name", "facebook/bart-large-cnn")
        )
    }
    
    handler_creator = handlers.get(handler_type.lower())
    if not handler_creator:
        raise ValueError(
            f"Unknown handler type: {handler_type}. "
            f"Available types: {', '.join(handlers.keys())}"
        )
    
    return handler_creator()
