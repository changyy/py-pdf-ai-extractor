from .base_handler import BaseHandler
import openai
from typing import Dict, Optional
import json

DEFAULT_SYSTEM_PROMPT = """You are a document analyzer. You need to extract an abstract and keywords from the given document.
Your response must be in JSON format with the following structure exactly:
{
    "abstract": "brief summary of the document",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}
The abstract should be concise and capture the main points of the document.
Keywords should be specific and relevant to the document's content."""

DEFAULT_USER_PROMPT = """Please analyze this document and provide:
1. A brief abstract (max 200 words)
2. A list of up to 10 keywords

Return your analysis in the specified JSON format.

Document content: {text}"""

class OpenAIHandler(BaseHandler):
    """Handler for processing documents using OpenAI API"""
    def __init__(self, 
                 api_key: str,
                 model: str = "gpt-4o-mini",
                 system_prompt: Optional[str] = None,
                 user_prompt: Optional[str] = None,
                 temperature: float = 0.3,
                 max_tokens: int = 500,
                 max_content_length: int = 4000
                 ):
        super().__init__()
        if not api_key:
            raise ValueError("OpenAI API key is required")
            
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.user_prompt = user_prompt or DEFAULT_USER_PROMPT
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_content_length = max_content_length
        
    def analyze_text(self, text: str) -> Dict:
        if not text:
            return {"abstract": "", "keywords": [], "bookmarks": []}
            
        try:
            # Prepare text for OpenAI API
            prompt = self.user_prompt.format(text=text[:self.max_content_length] if self.max_content_length > 0 else text)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}  # Ensure JSON response format
            )
            
            # Parse response
            try:
                result = json.loads(response.choices[0].message.content)
                return {
                    "abstract": result.get("abstract", ""),
                    "keywords": result.get("keywords", []),
                    "bookmarks": self.extract_bookmarks()  # Use local bookmark extraction
                }
            except Exception as e:
                raise Exception(f"Failed to parse OpenAI response: {str(e)}, response: {response}")
                
        except Exception as e:
            raise Exception(f"OpenAI analysis failed: {str(e)}")
