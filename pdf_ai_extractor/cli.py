import click
import json
import sys
import os
from typing import List, Dict, TextIO
from pathlib import Path
from .handlers import (
    BaseHandler,
    LocalHandler,
    OpenAIHandler,
    HuggingFaceHandler,
    create_handler
)

def process_single_pdf(handler: BaseHandler, pdf_path: str) -> Dict:
    """Process a single PDF file and extract information"""
    try:
        result = handler.result(pdf_path)
        return {
            "path": pdf_path,
            "abstract": result.get("abstract", ""),
            "keywords": result.get("keywords", []),
            "bookmarks": result.get("bookmarks", []),
            "error": result.get("error", None),
        }
    except Exception as e:
        return {
            "path": pdf_path,
            "error": str(e),
            "abstract": "",
            "keywords": [],
            "bookmarks": []
        }

def process_pdf_files(handler: BaseHandler, path: str) -> List[Dict]:
    """Process PDF files from a file path or directory"""
    results = []
    
    if os.path.isfile(path):
        if path.lower().endswith('.pdf'):
            results.append(process_single_pdf(handler, path))
    else:
        # Process directory
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    results.append(process_single_pdf(handler, pdf_path))
    
    return results

def output_results(results: List[Dict], output: TextIO = sys.stdout):
    """Output results to specified file or stdout"""
    json.dump(results, output, ensure_ascii=False, indent=2)
    # Ensure newline if not stdout
    if output is not sys.stdout:
        output.write("\n")

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--backend', '-b', 
              type=click.Choice(['local', 'openai', 'huggingface', 'xai']), 
              default='local',
              help='Select analysis backend')
@click.option('--api-key', '-k',
              help='API key (for OpenAI or xAI)')
@click.option('--model', '-m',
              help='Model name (for HuggingFace)',
              default='facebook/bart-large-cnn')
@click.option('--output', '-o',
              type=click.File('w', encoding='utf-8'),
              default='-',  # '-' represents stdout
              help='Output file path (defaults to stdout)')
def main(path: str, backend: str, api_key: str, model: str, output: TextIO):
    """Analyze PDF files and extract metadata using various AI backends.
    
    PATH: Path to a PDF file or directory containing PDF files.
    
    Examples:
    
    \b
    # Analyze a single file
    pdf-ai-extractor example.pdf
    
    # Use OpenAI backend
    pdf-ai-extractor -b openai -k YOUR_API_KEY example.pdf
    
    # Process entire directory
    pdf-ai-extractor path/to/pdfs/
    
    # Save results to file
    pdf-ai-extractor example.pdf -o results.json
    """
    try:
        # Create appropriate handler
        config = {
            "api_key": api_key,
            "model_name": model
        }
        handler = create_handler(backend, config)
        
        # Process files
        results = process_pdf_files(handler, path)
        
        # Output results
        output_results(results, output)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    finally:
        if output != sys.stdout:
            output.close()

if __name__ == '__main__':
    main()
