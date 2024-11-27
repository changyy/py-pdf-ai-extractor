from .base_handler import BaseHandler
from typing import Dict
from tqdm import tqdm
import sys

class LocalHandler(BaseHandler):
    def analyze_text(self, text: str) -> Dict:
        output = {"abstract": "", "keywords": [], "bookmarks": []}
        if not text:
            return output
        errors = []

        with tqdm(total=3, desc="Processing PDF", file=sys.stderr) as pbar:
            try:
                output["bookmarks"] = self.extract_bookmarks()
            except Exception as e:
                errors.append(f"Bookmark extraction failed: {str(e)}")
            pbar.update(1)
 
            try:
                output["keywords"] = self.extract_keywords(text)
            except Exception as e:
                errors.append(f"Keyword extraction failed: {str(e)}")
            pbar.update(1)
 
            try:
                output["abstract"] = self.extract_summary(text)
            except Exception as e:
                errors.append(f"Summary extraction failed: {str(e)}")
            pbar.update(1)
          
        if errors:
            output["error"] = errors
        return output
      
