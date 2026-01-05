import google.generativeai as genai
from typing import Dict, Optional
import os


def initialize_client(api_key: Optional[str] = None):
    """
    Initialize Google Generative AI client.
    
    Args:
        api_key: Google GenAI API key. If None, reads from GOOGLE_API_KEY env var.
    """
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("Google API key not provided. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
    
    genai.configure(api_key=api_key)
    return genai


def process_with_ai(text: str, model_name: str = "gemini-pro", api_key: Optional[str] = None) -> str:
    """
    Process text using Google Generative AI.
    
    Args:
        text: Text content to process
        model_name: Name of the model to use (default: gemini-pro)
        api_key: Google GenAI API key (optional, uses env var if not provided)
        
    Returns:
        AI-generated response
    """
    try:
        # Initialize client
        initialize_client(api_key)
        
        # Get the model
        model = genai.GenerativeModel(model_name)
        
        # Create a prompt
        prompt = f"""Please analyze the following PDF content and provide a summary:

{text[:5000]}  # Limiting text length for demo

Provide a concise summary of the main points."""
        
        # Generate response
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        # Return placeholder if API is not configured
        return f"[AI Processing Placeholder] Would process text with {model_name}. Error: {str(e)}"


def generate_summary(text: str, api_key: Optional[str] = None) -> Dict:
    """
    Generate a summary of the PDF text using AI.
    
    Args:
        text: Text content from PDF
        api_key: Google GenAI API key (optional)
        
    Returns:
        Dictionary with summary information
    """
    try:
        initialize_client(api_key)
        model = genai.GenerativeModel("gemini-pro")
        
        prompt = f"Summarize the following document in 3-5 bullet points:\n\n{text}"
        response = model.generate_content(prompt)
        
        return {
            "summary": response.text,
            "status": "success"
        }
    except Exception as e:
        return {
            "summary": f"AI summary unavailable: {str(e)}",
            "status": "error"
        }

