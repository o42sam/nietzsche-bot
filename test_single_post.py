#!/usr/bin/env python3
"""
Test script to post a single Nietzsche quote.

Run with: export $(cat .env | xargs) && python3 test_single_post.py
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_extractor import PDFExtractor
from groq_processor import GroqProcessor
from x_poster import XPoster


def test_single_post():
    """Test posting a single quote."""
    print("=" * 60)
    print("Testing Single Quote Post")
    print("=" * 60)
    print()

    try:
        # Step 1: Extract a random quote from PDF
        print("Step 1: Extracting random sentence from PDF...")
        pdf_path = os.getenv('PDF_PATH')
        if not pdf_path:
            raise ValueError("PDF_PATH not set in .env file")

        extractor = PDFExtractor(pdf_path)
        original = extractor.get_random_sentence()
        print(f"Original quote: {original}")
        print(f"Length: {len(original)} characters")
        print()

        # Step 2: Rephrase with Groq
        print("Step 2: Rephrasing with Groq API (FREE)...")
        print("(This may take a moment...)")
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not set in .env file")

        processor = GroqProcessor(api_key=groq_api_key)
        rephrased = processor.rephrase_quote(original)
        print(f"Rephrased quote: {rephrased}")
        print(f"Length: {len(rephrased)} characters")
        print()

        # Step 3: Post to X (Twitter)
        print("Step 3: Posting to X (Twitter)...")
        poster = XPoster(
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_SECRET')
        )

        tweet_id = poster.post_tweet(rephrased)
        print(f"Successfully posted tweet!")
        print(f"Tweet ID: {tweet_id}")
        print()

        print("=" * 60)
        print("SUCCESS! Quote posted to X (Twitter)")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_single_post()
    sys.exit(0 if success else 1)
