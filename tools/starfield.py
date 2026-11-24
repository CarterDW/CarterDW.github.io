"""Seamless starfield tile for the page background: sparse, faint stars on a transparent PNG.

Most stars are single soft pixels; a few are brighter with a small glow. Colors range from
slightly blue to slightly warm white. Positions wrap around the edges, so the tile repeats seamlessly.
"""
import sys
import numpy as np
from PIL import Image

def starfield(size=512, n_faint=110, n_bright=9, seed=3):
    rng = np.random.default_rng(seed)
    rgba = np.zeros((size, size, 4))
    yy, xx = np.mgrid[0:size, 0:size]
    def add(x, y, peak, sigma, color):
        dx = (xx - x + size / 2) % size - size / 2          # periodic distance
        dy = (yy - y + size / 2) % size - size / 2
        a = peak * np.exp(-(dx**2 + dy**2) / (2 * sigma**2))
        rgba[..., 3] = np.maximum(rgba[..., 3], a)
        for c in range(3):
            rgba[..., c] = np.where(a >= rgba[..., 3] - 1e-9, color[c], rgba[..., c])
    tints = [(200, 215, 255), (225, 232, 255), (255, 250, 240), (255, 238, 215)]
    for _ in range(n_faint):
        add(rng.uniform(0, size), rng.uniform(0, size), rng.uniform(0.25, 0.7), rng.uniform(0.45, 0.7),
            tints[rng.integers(len(tints))])
    for _ in range(n_bright):
        add(rng.uniform(0, size), rng.uniform(0, size), rng.uniform(0.8, 1.0), rng.uniform(0.9, 1.4),
            tints[rng.integers(len(tints))])
    rgba[..., 3] *= 255
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/img/stars.png"
    img = starfield()
    img.save(out, optimize=True)
    print(out, img.size)
