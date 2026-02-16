"""
Main entry point for the Sidekick application.

Run this file to launch the Gradio UI.
"""
import gradio as gr
import uuid
from dotenv import load_dotenv

from graph import sidekick_graph


# Load environment variables
load_dotenv(override=True)


def make_thread_id() -> str:
    """Generate a unique thread ID for conversation tracking."""
    return str(uuid.uuid4())


async def process_message(message, success_criteria, history, thread):
    """
    Process a user message through the Sidekick graph.
    
    Args:
        message: User's task request
        success_criteria: How to judge task completion
        history: Chat history for UI display
        thread: Conversation thread ID
        
    Returns:
        Updated chat history with worker response and evaluator feedback
    """
    config = {"configurable": {"thread_id": thread}}

    state = {
        "messages": message,
        "success_criteria": success_criteria,
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False
    }
    
    # Run the graph
    result = await sidekick_graph.ainvoke(state, config=config)
    
    # Format messages for display
    user = {"role": "user", "content": message}
    reply = {"role": "assistant", "content": result["messages"][-2].content}
    feedback = {"role": "assistant", "content": result["messages"][-1].content}
    
    return history + [user, reply, feedback]


async def reset():
    """Reset the conversation and generate a new thread ID."""
    return "", "", None, make_thread_id()


def create_ui():
    """
    Create the Gradio UI for Sidekick.
    
    Returns:
        Gradio Blocks interface
    """
    with gr.Blocks(theme=gr.themes.Default(primary_hue="emerald")) as demo:
        gr.Markdown("""
        # 🤖 Sidekick Personal Co-worker
        
        Your autonomous assistant that can browse the web and complete tasks!
        
        **How to use:**
        1. Enter your task request
        2. Define success criteria (how to judge completion)
        3. Click "Go!" and watch Sidekick work autonomously
        
        Sidekick will loop until the task meets your criteria or asks for your help.
        """)
        
        thread = gr.State(make_thread_id())
        
        with gr.Row():
            chatbot = gr.Chatbot(label="Sidekick Conversation", height=400, type="messages")
        
        with gr.Group():
            with gr.Row():
                message = gr.Textbox(
                    show_label=False,
                    placeholder="Your request to your sidekick (e.g., 'Find the latest iPhone price on Apple's website')",
                    scale=4
                )
            with gr.Row():
                success_criteria = gr.Textbox(
                    show_label=False,
                    placeholder="What are your success criteria? (e.g., 'Must include model name and price in USD')",
                    scale=4
                )
        
        with gr.Row():
            reset_button = gr.Button("Reset", variant="stop", scale=1)
            go_button = gr.Button("Go!", variant="primary", scale=2)
        
        # Event handlers
        message.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
        success_criteria.submit(process_message, [message, success_criteria, chatbot, thread], [chatbot])
        go_button.click(process_message, [message, success_criteria, chatbot, thread], [chatbot])
        reset_button.click(reset, [], [message, success_criteria, chatbot, thread])
    
    return demo


def main():
    """Launch the Sidekick application."""
    print("🤖 Starting Sidekick Personal Co-worker...")
    print("📦 Loading graph and tools...")
    
    demo = create_ui()
    
    print("✅ Ready! Launching UI...")
    demo.launch(share=False)


if __name__ == "__main__":
    main()
