"""
Hugging Face Inference API integration for text processing.
Uses free serverless inference API - no authentication required for public models.
"""
import json
import requests
from typing import Optional


class HuggingFaceProcessor:
    """Process text using Hugging Face's free Inference API."""

    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        """
        Initialize Hugging Face processor.

        Args:
            model: Model name to use (default: Mistral 7B Instruct)
                   Other free options:
                   - "mistralai/Mixtral-8x7B-Instruct-v0.1" (larger, slower)
                   - "HuggingFaceH4/zephyr-7b-beta" (alternative)
                   - "meta-llama/Llama-2-7b-chat-hf" (if available)
        """
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self._test_connection()

    def _test_connection(self) -> None:
        """Test connection to Hugging Face API."""
        try:
            # Simple test request
            response = requests.post(
                self.api_url,
                json={"inputs": "test", "parameters": {"max_new_tokens": 5}},
                timeout=10
            )
            # If model is loading, it will return 503 with estimated_time
            if response.status_code == 503:
                result = response.json()
                if "estimated_time" in result:
                    print(f"Model is loading, estimated wait: {result['estimated_time']}s")
                    return  # This is okay, model will be ready soon
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
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
        prompt = f"""<s>[INST] You are rephrasing philosophical quotes from Friedrich Nietzsche's "Beyond Good and Evil".

Original quote: "{text}"

Task: Rephrase this quote in a modern, engaging way while preserving its philosophical meaning.
Keep it concise (under 280 characters) and impactful for social media.
Do not add quotation marks, explanations, or commentary. Only output the rephrased quote. [/INST]

Rephrased quote: """

        try:
            # Try up to 3 times (in case model is loading)
            for attempt in range(3):
                response = requests.post(
                    self.api_url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 150,
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "do_sample": True,
                            "return_full_text": False
                        }
                    },
                    timeout=60
                )

                # If model is loading, wait and retry
                if response.status_code == 503:
                    result = response.json()
                    if "estimated_time" in result:
                        wait_time = min(result["estimated_time"], 20)  # Cap at 20s
                        print(f"Model loading, waiting {wait_time}s...")
                        import time
                        time.sleep(wait_time)
                        continue

                response.raise_for_status()

                result = response.json()

                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    rephrased = result[0].get('generated_text', '').strip()
                elif isinstance(result, dict):
                    rephrased = result.get('generated_text', '').strip()
                else:
                    rephrased = str(result).strip()

                # Clean up common artifacts
                rephrased = rephrased.replace('"', '').replace("'", "'")

                # Remove any remaining instruction tags
                if '[/INST]' in rephrased:
                    rephrased = rephrased.split('[/INST]')[-1].strip()

                # Remove common prefixes
                for prefix in ['Rephrased quote:', 'Here is', 'Here\'s']:
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

                # If response is too short or empty, fallback to original
                break

            # If all attempts failed or response was invalid, return original
            print("Warning: Could not rephrase quote, using original")
            return text if len(text) <= 280 else text[:277] + "..."

        except requests.exceptions.RequestException as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            # Fallback to original text
            return text if len(text) <= 280 else text[:277] + "..."
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Hugging Face response: {str(e)}")
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
