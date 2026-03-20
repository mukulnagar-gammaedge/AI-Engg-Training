import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq



pdf_path = "sample.pdf"

# Load PDF
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)

#   Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Store chunks in simple in-memory Chroma
vector_store = Chroma(
    collection_name="my_pdf_chunks",
    embedding_function=embeddings
)

vector_store.add_documents(chunks)

#  Ask a question
question = "What is PDF?"

#  Search with scores
#    score here is distance-like: smaller is better
results = vector_store.similarity_search_with_score(question, k=3)

#  Apply a simple threshold
#    lower score = more similar
threshold = 1.0

good_chunks = []
for doc, score in results:
    if score <= threshold:
        good_chunks.append((doc, score))

# Stop if nothing is relevant enough
if not good_chunks:
    print("No relevant context found.")
    raise SystemExit

#  Build context text
context_text = ""
for doc, score in good_chunks:
    context_text += doc.page_content + "\n\n"

print("QUESTION:")
print(question)
print("\nRETRIEVED CHUNKS:\n")

for doc, score in good_chunks:
    print(f"Score: {score:.4f}")
    print(doc.page_content[:500])
    print("-" * 50)

#  LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="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"
)

prompt = f"""
Answer the question only from the context below.

If the answer is not in the context, say:
"I could not find the answer in the PDF."

Context:
{context_text}

Question:
{question}
"""

response = llm.invoke(prompt)

print("\nFINAL ANSWER:\n")
print(response.content)