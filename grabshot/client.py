"""GrabShot API client."""

import urllib.request
import urllib.parse
import urllib.error
import json
from pathlib import Path
from typing import Optional, Union


class GrabShotError(Exception):
    """Raised when the GrabShot API returns an error."""

    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class Screenshot:
    """Represents a captured screenshot."""

    def __init__(self, data: bytes, content_type: str = "image/png"):
        self.data = data
        self.content_type = content_type

    def save(self, path: Union[str, Path]) -> Path:
        """Save the screenshot to a file."""
        path = Path(path)
        path.write_bytes(self.data)
        return path

    @property
    def size(self) -> int:
        """Size of the screenshot in bytes."""
        return len(self.data)


class GrabShot:
    """GrabShot API client.

    Args:
        api_key: Your GrabShot API key. Get one free at https://grabshot.dev
        base_url: API base URL (default: https://grabshot.dev)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = GrabShot("your-api-key")
        >>> screenshot = client.capture("https://example.com")
        >>> screenshot.save("example.png")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://grabshot.dev",
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def capture(
        self,
        url: str,
        *,
        width: int = 1280,
        height: int = 800,
        full_page: bool = False,
        format: str = "png",
        quality: Optional[int] = None,
        delay: Optional[int] = None,
        device_frame: Optional[str] = None,
        dark_mode: bool = False,
        hide_cookie_banners: bool = False,
        block_ads: bool = False,
        selector: Optional[str] = None,
        wait_for: Optional[str] = None,
    ) -> Screenshot:
        """Capture a screenshot of a URL.

        Args:
            url: The URL to screenshot
            width: Viewport width in pixels (default: 1280)
            height: Viewport height in pixels (default: 800)
            full_page: Capture full scrollable page (default: False)
            format: Image format - "png", "jpeg", or "webp" (default: "png")
            quality: JPEG/WebP quality 1-100 (default: auto)
            delay: Wait N milliseconds before capture (default: none)
            device_frame: Add device frame - "iphone", "macbook", etc. (default: none)
            dark_mode: Enable dark mode (default: False)
            hide_cookie_banners: Auto-dismiss cookie banners (default: False)
            block_ads: Block ads and trackers (default: False)
            selector: CSS selector to capture specific element (default: none)
            wait_for: CSS selector to wait for before capture (default: none)

        Returns:
            Screenshot object with .save() and .data attributes

        Raises:
            GrabShotError: If the API returns an error
        """
        params = {
            "url": url,
            "apiKey": self.api_key,
            "width": str(width),
            "height": str(height),
            "format": format,
        }

        if full_page:
            params["fullPage"] = "true"
        if quality is not None:
            params["quality"] = str(quality)
        if delay is not None:
            params["delay"] = str(delay)
        if device_frame:
            params["deviceFrame"] = device_frame
        if dark_mode:
            params["darkMode"] = "true"
        if hide_cookie_banners:
            params["hideCookieBanners"] = "true"
        if block_ads:
            params["blockAds"] = "true"
        if selector:
            params["selector"] = selector
        if wait_for:
            params["waitFor"] = wait_for

        query = urllib.parse.urlencode(params)
        api_url = f"{self.base_url}/v1/screenshot?{query}"

        req = urllib.request.Request(api_url)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = resp.read()
                content_type = resp.headers.get("Content-Type", "image/png")
                return Screenshot(data, content_type)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(body)
                msg = err.get("error", body)
            except json.JSONDecodeError:
                msg = body
            raise GrabShotError(msg, e.code) from e
        except urllib.error.URLError as e:
            raise GrabShotError(f"Connection failed: {e.reason}") from e

    def pdf(
        self,
        url: str,
        *,
        format: str = "A4",
        landscape: bool = False,
        print_background: bool = True,
        margin: Optional[str] = None,
    ) -> bytes:
        """Convert a URL to PDF using the PDFMagic API.

        Args:
            url: The URL to convert
            format: Paper format - "A4", "Letter", etc. (default: "A4")
            landscape: Landscape orientation (default: False)
            print_background: Include background graphics (default: True)
            margin: CSS margin string e.g. "1cm" (default: none)

        Returns:
            PDF bytes

        Raises:
            GrabShotError: If the API returns an error
        """
        params = {
            "url": url,
            "apiKey": self.api_key,
            "format": format,
        }
        if landscape:
            params["landscape"] = "true"
        if print_background:
            params["printBackground"] = "true"
        if margin:
            params["margin"] = margin

        query = urllib.parse.urlencode(params)
        api_url = f"https://pdf.grabshot.dev/v1/pdf?{query}"

        req = urllib.request.Request(api_url)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise GrabShotError(body, e.code) from e

    def meta(self, url: str) -> dict:
        """Extract meta tags from a URL using the MetaPeek API.

        Args:
            url: The URL to extract meta from

        Returns:
            Dictionary of meta tag data

        Raises:
            GrabShotError: If the API returns an error
        """
        params = {"url": url, "apiKey": self.api_key}
        query = urllib.parse.urlencode(params)
        api_url = f"https://metapeek.grabshot.dev/v1/meta?{query}"

        req = urllib.request.Request(api_url)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise GrabShotError(body, e.code) from e
