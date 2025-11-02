#!/usr/bin/env python3
"""
Test script to verify Grok API integration.

Run with: export $(cat .env | xargs) && python3 test_grok.py
Or: set -a && source .env && set +a && python3 test_grok.py
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from grok_processor import GrokProcessor


def test_grok_api():
    """Test Grok API connection and rephrasing."""
    print("=" * 60)
    print("Testing Grok API")
    print("=" * 60)
    print()

    # Get API key
    api_key = os.getenv('GROK_API_KEY')
    if not api_key:
        print("ERROR: GROK_API_KEY not set in environment")
        print("Run: export GROK_API_KEY='your_key_here'")
        return False

    try:
        # Initialize processor
        print("1. Initializing Grok processor...")
        processor = GrokProcessor(api_key=api_key)
        print("   ✓ Processor initialized")
        print()

        # Test connection
        print("2. Testing API connection...")
        if processor.test_connection():
            print("   ✓ Connection successful")
        else:
            print("   ✗ Connection failed")
            return False
        print()

        # Test rephrasing
        print("3. Testing quote rephrasing...")
        test_quote = "He who fights with monsters should look to it that he himself does not become a monster. And if you gaze long into an abyss, the abyss also gazes into you."
        print(f"   Original: {test_quote}")
        print()
        print("   Rephrasing (this may take a moment)...")

        rephrased = processor.rephrase_quote(test_quote)
        print(f"   Rephrased: {rephrased}")
        print(f"   Length: {len(rephrased)} characters")
        print()

        if rephrased and len(rephrased) <= 280:
            print("   ✓ Rephrasing successful")
            print()
            print("=" * 60)
            print("✓ All Grok API tests passed!")
            print("=" * 60)
            return True
        else:
            print("   ✗ Rephrasing failed or too long")
            return False

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_grok_api()
    sys.exit(0 if success else 1)
