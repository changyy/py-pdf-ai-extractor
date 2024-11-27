import pytest
from unittest.mock import patch, MagicMock
from pdf_ai_extractor.handlers import HuggingFaceHandler

def test_huggingface_handler_init():
    """測試 HuggingFace 處理器初始化"""
    with patch('pdf_ai_extractor.handlers.huggingface_handler.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock()
        handler = HuggingFaceHandler()
        assert handler.pdf_path is None
        assert handler.document is None
        assert handler.top_n == 20
        assert handler.min_length == 50
        assert handler.max_length == 150
        assert handler.model_name == "facebook/bart-large-cnn"

def test_huggingface_handler_init_error():
    """測試初始化錯誤處理"""
    with patch('pdf_ai_extractor.handlers.huggingface_handler.pipeline') as mock_pipeline:
        mock_pipeline.side_effect = RuntimeError("Model load error")
        with pytest.raises(Exception) as exc_info:
            HuggingFaceHandler()
        assert "Failed to initialize HuggingFace model" in str(exc_info.value)

def test_huggingface_handler_analyze(sample_pdf):
    """測試 HuggingFace 分析功能"""
    with patch('pdf_ai_extractor.handlers.huggingface_handler.pipeline') as mock_pipeline:
        # 設置模擬的 pipeline
        mock_summarizer = MagicMock()
        mock_summarizer.return_value = [{"summary_text": "Test summary"}]
        mock_pipeline.return_value = mock_summarizer

        handler = HuggingFaceHandler()
        handler.set_pdf_path(sample_pdf)
        result = handler.result()
        
        assert isinstance(result, dict)
        assert "abstract" in result
        assert "keywords" in result
        assert "bookmarks" in result
        assert result["abstract"] == "Test summary"
        assert isinstance(result["keywords"], list)
        assert isinstance(result["bookmarks"], list)

def test_huggingface_handler_empty_text():
    """測試空文本處理"""
    with patch('pdf_ai_extractor.handlers.huggingface_handler.pipeline') as mock_pipeline:
        mock_summarizer = MagicMock()
        mock_summarizer.return_value = [{"summary_text": ""}]
        mock_pipeline.return_value = mock_summarizer

        handler = HuggingFaceHandler()
        result = handler.analyze_text("")
        
        assert isinstance(result, dict)
        assert result["abstract"] == ""
        assert result["keywords"] == []
        assert result["bookmarks"] == []

def test_huggingface_handler_summary_error(sample_pdf):
    """測試摘要生成錯誤處理"""
    with patch('pdf_ai_extractor.handlers.huggingface_handler.pipeline') as mock_pipeline:
        mock_summarizer = MagicMock()
        mock_summarizer.side_effect = Exception("Summarization error")
        mock_pipeline.return_value = mock_summarizer

        handler = HuggingFaceHandler()
        handler.set_pdf_path(sample_pdf)
        result = handler.result()
        
        assert isinstance(result, dict)
        assert "error" in result
        assert any("Summary generation failed" in str(err) for err in result["error"])

def test_huggingface_handler_device_selection():
    """測試設備選擇"""
    with patch('pdf_ai_extractor.handlers.huggingface_handler.pipeline') as mock_pipeline:
        # 測試 CPU
        HuggingFaceHandler(device="cpu")
        mock_pipeline.assert_called_with(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1
        )
        
        mock_pipeline.reset_mock()
        
        # 測試 CUDA
        HuggingFaceHandler(device="cuda")
        mock_pipeline.assert_called_with(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0
        )
