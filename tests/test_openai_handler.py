# tests/test_openai_handler.py
import pytest
from unittest.mock import patch, MagicMock
from pdf_ai_extractor.handlers import OpenAIHandler

def test_openai_handler_init():
    """測試 OpenAI 處理器初始化"""
    handler = OpenAIHandler(api_key="test-key")
    assert handler.pdf_path is None
    assert handler.document is None
    assert handler.top_n == 20
    assert handler.min_length == 4
    assert handler.min_freq == 2

def test_openai_handler_no_api_key():
    """測試沒有 API key 的情況"""
    with pytest.raises(ValueError):  # 改用更具體的錯誤類型
        OpenAIHandler(api_key="")

@patch('openai.OpenAI')
def test_openai_handler_analyze(mock_openai, sample_pdf):
    """測試 OpenAI 分析功能"""
    # 模擬 OpenAI 回應
    mock_message = MagicMock()
    mock_message.content = """
    {
        "abstract": "Test summary",
        "keywords": ["test", "analysis", "document"]
    }
    """
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    handler = OpenAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    result = handler.result()
    
    assert isinstance(result, dict)
    assert "abstract" in result
    assert "keywords" in result
    assert "bookmarks" in result
    assert result["abstract"].strip() == "Test summary"
    assert len(result["keywords"]) == 3
    assert "test" in result["keywords"]

@patch('openai.OpenAI')
def test_openai_handler_api_error(mock_openai, sample_pdf):
    """測試 API 錯誤處理"""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai.return_value = mock_client

    handler = OpenAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    with pytest.raises(Exception) as exc_info:
        handler.result()
    assert "OpenAI analysis failed" in str(exc_info.value)

@patch('openai.OpenAI')
def test_openai_handler_invalid_json_response(mock_openai, sample_pdf):
    """測試無效的 JSON 回應"""
    mock_message = MagicMock()
    mock_message.content = "Invalid JSON"
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    handler = OpenAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    with pytest.raises(Exception) as exc_info:
        handler.result()
    assert "Failed to parse OpenAI response" in str(exc_info.value)
