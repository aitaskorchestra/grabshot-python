"""GrabShot - Website Screenshot API client for Python.

Capture website screenshots with a simple API call. Free tier included.

Usage:
    from grabshot import GrabShot

    client = GrabShot("your-api-key")
    screenshot = client.capture("https://example.com")
    screenshot.save("example.png")

Get your free API key at https://grabshot.dev
"""

__version__ = "1.0.0"

from .client import GrabShot, Screenshot, GrabShotError

__all__ = ["GrabShot", "Screenshot", "GrabShotError"]
