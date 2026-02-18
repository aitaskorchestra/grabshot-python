"""GrabShot API client."""

import json
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional


class GrabShotError(Exception):
    """Error from the GrabShot API."""
    def __init__(self, message: str, status: int = 0):
        super().__init__(message)
        self.status = status


class GrabShot:
    """
    GrabShot Screenshot API client.

    Usage:
        from grabshot import GrabShot

        client = GrabShot("your-api-key")
        screenshot = client.capture("https://example.com")

        # Save to file
        with open("screenshot.png", "wb") as f:
            f.write(screenshot)

        # With options
        screenshot = client.capture(
            "https://example.com",
            width=1440,
            height=900,
            format="webp",
            full_page=True,
            ai_cleanup=True,
        )
    """

    BASE_URL = "https://grabshot.dev/api"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        if base_url:
            self.BASE_URL = base_url.rstrip("/")

    def capture(
        self,
        url: str,
        *,
        width: int = 1280,
        height: int = 800,
        format: str = "png",
        full_page: bool = False,
        ai_cleanup: bool = False,
        delay: int = 0,
        selector: Optional[str] = None,
    ) -> bytes:
        """
        Capture a screenshot of a URL.

        Args:
            url: The URL to screenshot.
            width: Viewport width in pixels (default: 1280).
            height: Viewport height in pixels (default: 800).
            format: Image format - 'png', 'jpeg', or 'webp' (default: 'png').
            full_page: Capture the full scrollable page (default: False).
            ai_cleanup: Use AI to remove popups/banners - paid plans only (default: False).
            delay: Wait N milliseconds before capture (default: 0).
            selector: CSS selector to capture a specific element.

        Returns:
            Screenshot image as bytes.

        Raises:
            GrabShotError: If the API returns an error.
        """
        params = {
            "url": url,
            "width": str(width),
            "height": str(height),
            "format": format,
            "fullPage": str(full_page).lower(),
        }
        if ai_cleanup:
            params["aiCleanup"] = "true"
        if delay > 0:
            params["delay"] = str(delay)
        if selector:
            params["selector"] = selector

        query = urllib.parse.urlencode(params)
        req_url = f"{self.BASE_URL}/screenshot?{query}"

        req = urllib.request.Request(req_url)
        req.add_header("X-API-Key", self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
                msg = data.get("error", body)
            except (json.JSONDecodeError, ValueError):
                msg = body
            raise GrabShotError(msg, status=e.code) from e
        except urllib.error.URLError as e:
            raise GrabShotError(f"Connection error: {e.reason}") from e

    def pdf(
        self,
        url: str,
        *,
        format: str = "A4",
        landscape: bool = False,
        print_background: bool = True,
    ) -> bytes:
        """
        Convert a URL to PDF via PDFMagic.

        Args:
            url: The URL to convert.
            format: Paper format (default: 'A4').
            landscape: Landscape orientation (default: False).
            print_background: Include background colors/images (default: True).

        Returns:
            PDF file as bytes.
        """
        params = {
            "url": url,
            "format": format,
            "landscape": str(landscape).lower(),
            "printBackground": str(print_background).lower(),
        }
        query = urllib.parse.urlencode(params)
        req_url = f"https://pdf.grabshot.dev/api/pdf?{query}"

        req = urllib.request.Request(req_url)
        req.add_header("X-API-Key", self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
                msg = data.get("error", body)
            except (json.JSONDecodeError, ValueError):
                msg = body
            raise GrabShotError(msg, status=e.code) from e

    def meta(self, url: str) -> dict:
        """
        Extract meta tags from a URL via MetaPeek.

        Args:
            url: The URL to analyze.

        Returns:
            Dictionary of meta tag data.
        """
        params = {"url": url}
        query = urllib.parse.urlencode(params)
        req_url = f"https://metapeek.grabshot.dev/api/extract?{query}"

        req = urllib.request.Request(req_url)
        req.add_header("X-API-Key", self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
                msg = data.get("error", body)
            except (json.JSONDecodeError, ValueError):
                msg = body
            raise GrabShotError(msg, status=e.code) from e
