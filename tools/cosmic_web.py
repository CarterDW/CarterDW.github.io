"""Background image for the site: a 2D cosmic web from the Zel'dovich approximation.

Particles start on a grid at q and move to x = q + D * psi(q), where psi = -grad(phi) and phi is a
Gaussian random field with a CDM-like power spectrum (P_phi ~ k^-n, smoothed at small scales).
The image is the log of the particle density, so filaments and nodes are bright and voids are dark.
Periodic box, so the image tiles seamlessly.
"""
import numpy as np
from PIL import Image

def cosmic_web(ny=2400, nx=4800, sigma_delta=2.4, slope=-1.1, kc_cells=22.0, seed=11, sub=3, blur=1.2):
    """Zel'dovich particles on an (ny, nx) grid, binned onto an (ny/sub, nx/sub) mesh.

    The linear density has P(k) ~ k^slope with a Gaussian cutoff at wavelength kc_cells (in mesh cells),
    scaled to rms sigma_delta (the growth factor). Displacement: psi_k = i k delta_k / k^2, so div psi = -delta.
    """
    rng = np.random.default_rng(seed)
    ky = np.fft.fftfreq(ny) * 2 * np.pi
    kx = np.fft.rfftfreq(nx) * 2 * np.pi
    KY, KX = np.meshgrid(ky, kx, indexing="ij")
    k2 = KX**2 + KY**2
    k2[0, 0] = np.inf
    kc = 2 * np.pi / (kc_cells * sub)
    amp = np.sqrt(k2 ** (slope / 2) * np.exp(-k2 / kc**2))
    delta_k = np.fft.rfft2(rng.standard_normal((ny, nx))) * amp
    delta = np.fft.irfft2(delta_k, s=(ny, nx))
    delta_k *= sigma_delta / delta.std()
    psi_y = np.fft.irfft2(1j * KY * delta_k / k2, s=(ny, nx))
    psi_x = np.fft.irfft2(1j * KX * delta_k / k2, s=(ny, nx))
    qy, qx = np.mgrid[0:ny, 0:nx].astype(float) + 0.5
    y = (qy + psi_y) % ny
    x = (qx + psi_x) % nx
    H, _, _ = np.histogram2d(y.ravel(), x.ravel(), bins=(ny // sub, nx // sub), range=((0, ny), (0, nx)))
    # periodic Gaussian blur in Fourier space (removes the particle-grid pattern)
    fy = np.fft.fftfreq(H.shape[0])[:, None]; fx = np.fft.rfftfreq(H.shape[1])[None, :]
    H = np.fft.irfft2(np.fft.rfft2(H) * np.exp(-2 * (np.pi * blur) ** 2 * (fy**2 + fx**2)), s=H.shape)
    return np.clip(H, 0, None)

def colorize(H, gamma=1.15):
    d = np.log1p(H / H.mean())
    lo, hi = np.percentile(d, 35), np.percentile(d, 99.8)
    d = np.clip((d - lo) / (hi - lo), 0, 1) ** gamma
    # near-black navy voids -> indigo walls -> blue filaments -> white nodes
    stops = np.array([[0.00, 5, 7, 18], [0.30, 16, 18, 48], [0.60, 52, 62, 140],
                      [0.85, 125, 170, 230], [1.00, 240, 246, 255]], float)
    rgb = np.stack([np.interp(d, stops[:, 0], stops[:, c]) for c in (1, 2, 3)], axis=-1)
    return Image.fromarray(rgb.astype(np.uint8))

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/img/cosmic-web.jpg"
    H = cosmic_web()
    # periodic box: roll sideways so the brightest cluster sits right of the header text
    H = np.roll(H, int(0.40 * H.shape[1]), axis=1)
    img = colorize(H)
    img.save(out, quality=82, optimize=True, progressive=True)
    print(out, img.size)
