"""make.fun news-image-20261124 entry: write the pre-rendered news page to the output dir.

Stdlib only, no network. entry.png is rendered at build time by build.py, so every run
writes the same bytes.
"""
import os
from pathlib import Path

src = Path(__file__).resolve().parent / 'entry.png'
data = src.read_bytes()
assert data[:8] == b'\x89PNG\r\n\x1a\n' and len(data) <= 1 << 20, 'entry.png must be a PNG under 1 MiB'

out = Path(os.environ.get('MAKEFUN_OUTPUT_DIR') or '/output')
out.mkdir(parents=True, exist_ok=True)
(out / 'entry.png').write_bytes(data)
