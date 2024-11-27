from abc import ABC, abstractmethod
from typing import Dict
from collections import Counter
from typing import Dict, List
from transformers import pipeline
import os
import fitz  # PyMuPDF
import jieba
import platform
import torch

class BaseHandler(ABC):
    def __init__(self):
        self.pdf_path = None
        self.document = None
        self.top_n = 20
        self.min_length = 4
        self.min_freq = 2

        if not os.environ.get("TOKENIZERS_PARALLELISM"):
            os.environ["TOKENIZERS_PARALLELISM"] = "false"

        self.device = self._get_device()

    def __del__(self):
        if self.document:
            self.document.close()
            self.document = None
        if self.pdf_path:
            self.pdf_path = None

    def _get_device(self) -> str:
        if torch.backends.mps.is_available() and platform.processor() == 'arm':
            # MacOS M1/M2
            return "mps"
        elif torch.cuda.is_available():
            # NVIDIA GPU
            return "cuda"
        else:
            # CPU
            return "cpu"

    def set_pdf_path(self, pdf_path: str) -> bool:
        if pdf_path and len(pdf_path) > 0:
            try:
                self.pdf_path = pdf_path
                self.document = fitz.open(pdf_path)
                return True
            except Exception as e:
                self.pdf_path = None
                self.document = None
                raise Exception(f"Error processing {pdf_path}: {str(e)}")
        return False
    
    def set_jieba_config(self, top_n: int = 20, min_length: int = 4, min_freq: int = 2):
        self.top_n = top_n
        self.min_length = min_length
        self.min_freq = min_freq

    def extract_bookmarks(self) -> List[str]:
        if self.document:
            try:
                toc = self.document.get_toc()
                bookmarks = [item[1] for item in toc]
                return bookmarks
            except Exception as e:
                raise Exception(f"Bookmark extraction failed: {str(e)}")
        return []
    
    def extract_text(self) -> str:
        text = ""
        if not self.pdf_path or not self.document:
            return text
        try:
            for page_num in range(len(self.document)):
                page = self.document.load_page(page_num)
                text += page.get_text() + "\n"
        except Exception as e:
            raise Exception(f"Text extraction failed: {str(e)}")
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        keywords = []
        try:
            words = jieba.cut(text)
            words = [word.lower() for word in words if len(word) >= self.min_length]
            word_freq = Counter(words)
            keywords = [word for word, freq in word_freq.most_common(self.top_n) if freq >= self.min_freq]
        except Exception as e:
            raise Exception(f"Keyword extraction failed: {str(e)}")
        return keywords
    
    def extract_summary(self, text: str) -> str:
        summary = ""
        try:
            device_arg = -1 if self.device == "cpu" else 0
            summarizer = pipeline(
                "summarization", 
                model="sshleifer/distilbart-cnn-12-6",
                device=device_arg if self.device != "mps" else "mps"
            )
            summary = summarizer(text[:512], max_length=512, min_length=50, do_sample=False)
            summary = summary[0]["summary_text"]
        except Exception as e:
            raise Exception(f"Summary extraction failed: {str(e)}")
        return summary

    @abstractmethod
    def analyze_text(self, text: str) -> Dict:
        #return { "abstract": self.extract_summary(text), "keywords": self.extract_keywords(text), "bookmarks": self.extract_bookmarks()}
        return { "abstract": "", "keywords": [], "bookmarks": []}

    def result(self, pdf_path:str = "") -> Dict:
        if not self.pdf_path or not self.document:
            if pdf_path != "":
                self.set_pdf_path(pdf_path)
        if not self.pdf_path or not self.document:
            return { "abstract": "", "keywords": [], "bookmarks": [] , "error": "PDF file not found" }
        
        text = self.extract_text()
        return self.analyze_text(text)
