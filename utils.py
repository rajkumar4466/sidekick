"""
Utility functions for the Sidekick system.
"""
from typing import List, Any
from langchain_core.messages import HumanMessage, AIMessage


def format_conversation(messages: List[Any]) -> str:
    """
    Format the message history into a readable conversation string.
    
    Args:
        messages: List of LangChain message objects
        
    Returns:
        Formatted string representation of the conversation
    """
    conversation = "Conversation history:\n\n"
    for message in messages:
        if isinstance(message, HumanMessage):
            conversation += f"User: {message.content}\n"
        elif isinstance(message, AIMessage):
            text = message.content or "[Tools use]"
            conversation += f"Assistant: {text}\n"
    return conversation
