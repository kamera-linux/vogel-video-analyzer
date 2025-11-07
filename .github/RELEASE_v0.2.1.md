# Release v0.2.1 - German Translations & Custom Model Training

## 🎉 Highlights

- **🇩🇪 Deutsche Übersetzungen** - Vollständige i18n-Unterstützung für Vogelnamen und UI
- **🎓 Custom Model Training** - Tools zum Trainieren eigener Modelle für spezifische Vogelarten
- **📦 Lokale Modelle** - Unterstützung für lokal trainierte Modelle

## ✨ Neue Features

### Deutsche Übersetzungen
- 30+ Vogelnamen übersetzt (Kohlmeise, Blaumeise, Rotkehlchen, etc.)
- Alle UI-Nachrichten auf Deutsch verfügbar
- Automatische Spracherkennung aus System-Locale

### Custom Model Support
- Species Classifier akzeptiert jetzt lokale Pfade zusätzlich zu Hugging Face IDs
- Ermöglicht Training auf spezifische Vogelarten
- Bessere Genauigkeit für lokale Gartenvögel

### Training Tools (`training/` Verzeichnis)
- **`extract_birds.py`** - Extrahiert Vogel-Crops aus Videos für Dataset-Erstellung
- **`organize_dataset.py`** - Organisiert Bilder in Train/Val Splits (80/20)
- **`train_custom_model.py`** - Trainiert EfficientNet-basierte Classifier
- **`test_model.py`** - Testet trainierte Modelle auf Validierungsdaten
- Vollständige Dokumentation in `training/README.md`

## 🔄 Änderungen

- **Standard Species Model**: Gewechselt von `dima806/bird_species_image_detection` zu `chriamue/bird-species-classifier`
  - Höhere Konfidenzwerte (0.3-0.6 vs 0.01-0.06)
  - Kleinere Modellgröße (8.5M vs 86M Parameter)
  - Bessere Performance in Tests
- **Standard Confidence Threshold**: Erhöht von 0.1 auf 0.3
  - Reduziert False Positives
  - Besser abgestimmt auf chriamue Modell

## 🐛 Fixes

- **Critical:** Fixed species detection aggregation error ("unhashable type: 'list'")
- Species statistics korrekt aus bird detections extrahiert
- Verbesserte Fehlermeldungen für Species Classification

## 📚 Dokumentation

- ⚠️ Experimentelle Warnung für vortrainierte Modelle hinzugefügt
- Custom Model Training Workflow dokumentiert
- Deutsche README (`README.de.md`) aktualisiert
- `SECURITY.md` für v0.2.x aktualisiert

## 🎓 Custom Model Training

Vortrainierte Modelle identifizieren europäische Gartenvögel oft falsch als exotische Arten. Mit den neuen Training-Tools kannst du jetzt dein eigenes Modell trainieren:

```bash
# 1. Bilder extrahieren
python training/extract_birds.py video.mp4 -o ~/vogel-training-data/kohlmeise_video1/

# 2. Dataset organisieren
cd ~/vogel-training-data
python /pfad/zu/vogel-video-analyzer/training/organize_dataset.py

# 3. Modell trainieren
pip install torch torchvision datasets accelerate
python /pfad/zu/vogel-video-analyzer/training/train_custom_model.py

# 4. Eigenes Modell verwenden
vogel-analyze --identify-species --species-model ~/vogel-models/bird-classifier-*/final/ video.mp4
```

Siehe `training/README.md` für Details.

## 📦 Installation

```bash
# Standard Installation
pip install vogel-video-analyzer==0.2.1

# Mit Species Identification
pip install vogel-video-analyzer[species]==0.2.1
```

## 🔗 Links

- **PyPI**: https://pypi.org/project/vogel-video-analyzer/0.2.1/
- **Changelog**: [CHANGELOG.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/v0.2.1/CHANGELOG.md)
- **Training Guide**: [training/README.md](https://github.com/kamera-linux/vogel-video-analyzer/blob/v0.2.1/training/README.md)

## ⚠️ Hinweise

- Vortrainierte Modelle können europäische Gartenvögel als exotische Arten fehlidentifizieren
- Für beste Ergebnisse mit lokalen Vogelarten: Eigenes Modell trainieren
- Training benötigt ~3-4 Stunden auf Raspberry Pi 5
- Empfohlen: 30-50+ Bilder pro Vogelart für gute Genauigkeit

---

**Full Changelog**: https://github.com/kamera-linux/vogel-video-analyzer/compare/v0.2.0...v0.2.1
