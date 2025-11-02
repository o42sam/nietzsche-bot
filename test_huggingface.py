#!/usr/bin/env python3
"""
Test HuggingFace model integration with a single post.
"""
import os
import sys
from huggingface_processor import HuggingFaceProcessor
from pdf_extractor import PDFExtractor


def test_huggingface_post():
    """Test HuggingFace integration with a single post."""

    print("=" * 60)
    print("HuggingFace Model Integration Test")
    print("=" * 60)

    # Initialize PDF extractor
    pdf_path = os.getenv("PDF_PATH", "./nietzsche.pdf")
    print(f"\n1. Loading quotes from: {pdf_path}")

    try:
        pdf_extractor = PDFExtractor(pdf_path)
        quote = pdf_extractor.get_random_sentence()
        print(f"   ✓ Original quote extracted ({len(quote)} chars)")
        print(f"   ✓ Total sentences available: {pdf_extractor.get_sentence_count()}")
        print(f"\n   Original quote:")
        print(f"   {'-' * 56}")
        print(f"   {quote}")
        print(f"   {'-' * 56}")
    except Exception as e:
        print(f"   ✗ Error extracting quote: {e}")
        return False

    # Initialize HuggingFace processor
    print(f"\n2. Initializing HuggingFace processor...")
    model = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
    print(f"   Model: {model}")

    try:
        hf_processor = HuggingFaceProcessor(model=model)
        print(f"   ✓ HuggingFace processor initialized")
    except Exception as e:
        print(f"   ✗ Error initializing processor: {e}")
        return False

    # Test rephrasing
    print(f"\n3. Testing quote rephrasing...")
    print(f"   (This may take 20-60 seconds if model is loading)")

    try:
        rephrased = hf_processor.rephrase_quote(quote)
        print(f"   ✓ Quote rephrased successfully ({len(rephrased)} chars)")
        print(f"\n   Rephrased quote:")
        print(f"   {'-' * 56}")
        print(f"   {rephrased}")
        print(f"   {'-' * 56}")

        # Validate length for Twitter
        if len(rephrased) > 280:
            print(f"\n   ⚠ Warning: Quote is {len(rephrased)} chars (exceeds 280)")
        else:
            print(f"\n   ✓ Quote length OK for Twitter ({len(rephrased)}/280 chars)")

    except Exception as e:
        print(f"   ✗ Error rephrasing quote: {e}")
        return False

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✓ PDF extraction: SUCCESS")
    print("✓ HuggingFace initialization: SUCCESS")
    print("✓ Quote rephrasing: SUCCESS")
    print("\nHuggingFace integration test PASSED!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    # Load environment variables from .env file
    import os
    from pathlib import Path

    # Read .env file manually
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

    success = test_huggingface_post()
    sys.exit(0 if success else 1)
