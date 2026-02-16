"""
LangGraph workflow builder for the Sidekick system.
"""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
import nest_asyncio

from state import State
from agents import worker, evaluator, worker_router, route_based_on_evaluation


# Apply nest_asyncio for Playwright compatibility
nest_asyncio.apply()


# Initialize Playwright browser tools
def setup_tools(headless: bool = False):
    """
    Set up Playwright browser tools.
    
    Args:
        headless: Whether to run browser in headless mode
        
    Returns:
        List of Playwright tools
    """
    async_browser = create_async_playwright_browser(headless=headless)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    return toolkit.get_tools()


# Get tools
tools = setup_tools(headless=False)  # Set to True for production

# Initialize worker LLM with tools
worker_llm = ChatOpenAI(model="gpt-4o-mini")
worker_llm_with_tools = worker_llm.bind_tools(tools)


def build_graph():
    """
    Build and compile the Sidekick LangGraph workflow.
    
    Graph structure:
        START → worker → [has tool calls?]
                   ↓ yes → tools → worker
                   ↓ no
               evaluator → [success/stuck?]
                   ↓ yes → END
                   ↓ no (with feedback)
                 worker (retry with improvements)
    
    Returns:
        Compiled LangGraph with checkpointing enabled
    """
    # Create graph builder
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node("worker", worker)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    graph_builder.add_node("evaluator", evaluator)

    # Add edges
    graph_builder.add_conditional_edges(
        "worker",
        worker_router,
        {"tools": "tools", "evaluator": "evaluator"}
    )
    graph_builder.add_edge("tools", "worker")
    graph_builder.add_conditional_edges(
        "evaluator",
        route_based_on_evaluation,
        {"worker": "worker", "END": END}
    )
    graph_builder.add_edge(START, "worker")

    # Compile with memory
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    
    return graph


# Build the graph (singleton)
sidekick_graph = build_graph()
