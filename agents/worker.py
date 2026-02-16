"""
Worker agent node - performs the actual task work.
"""
from typing import Dict, Any
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from state import State


# Initialize the worker LLM (will be bound with tools in graph.py)
worker_llm = ChatOpenAI(model="gpt-4o-mini")


def worker(state: State) -> Dict[str, Any]:
    """
    Worker node that attempts to complete the task.
    
    This agent:
    - Reads the success criteria
    - Uses tools (Playwright browser) to complete tasks
    - Incorporates feedback from previous attempts
    - Can ask clarifying questions when stuck
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated messages
    """
    system_message = f"""You are a helpful assistant that can use tools to complete tasks.
You keep working on a task until either you have a question or clarification for the user, or the success criteria is met.
This is the success criteria:
{state['success_criteria']}
You should reply either with a question for the user about this assignment, or with your final response.
If you have a question for the user, you need to reply by clearly stating your question. An example might be:

Question: please clarify whether you want a summary or a detailed answer

If you've finished, reply with the final answer, and don't ask a question; simply reply with the answer.
"""
    
    if state.get("feedback_on_work"):
        system_message += f"""
Previously you thought you completed the assignment, but your reply was rejected because the success criteria was not met.
Here is the feedback on why this was rejected:
{state['feedback_on_work']}
With this feedback, please continue the assignment, ensuring that you meet the success criteria or have a question for the user."""
    
    # Add or update the system message
    found_system_message = False
    messages = state["messages"]
    for message in messages:
        if isinstance(message, SystemMessage):
            message.content = system_message
            found_system_message = True
    
    if not found_system_message:
        messages = [SystemMessage(content=system_message)] + messages
    
    # Invoke the LLM with tools (bound in graph.py)
    # Note: This will be called with worker_llm_with_tools from graph context
    from graph import worker_llm_with_tools
    response = worker_llm_with_tools.invoke(messages)
    
    # Return updated state (messages will be appended via reducer)
    return {
        "messages": [response],
    }
