




# A Bit advance example 
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END



# 1. Define graph state

class QAState(TypedDict):
    query: str
    query_type: str
    retrieved_docs: List[str]
    draft_answer: str
    final_answer: str



# 2. Small fake document store

DOCUMENTS = [
    "Python is a high-level programming language known for readability.",
    "FastAPI is a modern Python web framework for building APIs.",
    "Django is a batteries-included Python web framework.",
    "LangGraph is used to build stateful and branching AI workflows.",
    "LangChain helps build LLM applications with chains, tools, and retrieval."
]



# 3. Helper retrieval function

def simple_retrieve(query: str, docs: List[str], top_k: int = 2) -> List[str]:
    """
    Very basic retrieval:
    score each document by counting how many query words appear in it.
    """
    query_words = query.lower().split()

    scored = []
    for doc in docs:
        score = 0
        doc_lower = doc.lower()
        for word in query_words:
            if word in doc_lower:
                score += 1
        scored.append((score, doc))

    scored.sort(reverse=True, key=lambda x: x[0])

    # keep docs with score > 0
    results = [doc for score, doc in scored if score > 0][:top_k]
    return results



# 4. Node: classify query

def classify_query(state: QAState) -> dict:
    query = state["query"].lower()

    # Very simple classification rules
    if "compare" in query or "difference" in query or "vs" in query:
        query_type = "comparison"
    elif "weather" in query or "cricket score" in query or "stock price" in query:
        query_type = "out_of_scope"
    else:
        query_type = "factual"

    return {"query_type": query_type}



# 5. Router function

def route_query(state: QAState) -> str:
    return state["query_type"]



# 6. Node: factual path

def factual_rag(state: QAState) -> dict:
    query = state["query"]
    docs = simple_retrieve(query, DOCUMENTS, top_k=2)

    if not docs:
        answer = "I could not find relevant information in the documents."
    else:
        answer = "Based on the documents: " + " ".join(docs)

    return {
        "retrieved_docs": docs,
        "draft_answer": answer
    }



# 7. Node: comparison path

def comparison_rag(state: QAState) -> dict:
    query = state["query"]
    docs = simple_retrieve(query, DOCUMENTS, top_k=3)

    if len(docs) < 2:
        answer = "I do not have enough document evidence to make a comparison."
    else:
        answer = (
            "Here is a simple comparison based on multiple documents: "
            + " | ".join(docs)
        )

    return {
        "retrieved_docs": docs,
        "draft_answer": answer
    }



# 8. Node: out-of-scope path

def out_of_scope_response(state: QAState) -> dict:
    return {
        "retrieved_docs": [],
        "draft_answer": (
            "Sorry, this question is outside the scope of the available documents."
        )
    }



# 9. Node: validate response

def validate_response(state: QAState) -> dict:
    answer = state["draft_answer"]
    docs = state["retrieved_docs"]
    query_type = state["query_type"]

    # Very basic guardrails
    if query_type in ["factual", "comparison"] and not docs:
        final_answer = (
            "I cannot answer confidently because no relevant supporting document was found."
        )
    elif len(answer.strip()) == 0:
        final_answer = "I could not generate a valid answer."
    else:
        final_answer = answer

    return {"final_answer": final_answer}



# 10. Build the graph

builder = StateGraph(QAState)

builder.add_node("classify_query", classify_query)
builder.add_node("factual_rag", factual_rag)
builder.add_node("comparison_rag", comparison_rag)
builder.add_node("out_of_scope_response", out_of_scope_response)
builder.add_node("validate_response", validate_response)

builder.add_edge(START, "classify_query")

builder.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "factual": "factual_rag",
        "comparison": "comparison_rag",
        "out_of_scope": "out_of_scope_response",
    },
)

builder.add_edge("factual_rag", "validate_response")
builder.add_edge("comparison_rag", "validate_response")
builder.add_edge("out_of_scope_response", "validate_response")

builder.add_edge("validate_response", END)

graph = builder.compile()



# 11. Run examples

if __name__ == "__main__":
    examples = [
        {"query": "What is FastAPI?"},
        {"query": "Compare FastAPI vs Django"},
        {"query": "What is the weather in Delhi?"}
    ]

    for example in examples:
        result = graph.invoke(example)
        print("\nQUESTION:", example["query"])
        print("TYPE:", result["query_type"])
        print("DOCS:", result["retrieved_docs"])
        print("ANSWER:", result["final_answer"])