# GrabShot - Website Screenshot API for Python

Capture website screenshots with a single API call. No headless browser setup, no Puppeteer, no Selenium. Just `pip install grabshot` and go.

## Quick Start

```bash
pip install grabshot
```

```python
from grabshot import GrabShot

client = GrabShot("your-api-key")  # Free at https://grabshot.dev
screenshot = client.capture("https://example.com")
screenshot.save("example.png")
```

**Get your free API key at [grabshot.dev](https://grabshot.dev)** - 25 screenshots/month on the free plan, no credit card required.

## Features

- **One line of code** to capture any URL
- **Full-page screenshots** - capture the entire scrollable page
- **Device frames** - wrap screenshots in iPhone, MacBook, etc.
- **Dark mode** - capture sites in dark mode
- **Element capture** - screenshot a specific CSS selector
- **Multiple formats** - PNG, JPEG, WebP
- **Cookie banner removal** - auto-dismiss cookie popups
- **Ad blocking** - clean screenshots without ads
- **PDF conversion** - convert any URL to PDF
- **Meta extraction** - pull Open Graph, Twitter Card, and meta tags
- **Zero dependencies** - uses only Python standard library

## Examples

### Full-page screenshot

```python
screenshot = client.capture(
    "https://example.com",
    full_page=True
)
screenshot.save("full-page.png")
```

### Mobile screenshot with device frame

```python
screenshot = client.capture(
    "https://example.com",
    width=390,
    height=844,
    device_frame="iphone"
)
screenshot.save("mobile.png")
```

### Dark mode JPEG

```python
screenshot = client.capture(
    "https://example.com",
    format="jpeg",
    quality=85,
    dark_mode=True
)
screenshot.save("dark.jpg")
```

### Capture specific element

```python
screenshot = client.capture(
    "https://example.com",
    selector="#hero-section"
)
screenshot.save("hero.png")
```

### Clean screenshot (no ads, no cookie banners)

```python
screenshot = client.capture(
    "https://example.com",
    hide_cookie_banners=True,
    block_ads=True
)
screenshot.save("clean.png")
```

### Convert URL to PDF

```python
pdf_bytes = client.pdf("https://example.com", format="A4")
with open("page.pdf", "wb") as f:
    f.write(pdf_bytes)
```

### Extract meta tags

```python
meta = client.meta("https://example.com")
print(meta["title"])
print(meta["og:image"])
```

## API Reference

### `GrabShot(api_key, base_url="https://grabshot.dev", timeout=30)`

Create a client instance.

### `client.capture(url, **options) -> Screenshot`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | required | URL to capture |
| `width` | int | 1280 | Viewport width (px) |
| `height` | int | 800 | Viewport height (px) |
| `full_page` | bool | False | Capture full scrollable page |
| `format` | str | "png" | "png", "jpeg", or "webp" |
| `quality` | int | auto | JPEG/WebP quality (1-100) |
| `delay` | int | None | Wait before capture (ms) |
| `device_frame` | str | None | "iphone", "macbook", etc. |
| `dark_mode` | bool | False | Enable dark mode |
| `hide_cookie_banners` | bool | False | Remove cookie popups |
| `block_ads` | bool | False | Block ads and trackers |
| `selector` | str | None | CSS selector to capture |
| `wait_for` | str | None | CSS selector to wait for |

### `Screenshot`

- `.save(path)` - Save to file, returns Path
- `.data` - Raw bytes
- `.size` - Size in bytes

## Pricing

| Plan | Price | Screenshots/mo |
|------|-------|----------------|
| Free | $0 | 25 |
| Starter | $9/mo | 1,000 |
| Pro | $29/mo | 10,000 |
| Business | $79/mo | 50,000 |

## Why GrabShot?

- **No infrastructure** - No Docker, no Chrome, no Puppeteer to maintain
- **Fast** - Screenshots in ~2 seconds, globally distributed
- **Reliable** - 99.9% uptime, automatic retries
- **Affordable** - Free tier to get started, pay as you grow

## License

MIT
