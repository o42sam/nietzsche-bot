"""
Hugging Face Inference API integration for text processing.
Uses free serverless inference API with authentication token.
"""
import os
from typing import Optional

try:
    from huggingface_hub import InferenceClient
    HAS_HF_HUB = True
except ImportError:
    HAS_HF_HUB = False
    print("Warning: huggingface-hub not installed. Install with: pip install huggingface-hub")


class HuggingFaceProcessor:
    """Process text using Hugging Face's free Inference API."""

    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.2", api_token: Optional[str] = None):
        """
        Initialize Hugging Face processor.

        Args:
            model: Model name to use (default: Mistral 7B Instruct)
                   Other free options:
                   - "mistralai/Mistral-7B-Instruct-v0.2" (recommended)
                   - "HuggingFaceH4/zephyr-7b-beta" (alternative)
                   - "microsoft/phi-2" (smaller, faster)
            api_token: HuggingFace API token (optional, will use HF_API_TOKEN env var if not provided)
        """
        if not HAS_HF_HUB:
            raise ImportError("huggingface-hub is required. Install with: pip install huggingface-hub")

        self.model = model
        self.api_token = api_token or os.getenv("HF_API_TOKEN")

        if not self.api_token:
            raise ValueError(
                "HuggingFace API token is required. "
                "Get one at https://huggingface.co/settings/tokens and set HF_API_TOKEN environment variable"
            )

        # Create inference client
        self.client = InferenceClient(token=self.api_token)
        self._test_connection()

    def _test_connection(self) -> None:
        """Test connection to Hugging Face API."""
        try:
            # Simple test with conversational task
            messages = [{"role": "user", "content": "Hi"}]
            response = self.client.chat_completion(
                messages=messages,
                model=self.model,
                max_tokens=5
            )
            print(f"✓ HuggingFace connection successful (model: {self.model})")
        except Exception as e:
            print(f"Warning: Could not verify connection to Hugging Face API: {str(e)}")
            print("This may be normal if the model is still loading.")

    def rephrase_quote(self, text: str) -> str:
        """
        Rephrase a quote using Hugging Face Inference API.

        Args:
            text: Original text to rephrase

        Returns:
            Rephrased text
        """
        # Prepare the conversation
        messages = [
            {
                "role": "system",
                "content": "You are rephrasing philosophical quotes from Friedrich Nietzsche's works. "
                          "Rephrase quotes in a modern, engaging way while preserving their philosophical meaning. "
                          "Keep responses under 280 characters for social media. "
                          "Only output the rephrased quote without any explanations or commentary."
            },
            {
                "role": "user",
                "content": f"Rephrase this Nietzsche quote: \"{text}\""
            }
        ]

        try:
            # Try up to 3 times (in case model is loading)
            for attempt in range(3):
                try:
                    response = self.client.chat_completion(
                        messages=messages,
                        model=self.model,
                        max_tokens=150,
                        temperature=0.8,
                    )

                    # Extract the rephrased text
                    if response and response.choices:
                        rephrased = response.choices[0].message.content.strip()

                        # Clean up common artifacts
                        rephrased = rephrased.replace('"', '').replace("'", "'")

                        # Remove common prefixes
                        for prefix in ['Rephrased quote:', 'Here is', 'Here\'s', 'Rephrased:']:
                            if rephrased.lower().startswith(prefix.lower()):
                                rephrased = rephrased[len(prefix):].strip()
                                if rephrased.startswith(':'):
                                    rephrased = rephrased[1:].strip()

                        # Ensure it's not too long
                        if len(rephrased) > 280:
                            rephrased = rephrased[:277] + "..."

                        # If we got a valid response, return it
                        if rephrased and len(rephrased) > 20:
                            return rephrased

                except Exception as e:
                    if "loading" in str(e).lower() and attempt < 2:
                        print(f"Model loading, waiting 20s... (attempt {attempt + 1}/3)")
                        import time
                        time.sleep(20)
                        continue
                    raise

            # If all attempts failed or response was invalid, fallback
            print("Warning: Could not rephrase quote, using original")
            return text if len(text) <= 280 else text[:277] + "..."

        except Exception as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            # Fallback to original text
            return text if len(text) <= 280 else text[:277] + "..."

    def test_connection(self) -> bool:
        """
        Test connection to Hugging Face API.

        Returns:
            True if connection successful
        """
        try:
            self._test_connection()
            return True
        except Exception:
            return False
