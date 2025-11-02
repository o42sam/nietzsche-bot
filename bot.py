"""
Main bot application with scheduling and logging.
"""
import os
import sys
import time
import logging
import signal
from datetime import datetime
from pathlib import Path
from typing import Optional
import schedule

from pdf_extractor import PDFExtractor
from huggingface_processor import HuggingFaceProcessor
from x_poster import XPoster


class NietzscheBot:
    """Automated Nietzsche quote posting bot."""

    def __init__(self, config: dict):
        """
        Initialize the bot.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.running = False
        self._setup_logging()
        self._initialize_components()

    def _setup_logging(self) -> None:
        """Configure logging."""
        log_dir = Path(self.config.get('log_dir', 'logs'))
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"nietzsche_bot_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_components(self) -> None:
        """Initialize PDF extractor, Hugging Face processor, and X poster."""
        try:
            # Initialize PDF extractor
            pdf_path = self.config['pdf_path']
            self.logger.info(f"Loading PDF from {pdf_path}")
            self.pdf_extractor = PDFExtractor(pdf_path)
            self.logger.info(f"Loaded {self.pdf_extractor.get_sentence_count()} sentences")

            # Initialize Hugging Face processor (completely free!)
            model = self.config.get('hf_model', 'mistralai/Mistral-7B-Instruct-v0.2')
            self.logger.info(f"Connecting to Hugging Face API (model: {model})")
            self.processor = HuggingFaceProcessor(model=model)
            self.logger.info("Hugging Face API connection established")

            # Initialize X poster
            self.logger.info("Initializing X API client")
            self.x_poster = XPoster(
                consumer_key=self.config['x_api_key'],
                consumer_secret=self.config['x_api_secret'],
                access_token=self.config['x_access_token'],
                access_token_secret=self.config['x_access_secret']
            )
            self.logger.info("X API client initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize components: {str(e)}")
            raise

    def post_quote(self) -> None:
        """Generate and post a Nietzsche quote."""
        try:
            self.logger.info("Starting quote posting process")

            # Get random sentence
            original_quote = self.pdf_extractor.get_random_sentence()
            self.logger.info(f"Selected quote: {original_quote[:50]}...")

            # Rephrase using Hugging Face
            self.logger.info("Rephrasing quote with Hugging Face API")
            rephrased_quote = self.processor.rephrase_quote(original_quote)
            self.logger.info(f"Rephrased quote: {rephrased_quote[:50]}...")

            # Post to X
            self.logger.info("Posting to X")
            tweet_id = self.x_poster.post_tweet(rephrased_quote)
            self.logger.info(f"Successfully posted tweet: {tweet_id}")

        except Exception as e:
            self.logger.error(f"Error posting quote: {str(e)}", exc_info=True)

    def start(self) -> None:
        """Start the bot with scheduled posting."""
        self.logger.info("Starting Nietzsche Bot")
        self.logger.info(f"Posting interval: {self.config.get('post_interval_hours', 2)} hours")

        # Post immediately on startup if configured
        if self.config.get('post_on_startup', False):
            self.logger.info("Posting initial quote on startup")
            self.post_quote()

        # Schedule regular posts
        interval_hours = self.config.get('post_interval_hours', 2)
        schedule.every(interval_hours).hours.do(self.post_quote)

        self.logger.info("Bot started successfully. Press Ctrl+C to stop.")
        self.running = True

        # Run scheduler
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal")
            self.stop()

    def stop(self) -> None:
        """Stop the bot."""
        self.logger.info("Stopping Nietzsche Bot")
        self.running = False
        schedule.clear()
        self.logger.info("Bot stopped")

    def test_components(self) -> bool:
        """
        Test all components.

        Returns:
            True if all tests pass
        """
        self.logger.info("Testing components...")

        try:
            # Test PDF extractor
            self.logger.info("Testing PDF extractor")
            test_sentence = self.pdf_extractor.get_random_sentence()
            self.logger.info(f"PDF test successful: {test_sentence[:50]}...")

            # Test Hugging Face API
            self.logger.info("Testing Hugging Face API connection")
            if not self.processor.test_connection():
                raise Exception("Hugging Face API connection test failed")
            self.logger.info("Hugging Face API test successful")

            # Test X API
            self.logger.info("Testing X API connection")
            if not self.x_poster.test_connection():
                raise Exception("X API connection test failed")
            self.logger.info("X API test successful")

            self.logger.info("All component tests passed!")
            return True

        except Exception as e:
            self.logger.error(f"Component test failed: {str(e)}")
            return False


def load_config() -> dict:
    """
    Load configuration from environment variables.

    Returns:
        Configuration dictionary
    """
    required_vars = [
        'PDF_PATH',
        'X_API_KEY',
        'X_API_SECRET',
        'X_ACCESS_TOKEN',
        'X_ACCESS_SECRET'
    ]

    # Check required variables
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return {
        'pdf_path': os.getenv('PDF_PATH'),
        'x_api_key': os.getenv('X_API_KEY'),
        'x_api_secret': os.getenv('X_API_SECRET'),
        'x_access_token': os.getenv('X_ACCESS_TOKEN'),
        'x_access_secret': os.getenv('X_ACCESS_SECRET'),
        'hf_model': os.getenv('HF_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2'),
        'post_interval_hours': int(os.getenv('POST_INTERVAL_HOURS', '2')),
        'post_on_startup': os.getenv('POST_ON_STARTUP', 'false').lower() == 'true',
        'log_dir': os.getenv('LOG_DIR', 'logs')
    }


def main():
    """Main entry point."""
    print("=" * 60)
    print("Nietzsche Quote Bot - X (Twitter) Automation")
    print("=" * 60)
    print()

    try:
        # Load configuration
        config = load_config()

        # Initialize bot
        bot = NietzscheBot(config)

        # Test components
        print("\nTesting components...")
        if not bot.test_components():
            print("Component tests failed. Please check logs.")
            sys.exit(1)

        print("\nAll tests passed! Starting bot...")
        print()

        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            print("\nShutdown signal received")
            bot.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start bot
        bot.start()

    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
