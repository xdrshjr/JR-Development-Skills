# Nano Banana Draw

AI-powered image generation and editing skill for Claude Code, using Google's Gemini 3 Pro Image API.

## Features

- **Text-to-Image**: Generate images from natural language descriptions
- **Image Editing**: Modify existing images with text instructions
- **Multi-Resolution**: 1K (fast), 2K (balanced), 4K (maximum quality)
- **Auto API Key Detection**: Checks `--api-key` arg → `.env` file → `GEMINI_API_KEY` environment variable

## Quick Start

### 1. Get a Gemini API Key

Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).

### 2. Set the API Key

```bash
# Option A: Environment variable (recommended)
export GEMINI_API_KEY="your-key-here"

# Option B: .env file in the skill directory
echo 'GEMINI_API_KEY=your-key-here' > nano-banana-draw/.env
```

### 3. Use the Skill

In Claude Code, simply ask:

```
"Draw a sunset over mountains"
"Generate a cyberpunk cityscape at 4K resolution"
"Edit this image to add rain effects" (with an image path)
/nano-banana-draw
```

## Trigger Phrases

```
"generate an image"
"draw something"
"create a picture"
"edit this image"
"生成图片"
"画图"
"绘图"
/nano-banana-draw
```

## Resolution Guide

| Resolution | Size | Generation Time | Best For |
|-----------|------|----------------|----------|
| 1K | ~1024px | 2-3 min | Previews, quick iterations |
| 2K | ~2048px | 3-4 min | General use, presentations |
| 4K | ~4096px | 4-6 min | Print, high-quality output |

## Script Usage (Standalone)

```bash
# Text-to-image
uv run scripts/generate_image.py --prompt "a serene lake at dawn" --filename "img/lake.png"

# Image editing
uv run scripts/generate_image.py --prompt "add northern lights to the sky" --filename "img/lake-aurora.png" --input-image "img/lake.png"

# With explicit resolution and API key
uv run scripts/generate_image.py --prompt "mountain landscape" --filename "img/mountain.png" --resolution 4K --api-key "your-key"
```

## Requirements

- `uv` (Python package runner — auto-installs dependencies)
- `google-genai` >= 1.65.0 (required for `types.ImageConfig` support)
- `pillow` >= 10.0.0
- Google Gemini API key with image generation access

### If `uv run` fails on Windows

Some Windows environments have issues with `uv` installing certain packages (e.g., `rsa`). In that case, install dependencies manually and use `python` directly:

```bash
pip install "google-genai>=1.65.0" pillow
python scripts/generate_image.py --prompt "your prompt" --filename "output.png"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `has no attribute 'ImageConfig'` | Upgrade: `pip install --upgrade google-genai` (need >= 1.65.0) |
| `'GenerateContentResponse' object has no attribute 'parts'` | Upgrade `google-genai` to >= 1.65.0 |
| `uv run` fails with package install errors on Windows | Use `pip install` + `python` instead (see above) |
| `404 NOT_FOUND` model error | Ensure model is `gemini-3-pro-image-preview`; verify with API |
