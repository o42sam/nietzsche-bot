"""
Grok API integration for text processing.
"""
import os
import requests
from typing import Optional


class GrokProcessor:
    """Process text using Grok API (xAI)."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Grok processor.

        Args:
            api_key: Grok API key (xAI API key)
        """
        self.api_key = api_key or os.getenv('GROK_API_KEY')
        if not self.api_key:
            raise ValueError("GROK_API_KEY is required")

        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"  # or "grok-2-latest"

    def rephrase_quote(self, text: str) -> str:
        """
        Rephrase a quote using Grok.

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
                            "content": "You are a philosophical writer who rephrases Nietzsche's quotes in a modern, engaging way for social media. Keep responses concise and under 280 characters."
                        },
                        {
                            "role": "user",
                            "content": f"Rephrase this Nietzsche quote in a modern, engaging way (under 280 chars): \"{text}\""
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
                raise Exception(f"Grok API returned {response.status_code}: {error_detail}")

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
            raise Exception(f"Error calling Grok API: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing Grok response: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test connection to Grok API.

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
