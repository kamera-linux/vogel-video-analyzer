# 🐦 Vogel Video Analyzer

**Sprachen:** [🇬🇧 English](README.md) | [🇩🇪 Deutsch](README.de.md)

<p align="left">
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/vogel-video-analyzer.svg"></a>
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/vogel-video-analyzer.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="PyPI Status" src="https://img.shields.io/pypi/status/vogel-video-analyzer.svg"></a>
  <a href="https://pepy.tech/project/vogel-video-analyzer"><img alt="Downloads" src="https://static.pepy.tech/badge/vogel-video-analyzer"></a>
</p>

**YOLOv8-basiertes Videoanalyse-Tool zur automatisierten Erkennung und Quantifizierung von Vogelinhalten.**

Ein leistungsstarkes Kommandozeilen-Tool und Python-Bibliothek zur Analyse von Videos, um Vogelvorkommen mithilfe modernster YOLOv8-Objekterkennung zu erkennen und zu quantifizieren.

---

## ✨ Funktionen

- 🤖 **YOLOv8-basierte Erkennung** - Präzise Vogelerkennung mit vortrainierten Modellen
- 📊 **Detaillierte Statistiken** - Frame-für-Frame-Analyse mit Vogelinhalt in Prozent
- 🎯 **Segment-Erkennung** - Identifiziert zusammenhängende Zeitperioden mit Vogelvorkommen
- ⚡ **Performance-Optimiert** - Konfigurierbare Sample-Rate für schnellere Verarbeitung
- 📄 **JSON-Export** - Strukturierte Berichte zur Archivierung und Weiterverarbeitung
- 🗑️ **Intelligentes Auto-Löschen** - Entfernt Videodateien oder Ordner ohne Vogelinhalt
- 📝 **Logging-Unterstützung** - Strukturierte Logs für Batch-Verarbeitungs-Workflows
- 🐍 **Bibliothek & CLI** - Als eigenständiges Tool oder in Python-Projekten integrierbar

---

## 🚀 Schnellstart

### Installation

#### Empfohlen: Mit virtueller Umgebung

```bash
# venv installieren falls nötig (Debian/Ubuntu)
sudo apt install python3-venv

# Virtuelle Umgebung erstellen
python3 -m venv ~/venv-vogel

# Aktivieren
source ~/venv-vogel/bin/activate  # Unter Windows: ~/venv-vogel\Scripts\activate

# Paket installieren
pip install vogel-video-analyzer
```

#### Direkte Installation

```bash
pip install vogel-video-analyzer
```

### Grundlegende Verwendung

```bash
# Einzelnes Video analysieren
vogel-analyze video.mp4

# Schnellere Analyse (jedes 5. Frame)
vogel-analyze --sample-rate 5 video.mp4

# Als JSON exportieren
vogel-analyze --output report.json video.mp4

# Nur Videodateien mit 0% Vogelinhalt löschen
vogel-analyze --delete-file *.mp4

# Ganze Ordner mit 0% Vogelinhalt löschen
vogel-analyze --delete-folder ~/Videos/*/*.mp4

# Verzeichnis batch-verarbeiten
vogel-analyze ~/Videos/Birds/**/*.mp4
```

---

## 📖 Verwendungsbeispiele

### Kommandozeilen-Interface

#### Basis-Analyse
```bash
# Einzelnes Video mit Standardeinstellungen analysieren
vogel-analyze bird_video.mp4
```

**Ausgabe:**
```
🎬 Video Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Datei: /path/to/bird_video.mp4
📊 Gesamt-Frames: 450 (analysiert: 90)
⏱️  Dauer: 15.0 Sekunden
🐦 Vogel-Frames: 72 (80.0%)
🎯 Vogel-Segmente: 2

📍 Erkannte Segmente:
  ┌ Segment 1: 00:00:02 - 00:00:08 (72% Vogel-Frames)
  └ Segment 2: 00:00:11 - 00:00:14 (89% Vogel-Frames)

✅ Status: Signifikante Vogelaktivität erkannt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Erweiterte Optionen
```bash
# Benutzerdefinierter Schwellenwert und Sample-Rate
vogel-analyze --threshold 0.4 --sample-rate 10 video.mp4

# Ausgabesprache festlegen (en/de, standardmäßig automatisch erkannt)
vogel-analyze --language de video.mp4

# Nur Videodateien mit 0% Vogelinhalt löschen
vogel-analyze --delete-file --sample-rate 5 *.mp4

# Ganze Ordner mit 0% Vogelinhalt löschen
vogel-analyze --delete-folder --sample-rate 5 ~/Videos/*/*.mp4

# JSON-Bericht und Log speichern
vogel-analyze --output report.json --log video.mp4
```

### Python-Bibliothek

```python
from vogel_video_analyzer import VideoAnalyzer

# Analyzer initialisieren
analyzer = VideoAnalyzer(
    model_path="yolov8n.pt",
    threshold=0.3
)

# Video analysieren
stats = analyzer.analyze_video("bird_video.mp4", sample_rate=5)

# Formatierten Bericht ausgeben
analyzer.print_report(stats)

# Auf Statistiken zugreifen
print(f"Vogelinhalt: {stats['bird_percentage']:.1f}%")
print(f"Gefundene Segmente: {len(stats['bird_segments'])}")
```

---

## 🎯 Anwendungsfälle

### 1. Qualitätskontrolle für Vogelaufnahmen
Automatisch überprüfen, ob aufgenommene Videos tatsächlich Vögel enthalten:

```bash
vogel-analyze --threshold 0.5 --delete recordings/**/*.mp4
```

### 2. Archivverwaltung
Videos ohne Vogelinhalt identifizieren und entfernen, um Speicherplatz zu sparen:

```bash
# Videos mit 0% Vogelinhalt finden
vogel-analyze --output stats.json archive/**/*.mp4

# Leere Videos löschen
vogel-analyze --delete archive/**/*.mp4
```

### 3. Batch-Analyse für Forschung
Große Videosammlungen verarbeiten und strukturierte Berichte erstellen:

```bash
# Alle Videos analysieren und individuelle Berichte speichern
for video in research_data/**/*.mp4; do
    vogel-analyze --sample-rate 10 --output "${video%.mp4}_report.json" "$video"
done
```

### 4. Integration in Automatisierungs-Workflows
Als Teil automatisierter Aufnahme-Pipelines verwenden:

```python
from vogel_video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer(threshold=0.3)
stats = analyzer.analyze_video("latest_recording.mp4", sample_rate=5)

# Nur Videos mit signifikantem Vogelinhalt behalten
if stats['bird_percentage'] < 10:
    print("Unzureichender Vogelinhalt, lösche...")
    # Löschung handhaben
else:
    print(f"✅ Qualitätsvideo: {stats['bird_percentage']:.1f}% Vogelinhalt")
```

---

## ⚙️ Konfigurationsoptionen

| Option | Beschreibung | Standard | Werte |
|--------|-------------|---------|--------|
| `--model` | Zu verwendendes YOLO-Modell | `yolov8n.pt` | Beliebiges YOLO-Modell |
| `--threshold` | Konfidenz-Schwellenwert | `0.3` | `0.0` - `1.0` |
| `--sample-rate` | Jedes N-te Frame analysieren | `5` | `1` - `∞` |
| `--output` | JSON-Bericht speichern | - | Dateipfad |
| `--delete` | Videos mit 0% auto-löschen | `False` | Flag |
| `--log` | Logging aktivieren | `False` | Flag |

### Sample-Rate-Empfehlungen

| Video-FPS | Sample-Rate | Analysierte Frames | Performance |
|-----------|-------------|-------------------|-------------|
| 30 fps | 1 | 100% (alle Frames) | Langsam, höchste Präzision |
| 30 fps | 5 | 20% | ⭐ **Empfohlen** - Gute Balance |
| 30 fps | 10 | 10% | Schnell, ausreichend |
| 30 fps | 20 | 5% | Sehr schnell, Basis-Check |

### Schwellenwerte

| Schwellenwert | Beschreibung | Anwendungsfall |
|--------------|-------------|----------------|
| 0.2 | Sehr empfindlich | Erkennt entfernte/teilweise verdeckte Vögel |
| 0.3 | **Standard** | Ausgewogene Erkennung |
| 0.5 | Konservativ | Nur deutlich sichtbare Vögel |
| 0.7 | Sehr strikt | Nur perfekte Erkennungen |

---

## 🔍 Technische Details

### Modell-Such-Hierarchie

Der Analyzer sucht YOLOv8-Modelle in dieser Reihenfolge:

1. `models/` Verzeichnis (lokal)
2. `config/models/` Verzeichnis
3. Aktuelles Verzeichnis
4. Auto-Download von Ultralytics (Fallback)

### Erkennungs-Algorithmus

- **Zielklasse:** Vogel (COCO-Klasse 14)
- **Inferenz:** Frame-für-Frame YOLOv8-Erkennung
- **Segment-Erkennung:** Gruppiert aufeinanderfolgende Vogel-Frames mit max. 2-Sekunden-Lücken
- **Performance:** ~5x Beschleunigung mit sample-rate=5 bei 30fps-Videos

### Ausgabeformat

JSON-Berichte enthalten:
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

## 📚 Dokumentation

- **GitHub Repository:** [vogel-video-analyzer](https://github.com/kamera-linux/vogel-video-analyzer)
- **Elternprojekt:** [vogel-kamera-linux](https://github.com/kamera-linux/vogel-kamera-linux)
- **Issue Tracker:** [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)

---

## 🤝 Mitwirken

Beiträge sind willkommen! Wir freuen uns über Fehlerberichte, Feature-Vorschläge, Dokumentationsverbesserungen und Code-Beiträge.

Bitte lesen Sie unseren [Contributing Guide](CONTRIBUTING.md) für Details zu:
- Einrichtung Ihrer Entwicklungsumgebung
- Unseren Code-Stil und Richtlinien
- Den Pull-Request-Prozess
- Wie man Fehler meldet und Features vorschlägt

Für Sicherheitslücken siehe bitte unsere [Sicherheitsrichtlinie](SECURITY.md).

---

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE)-Datei für Details.

---

## 🙏 Danksagungen

- **Ultralytics YOLOv8** - Leistungsstarkes Objekterkennungs-Framework
- **OpenCV** - Computer-Vision-Bibliothek
- **Vogel-Kamera-Linux** - Elternprojekt für automatisierte Vogelbeobachtung

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- **Diskussionen:** [GitHub Discussions](https://github.com/kamera-linux/vogel-video-analyzer/discussions)

---

**Mit ❤️ erstellt vom Vogel-Kamera-Linux Team**
