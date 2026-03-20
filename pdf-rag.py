import os
import pdfplumber
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



# 1. Read text from PDF

pdf_path = "sample.pdf"   

full_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"



# 2. Split text into simple chunks

# Simple chunking: split by paragraph-like blocks
raw_chunks = full_text.split("\n\n")

chunks = []
for chunk in raw_chunks:
    clean_chunk = chunk.strip()
    if clean_chunk:
        chunks.append(clean_chunk)

print("Chunks")
print(chunks)
'''#Overlap Chunking 

raw_chunks = full_text.split('\n\n')
# Clean and filter empty chunks
initial_chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

overlap_chunks = []
overlap_size = 1 # Number of chunks to overlap

for i in range(0, len(initial_chunks) - 1):
    # Combine current chunk with the next(s)
    overlap_pair = " ".join(initial_chunks[i:i + 1 + overlap_size])
    overlap_chunks.append(overlap_pair)'''







# 3. Load embedding model

model = SentenceTransformer("all-MiniLM-L6-v2")

# Make embeddings for all chunks
#chunk_embeddings = model.encode(chunks)
chunk_embeddings = model.encode(chunks)



# 4. Ask question

question = "What is PDF?"

# Convert question to embedding
question_embedding = model.encode([question])



# 5. Compare question with chunks

scores = cosine_similarity(question_embedding, chunk_embeddings)[0]



# 6. Apply threshold

threshold = 0.30

matched_chunks = []

for i in range(len(chunks)):
    score = float(scores[i])

    if score >= threshold:
        matched_chunks.append({
            "chunk": chunks[i],
            "score": score
        })

print("Matched chunks")
print(matched_chunks)


# Sort best matches first
matched_chunks.sort(key=lambda x: x["score"], reverse=True)

# Keep top 3 only
top_chunks = matched_chunks[:3]
print("top chunk")
print(top_chunks)



# 7. If nothing matches, stop

if not top_chunks:
    print("No relevant context found from the PDF.")
    exit()



# 8. Build context for LLM

context_text = ""

for item in top_chunks:
    context_text += item["chunk"] + "\n\n"

print("Question:")
print(question)

print("\nRetrieved Chunks:")
for item in top_chunks:
    print(f"Score: {item['score']:.4f}")
    print(item["chunk"])
    print("-" * 50)



# 9. Send context + question to LLM

client = Groq(api_key="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")

prompt = f"""
Answer the question only from the context below.
If the answer is not found in the context, say:
"I could not find the answer in the PDF."

Context:
{context_text}

Question:
{question}
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

answer = response.choices[0].message.content



# 10. Final output

print("\nFinal Answer:")
print(answer)