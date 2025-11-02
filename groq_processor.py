"""
Groq API integration for text processing.
FREE tier available - fast inference!
"""
import os
import requests
from typing import Optional


class GroqProcessor:
    """Process text using Groq API (free tier available)."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq processor.

        Args:
            api_key: Groq API key
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")

        self.base_url = "https://api.groq.com/openai/v1"
        # Available models on Groq free tier:
        # - llama-3.3-70b-versatile (recommended)
        # - llama-3.1-70b-versatile
        # - mixtral-8x7b-32768
        # - gemma2-9b-it
        self.model = "llama-3.3-70b-versatile"

    def rephrase_quote(self, text: str) -> str:
        """
        Rephrase a quote using Groq.

        Args:
            text: Original text to rephrase

        Returns:
            Rephrased text
        """
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a philosophical writer who rephrases Nietzsche's quotes in a modern, engaging way for social media. Keep responses concise and under 280 characters. Only output the rephrased quote, nothing else."
                        },
                        {
                            "role": "user",
                            "content": f"Rephrase this Nietzsche quote in a modern, engaging way (under 280 chars, no quotes or explanations): {text}"
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 150
                },
                timeout=30
            )

            # Add detailed error info
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Groq API returned {response.status_code}: {error_detail}")

            response.raise_for_status()

            result = response.json()
            rephrased = result['choices'][0]['message']['content'].strip()

            # Clean up common artifacts
            rephrased = rephrased.replace('"', '').replace('"', '').replace('"', '')
            rephrased = rephrased.replace("'", "'").replace("'", "'")

            # Remove any leading/trailing quotes
            rephrased = rephrased.strip("'\"")

            # Ensure it's not too long
            if len(rephrased) > 280:
                rephrased = rephrased[:277] + "..."

            return rephrased if rephrased else text

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Groq API: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing Groq response: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test connection to Groq API.

        Returns:
            True if connection successful
        """
        try:
            # Simple test request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": "Hello"}
                    ],
                    "max_tokens": 10
                },
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
