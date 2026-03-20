



from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq

# -----------------------------
# 1) Small knowledge base
# -----------------------------
knowledge_base = [
    "RAG stands for Retrieval-Augmented Generation.",
    "FastAPI is a Python framework for building APIs.",
    "Cosine similarity measures how similar two vectors are.",
    "Embeddings convert text into numerical vectors.",
]

# -----------------------------
# 2) Tool: search knowledge base
# -----------------------------
@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base for the most relevant note."""
    query = query.lower()

    matches = []
    for item in knowledge_base:
        text = item.lower()
        score = 0

        for word in query.split():
            if word in text:
                score += 1

        if score > 0:
            matches.append((score, item))

    if not matches:
        return "No useful match found in the knowledge base."

    matches.sort(reverse=True)
    best_items = [item for _, item in matches[:3]]
   
    return "\n".join(best_items)

# -----------------------------
# 3) Tool: basic math
# -----------------------------
@tool
def calculate(expression: str) -> str:
    
    try:
        # very basic safe eval setup
        allowed_names = {}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Could not calculate that expression. Error: {e}"

# -----------------------------
# 4) Tool: web search
# -----------------------------
web_search = TavilySearch(max_results=3,
                          tavily_api_key="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"
)

# -----------------------------
# 5) Model
# -----------------------------
model = init_chat_model("llama-3.1-8b-instant",
                         model_provider="groq",
                         api_key="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")

# -----------------------------
# 6) Agent
# -----------------------------
agent = create_agent(
    model=model,
    tools=[search_knowledge_base, calculate, web_search],
    system_prompt=(
        "You are a helpful assistant. "
        "Use the knowledge base tool for internal facts, "
        "the calculator for math, "
        "and web search for current information."
    ),
)

# -----------------------------
# 7) Try it
# -----------------------------
questions = [
    "What does RAG stand for?",
    "What is 125 * 18 + 7?",
    "Who is the current president of France?",
]

for q in questions:
    print("\n" + "=" * 60)
    print("USER:", q)

    result = agent.invoke(
        {"messages": [{"role": "user", "content": q}]}
    )

    print("\nAGENT:")
    print(result["messages"][-1].content)