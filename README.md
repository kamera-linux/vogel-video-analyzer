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
- 🦜 **Species Identification** - Identify bird species using Hugging Face models (optional)
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

# Install package (basic)
pip install vogel-video-analyzer

# Install with species identification support (optional)
pip install vogel-video-analyzer[species]
```

#### Direct Installation

```bash
# Basic installation
pip install vogel-video-analyzer

# With species identification support
pip install vogel-video-analyzer[species]
```

### Basic Usage

```bash
# Analyze a single video
vogel-analyze video.mp4

# Identify bird species
vogel-analyze --identify-species video.mp4

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

#### Species Identification (Optional)
```bash
# Identify bird species in video
vogel-analyze --identify-species bird_video.mp4
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

🦜 Detected Species:
   3 species detected

  • Parus major (Great Tit)
    45 detections (avg confidence: 0.89)
  • Turdus merula (Blackbird)
    18 detections (avg confidence: 0.85)
  • Erithacus rubecula (European Robin)
    9 detections (avg confidence: 0.82)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**⚠️ Experimental Feature:** Pre-trained models may misidentify European garden birds as exotic species. For accurate identification of local bird species, consider training a custom model (see [Custom Model Training](#-custom-model-training)).

**Installation:**
```bash
pip install vogel-video-analyzer[species]
```

The first time you run species identification, the model (~100-300MB) will be downloaded automatically and cached locally for future use.

#### Using Custom Models

You can use locally trained models for better accuracy with your specific bird species:

```bash
# Use custom model
vogel-analyze --identify-species --species-model ~/vogel-models/my-model/ video.mp4
```

See the [Custom Model Training](#-custom-model-training) section for details on training your own model.

#### Advanced Options
```bash
# Custom threshold and sample rate
vogel-analyze --threshold 0.4 --sample-rate 10 video.mp4

# Species identification with faster analysis
vogel-analyze --identify-species --sample-rate 10 video.mp4

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

# Initialize analyzer (basic)
analyzer = VideoAnalyzer(
    model_path="yolov8n.pt",
    threshold=0.3
)

# Initialize analyzer with species identification
analyzer = VideoAnalyzer(
    model_path="yolov8n.pt",
    threshold=0.3,
    identify_species=True
)

# Analyze video
```
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

## 🎓 Custom Model Training

Pre-trained bird species classifiers are trained on global datasets and often misidentify European garden birds as exotic species. For better accuracy with your specific bird species, you can train a custom model.

### Why Train a Custom Model?

**Problem with pre-trained models:**
- Identify common European birds (Kohlmeise, Blaumeise) as exotic Asian pheasants
- Low confidence scores (often <0.1)
- Trained on datasets dominated by American and exotic birds

**Benefits of custom models:**
- High accuracy for YOUR specific bird species
- Trained on YOUR camera setup and lighting conditions
- Confidence scores >0.9 for correctly identified birds

### Quick Start

**1. Extract bird images from your videos:**
```bash
python training/extract_birds.py ~/Videos/kohlmeise.mp4 \
  -o ~/vogel-training-data/kohlmeise_video1/ \
  --sample-rate 50
```

**2. Organize dataset (80/20 train/val split):**
```bash
cd ~/vogel-training-data
python /path/to/vogel-video-analyzer/training/organize_dataset.py
```

**3. Train the model (requires ~3-4 hours on Raspberry Pi 5):**
```bash
# Install training dependencies
pip install torch torchvision datasets accelerate

# Start training
python /path/to/vogel-video-analyzer/training/train_custom_model.py
```

**4. Use your trained model:**
```bash
vogel-analyze --identify-species \
  --species-model ~/vogel-models/bird-classifier-*/final/ \
  video.mp4
```

### Recommended Dataset Size

- **Minimum:** 30-50 images per bird species
- **Optimal:** 100+ images per bird species
- **Balance:** Similar number of images for each species

### Complete Documentation

See [`training/README.md`](training/README.md) for:
- Detailed training workflow
- Script documentation
- Troubleshooting guide
- Tips for improving accuracy

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
