from abc import ABC, abstractmethod
from typing import List, Union

class BaseDocumentProcessor(ABC):
    def __init__(self, paths: Union[List[str], str]):
        self.paths = paths if isinstance(paths, list) else [paths]

    @abstractmethod
    def get_filepaths(self) -> List[str]:
        """
        Retrieves a list of file paths that are supported by Textract.
        Returns a list of file paths.
        """
        pass

    @abstractmethod
    def read_files(self, filepaths: List[str]) -> List[str]:
        """
        Reads the files from the given file paths and extracts text content.
        Returns a list of extracted text contents from the files.
        """
        pass

    @abstractmethod
    def convert_to_markdown(self, text: str) -> str:
        """
        Converts the given text content to Markdown format.
        Returns the converted Markdown text.
        """
        pass

    @abstractmethod
    def chunk_text(self, text: str, method: str = 'paragraph') -> List[str]:
        """
        Chunks the given text content into smaller pieces based on the specified method.
        Supported methods: 'paragraph', 'sentence'.
        Returns a list of text chunks.
        """
        pass

    @abstractmethod
    def process_documents(self, chunk_method: str = 'paragraph') -> List[str]:
        """
        Processes the documents by getting file paths, reading, converting, and chunking the text.
        Returns a list of processed text chunks.
        """
        pass
