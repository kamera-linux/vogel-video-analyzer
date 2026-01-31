"""
Vogel Video Analyzer - YOLOv8-based video analysis for bird content detection

A command-line tool and Python library for analyzing videos to detect and quantify bird presence.
"""

__version__ = "0.5.3"
__author__ = "Vogel-Kamera-Linux Team"
__license__ = "MIT"

from .analyzer import (
    VideoAnalyzer,
    COCO_CLASS_BIRD,
    DEFAULT_DETECTION_THRESHOLD,
    DEFAULT_SPECIES_THRESHOLD,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_FLAG_SIZE,
    DEFAULT_FONT_SIZE
)
from .cli import main

__all__ = [
    "VideoAnalyzer",
    "main",
    "__version__",
    "COCO_CLASS_BIRD",
    "DEFAULT_DETECTION_THRESHOLD",
    "DEFAULT_SPECIES_THRESHOLD",
    "DEFAULT_SAMPLE_RATE",
    "DEFAULT_FLAG_SIZE",
    "DEFAULT_FONT_SIZE"
]
