"""
PDF text extraction utility for Nietzsche quotes bot.
"""
import random
import re
from pathlib import Path
from typing import List
import PyPDF2


class PDFExtractor:
    """Extract and manage text from PDF files."""

    def __init__(self, pdf_path: str):
        """
        Initialize PDF extractor.

        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        self.sentences: List[str] = []
        self._load_pdf()

    def _load_pdf(self) -> None:
        """Load and extract text from PDF."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                for page in pdf_reader.pages:
                    text += page.extract_text() + " "

                # Clean and split into sentences
                text = self._clean_text(text)
                self.sentences = self._split_sentences(text)

        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text.

        Args:
            text: Raw text from PDF

        Returns:
            Cleaned text
        """
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers and common artifacts
        text = re.sub(r'\d+\s*$', '', text, flags=re.MULTILINE)
        return text.strip()

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: Cleaned text

        Returns:
            List of sentences
        """
        # Split on sentence-ending punctuation
        sentences = re.split(r'[.!?]+', text)

        # Clean and filter sentences
        cleaned = []
        for sentence in sentences:
            sentence = sentence.strip()
            # Keep sentences that are between 20 and 280 characters (Twitter limit)
            if 20 <= len(sentence) <= 280:
                cleaned.append(sentence)

        return cleaned

    def get_random_sentence(self) -> str:
        """
        Get a random sentence from the PDF.

        Returns:
            Random sentence
        """
        if not self.sentences:
            raise ValueError("No sentences available")

        return random.choice(self.sentences)

    def get_sentence_count(self) -> int:
        """
        Get total number of available sentences.

        Returns:
            Number of sentences
        """
        return len(self.sentences)
