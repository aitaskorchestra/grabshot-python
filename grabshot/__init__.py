"""GrabShot - Website Screenshot API SDK

Capture website screenshots with a simple Python API.
Free tier: 25 screenshots/month. No credit card required.

Usage:
    from grabshot import GrabShot

    client = GrabShot("your-api-key")
    screenshot = client.capture("https://example.com")

    # Save to file
    screenshot.save("example.png")

    # Or get bytes
    image_bytes = screenshot.content

Get your free API key at https://grabshot.dev
"""

__version__ = "1.0.0"
__author__ = "GrabShot"
__url__ = "https://grabshot.dev"

import requests
from pathlib import Path
from typing import Optional, Dict, Any, Union


class ScreenshotResult:
    """Result of a screenshot capture."""

    def __init__(self, content: bytes, content_type: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.content_type = content_type
        self.metadata = metadata or {}

    def save(self, path: Union[str, Path]) -> Path:
        """Save screenshot to a file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.content)
        return path

    @property
    def size(self) -> int:
        """Size of the screenshot in bytes."""
        return len(self.content)


class GrabShotError(Exception):
    """Base exception for GrabShot errors."""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class GrabShot:
    """GrabShot API client.

    Args:
        api_key: Your GrabShot API key (get one free at https://grabshot.dev)
        base_url: API base URL (default: https://grabshot.dev)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = GrabShot("gs_your_api_key")
        >>> result = client.capture("https://github.com", width=1440, format="png")
        >>> result.save("github.png")
    """

    def __init__(self, api_key: str, base_url: str = "https://grabshot.dev", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"X-API-Key": api_key})

    def capture(
        self,
        url: str,
        *,
        width: int = 1280,
        height: int = 800,
        format: str = "png",
        full_page: bool = False,
        delay: int = 0,
        selector: Optional[str] = None,
        dark_mode: bool = False,
        block_ads: bool = False,
        hide_cookie_banners: bool = False,
        retina: bool = False,
        quality: Optional[int] = None,
        ai_cleanup: bool = False,
    ) -> ScreenshotResult:
        """Capture a screenshot of a URL.

        Args:
            url: The URL to screenshot
            width: Viewport width in pixels (default: 1280)
            height: Viewport height in pixels (default: 800)
            format: Image format - "png", "jpeg", or "webp" (default: "png")
            full_page: Capture the full scrollable page (default: False)
            delay: Wait N milliseconds before capture (default: 0)
            selector: CSS selector to capture specific element
            dark_mode: Enable dark mode (default: False)
            block_ads: Block ads and trackers (default: False)
            hide_cookie_banners: Hide cookie consent banners (default: False)
            retina: 2x resolution for retina displays (default: False)
            quality: JPEG/WebP quality 1-100 (default: auto)
            ai_cleanup: AI-powered cleanup of popups/overlays (paid plans only)

        Returns:
            ScreenshotResult with .content (bytes), .save(path), .size

        Raises:
            GrabShotError: If the API returns an error
        """
        params = {
            "url": url,
            "width": width,
            "height": height,
            "format": format,
            "full_page": str(full_page).lower(),
        }

        if delay > 0:
            params["delay"] = delay
        if selector:
            params["selector"] = selector
        if dark_mode:
            params["dark_mode"] = "true"
        if block_ads:
            params["block_ads"] = "true"
        if hide_cookie_banners:
            params["hide_cookie_banners"] = "true"
        if retina:
            params["retina"] = "true"
        if quality is not None:
            params["quality"] = quality
        if ai_cleanup:
            params["ai_cleanup"] = "true"

        response = self._session.get(
            f"{self.base_url}/api/screenshot",
            params=params,
            timeout=self.timeout,
        )

        if response.status_code != 200:
            try:
                error_data = response.json()
                message = error_data.get("error", response.text)
            except Exception:
                message = response.text
            raise GrabShotError(message, response.status_code)

        return ScreenshotResult(
            content=response.content,
            content_type=response.headers.get("content-type", f"image/{format}"),
        )

    def html_to_image(
        self,
        html: str,
        *,
        width: int = 1280,
        format: str = "png",
        **kwargs,
    ) -> ScreenshotResult:
        """Render HTML string to an image.

        Args:
            html: HTML content to render
            width: Viewport width (default: 1280)
            format: Output format (default: "png")

        Returns:
            ScreenshotResult
        """
        response = self._session.post(
            f"{self.base_url}/api/screenshot",
            json={"html": html, "width": width, "format": format, **kwargs},
            timeout=self.timeout,
        )

        if response.status_code != 200:
            try:
                error_data = response.json()
                message = error_data.get("error", response.text)
            except Exception:
                message = response.text
            raise GrabShotError(message, response.status_code)

        return ScreenshotResult(
            content=response.content,
            content_type=response.headers.get("content-type", f"image/{format}"),
        )

    def pdf(
        self,
        url: str,
        *,
        format: str = "A4",
        landscape: bool = False,
        print_background: bool = True,
    ) -> ScreenshotResult:
        """Generate PDF from a URL (via pdf.grabshot.dev).

        Args:
            url: URL to convert to PDF
            format: Paper format (default: "A4")
            landscape: Landscape orientation (default: False)
            print_background: Include background graphics (default: True)

        Returns:
            ScreenshotResult with PDF content
        """
        response = self._session.get(
            "https://pdf.grabshot.dev/api/pdf",
            params={
                "url": url,
                "format": format,
                "landscape": str(landscape).lower(),
                "printBackground": str(print_background).lower(),
            },
            timeout=self.timeout,
        )

        if response.status_code != 200:
            try:
                message = response.json().get("error", response.text)
            except Exception:
                message = response.text
            raise GrabShotError(message, response.status_code)

        return ScreenshotResult(
            content=response.content,
            content_type="application/pdf",
        )

    def meta(self, url: str) -> Dict[str, Any]:
        """Extract metadata from a URL (via metapeek.grabshot.dev).

        Args:
            url: URL to extract metadata from

        Returns:
            Dictionary with title, description, og tags, etc.
        """
        response = self._session.get(
            "https://metapeek.grabshot.dev/api/meta",
            params={"url": url},
            timeout=self.timeout,
        )

        if response.status_code != 200:
            try:
                message = response.json().get("error", response.text)
            except Exception:
                message = response.text
            raise GrabShotError(message, response.status_code)

        return response.json()

    def __repr__(self):
        return f"GrabShot(base_url={self.base_url!r})"
