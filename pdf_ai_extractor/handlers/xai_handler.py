from .base_handler import BaseHandler
import requests
from typing import Dict, Optional
import json
import re

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

class XAIHandler(BaseHandler):
    """使用 xAI API 的處理器"""
    def __init__(self, 
                 api_key: str,
                 model: str = "grok-beta",
                 system_prompt: Optional[str] = None,
                 user_prompt: Optional[str] = None,
                 temperature: float = 0.0,
                 max_content_length: int = 4000
                 ):
        super().__init__()
        if not api_key:
            raise ValueError("xAI API key is required")
            
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.user_prompt = user_prompt or DEFAULT_USER_PROMPT
        self.temperature = temperature
        self.max_content_length = max_content_length

    def _clean_json_string(self, content: str) -> Dict:
        """清理並解析回應內容中的 JSON"""
        try:
            # 先嘗試直接解析
            return json.loads(content)
        except json.JSONDecodeError:
            # 如果失敗，清理格式後再試
            try:
                # 移除 markdown 的 code block 標記
                cleaned = re.sub(r'```json\n', '', content)
                cleaned = re.sub(r'\n```', '', cleaned)
                # 移除可能的縮進和多餘空白
                cleaned = cleaned.strip()
                return json.loads(cleaned)
            except json.JSONDecodeError:
                # 如果還是失敗，檢查是否有轉義字符
                try:
                    cleaned = cleaned.encode().decode('unicode_escape')
                    return json.loads(cleaned)
                except:
                    raise ValueError(f"Unable to parse JSON content: {content}")
        
    def analyze_text(self, text: str) -> Dict:
        if not text:
            return {"abstract": "", "keywords": [], "bookmarks": []}
            
        try:
            # 準備發送到 xAI 的文本
            prompt = self.user_prompt.format(text=text[:self.max_content_length] if self.max_content_length > 0 else text)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.temperature,
                "stream": False
            }
            
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            try:
                message_content = response_data['choices'][0]['message']['content']
                # 使用增強的 JSON 解析
                result = self._clean_json_string(message_content)
                
                # 確保結果是字典類型
                if not isinstance(result, dict):
                    raise ValueError("Parsed result is not a dictionary")
                
                return {
                    "abstract": result.get("abstract", "").strip(),
                    "keywords": result.get("keywords", []),
                    "bookmarks": self.extract_bookmarks()
                }
            except Exception as e:
                # 如果 JSON 解析完全失敗，使用原始內容
                return {
                    "abstract": message_content.strip(),
                    "keywords": [],
                    "bookmarks": self.extract_bookmarks(),
                    "error": f"Content parsing error: {str(e)}"
                }
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"xAI API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"xAI analysis failed: {str(e)}")
