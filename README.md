# 🐦 Vogel Video Analyzer

**Languages:** [🇬🇧 English](README.md) | [🇩🇪 Deutsch](README.de.md)

<p align="left">
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/vogel-video-analyzer.svg"></a>
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/vogel-video-analyzer.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="PyPI Status" src="https://img.shields.io/pypi/status/vogel-video-analyzer.svg"></a>
  <a href="https://pepy.tech/project/vogel-video-analyzer"><img alt="Downloads" src="https://static.pepy.tech/badge/vogel-video-analyzer"></a>
</p>

**YOLOv8-based video analysis tool for automated bird content detection and quantification.**

A powerful command-line tool and Python library for analyzing videos to detect and quantify bird presence using state-of-the-art YOLOv8 object detection.

---

## ✨ Features

- 🤖 **YOLOv8-powered Detection** - Accurate bird detection using pre-trained models
- 📊 **Detailed Statistics** - Frame-by-frame analysis with bird content percentage
- 🎯 **Segment Detection** - Identifies continuous time periods with bird presence
- ⚡ **Performance Optimized** - Configurable sample rate for faster processing
- 📄 **JSON Export** - Structured reports for archival and further analysis
- 🗑️ **Smart Auto-Delete** - Remove video files or folders without bird content
- 📝 **Logging Support** - Structured logs for batch processing workflows
- 🐍 **Library & CLI** - Use as standalone tool or integrate into your Python projects

---

## 🚀 Quick Start

### Installation

#### Recommended: Using Virtual Environment

```bash
# Install venv if needed (Debian/Ubuntu)
sudo apt install python3-venv

# Create virtual environment
python3 -m venv ~/venv-vogel

# Activate it
source ~/venv-vogel/bin/activate  # On Windows: ~/venv-vogel\Scripts\activate

# Install package
pip install vogel-video-analyzer
```

#### Direct Installation

```bash
pip install vogel-video-analyzer
```

### Basic Usage

```bash
# Analyze a single video
vogel-analyze video.mp4

# Faster analysis (every 5th frame)
vogel-analyze --sample-rate 5 video.mp4

# Export to JSON
vogel-analyze --output report.json video.mp4

# Delete only video files with 0% bird content
vogel-analyze --delete-file *.mp4

# Delete entire folders with 0% bird content  
vogel-analyze --delete-folder ~/Videos/*/*.mp4

# Batch process directory
vogel-analyze ~/Videos/Birds/**/*.mp4
```

---

## 📖 Usage Examples

### Command Line Interface

#### Basic Analysis
```bash
# Analyze single video with default settings
vogel-analyze bird_video.mp4
```

**Output:**
```
🎬 Video Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: /path/to/bird_video.mp4
📊 Total Frames: 450 (analyzed: 90)
⏱️  Duration: 15.0 seconds
🐦 Bird Frames: 72 (80.0%)
🎯 Bird Segments: 2

📍 Detected Segments:
  ┌ Segment 1: 00:00:02 - 00:00:08 (72% bird frames)
  └ Segment 2: 00:00:11 - 00:00:14 (89% bird frames)

✅ Status: Significant bird activity detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Advanced Options
```bash
# Custom threshold and sample rate
vogel-analyze --threshold 0.4 --sample-rate 10 video.mp4

# Set output language (en/de, auto-detected by default)
vogel-analyze --language de video.mp4

# Delete only video files with 0% bird content
vogel-analyze --delete-file --sample-rate 5 *.mp4

# Delete entire folders with 0% bird content
vogel-analyze --delete-folder --sample-rate 5 ~/Videos/*/*.mp4

# Save JSON report and log
vogel-analyze --output report.json --log video.mp4
```

### Python Library

```python
from vogel_video_analyzer import VideoAnalyzer

# Initialize analyzer
analyzer = VideoAnalyzer(
    model_path="yolov8n.pt",
    threshold=0.3
)

# Analyze video
stats = analyzer.analyze_video("bird_video.mp4", sample_rate=5)

# Print formatted report
analyzer.print_report(stats)

# Access statistics
print(f"Bird content: {stats['bird_percentage']:.1f}%")
print(f"Segments found: {len(stats['bird_segments'])}")
```

---

## 🎯 Use Cases

### 1. Quality Control for Bird Recordings
Automatically verify that recorded videos actually contain birds:

```bash
vogel-analyze --threshold 0.5 --delete recordings/**/*.mp4
```

### 2. Archive Management
Identify and remove videos without bird content to save storage:

```bash
# Find videos with 0% bird content
vogel-analyze --output stats.json archive/**/*.mp4

# Delete empty videos
vogel-analyze --delete archive/**/*.mp4
```

### 3. Batch Analysis for Research
Process large video collections and generate structured reports:

```bash
# Analyze all videos and save individual reports
for video in research_data/**/*.mp4; do
    vogel-analyze --sample-rate 10 --output "${video%.mp4}_report.json" "$video"
done
```

### 4. Integration in Automation Workflows
Use as part of automated recording pipelines:

```python
from vogel_video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer(threshold=0.3)
stats = analyzer.analyze_video("latest_recording.mp4", sample_rate=5)

# Only keep videos with significant bird content
if stats['bird_percentage'] < 10:
    print("Insufficient bird content, deleting...")
    # Handle deletion
else:
    print(f"✅ Quality video: {stats['bird_percentage']:.1f}% bird content")
```

---

## ⚙️ Configuration Options

| Option | Description | Default | Values |
|--------|-------------|---------|--------|
| `--model` | YOLO model to use | `yolov8n.pt` | Any YOLO model |
| `--threshold` | Confidence threshold | `0.3` | `0.0` - `1.0` |
| `--sample-rate` | Analyze every Nth frame | `5` | `1` - `∞` |
| `--output` | Save JSON report | - | File path |
| `--delete` | Auto-delete 0% videos | `False` | Flag |
| `--log` | Enable logging | `False` | Flag |

### Sample Rate Recommendations

| Video FPS | Sample Rate | Frames Analyzed | Performance |
|-----------|-------------|----------------|-------------|
| 30 fps | 1 | 100% (all frames) | Slow, highest precision |
| 30 fps | 5 | 20% | ⭐ **Recommended** - Good balance |
| 30 fps | 10 | 10% | Fast, sufficient |
| 30 fps | 20 | 5% | Very fast, basic check |

### Threshold Values

| Threshold | Description | Use Case |
|-----------|-------------|----------|
| 0.2 | Very sensitive | Detects distant/partially obscured birds |
| 0.3 | **Standard** | Balanced detection |
| 0.5 | Conservative | Only clearly visible birds |
| 0.7 | Very strict | Only perfect detections |

---

## 🔍 Technical Details

### Model Search Hierarchy

The analyzer searches for YOLOv8 models in this order:

1. `models/` directory (local)
2. `config/models/` directory
3. Current directory
4. Auto-download from Ultralytics (fallback)

### Detection Algorithm

- **Target Class:** Bird (COCO class 14)
- **Inference:** Frame-by-frame YOLOv8 detection
- **Segment Detection:** Groups consecutive bird frames with max 2-second gaps
- **Performance:** ~5x speedup with sample-rate=5 on 30fps videos

### Output Format

JSON reports include:
```json
{
  "video_file": "bird_video.mp4",
  "duration_seconds": 15.0,
  "total_frames": 450,
  "frames_analyzed": 90,
  "bird_percentage": 80.0,
  "bird_segments": [
    {
      "start": 2.0,
      "end": 8.0,
      "detections": 36
    }
  ]
}
```

---

## 📚 Documentation

- **GitHub Repository:** [vogel-video-analyzer](https://github.com/kamera-linux/vogel-video-analyzer)
- **Parent Project:** [vogel-kamera-linux](https://github.com/kamera-linux/vogel-kamera-linux)
- **Issue Tracker:** [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)

---

## 🤝 Contributing

Contributions are welcome! We appreciate bug reports, feature suggestions, documentation improvements, and code contributions.

Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- How to set up your development environment
- Our code style and guidelines
- The pull request process
- How to report bugs and suggest features

For security vulnerabilities, please see our [Security Policy](SECURITY.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ultralytics YOLOv8** - Powerful object detection framework
- **OpenCV** - Computer vision library
- **Vogel-Kamera-Linux** - Parent project for automated bird observation

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/kamera-linux/vogel-video-analyzer/discussions)

---

**Made with ❤️ by the Vogel-Kamera-Linux Team**
