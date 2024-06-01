# src/document_processor.py
import textract
import pypandoc
import spacy
import os
import logging
from pathlib import Path
from typing import List
from .base import BaseDocumentProcessor

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor(BaseDocumentProcessor):
    SUPPORTED_EXTENSIONS = [
        '.csv', '.doc', '.docx', '.eml', '.epub', '.gif', '.jpg', '.jpeg', '.json',
        '.html', '.htm', '.mp3', '.msg', '.odt', '.ogg', '.pdf', '.png', '.pptx',
        '.ps', '.rtf', '.tiff', '.tif', '.txt', '.wav', '.xlsx', '.xls'
    ]

    def get_filepaths(self) -> List[str]:
        filepaths = []
        for path in self.paths:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if any(file.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS):
                            filepaths.append(os.path.join(root, file))
            elif os.path.isfile(path):
                if any(path.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS):
                    filepaths.append(path)
            else:
                logger.warning(f"Skipping non-file path: {path}")
        return filepaths

    def read_files(self, filepaths: List[str]) -> List[str]:
        texts = []
        for filepath in filepaths:
            try:
                text = textract.process(filepath).decode('utf-8')
                texts.append(text)
                logger.info(f"Successfully extracted text from {filepath}")
            except Exception as e:
                logger.error(f"Failed to extract text from {filepath}: {e}")
                if "tesseract" in str(e).lower():
                    logger.error("Ensure that Tesseract OCR is installed and added to your system's PATH.")
        return texts

    def convert_to_markdown(self, text: str) -> str:
        try:
            return pypandoc.convert_text(text, 'md', format='html')
        except Exception as e:
            logger.error(f"Failed to convert text to Markdown: {e}")
            return text  # Return original text if conversion fails

    def chunk_text(self, text: str, method: str = 'paragraph') -> List[str]:
        if method == 'paragraph':
            return text.split('\n\n')
        elif method == 'sentence':
            doc = nlp(text)
            return [sent.text for sent in doc.sents]
        else:
            raise ValueError("Unsupported chunking method")

    def process_documents(self, chunk_method: str = 'paragraph') -> List[str]:
        filepaths = self.get_filepaths()
        texts = self.read_files(filepaths)
        markdown_texts = [self.convert_to_markdown(text) for text in texts]
        chunks = []
        for text in markdown_texts:
            chunks.extend(self.chunk_text(text, method=chunk_method))
        return chunks
