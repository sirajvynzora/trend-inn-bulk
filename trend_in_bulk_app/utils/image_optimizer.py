from pathlib import Path

from PIL import Image


def optimize_image(path: str, max_size: tuple[int, int] = (1200, 1200), quality: int = 70, force_square: bool = False) -> None:
    """Optimize an image in place if it exists on disk."""
    image_path = Path(path)
    if not image_path.exists():
        return

    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail(max_size)
            
            if force_square:
                longest_edge = max(img.width, img.height)
                canvas = Image.new("RGB", (longest_edge, longest_edge), (255, 255, 255))
                offset_x = (longest_edge - img.width) // 2
                offset_y = (longest_edge - img.height) // 2
                canvas.paste(img, (offset_x, offset_y))
                img = canvas

            img.save(image_path, quality=quality, optimize=True)
    except Exception:
        # Keep model save resilient even if optimization fails.
        return
