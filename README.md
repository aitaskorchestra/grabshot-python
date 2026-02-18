# GrabShot - Screenshot API for Python

Capture website screenshots, generate PDFs, and extract meta tags with the [GrabShot](https://grabshot.dev) API. Zero dependencies.

## Install

```bash
pip install grabshot
```

## Quick Start

```python
from grabshot import GrabShot

client = GrabShot("your-api-key")

# Capture a screenshot
img = client.capture("https://example.com")
with open("screenshot.png", "wb") as f:
    f.write(img)
```

## Options

```python
# Full page screenshot in WebP
img = client.capture(
    "https://example.com",
    width=1440,
    height=900,
    format="webp",
    full_page=True,
)

# AI cleanup (removes popups/banners) - paid plans
img = client.capture("https://example.com", ai_cleanup=True)

# Capture a specific element
img = client.capture("https://example.com", selector="#hero")

# Wait for dynamic content
img = client.capture("https://example.com", delay=2000)
```

## PDF Generation

```python
pdf = client.pdf("https://example.com")
with open("page.pdf", "wb") as f:
    f.write(pdf)

# Landscape A3
pdf = client.pdf("https://example.com", format="A3", landscape=True)
```

## Meta Tag Extraction

```python
meta = client.meta("https://example.com")
print(meta["title"])
print(meta["description"])
print(meta["og:image"])
```

## Error Handling

```python
from grabshot import GrabShot, GrabShotError

client = GrabShot("your-api-key")
try:
    img = client.capture("https://example.com")
except GrabShotError as e:
    print(f"API error ({e.status}): {e}")
```

## Pricing

| Plan | Price | Screenshots/mo |
|------|-------|---------------|
| Free | $0 | 25 |
| Starter | $9/mo | 1,000 |
| Pro | $29/mo | 10,000 |
| Business | $79/mo | 50,000 |

Get your API key at [grabshot.dev](https://grabshot.dev)

## Links

- [Documentation](https://grabshot.dev/docs)
- [Dashboard](https://grabshot.dev/dashboard)
- [Node.js SDK](https://www.npmjs.com/package/grabshot)
