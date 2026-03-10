import os
from PIL import Image


def pixel_artify(
    image: Image.Image, pixel_size: int = 8, num_colors: int = 16
) -> Image.Image:
    """
    Turns a card into pixel art:
    - Downscales to create big pixels
    - Reduces the color palette (dithered for nice retro feel)
    - Upscales back with sharp nearest-neighbor so you get perfect square pixels
    """
    original_width, original_height = image.size

    # Step 1: Shrink down
    small = image.resize(
        (original_width // pixel_size, original_height // pixel_size),
        resample=Image.NEAREST,
    )

    # Step 2: Reduce colors (with Floyd-Steinberg dithering for that classic pixel-art vibe)
    quantized = small.quantize(
        colors=num_colors, dither=Image.Dither.FLOYDSTEINBERG
    ).convert("RGB")  # back to RGB so we can upscale cleanly

    # Step 3: Blow it back up with blocky pixels
    pixelated = quantized.resize(
        (original_width, original_height), resample=Image.NEAREST
    )

    # TODO: try out adding this in?
    # pixelated = pixelated.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return pixelated


# ========================= CONFIGURATION =========================
INPUT_FOLDER = "cards"  # ← put your 78 original images here
OUTPUT_FOLDER = "pixel_cards"  # ← results will go here

PIXEL_SIZE = 4  # Lower = finer pixel art, higher = chunkier (try 3–8)
NUM_COLORS = 28  # More colors = richer detail on Rider-Waite cards (16–32)
# =================================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Starting pixel-art conversion of 78 Rider-Waite cards...\n")

for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        input_path = os.path.join(INPUT_FOLDER, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.png")

        try:
            with Image.open(input_path) as img:
                # Convert to RGB (handles RGBA cards safely)
                if img.mode in ("RGBA", "LA", "P"):
                    # Preserve any transparency as white background (most tarot scans don't need it)
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(
                        img, mask=img.split()[-1] if img.mode == "RGBA" else None
                    )
                    img = background
                else:
                    img = img.convert("RGB")

                pixel_card = pixel_artify(
                    img, pixel_size=PIXEL_SIZE, num_colors=NUM_COLORS
                )
                pixel_card.save(output_path, optimize=True)

            print(f"✓ {filename}")

        except Exception as e:
            print(f"✗ Error with {filename}: {e}")

print("\nAll done! Check the 'pixel_cards' folder.")
