"""
Llama API integration for text processing.
FREE models available via HuggingFace Inference API or Together AI.
"""
import os
import requests
from typing import Optional


class LlamaProcessor:
    """Process text using Llama API (free tier available via Together AI)."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Llama processor using Together AI.

        Args:
            api_key: Together AI API key (free tier available)
        """
        self.api_key = api_key or os.getenv('LLAMA_API_KEY')
        if not self.api_key:
            raise ValueError("LLAMA_API_KEY is required")

        # Using Together AI which has free tier for Llama models
        self.base_url = "https://api.together.xyz/v1"
        # Free models available:
        # - meta-llama/Llama-3.2-3B-Instruct-Turbo (fast, small)
        # - meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo (balanced)
        # - meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo (best quality)
        self.model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    def rephrase_quote(self, text: str) -> str:
        """
        Rephrase a quote using Llama.

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
                    "max_tokens": 150,
                    "top_p": 0.9
                },
                timeout=30
            )

            # Add detailed error info
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Llama API returned {response.status_code}: {error_detail}")

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
            raise Exception(f"Error calling Llama API: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing Llama response: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test connection to Llama API.

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
