import pytest
import warnings
import os
from tempfile import NamedTemporaryFile
import fitz

def pytest_configure(config):
    # 更精確的警告過濾
    warnings.filterwarnings(
        action="ignore",
        category=DeprecationWarning,
        module="importlib._bootstrap"
    )
    
    warnings.filterwarnings(
        action="ignore",
        category=UserWarning,
        module="torch.nn.modules.transformer"
    )
    
    # 系統級別的警告
    warnings.filterwarnings(
        action="ignore",
        category=DeprecationWarning,
        message="builtin type.*has no __module__ attribute"
    )

@pytest.fixture
def sample_pdf():
    """創建一個測試用的 PDF 文件"""
    with NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        doc = fitz.open()
        page = doc.new_page()
        
        # 添加標題和內容
        page.insert_text((50, 50), "Test Document Title")
        page.insert_text((50, 100), "This is a test document for PDF analysis.")
        page.insert_text((50, 150), "It contains sample text for testing purposes.")
        
        # 添加書籤
        doc.set_toc([
            [1, "Chapter 1", 1],
            [2, "Section 1.1", 1],
            [1, "Chapter 2", 1]
        ])
        
        doc.save(f.name)
        doc.close()
        
        yield f.name
        
        # 清理
        os.unlink(f.name)
