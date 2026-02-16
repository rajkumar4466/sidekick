# 🤖 Sidekick Personal Co-worker

An autonomous AI assistant that can browse the web, complete tasks, evaluate its own work, and loop until success criteria are met.

## 🎯 Features

- **Autonomous Task Completion**: Give it a task and success criteria, watch it work
- **Browser Automation**: Uses Playwright to interact with websites
- **Self-Evaluation**: Built-in evaluator agent that checks work quality
- **Self-Improvement Loop**: Refines work based on feedback until criteria met
- **Human-in-the-Loop**: Asks for help when stuck or needs clarification
- **Persistent Memory**: Maintains conversation context across interactions

## 🏗️ Architecture

### Multi-Agent System

1. **Worker Agent**: Does the actual work using browser tools
2. **Evaluator Agent**: Judges quality and provides feedback
3. **Self-Improvement Loop**: Worker → Evaluator → (feedback) → Worker → ...

### Workflow

```
START → Worker → [Uses tools?] → Tools → Worker
                      ↓ No
                  Evaluator → [Success?] → END
                      ↓ No (with feedback)
                    Worker (tries again)
```

## 📁 Project Structure

```
sidekick/
├── README.md              # This file
├── main.py                # Entry point (Gradio UI)
├── state.py               # State definitions (TypedDict + Pydantic)
├── graph.py               # LangGraph workflow builder
├── utils.py               # Helper functions
└── agents/
    ├── __init__.py
    ├── worker.py          # Worker agent node
    ├── evaluator.py       # Evaluator agent node
    └── routers.py         # Routing logic
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Virtual environment with dependencies installed
- OpenAI API key in `.env`

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/mithra_sundaram/Desktop/code/AI/projects/sidekick
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

### Running the Application

**Option 1: Direct Python execution**
```bash
cd /Users/mithra_sundaram/Desktop/code/AI/projects/sidekick
source .venv/bin/activate
python main.py
```

**Option 2: Use the run script**
```bash
./run.sh
```

## 📝 Usage Example

**Task:**
```
Message: "Find the price of the latest iPhone Pro on Apple's website"
Success Criteria: "Must include the model name and price in USD"
```

**Sidekick will:**
1. Navigate to apple.com using browser tools
2. Search for iPhone pricing information
3. Extract relevant details
4. Evaluator checks: Does it have model + USD price?
5. If yes → Done! If no → Try again with feedback

## 🔧 Configuration

### Headless Mode

By default, the browser runs in **visible mode** for debugging. To run headless:

**Edit `graph.py`:**
```python
tools = setup_tools(headless=True)  # Change False to True
```

### Model Selection

Both agents use `gpt-4o-mini` by default. To change:

**Edit `agents/worker.py` and `agents/evaluator.py`:**
```python
worker_llm = ChatOpenAI(model="gpt-4o")  # Use more powerful model
```

## 🎓 Key Concepts

### State Management

- **TypedDict**: Defines the state structure
- **Reducer** (`add_messages`): Accumulates messages instead of replacing
- **Boolean Flags**: Track completion and user input needs

### Structured Outputs

Uses Pydantic models to ensure evaluator returns consistent feedback:

```python
class EvaluatorOutput(BaseModel):
    feedback: str
    success_criteria_met: bool
    user_input_needed: bool
```

### Checkpointing

Maintains conversation state across turns using `MemorySaver` - each thread has its own persistent memory.

## 🐛 Troubleshooting

### Import Errors

Make sure you're in the correct directory and using the virtual environment:

```bash
cd /Users/mithra_sundaram/Desktop/code/AI/projects/agents
.venv/bin/python 4_langgraph/sidekick/main.py
```

### Playwright Issues

If you get `NotImplementedError` with Playwright:

```bash
# Install browsers
playwright install

# Make sure nest_asyncio is installed
pip install nest_asyncio
```

### Browser Not Opening

Check `graph.py` - ensure `headless=False` if you want to see the browser.

## 🎯 Next Steps

- Add more specialized tools (API calls, database queries)
- Implement multi-turn planning for complex tasks
- Add result summarization and reporting
- Create different agent personas for different domains
- Add voice interface integration

## 📚 Learn More

This project demonstrates:
- ✅ Multi-agent collaboration
- ✅ Self-evaluation and improvement loops
- ✅ Browser automation with Playwright
- ✅ Structured outputs with Pydantic
- ✅ State management with TypedDict + reducers
- ✅ Persistent memory with checkpointing

Based on the LangGraph framework and Week 4 of the Udemy AI Agents course.

---

**Happy automating with Sidekick! 🚀**
