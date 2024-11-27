from .base_handler import BaseHandler
from transformers import pipeline
from typing import Dict, Optional, List
from tqdm import tqdm
import sys
import torch

class HuggingFaceHandler(BaseHandler):
    """Handler for processing documents using HuggingFace models"""
    def __init__(self, 
                 model_name: str = "facebook/bart-large-cnn",
                 device: Optional[str] = None,
                 max_content_length: int = 1024,
                 min_length: int = 50,
                 max_length: int = 150
                 ):
        super().__init__()
        
        # Configure device
        if device is None:
            if torch.backends.mps.is_available():
                device = "mps"
            elif torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
                
        self.device = device
        self.model_name = model_name
        self.max_content_length = max_content_length
        self.min_length = min_length
        self.max_length = max_length
        
        # Initialize summarization model
        try:
            device_arg = -1 if device == "cpu" else 0
            self.summarizer = pipeline(
                "summarization", 
                model=model_name,
                device=device_arg if device != "mps" else device
            )
        except Exception as e:
            raise Exception(f"Failed to initialize HuggingFace model: {str(e)}")

    def analyze_text(self, text: str) -> Dict:
        output = {"abstract": "", "keywords": [], "bookmarks": []}
        if not text:
            return output
        
        errors: List[str] = []
        with tqdm(total=3, desc="Processing with HuggingFace", file=sys.stderr) as pbar:
            # Extract bookmarks
            try:
                output["bookmarks"] = self.extract_bookmarks()
            except Exception as e:
                errors.append(f"Bookmark extraction failed: {str(e)}")
            pbar.update(1)

            # Extract keywords
            try:
                output["keywords"] = self.extract_keywords(text)
            except Exception as e:
                errors.append(f"Keyword extraction failed: {str(e)}")
            pbar.update(1)

            # Generate summary
            try:
                # Limit input text length
                text = text[:self.max_content_length]
                summary = self.summarizer(
                    text,
                    max_length=self.max_length,
                    min_length=self.min_length,
                    do_sample=False
                )
                output["abstract"] = summary[0]["summary_text"].strip()
            except Exception as e:
                errors.append(f"Summary generation failed: {str(e)}")
            pbar.update(1)

        if errors:
            output["error"] = errors

        return output
