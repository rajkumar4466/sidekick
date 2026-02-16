"""
State management for the Sidekick agent system.
"""
from typing import Annotated, TypedDict, List, Any, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class EvaluatorOutput(BaseModel):
    """Structured output from the evaluator agent."""
    feedback: str = Field(description="Feedback on the assistant's response")
    success_criteria_met: bool = Field(description="Whether the success criteria have been met")
    user_input_needed: bool = Field(description="True if more input is needed from the user, or clarifications, or the assistant is stuck")


class State(TypedDict):
    """
    The shared state that flows through the graph.
    
    - messages: Conversation history (uses reducer to accumulate)
    - success_criteria: What defines task completion
    - feedback_on_work: Evaluator's critique for improvement
    - success_criteria_met: Boolean flag for completion
    - user_input_needed: Boolean flag for human-in-the-loop
    """
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool
