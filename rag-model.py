from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
import os


# 1. Ek sample database liya h 

documents = [
    "FastAPI is a Python framework used to build APIs.",
    "RAG stands for Retrieval-Augmented Generation.",
    "Embeddings convert text into numerical vectors.",
    "Cosine similarity is used to measure similarity between vectors.",
    "Vector databases help store and search embeddings efficiently."
]


# 2. Load embedding model

embedding_model = SentenceTransformer("all-MiniLM-L6-v2") #text-embedding-ada-002 1536

# generate embedding for the documents 
document_embeddings = embedding_model.encode(documents)
# To see the embedding flow 
print("Document's embeddings")
print(document_embeddings)

# 3. User question

question = "What is Apple?"

# Convert question to embedding
question_embedding = embedding_model.encode([question])
# To see the flow 
print("Question's embeddings")
print(question_embedding)


# 4. Retrieval step

scores = cosine_similarity(question_embedding, document_embeddings)[0]

best_index = scores.argmax()
best_document = documents[best_index]

print("Question:")
print(question)

print("\nBest Retrieved Document:")
print(best_document)

print("\nSimilarity Score:")
print(scores[best_index])


# 5. Generation step

client = Groq(api_key="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")

prompt = f"""
Answer the question only from the context below.

Context:
{best_document}

Question:
{question}
If the answer is not contained in the context, say:
"I don't have enough information to answer that."
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

answer = response.choices[0].message.content

print("\nFinal Answer:")
print(answer)