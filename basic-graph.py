from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define a simple state
class State(TypedDict):
    query: str
    answer: str

# Node 1: Take query
def get_query(state: State):
    print("Got query:", state["query"])
    return state

# Node 2: Make a dummy answer
def answer_query(state: State):
    state["answer"] = f"You asked: {state['query']}"
    return state

# Node 3: Return answer
def return_answer(state: State):
    print("Final Answer:", state["answer"])
    return state

# Build graph
workflow = StateGraph(State)

workflow.add_node("get_query", get_query)
workflow.add_node("answer_query", answer_query)
workflow.add_node("return_answer", return_answer)

workflow.set_entry_point("get_query")
workflow.add_edge("get_query", "answer_query")
workflow.add_edge("answer_query", "return_answer")
workflow.add_edge("return_answer", END)

# Compile
app = workflow.compile()

# Run demo
app.invoke({"query": "What is LangGraph?"})
