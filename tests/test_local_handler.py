import pytest

from pdf_ai_extractor.handlers import LocalHandler


def test_local_handler_init():
    """測試基礎處理器初始化"""
    handler = LocalHandler()
    assert handler.pdf_path is None
    assert handler.document is None
    assert handler.top_n == 20
    assert handler.min_length == 4
    assert handler.min_freq == 2

def test_local_handler_set_pdf_path(sample_pdf):
    """測試設定 PDF 路徑"""
    handler = LocalHandler()
    assert handler.set_pdf_path(sample_pdf) is True
    assert handler.pdf_path == sample_pdf
    assert handler.document is not None

def test_local_handler_invalid_pdf():
    """測試無效的 PDF 路徑"""
    handler = LocalHandler()
    with pytest.raises(Exception):
        handler.set_pdf_path("non_existent.pdf")

def test_local_handler_analyze(sample_pdf):
    """測試本地處理器分析功能"""
    handler = LocalHandler()
    handler.set_pdf_path(sample_pdf)
    result = handler.result()
    
    assert isinstance(result, dict)
    assert "abstract" in result
    assert "keywords" in result
    assert "bookmarks" in result
    assert isinstance(result["keywords"], list)
    assert isinstance(result["bookmarks"], list)
