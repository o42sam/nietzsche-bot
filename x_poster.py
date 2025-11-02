"""
X (Twitter) API v2 posting functionality.
"""
import tweepy
from typing import Optional
import logging


class XPoster:
    """Handle posting to X using API v2."""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str
    ):
        """
        Initialize X API client.

        Args:
            consumer_key: API key
            consumer_secret: API key secret
            access_token: Access token
            access_token_secret: Access token secret
        """
        self.logger = logging.getLogger(__name__)

        try:
            self.client = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            self._verify_credentials()
        except Exception as e:
            raise Exception(f"Failed to initialize X API client: {str(e)}")

    def _verify_credentials(self) -> None:
        """Verify API credentials are valid."""
        try:
            # Test credentials by getting user info
            self.client.get_me()
            self.logger.info("X API credentials verified successfully")
        except tweepy.errors.Unauthorized:
            raise Exception("Invalid X API credentials")
        except Exception as e:
            raise Exception(f"Error verifying credentials: {str(e)}")

    def post_tweet(self, text: str) -> Optional[str]:
        """
        Post a tweet to X.

        Args:
            text: Tweet text (max 280 characters)

        Returns:
            Tweet ID if successful, None otherwise
        """
        if len(text) > 280:
            self.logger.warning(f"Tweet too long ({len(text)} chars), truncating")
            text = text[:277] + "..."

        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            self.logger.info(f"Tweet posted successfully: {tweet_id}")
            return tweet_id

        except tweepy.errors.TweepyException as e:
            self.logger.error(f"Error posting tweet: {str(e)}")
            raise Exception(f"Failed to post tweet: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test connection to X API.

        Returns:
            True if connection successful
        """
        try:
            self.client.get_me()
            return True
        except Exception:
            return False
