# Release v0.3.0 - Video Annotation & Multilingual Support

**Release Date:** November 14, 2025

**Languages:** [🇬🇧 English](#english) | [🇩🇪 Deutsch](#deutsch)

---

## English

### 🎉 Major Features

#### 1. 🎬 Video Annotation
Create beautiful annotated videos with bounding boxes and species labels!

**Key Features:**
- ✅ Automatic output path generation (`video.mp4` → `video_annotated.mp4`)
- ✅ Batch processing support (process multiple videos at once)
- ✅ Green bounding boxes around detected birds (3px width)
- ✅ Large, high-contrast text labels (34pt/38pt, black on white)
- ✅ Text positioned above birds to avoid covering subjects
- ✅ Audio preservation (automatic ffmpeg merge)
- ✅ Flicker-free animation (detection caching)
- ✅ Real-time progress indicator

**Usage:**
```bash
# Single video with auto-generated output path
vogel-analyze --annotate-video --multilingual --identify-species video.mp4
# Creates: video_annotated.mp4

# Multiple videos at once
vogel-analyze --annotate-video --multilingual --identify-species *.mp4
# Creates: video1_annotated.mp4, video2_annotated.mp4, etc.

# Custom output path (single video only)
vogel-analyze --annotate-video --annotate-output custom.mp4 --multilingual video.mp4
```

#### 2. 🌍 Multilingual Species Labels
Display bird names in English and German with the `--multilingual` flag!

**Supported Languages:**
- 🇬🇧 **English** (primary)
- 🇩🇪 **German** (full support)
- 🇯🇵 **Japanese** (39 species, database only)

**Display Format:**
```
EN: Hawfinch
DE: Kernbeißer
75%
```

**Bird Species Database:**
- **8 birds** from German model (kamera-linux/german-bird-classifier)
- **39 total species** with full translations
- Automatic German → English → Translation mapping

**German Model Birds:**
1. Blaumeise (Blue Tit)
2. Grünling (European Greenfinch)
3. Haussperling (House Sparrow)
4. Kernbeißer (Hawfinch)
5. Kleiber (Eurasian Nuthatch)
6. Kohlmeise (Parus Major)
7. Rotkehlchen (European Robin)
8. Sumpfmeise (Marsh Tit)

### 🔧 Technical Improvements

#### Unicode Text Rendering
- Replaced OpenCV's ASCII-only `cv2.putText()` with PIL/Pillow
- Full Unicode support (German umlauts: ä, ö, ü, ß)
- DejaVuSans font for excellent Latin character rendering
- RGB↔BGR color conversion for OpenCV compatibility

#### Enhanced User Experience
- **High Contrast Text:** Black text on white background (was: white on green)
- **Larger Text:** 34pt/38pt font sizes (was: 22pt)
- **Better Positioning:** Text above bird (10px gap) to avoid covering subject
- **Wider Text Box:** 550px wide (was: 400px)
- **Flicker Prevention:** Detection caching for smooth animations

#### German Output Messages
All CLI output now fully translated to German:
- "Erstelle annotiertes Video..." (Creating annotated video...)
- "Verarbeitete Frames: 28/852" (Frames processed: 28/852)
- "Erkannte Vögel gesamt: 19" (Total birds detected: 19)
- "Füge Audio vom Original-Video hinzu..." (Merging audio...)
- "Audio erfolgreich hinzugefügt" (Audio successfully merged)

### 📦 Installation

**Standard Installation:**
```bash
pip install vogel-video-analyzer
```

**With Species Identification:**
```bash
pip install vogel-video-analyzer[species]
```

**System Requirements:**
```bash
# For audio preservation (Ubuntu/Debian)
sudo apt install ffmpeg

# For PIL/Pillow (usually automatic with [species])
pip install Pillow
```

### 🚀 Quick Start Examples

**Basic Video Annotation:**
```bash
vogel-analyze --annotate-video video.mp4
```

**With Species Identification:**
```bash
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --annotate-video \
  --multilingual \
  video.mp4
```

**Batch Processing:**
```bash
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --sample-rate 30 \
  --threshold 0.5 \
  --species-threshold 0.6 \
  --annotate-video \
  --multilingual \
  ~/Videos/Birds/*.mp4
```

**Performance Optimization:**
```bash
# Fast processing (every 30th frame)
vogel-analyze --annotate-video --sample-rate 30 video.mp4

# High accuracy (every 5th frame, slower)
vogel-analyze --annotate-video --sample-rate 5 video.mp4
```

### 🐛 Bug Fixes

1. **Fixed:** Emoji rendering issues (□□□□□□ box characters)
   - **Solution:** Removed emojis, use text labels instead
   
2. **Fixed:** Japanese characters not displaying
   - **Solution:** Font compatibility (DejaVuSans for Latin only)
   
3. **Fixed:** Low text contrast (white on green was hard to read)
   - **Solution:** Changed to black on white background
   
4. **Fixed:** Text covering birds in video
   - **Solution:** Repositioned text box above bounding box
   
5. **Fixed:** Flickering bounding boxes
   - **Solution:** Implemented detection caching

### ⚠️ Breaking Changes

**CLI Syntax Change:**
- **Old:** `--annotate-video OUTPUT input.mp4`
- **New:** `--annotate-video input.mp4` (auto-generates output path)
- **Custom output:** `--annotate-video --annotate-output OUTPUT input.mp4`

### 📚 Updated Documentation

All README files updated with v0.3.0 features:
- README.md (English)
- README.de.md (German)
- README.ja.md (Japanese)

New sections:
- Video Annotation usage examples
- Multilingual species identification
- Performance optimization tips
- Batch processing workflows

### 🙏 Acknowledgments

Thanks to all contributors and users who provided feedback on:
- Font rendering issues
- Text visibility improvements
- Multilingual support requests
- Performance optimization suggestions

---

## Deutsch

### 🎉 Hauptfeatures

#### 1. 🎬 Video-Annotation
Erstelle wunderschön annotierte Videos mit Bounding Boxes und Artennamen!

**Hauptfunktionen:**
- ✅ Automatische Ausgabepfad-Generierung (`video.mp4` → `video_annotated.mp4`)
- ✅ Batch-Verarbeitung (mehrere Videos gleichzeitig)
- ✅ Grüne Bounding Boxes um erkannte Vögel (3px Breite)
- ✅ Große, kontraststarke Textlabels (34pt/38pt, schwarz auf weiß)
- ✅ Text über den Vögeln positioniert (verdeckt nicht das Motiv)
- ✅ Audio-Erhaltung (automatisches ffmpeg-Merge)
- ✅ Flimmerfreie Animation (Detection Caching)
- ✅ Echtzeit-Fortschrittsanzeige

**Verwendung:**
```bash
# Einzelnes Video mit automatischem Ausgabepfad
vogel-analyze --annotate-video --multilingual --identify-species video.mp4
# Erstellt: video_annotated.mp4

# Mehrere Videos gleichzeitig
vogel-analyze --annotate-video --multilingual --identify-species *.mp4
# Erstellt: video1_annotated.mp4, video2_annotated.mp4, etc.

# Benutzerdefinierter Ausgabepfad (nur einzelnes Video)
vogel-analyze --annotate-video --annotate-output custom.mp4 --multilingual video.mp4
```

#### 2. 🌍 Mehrsprachige Artennamen
Zeige Vogelnamen auf Englisch und Deutsch mit dem `--multilingual` Flag!

**Unterstützte Sprachen:**
- 🇬🇧 **Englisch** (primär)
- 🇩🇪 **Deutsch** (volle Unterstützung)
- 🇯🇵 **Japanisch** (39 Arten, nur Datenbank)

**Anzeigeformat:**
```
EN: Hawfinch
DE: Kernbeißer
75%
```

**Vogel-Datenbank:**
- **8 Vögel** vom deutschen Modell (kamera-linux/german-bird-classifier)
- **39 Arten insgesamt** mit vollständigen Übersetzungen
- Automatisches Deutsch → Englisch → Übersetzung Mapping

**Deutsche Modell-Vögel:**
1. Blaumeise (Blue Tit)
2. Grünling (European Greenfinch)
3. Haussperling (House Sparrow)
4. Kernbeißer (Hawfinch)
5. Kleiber (Eurasian Nuthatch)
6. Kohlmeise (Parus Major)
7. Rotkehlchen (European Robin)
8. Sumpfmeise (Marsh Tit)

### 🔧 Technische Verbesserungen

#### Unicode-Textdarstellung
- OpenCVs ASCII-only `cv2.putText()` durch PIL/Pillow ersetzt
- Volle Unicode-Unterstützung (deutsche Umlaute: ä, ö, ü, ß)
- DejaVuSans-Schriftart für exzellente lateinische Zeichen
- RGB↔BGR Farbkonvertierung für OpenCV-Kompatibilität

#### Verbesserte Benutzererfahrung
- **Hoher Kontrast:** Schwarzer Text auf weißem Hintergrund (war: weiß auf grün)
- **Größere Schrift:** 34pt/38pt Schriftgrößen (war: 22pt)
- **Bessere Positionierung:** Text über dem Vogel (10px Abstand)
- **Breitere Textbox:** 550px breit (war: 400px)
- **Flimmer-Prävention:** Detection Caching für glatte Animationen

#### Deutsche Ausgabe-Nachrichten
Alle CLI-Ausgaben vollständig auf Deutsch übersetzt:
- "Erstelle annotiertes Video..."
- "Verarbeitete Frames: 28/852"
- "Erkannte Vögel gesamt: 19"
- "Füge Audio vom Original-Video hinzu..."
- "Audio erfolgreich hinzugefügt"

### 📦 Installation

**Standard-Installation:**
```bash
pip install vogel-video-analyzer
```

**Mit Artenerkennung:**
```bash
pip install vogel-video-analyzer[species]
```

**System-Anforderungen:**
```bash
# Für Audio-Erhaltung (Ubuntu/Debian)
sudo apt install ffmpeg

# Für PIL/Pillow (normalerweise automatisch mit [species])
pip install Pillow
```

### 🚀 Schnellstart-Beispiele

**Basis Video-Annotation:**
```bash
vogel-analyze --annotate-video video.mp4
```

**Mit Artenerkennung:**
```bash
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --annotate-video \
  --multilingual \
  video.mp4
```

**Batch-Verarbeitung:**
```bash
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --sample-rate 30 \
  --threshold 0.5 \
  --species-threshold 0.6 \
  --annotate-video \
  --multilingual \
  ~/Videos/Voegel/*.mp4
```

**Performance-Optimierung:**
```bash
# Schnelle Verarbeitung (jeder 30. Frame)
vogel-analyze --annotate-video --sample-rate 30 video.mp4

# Hohe Genauigkeit (jeder 5. Frame, langsamer)
vogel-analyze --annotate-video --sample-rate 5 video.mp4
```

### 🐛 Fehlerbehebungen

1. **Behoben:** Emoji-Darstellungsprobleme (□□□□□□ Box-Zeichen)
   - **Lösung:** Emojis entfernt, Textlabels verwenden
   
2. **Behoben:** Japanische Zeichen werden nicht angezeigt
   - **Lösung:** Schriftart-Kompatibilität (DejaVuSans nur für Latein)
   
3. **Behoben:** Niedriger Text-Kontrast (weiß auf grün schwer lesbar)
   - **Lösung:** Geändert zu schwarz auf weißem Hintergrund
   
4. **Behoben:** Text verdeckt Vögel im Video
   - **Lösung:** Textbox über Bounding Box neu positioniert
   
5. **Behoben:** Flackernde Bounding Boxes
   - **Lösung:** Detection Caching implementiert

### ⚠️ Breaking Changes

**CLI-Syntax-Änderung:**
- **Alt:** `--annotate-video OUTPUT input.mp4`
- **Neu:** `--annotate-video input.mp4` (automatische Pfadgenerierung)
- **Eigener Pfad:** `--annotate-video --annotate-output OUTPUT input.mp4`

### 📚 Aktualisierte Dokumentation

Alle README-Dateien mit v0.3.0 Features aktualisiert:
- README.md (Englisch)
- README.de.md (Deutsch)
- README.ja.md (Japanisch)

Neue Abschnitte:
- Video-Annotation Verwendungsbeispiele
- Mehrsprachige Artenerkennung
- Performance-Optimierung Tipps
- Batch-Verarbeitung Workflows

### 🙏 Danksagungen

Danke an alle Mitwirkenden und Nutzer für Feedback zu:
- Schriftdarstellungsproblemen
- Text-Sichtbarkeitsverbesserungen
- Mehrsprachigkeits-Anfragen
- Performance-Optimierungsvorschlägen

---

## Upgrade Instructions

### From v0.2.x to v0.3.0

**Python API:**
```python
# No breaking changes to the Python API
from vogel_video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer()

# New method available:
analyzer.annotate_video(
    "input.mp4",
    "output.mp4",
    sample_rate=30,
    multilingual=True
)
```

**CLI:**
```bash
# Old way (v0.2.x - still works with --annotate-output)
vogel-analyze --annotate-video output.mp4 input.mp4

# New way (v0.3.0 - recommended)
vogel-analyze --annotate-video input.mp4
# Output: input_annotated.mp4 (automatic)

# Custom output (v0.3.0)
vogel-analyze --annotate-video --annotate-output output.mp4 input.mp4
```

---

## System Requirements

- **Python:** 3.8 or higher
- **OpenCV:** opencv-python (installed automatically)
- **PIL/Pillow:** For Unicode text rendering (installed with [species])
- **ffmpeg:** For audio preservation (system package)
- **Optional:** transformers, torch (for species identification)

**Recommended:**
```bash
# Ubuntu/Debian
sudo apt install python3-venv ffmpeg

# Create virtual environment
python3 -m venv ~/venv-vogel
source ~/venv-vogel/bin/activate

# Install with species support
pip install vogel-video-analyzer[species]
```

---

## Known Issues

1. **Emoji support:** Removed due to font compatibility issues
   - **Workaround:** Use text labels (EN: / DE:) instead
   
2. **Japanese display:** Not shown in video (font limitations)
   - **Status:** Available in database for future use
   
3. **Large videos:** Processing time depends on resolution and sample rate
   - **Recommendation:** Use `--sample-rate 30` for 4K videos

---

## Future Roadmap

- 🔄 **v0.4.0:** GPU acceleration support
- 🎨 **v0.4.1:** Customizable text colors and box styles
- 🌐 **v0.5.0:** More language support (French, Spanish, Italian)
- 🦅 **v0.6.0:** Expanded bird species database (100+ species)
- 📊 **v0.7.0:** Advanced analytics and heat maps

---

## Download

**PyPI:** https://pypi.org/project/vogel-video-analyzer/0.3.0/

**GitHub:** https://github.com/kamera-linux/vogel-video-analyzer/releases/tag/v0.3.0

**Installation:**
```bash
pip install vogel-video-analyzer==0.3.0
```

---

## Changelog

Full changelog: [CHANGELOG.md](CHANGELOG.md)

---

**Maintained by:** Vogel-Kamera-Linux Team  
**License:** MIT  
**Repository:** https://github.com/kamera-linux/vogel-video-analyzer
