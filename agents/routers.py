"""
Routing logic for conditional edges in the graph.
"""
from state import State


def worker_router(state: State) -> str:
    """
    Route after the worker node.
    
    If the worker made tool calls, route to the tools node.
    Otherwise, route to the evaluator for judgment.
    
    Args:
        state: Current graph state
        
    Returns:
        Next node name: "tools" or "evaluator"
    """
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return "evaluator"


def route_based_on_evaluation(state: State) -> str:
    """
    Route after the evaluator node.
    
    If success criteria met or user input needed, end the workflow.
    Otherwise, loop back to worker for another attempt.
    
    Args:
        state: Current graph state
        
    Returns:
        Next node name: "END" or "worker"
    """
    if state["success_criteria_met"] or state["user_input_needed"]:
        return "END"
    else:
        return "worker"
