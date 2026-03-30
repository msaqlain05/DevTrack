"""
Vercel serverless entry: project root must be on ``sys.path`` so ``import app`` works.
"""
from pathlib import Path
import sys

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from app.main import app  # noqa: E402 — path must be set first

