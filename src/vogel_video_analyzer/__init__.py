"""
Vogel Video Analyzer - YOLOv8-based video analysis for bird content detection

A command-line tool and Python library for analyzing videos to detect and quantify bird presence.
"""

__version__ = "0.5.1"
__author__ = "Vogel-Kamera-Linux Team"
__license__ = "MIT"

from .analyzer import VideoAnalyzer
from .cli import main

__all__ = ["VideoAnalyzer", "main", "__version__"]
