#!/usr/bin/env python3
"""
Manual testing script for individual components.
Run this to test each component separately before running the full bot.
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_extractor import PDFExtractor
from ollama_processor import OllamaProcessor
from x_poster import XPoster


def test_pdf_extraction():
    """Test PDF extraction."""
    print("\n" + "=" * 60)
    print("Testing PDF Extraction")
    print("=" * 60)

    pdf_path = os.getenv('PDF_PATH')
    if not pdf_path:
        print("ERROR: PDF_PATH not set in environment")
        return False

    try:
        extractor = PDFExtractor(pdf_path)
        count = extractor.get_sentence_count()
        print(f"✓ Successfully loaded {count} sentences")

        if count > 0:
            sample = extractor.get_random_sentence()
            print(f"✓ Sample sentence: {sample[:100]}...")
            return True
        else:
            print("ERROR: No sentences extracted")
            return False

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def test_ollama():
    """Test Ollama connection and processing."""
    print("\n" + "=" * 60)
    print("Testing Ollama")
    print("=" * 60)

    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'llama2')

    try:
        processor = OllamaProcessor(base_url=ollama_url, model=ollama_model)
        print(f"✓ Connected to Ollama at {ollama_url}")
        print(f"✓ Using model: {ollama_model}")

        # Test with sample text
        test_text = "He who fights with monsters should look to it that he himself does not become a monster"
        print(f"\nOriginal: {test_text}")
        print("Rephrasing... (this may take a moment)")

        rephrased = processor.rephrase_quote(test_text)
        print(f"Rephrased: {rephrased}")
        print(f"✓ Successfully rephrased text ({len(rephrased)} chars)")

        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def test_x_api():
    """Test X API connection (does not post)."""
    print("\n" + "=" * 60)
    print("Testing X API Connection")
    print("=" * 60)

    required_vars = ['X_API_KEY', 'X_API_SECRET', 'X_ACCESS_TOKEN', 'X_ACCESS_SECRET']
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        return False

    try:
        poster = XPoster(
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_SECRET')
        )
        print("✓ X API credentials verified")
        print("✓ Connection successful")

        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def test_full_workflow():
    """Test the complete workflow without posting."""
    print("\n" + "=" * 60)
    print("Testing Complete Workflow (No Posting)")
    print("=" * 60)

    try:
        # Extract
        print("\n1. Extracting random sentence from PDF...")
        pdf_path = os.getenv('PDF_PATH')
        extractor = PDFExtractor(pdf_path)
        original = extractor.get_random_sentence()
        print(f"   Original: {original}")

        # Rephrase
        print("\n2. Rephrasing with Ollama...")
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'llama2')
        processor = OllamaProcessor(base_url=ollama_url, model=ollama_model)
        rephrased = processor.rephrase_quote(original)
        print(f"   Rephrased: {rephrased}")
        print(f"   Length: {len(rephrased)} chars")

        # Verify connection (don't post)
        print("\n3. Verifying X API connection...")
        poster = XPoster(
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_SECRET')
        )
        print("   ✓ Ready to post (test mode - not posting)")

        print("\n✓ Complete workflow test successful!")
        print("\nTo actually post this quote, run: python bot.py")

        return True

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Nietzsche Bot - Component Testing")
    print("=" * 60)
    print("\nMake sure you have set your environment variables:")
    print("  export $(cat .env | xargs)")
    print()

    # Check environment
    if not os.getenv('PDF_PATH'):
        print("WARNING: Environment variables may not be loaded")
        print("Run: export $(cat .env | xargs)")
        print()

    results = {
        'PDF Extraction': test_pdf_extraction(),
        'Ollama': test_ollama(),
        'X API': test_x_api(),
        'Full Workflow': test_full_workflow()
    }

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20} {status}")

    all_passed = all(results.values())
    print("\n" + ("=" * 60))

    if all_passed:
        print("All tests passed! Ready to run bot.py")
        return 0
    else:
        print("Some tests failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
