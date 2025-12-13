# 🐦 Vogel Video Analyzer

![Vogel Video Analyzer Banner](assets/banner.png)

**Languages:** [🇬🇧 English](README.md) | [🇩🇪 Deutsch](README.de.md) | [🇯🇵 日本語](README.ja.md)

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
- 📊 **HTML Reports (v0.5.0+)** - Interactive visual reports with charts and thumbnails
  - Activity timeline showing bird detections over time
  - Species distribution charts
  - Thumbnail gallery of best detections
  - Responsive design for desktop and mobile
  - Self-contained HTML files (no external dependencies)
- 🎬 **Video Annotation (v0.3.0+)** - Create annotated videos with bounding boxes and species labels
  - Automatic output path generation with timestamp (`video.mp4` → `video_annotated_YYYYMMDD_HHMMSS.mp4`)
  - Multilingual species labels with flag icons (🇬🇧 🇩🇪 🇯🇵)
  - 🏴 **Hybrid flag rendering (v0.4.2+)** - PNG images with automatic fallback
  - Configurable font sizes for optimal readability
  - Audio preservation from original video
  - Flicker-free bounding boxes with detection caching
  - Batch processing support for multiple videos
  - Right-positioned semi-transparent label boxes
- 🌍 **Multilingual Support (v0.3.0+)** - Bird names in English, German, and Japanese
  - 39 bird species with full translations
  - All 8 German model birds supported (kamera-linux/german-bird-classifier)
  - Display format: "EN: Hawfinch / DE: Kernbeißer / 75%"
- 📊 **Detailed Statistics** - Frame-by-frame analysis with bird content percentage
- 🎯 **Segment Detection** - Identifies continuous time periods with bird presence
- ⚡ **Performance Optimized** - Configurable sample rate for faster processing
- 📄 **JSON Export** - Structured reports for archival and further analysis
- 🗑️ **Smart Auto-Delete** - Remove video files or folders without bird content
- 📝 **Logging Support** - Structured logs for batch processing workflows
- 🌐 **i18n Support** - English, German, and Japanese interface translations
- 🐍 **Library & CLI** - Use as standalone tool or integrate into your Python projects

---

## 🎓 Want to Train Your Own Species Classifier?

Check out **[vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)** to extract training data from your videos and build custom models for your local bird species!

**Why train a custom model?**
- Pre-trained models often misidentify European garden birds as exotic species
- Custom models achieve >90% accuracy for YOUR specific birds
- Train on YOUR camera setup and lighting conditions

👉 **[Get Started with vogel-model-trainer →](https://github.com/kamera-linux/vogel-model-trainer)**

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

# Install ffmpeg for audio preservation (Ubuntu/Debian)
sudo apt install ffmpeg
```

#### Direct Installation

```bash
pip install vogel-video-analyzer
```

### Basic Usage

```bash
# Analyze a single video
vogel-analyze video.mp4

# Identify bird species
vogel-analyze --identify-species video.mp4

# Generate HTML report (v0.5.0+)
vogel-analyze --language en --identify-species --species-model kamera-linux/german-bird-classifier --species-threshold 0.80 --html-report report.html --sample-rate 15 --max-thumbnails 12 video.mp4
# View example: https://htmlpreview.github.io/?https://github.com/kamera-linux/vogel-video-analyzer/blob/main/examples/html_report_example.html

# Create annotated video (v0.3.0+)
vogel-analyze --identify-species --annotate-video video.mp4
# Output: video_annotated.mp4 (automatic)

# Create annotated video with multilingual labels
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --multilingual \
  --annotate-video \
  video.mp4

# Batch processing multiple videos
vogel-analyze --identify-species --annotate-video --multilingual *.mp4
# Creates: video1_annotated.mp4, video2_annotated.mp4, etc.

# Combined outputs: JSON + HTML report
vogel-analyze --identify-species -o data.json --html-report report.html video.mp4

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

The first time you run species identification, the model (~100-300MB) will be downloaded automatically and cached locally for future use.

**🚀 GPU Acceleration:** Species identification automatically uses CUDA (NVIDIA GPU) if available, significantly speeding up inference. Falls back to CPU if no GPU is detected.

#### Using Custom Models

You can use locally trained models for better accuracy with your specific bird species:

```bash
# Use custom model
vogel-analyze --identify-species --species-model ~/vogel-models/my-model/ video.mp4

# With custom confidence threshold (default: 0.3)
vogel-analyze --identify-species \
  --species-model ~/vogel-models/my-model/ \
  --species-threshold 0.5 \
  video.mp4
```

**Threshold Guidelines:**
- `0.1-0.2` - Maximize detections (exploratory)
- `0.3-0.5` - Balanced (recommended)
- `0.6-0.9` - High confidence only

See the [Custom Model Training](#-custom-model-training) section for details on training your own model.

#### Video Annotation (v0.4.0+)

Create professionally annotated videos with bounding boxes, species labels, and custom styling:

```bash
# Basic annotation with automatic timestamped output
vogel-analyze --identify-species --annotate-video input.mp4
# Output: input_annotated_20251123_195542.mp4

# With multilingual labels and custom font size
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --multilingual \
  --annotate-video \
  --font-size 16 \
  input.mp4

# With high-quality PNG flag icons (v0.4.2+)
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --multilingual \
  --annotate-video \
  --flag-dir assets/flags/ \
  input.mp4

# With confidence threshold (only show birds >= 50%)
vogel-analyze --identify-species \
  --species-threshold 0.5 \
  --multilingual \
  --annotate-video \
  --font-size 18 \
  input.mp4

# Batch processing multiple videos
vogel-analyze --identify-species \
  --annotate-video \
  --multilingual \
  --font-size 16 \
  *.mp4
# Creates: video1_annotated_20251123_195542.mp4, video2_annotated_20251123_195545.mp4, etc.

# Fast processing with sample rate
vogel-analyze --identify-species \
  --sample-rate 30 \
  --annotate-video \
  --font-size 14 \
  input.mp4
```

**Features:**
- 📦 **Bounding boxes** around detected birds (green, 3px width)
- 🏷️ **Multilingual species labels** with flag icons
  - 🇬🇧 English: European Robin
  - 🇩🇪 German: Rotkehlchen
  - 🇯🇵 Japanese: ヨーロッパコマドリ
- 🏴 **Hybrid flag rendering** (v0.4.2+): PNG images with automatic fallback
  - Confidence: 73%
- 🎨 **Customizable text size** (`--font-size 12-24`, default: 20)
- 🎯 **Confidence filtering** (`--species-threshold 0.0-1.0`, default: 0.0)
- 📍 **Smart positioning** (labels right of bird with semi-transparent background)
- 🎵 **Audio preservation** (automatic ffmpeg merge from original video)
- ⚡ **Flicker-free** animation (detection caching)
- ⏱️ **Timestamped outputs** (never overwrites existing files)
- 📊 **Real-time progress** indicator

**Label Display Format:**
```
🇬🇧 European Robin
🇩🇪 Rotkehlchen  
🇯🇵 ヨーロッパコマドリ
73%
```

#### Video Summary (v0.3.1+)

Create compressed videos by skipping segments without bird activity:

```bash
# Basic summary with default settings
vogel-analyze --create-summary video.mp4
# Output: video_summary.mp4

# Custom thresholds
vogel-analyze --create-summary \
  --skip-empty-seconds 5.0 \
  --min-activity-duration 1.0 \
  video.mp4

# Custom output path (single video only)
vogel-analyze --create-summary \
  --summary-output custom_summary.mp4 \
  video.mp4

# Batch processing multiple videos
vogel-analyze --create-summary *.mp4
# Creates: video1_summary.mp4, video2_summary.mp4, etc.

# Combine with faster processing
vogel-analyze --create-summary \
  --sample-rate 10 \
  video.mp4
```

**Features:**
- ✂️ **Smart segment detection** - Automatically identifies bird activity periods
- 🎵 **Audio preservation** - Maintains perfect audio sync (no pitch/speed changes)
- ⚙️ **Configurable thresholds**:
  - `--skip-empty-seconds` (default: 3.0) - Minimum duration of bird-free segments to skip
  - `--min-activity-duration` (default: 2.0) - Minimum duration of bird activity to keep
- 📊 **Compression statistics** - Shows original vs. summary duration
- ⚡ **Fast processing** - Uses ffmpeg concat (no re-encoding)
- 📁 **Automatic path generation** - Saves as `<original>_summary.mp4`

**How it works:**
1. Analyzes video frame-by-frame to detect bird presence
2. Identifies continuous segments with/without birds
3. Filters segments based on duration thresholds
4. Concatenates segments with audio using ffmpeg
5. Returns compression statistics

**Example Output:**
```
🔍 Analyzing video for bird activity: video.mp4...
   📊 Analyzing 18000 frames at 30.0 FPS...
   ✅ Analysis complete - 1250 frames with birds detected

📊 Bird activity segments identified
   📊 Segments to keep: 8
   ⏱️  Original duration: 0:10:00
   ⏱️  Summary duration: 0:02:45
   📉 Compression: 72.5% shorter

🎬 Creating summary video: video_summary.mp4...
   ✅ Summary video created successfully
   📁 video_summary.mp4
```

**Supported Languages:**
- 🇬🇧 English (primary)
- 🇩🇪 German (full support, 39 species)
- 🇯🇵 Japanese (39 species, database only)

**Supported Birds (German Model):**
All 8 birds from `kamera-linux/german-bird-classifier`:
- Blaumeise (Blue Tit)
- Grünfink (European Greenfinch)
- Haussperling (House Sparrow)
- Kernbeißer (Hawfinch)
- Kleiber (Eurasian Nuthatch)
- Kohlmeise (Great Tit)
- Rotkehlchen (European Robin)
- Sumpfmeise (Marsh Tit)

**Performance Tips:**
- Use `--sample-rate 30` for 4K videos (analyzes every 30th frame)
- Use `--sample-rate 5-10` for HD videos (balance speed vs accuracy)
- Lower sample rates = more detections but slower processing
- Audio is automatically preserved from original video
- Output maintains original resolution and framerate

**Requirements:**
```bash
# Install ffmpeg for audio preservation (Ubuntu/Debian)
sudo apt install ffmpeg
```

#### Advanced Options
```bash
# Custom threshold and sample rate
vogel-analyze --threshold 0.4 --sample-rate 10 video.mp4

# Species identification with confidence tuning
vogel-analyze --identify-species --species-threshold 0.4 video.mp4
vogel-analyze --identify-species --sample-rate 10 video.mp4

# Set output language (en/de/ja, auto-detected by default)
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
vogel-analyze --threshold 0.5 --delete-file recordings/**/*.mp4
```

### 2. Archive Management
Identify and remove videos without bird content to save storage:

```bash
# Find videos with 0% bird content
vogel-analyze --output stats.json archive/**/*.mp4

# Delete empty video files only
vogel-analyze --delete-file archive/**/*.mp4

# Delete entire folders with 0% bird content
vogel-analyze --delete-folder archive/**/*.mp4
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

### Core Options

| Option | Description | Default | Values |
|--------|-------------|---------|--------|
| `--model` | YOLO model to use | `yolov8n.pt` | Any YOLO model |
| `--threshold` | Bird detection confidence | `0.3` | `0.0` - `1.0` |
| `--sample-rate` | Analyze every Nth frame | `5` | `1` - `∞` |
| `--output` | Save JSON report | - | File path |
| `--delete-file` | Auto-delete 0% videos | `False` | Flag |
| `--delete-folder` | Auto-delete 0% folders | `False` | Flag |
| `--log` | Enable logging | `False` | Flag |

### Species Identification Options (v0.3.0+)

| Option | Description | Default | Values |
|--------|-------------|---------|--------|
| `--identify-species` | Enable species identification | `False` | Flag |
| `--species-model` | Hugging Face model name | `kamera-linux/german-bird-classifier` | Model ID |
| `--species-threshold` | Min confidence for species label | `0.0` | `0.0` - `1.0` |
| `--multilingual` | Show names in EN/DE/JA | `False` | Flag |

### Video Annotation Options (v0.4.0+)

| Option | Description | Default | Values |
|--------|-------------|---------|--------|
| `--annotate-video` | Create annotated video | `False` | Flag |
| `--font-size` | Label text size | `20` | `12` - `32` |
| `--flag-dir` | Custom flag images directory (v0.4.2+) | Auto-detect | Directory path |
| `--annotate-output` | Custom output path | Auto-generated | File path |

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

### Species Identification (GPU-Optimized)

- **GPU Batch Processing:** Processes all bird crops per frame simultaneously (v0.4.4+)
  - Single batch inference for all detected birds in a frame
  - Up to 8 crops processed in parallel (`batch_size=8`)
  - Up to 8x faster than sequential processing
  - Eliminates "pipelines sequentially on GPU" warning
- **Device Selection:** Automatic CUDA (NVIDIA GPU) detection with CPU fallback
- **Model Loading:** Downloads from Hugging Face Hub (~100-300MB, cached locally)
- **Threshold Filtering:** Configurable confidence threshold (default: 0.3)
- **Multilingual Support:** Bird names in English, German, and Japanese (39 species)

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

The training tools are now available as a standalone package: **[vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)**

**1. Install the training package:**
```bash
pip install vogel-model-trainer
```

**2. Extract bird images from your videos:**
```bash
vogel-trainer extract ~/Videos/kohlmeise.mp4 \
  --folder ~/vogel-training-data/ \
  --bird kohlmeise \
  --sample-rate 3
```

**3. Organize dataset (80/20 train/val split):**
```bash
vogel-trainer organize \
  --source ~/vogel-training-data/ \
  --output ~/vogel-training-data/organized/
```

**4. Train the model (requires ~3-4 hours on Raspberry Pi 5):**
```bash
vogel-trainer train
```

**5. Use your trained model:**
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

See the **[vogel-model-trainer documentation](https://github.com/kamera-linux/vogel-model-trainer)** for:
- Complete training workflow
- Iterative training for better accuracy
- Advanced usage and troubleshooting
- Performance tips and best practices

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
