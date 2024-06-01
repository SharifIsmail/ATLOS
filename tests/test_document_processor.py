# tests/test_document_processor.py
import pytest
from document_processor import DocumentProcessor

@pytest.fixture
def processor():
    return DocumentProcessor(["example_folder"])
def test_get_filepaths(processor):
    filepaths = processor.get_filepaths()
    assert all(filepath.endswith(tuple(DocumentProcessor.SUPPORTED_EXTENSIONS)) for filepath in filepaths)

def test_read_files(processor):
    filepaths = processor.get_filepaths()
    texts = processor.read_files(filepaths)
    assert len(texts) > 0
    assert all(isinstance(text, str) for text in texts)

def test_convert_to_markdown(processor):
    text = "<p>Example</p>"
    markdown = processor.convert_to_markdown(text)
    assert markdown.strip() == "Example"

def test_chunk_text(processor):
    text = "This is a sentence. This is another sentence."
    chunks = processor.chunk_text(text, method='sentence')
    assert len(chunks) == 2

def test_process_documents(processor):
    chunks = processor.process_documents(chunk_method='sentence')
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
