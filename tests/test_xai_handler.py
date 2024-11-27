import pytest
import requests
from unittest.mock import patch, MagicMock
from pdf_ai_extractor.handlers import XAIHandler

def test_xai_handler_init():
    """測試 xAI 處理器初始化"""
    handler = XAIHandler(api_key="test-key")
    assert handler.pdf_path is None
    assert handler.document is None
    assert handler.top_n == 20
    assert handler.min_length == 4
    assert handler.min_freq == 2
    assert handler.api_key == "test-key"
    assert handler.model == "grok-beta"

def test_xai_handler_no_api_key():
    """測試沒有 API key 的情況"""
    with pytest.raises(ValueError):
        XAIHandler(api_key="")

@patch('requests.post')
def test_xai_handler_analyze(mock_post, sample_pdf):
    """測試 xAI 分析功能"""
    # 模擬 xAI API 回應
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": """
                {
                    "abstract": "Test summary",
                    "keywords": ["test", "analysis", "document"]
                }
                """
            }
        }]
    }
    mock_post.return_value = mock_response

    handler = XAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    result = handler.result()
    
    assert isinstance(result, dict)
    assert "abstract" in result
    assert "keywords" in result
    assert "bookmarks" in result
    assert result["abstract"].strip() == "Test summary"
    assert len(result["keywords"]) == 3
    assert "test" in result["keywords"]

@patch('requests.post')
def test_xai_handler_api_error(mock_post, sample_pdf):
    """測試 API 錯誤處理"""
    mock_post.side_effect = requests.exceptions.RequestException("API Error")

    handler = XAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    with pytest.raises(Exception) as exc_info:
        handler.result()
    assert "xAI API request failed" in str(exc_info.value)

@patch('requests.post')
def test_xai_handler_http_error(mock_post, sample_pdf):
    """測試 HTTP 錯誤處理"""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error")
    mock_post.return_value = mock_response

    handler = XAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    with pytest.raises(Exception) as exc_info:
        handler.result()
    assert "xAI API request failed" in str(exc_info.value)

@patch('requests.post')
def test_xai_handler_invalid_json_response(mock_post, sample_pdf):
    """測試無效的 JSON 回應"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "Invalid JSON"
            }
        }]
    }
    mock_post.return_value = mock_response

    handler = XAIHandler(api_key="test-key")
    handler.set_pdf_path(sample_pdf)
    result = handler.result()
    
    # 不是拋出異常，而是檢查錯誤訊息在結果中
    assert isinstance(result, dict)
    assert "error" in result
    assert "Content parsing error" in str(result["error"])
    assert result["abstract"] == "Invalid JSON"
    assert result["keywords"] == []
