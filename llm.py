import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file
load_dotenv()

# Initialize the Client with your API Key
# If the key is missing, it will raise a clear error in your terminal
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

client = genai.Client(api_key=api_key)

# Configuration Constants
MODEL_NAME = "models/gemini-1.5-pro"  # Recommended for speed and reliability

def generate_answer(question, context_list):
    """
    Generates a concise answer based on retrieved context using Gemini 1.5 Flash.
    """
    # Prepare the context string
    context_text = "\n".join(context_list) if context_list else "No relevant documents found."
    
    # Structured System Prompt
    prompt = f"""
    You are a production-grade GenAI Assistant. 
    Use the following retrieved context to answer the user's question.
    
    Rules:
    1. If the context is empty or irrelevant, say: "I'm sorry, I don't have information on that in my knowledge base."
    2. Do not use outside knowledge.
    3. Be concise and professional.

    Context:
    {context_text}

    User Question: {question}
    """

    try:
        # Using the new SDK 'models.generate_content' method
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,  # Keep it focused and deterministic
                max_output_tokens=500,
            )
        )
        
        # Return the generated text
        return response.candidates[0].content.parts[0].text

    except Exception as e:
        # This handles API key issues, 404s, or safety blocks gracefully
        error_msg = str(e)
        print(f"--- LOG ERROR --- \n{error_msg}\n-----------------")
        
        if "API_KEY_INVALID" in error_msg:
            return "System Error: The API key is invalid or has been deactivated."
        elif "not found" in error_msg.lower():
            return f"System Error: The model '{MODEL_NAME}' is unavailable."
        
        return "I'm sorry, I encountered an internal error. Please try again later."

# Example usage (for testing purposes)
if __name__ == "__main__":
    test_context = ["The company policy allows 20 days of remote work per year."]
    test_question = "How many remote work days do I get?"
    print(generate_answer(test_question, test_context))