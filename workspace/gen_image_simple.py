import argparse
import os
import sys
from pathlib import Path
from io import BytesIO
import base64

# Simple script for Python 3.9+ without pipe operator and uv requirement
# Requires: pip install google-genai pillow

def get_api_key(provided_key):
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--resolution", default="1K")
    parser.add_argument("--api-key")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key", file=sys.stderr)
        sys.exit(1)

    try:
        from google import genai
        from google.genai import types
        from PIL import Image as PILImage
    except ImportError:
        print("Error: Missing dependencies. Run: pip install google-genai pillow", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    output_path = Path(args.filename)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=args.prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )

        image_saved = False
        for part in response.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                image = PILImage.open(BytesIO(image_data))
                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), 'PNG')
                else:
                    image.convert('RGB').save(str(output_path), 'PNG')
                image_saved = True

        if image_saved:
            print(f"Image saved: {output_path.resolve()}")
        else:
            print("Error: No image generated", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
