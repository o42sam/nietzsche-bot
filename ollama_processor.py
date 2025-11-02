"""
Ollama integration for text processing.
"""
import json
import requests
from typing import Optional


class OllamaProcessor:
    """Process text using local Ollama model."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialize Ollama processor.

        Args:
            base_url: Ollama API base URL
            model: Model name to use
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self._verify_connection()

    def _verify_connection(self) -> None:
        """Verify connection to Ollama server."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}: {str(e)}")

    def rephrase_quote(self, text: str) -> str:
        """
        Rephrase a quote using Ollama.

        Args:
            text: Original text to rephrase

        Returns:
            Rephrased text
        """
        prompt = f"""You are rephrasing philosophical quotes from Friedrich Nietzsche's "Beyond Good and Evil".

Original quote: "{text}"

Task: Rephrase this quote in a modern, engaging way while preserving its philosophical meaning.
Keep it concise (under 280 characters) and impactful for social media.
Do not add quotation marks, explanations, or commentary. Only output the rephrased quote.

Rephrased quote:"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                    }
                },
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            rephrased = result.get('response', '').strip()

            # Clean up common artifacts
            rephrased = rephrased.replace('"', '').replace("'", "'")

            # Ensure it's not too long
            if len(rephrased) > 280:
                rephrased = rephrased[:277] + "..."

            return rephrased if rephrased else text

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Ollama API: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Error parsing Ollama response: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test connection to Ollama.

        Returns:
            True if connection successful
        """
        try:
            self._verify_connection()
            return True
        except ConnectionError:
            return False
