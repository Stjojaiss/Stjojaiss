"""Optional: turn a portrait photo into assets/source.png (background removed, contrast boosted).

Needs: pip install rembg opencv-python. Without a photo, assets/source.png is the Salamandra mark.
Usage: python scripts/prep_photo.py path/to/photo.jpg
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

ROOT = Path(__file__).resolve().parent.parent

src = Image.open(sys.argv[1]).convert("RGBA")
cut = remove(src)
white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
white.alpha_composite(cut)
rgb = np.array(white.convert("RGB"))
lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
lab[..., 0] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(lab[..., 0])
Image.fromarray(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)).save(ROOT / "assets/source.png")
print("wrote assets/source.png")
