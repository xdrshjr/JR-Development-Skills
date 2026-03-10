#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.65.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate or edit images using Nano Banana Pro (Gemini 3 Pro Image) API.

Usage:
    # Text-to-image generation
    uv run generate_image.py --prompt "description" --filename "output.png" [--resolution 1K|2K|4K] [--api-key KEY]

    # Image editing (with input image)
    uv run generate_image.py --prompt "edit instructions" --filename "output.png" --input-image "source.png" [--resolution 1K|2K|4K] [--api-key KEY]
"""

import argparse
import os
import sys
from pathlib import Path


def load_env_file(env_path: Path) -> dict:
    """Load environment variables from .env file."""
    env_vars = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key with fallback chain: argument > .env file > environment variable."""
    if provided_key:
        return provided_key

    # Try .env in the skill's root directory (nano-banana-draw/)
    script_dir = Path(__file__).parent.parent
    env_path = script_dir / ".env"
    env_vars = load_env_file(env_path)
    if "GEMINI_API_KEY" in env_vars:
        return env_vars["GEMINI_API_KEY"]

    # Try .env in current working directory
    cwd_env = Path.cwd() / ".env"
    if cwd_env != env_path:
        cwd_vars = load_env_file(cwd_env)
        if "GEMINI_API_KEY" in cwd_vars:
            return cwd_vars["GEMINI_API_KEY"]

    return os.environ.get("GEMINI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Generate or edit images using Nano Banana Pro (Gemini 3 Pro Image)"
    )
    parser.add_argument(
        "--prompt", "-p", required=True, help="Image description or edit instructions"
    )
    parser.add_argument(
        "--filename", "-f", required=True,
        help="Output filename (e.g., 2026-03-10-14-30-00-sunset.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        help="Optional input image path for editing/modification"
    )
    parser.add_argument(
        "--resolution", "-r", choices=["1K", "2K", "4K"], default=None,
        help="Output resolution: 1K (~1024px), 2K (~2048px), or 4K (~4096px). Default: 1K (or auto-detect from input image)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides GEMINI_API_KEY env var and .env file)"
    )

    args = parser.parse_args()

    # Resolve API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key found.", file=sys.stderr)
        print("Provide a key via one of:", file=sys.stderr)
        print("  1. --api-key argument", file=sys.stderr)
        print("  2. GEMINI_API_KEY in .env file", file=sys.stderr)
        print("  3. GEMINI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import after key check to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    # Set up output path — handle both absolute and relative paths
    filename_path = Path(args.filename)
    output_path = filename_path if filename_path.is_absolute() else Path.cwd() / filename_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Handle input image for editing mode
    input_image = None
    output_resolution = args.resolution or "1K"
    if args.input_image:
        try:
            input_image = PILImage.open(args.input_image)
            print(f"Loaded input image: {args.input_image}")

            # Auto-detect resolution from input image only when user didn't specify
            if args.resolution is None:
                width, height = input_image.size
                max_dim = max(width, height)
                if max_dim >= 3000:
                    output_resolution = "4K"
                elif max_dim >= 1500:
                    output_resolution = "2K"
                else:
                    output_resolution = "1K"
                print(f"Auto-detected resolution: {output_resolution} (from {width}x{height})")
        except Exception as e:
            print(f"Error loading input image: {e}", file=sys.stderr)
            sys.exit(1)

    # Build request contents
    if input_image:
        contents = [input_image, args.prompt]
        print(f"Editing image with resolution {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(image_size=output_resolution),
            ),
        )

        image_saved = False
        # Handle different response structures across google-genai versions
        parts = getattr(response, 'parts', None)
        if parts is None:
            # Fallback: some versions use response.candidates[0].content.parts
            try:
                parts = response.candidates[0].content.parts
            except (AttributeError, IndexError):
                parts = []
        for part in parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                from io import BytesIO
                import base64

                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Normalize to RGB and save as PNG
                if image.mode == "RGBA":
                    rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), "PNG")
                elif image.mode == "RGB":
                    image.save(str(output_path), "PNG")
                else:
                    image.convert("RGB").save(str(output_path), "PNG")
                image_saved = True

        if image_saved:
            print(f"\nImage saved: {output_path.resolve()}")
        else:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
