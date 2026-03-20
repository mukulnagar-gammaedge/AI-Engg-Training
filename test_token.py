##Phase 1 Hands on 

'''import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

examples = [
    "Happiness",
    
 
]

for text in examples:
    token_ids = enc.encode(text)
    token_pieces = [enc.decode_single_token_bytes(t).decode("utf-8", errors="replace") for t in token_ids]

    print("=" * 60)
    print("TEXT:")
    print(repr(text))
    print("TOKEN IDS:")
    print(token_ids)
    print("TOKEN PIECES:")
    print(token_pieces)
    print("TOKEN COUNT:", len(token_ids))'''


'''import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

text = "Happiness"
tokens = tokenizer.encode(text)

print(tokens)
'''

##Phase 1.2 

# Checking embedding using open AI model but not working due to limit exceeded

'''from openai import OpenAI

client = OpenAI(api_key="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")

sentences = [

    "I love pizza.",
    "I enjoy eating pizza.",
    "Pizza is delicious.",
    "I hate pizza.",
    "I dislike eating pizza.",
    "Pizza tastes awful to me.",
    "The sky is blue.",
    "The ocean is blue.",
    "The grass is green.",
    "The sky is red.",
    "The ocean is red.",
    "The grass is purple.",
    "I am learning Python.",
    "I am coding in Python.",
    "I am studying programming.",
    "I am not learning Python.",
    "I am not coding in Python.",
    "I dislike programming.",
    "The cat sat on the mat.",
    "Quantum mechanics is fascinating."
]

embeddings = []

for s in sentences:
    res = client.embeddings.create(
        model="text-embedding-ada-002",
        input=s
    

    )
    vector = res.data[0].embedding
    embeddings.append(vector)


for i, vector in enumerate(em):
    print(f"Sentence {i+1}: {sentences[i]}")
    print(f"Embedding length: {len(vector)}")
    print(vector[:10], "...")  
    print()'''


# Doing the same with sentance tranformer 

'''from sentence_transformers import SentenceTransformer

# Load a pretrained embedding model
# You can try "all-MiniLM-L6-v2" (384 dimensions, fast) or "all-mpnet-base-v2" (768 dimensions, more accurate)
model = SentenceTransformer("all-MiniLM-L6-v2")

# 20 sentences: similar, opposite, unrelated
sentences = [
    "I love pizza.",
    "I enjoy eating pizza.",
    "Pizza is delicious.",
    "I hate pizza.",
    "I dislike eating pizza.",
    "Pizza tastes awful to me.",
    "The sky is blue.",
    "The ocean is blue.",
    "The grass is green.",
    "The sky is red.",
    "The ocean is red.",
    "The grass is purple.",
    "I am learning Python.",
    "I am coding in Python.",
    "I am studying programming.",
    "I am not learning Python.",
    "I am not coding in Python.",
    "I dislike programming.",
    "The cat sat on the mat.",
    "Quantum mechanics is fascinating."
]

# Generate embeddings
embeddings = model.encode(sentences)

# Print raw vectors
for i, vector in enumerate(embeddings):
    print(f"Sentence {i+1}: {sentences[i]}")
    print(f"Embedding length: {len(vector)}")
    print(vector[:10], "...")  # print first 10 floats for readability
    print()
'''


##Phase 1.3 
##calculating the cosine similarity between above sentances 



'''from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 20 sentences: similar, opposite, unrelated
sentences = [
    "I love pizza.",
    "I enjoy eating pizza.",
    "Pizza is delicious.",
    "I hate pizza.",
    "I dislike eating pizza.",
    "Pizza tastes awful to me.",
    "The sky is blue.",
    "The ocean is blue.",
    "The grass is green.",
    "The sky is red.",
    "The ocean is red.",
    "The grass is purple.",
    "I am learning Python.",
    "I am coding in Python.",
    "I am studying programming.",
    "I am not learning Python.",
    "I am not coding in Python.",
    "I dislike programming.",
    "The cat sat on the mat.",
    "Quantum mechanics is fascinating."
]

# Generate embeddings
embeddings = model.encode(sentences)

# Compute cosine similarity matrix
similarity_matrix = cosine_similarity(embeddings)

# Pretty print results
np.set_printoptions(precision=3, suppress=True)
print("Cosine Similarity Matrix (20x20):")
print(similarity_matrix)

# Example: check similarity between specific pairs
pairs_to_check = [
    (0, 1),  # "I love pizza." vs "I enjoy eating pizza."
    (0, 3),  # "I love pizza." vs "I hate pizza."
    (6, 7),  # "The sky is blue." vs "The ocean is blue."
    (12, 13),# "I am learning Python." vs "I am coding in Python."
    (12, 15) # "I am learning Python." vs "I am not learning Python."
]

for i, j in pairs_to_check:
    print(f"Similarity({sentences[i]} , {sentences[j]}) = {similarity_matrix[i][j]:.3f}")'''

'''
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 20 sentences: similar, opposite, unrelated
sentences = [
    "Quantum",
    "Apple"
 
]

# Generate embeddings
embeddings = model.encode(sentences)

# Compute cosine similarity matrix
similarity_matrix = cosine_similarity(embeddings)

# Pretty print results
np.set_printoptions(precision=3, suppress=True)
print("Cosine Similarity Matrix (20x20):")
print(similarity_matrix)

# Example: check similarity between specific pairs
pairs_to_check = [
    (0, 1),  
  
]

for i, j in pairs_to_check:
    print(f"Similarity({sentences[i]} , {sentences[j]}) = {similarity_matrix[i][j]:.3f}")

'''




## Build a simple function: input two sentences → output similarity score.
'''from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load a pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def sentence_similarity(sent1: str, sent2: str) -> float:
    """
    Compute cosine similarity between two sentences.
    Returns a score between -1 and 1.
    """
    embeddings = model.encode([sent1, sent2])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return sim

# Example usage
print("king vs queen:", sentence_similarity("king", "queen"))
print("apple vs quantum:", sentence_similarity("Apple", "Quantum"))
print("I love pizza vs I hate pizza:", sentence_similarity("I love pizza", "I hate pizza"))'''


##Phase 2 Hands on 

'''from fastapi import FastAPI, Body
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()


model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post("/embed/")
async def get_embed(sentences: list = Body(...)):
   
    embeddings = model.encode(sentences)
    
    
    return {"embeddings": embeddings.tolist()}

@app.post("/similarity/")
async def sentence_similarity(sent1: str, sent2: str) -> float:
    """
    Compute cosine similarity between two sentences.
    Returns a score between -1 and 1.
    """
    embeddings = model.encode([sent1, sent2])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return sim'''


#LLM call taken more than 30 seconds 

'''import signal
import time
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def safe_embed(sentences, timeout=30):
    def handler(signum, frame):
        raise TimeoutError(f"Task exceeded {timeout}s limit")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    
    start = time.perf_counter()
    
    try:
       
        embeddings = model.encode(sentences).tolist()
        duration = time.perf_counter() - start
        return {"status": "success", "data": embeddings, "time": f"{duration:.2f}s"}
    
    except TimeoutError as e:
        return {"status": "error", "message": str(e)}
    
    except Exception as e:
        return {"status": "error", "message": f"Unexpected: {str(e)}"}
    
    finally:
        signal.alarm(0)

sentences = ["This is a test sentence.", "Each string becomes a vector."]
result = safe_embed(sentences, timeout=10)

if result["status"] == "success":
    print(f"Done in {result['time']}! First vector length: {len(result['data'][0])}")
else:
    print(f"Failed: {result['message']}")'''



