from groq import Groq
client = Groq(api_key="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")

def detect_code_hallucination(problem_description, generated_code):
    prompt = f"""
    Analyze the following code snippet against the problem description. 
    Detect if there are any hallucinations (e.g., non-existent functions, incorrect API usage, or logical errors).
    
    Problem: {problem_description}
    Code: {generated_code}
    
    Output "Hallucination" or "No Hallucination" and explain why.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Example usage:
problem = "Write a Python function to sort a list."
code = "def sort_list(l): return l.non_existent_sort()" # Example hallucinated code
print(detect_code_hallucination(problem, code))
