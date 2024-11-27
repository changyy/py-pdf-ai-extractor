from setuptools import setup, find_packages
import re

def get_version():
    with open('pdf_ai_extractor/__init__.py', 'r') as f:
        content = f.read()
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="pdf-ai-extractor",
    version=get_version(),
    author="changyy",
    author_email="changyy.csie@gmail.com",
    description="PDF metadata and content extraction tool with AI-powered analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/changyy/py-pdf-ai-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",  # 改為 Beta，因為從 1.0.0 開始
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "PyMuPDF>=1.22.0",
        "jieba>=0.42.1",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "click>=8.0.0",
        "openai>=1.0.0",
        "transformers>=4.0.0",
        "numpy<2.0.0",
        "torch>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=1.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdf-ai-extractor=pdf_ai_extractor.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
