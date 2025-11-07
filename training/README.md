# Training Custom Bird Species Classifier

Dieses Verzeichnis enthält Scripts zum Trainieren eines eigenen Bird Species Classifiers für deine spezifischen Vogelarten.

## Warum ein Custom Model?

Die vortrainierten Modelle (wie `chriamue/bird-species-classifier`) wurden auf globalen Datensätzen trainiert und klassifizieren oft europäische Gartenvögel falsch als exotische Arten. Ein Custom Model, trainiert auf deinen eigenen Vogelhaus-Videos, liefert wesentlich bessere Ergebnisse.

## Workflow

### 1. Bilder aus Videos extrahieren

Nutze `extract_birds.py` um Vogel-Crops aus deinen Videos zu extrahieren:

```bash
python training/extract_birds.py <video_path> \
  -o ~/vogel-training-data/<species>_video1/ \
  --sample-rate 50
```

**Beispiel für mehrere Videos:**

```bash
# Kohlmeise
python training/extract_birds.py ~/Videos/Vogelhaus/kohlmeise1.mp4 \
  -o ~/vogel-training-data/kohlmeise_video1/

# Blaumeise
python training/extract_birds.py ~/Videos/Vogelhaus/blaumeise1.mp4 \
  -o ~/vogel-training-data/blaumeise_video1/

# Rotkehlchen
python training/extract_birds.py ~/Videos/Vogelhaus/rotkehlchen1.mp4 \
  -o ~/vogel-training-data/rotkehlchen_video1/

# usw.
```

**Tipp:** Verwende `--sample-rate 50` für 120fps Videos oder `--sample-rate 10` für 20-30fps Videos.

### 2. Dataset organisieren

Nachdem du Bilder für alle Vogelarten gesammelt hast, organisiere sie in Train/Val Split:

```bash
cd ~/vogel-training-data
python ~/path/to/vogel-video-analyzer/training/organize_dataset.py
```

Dies erstellt:
- `~/vogel-training-data/organized/train/` (80%)
- `~/vogel-training-data/organized/val/` (20%)

**Hinweis:** Die Script-Pfade in `organize_dataset.py` und `train_custom_model.py` müssen ggf. angepasst werden, wenn du ein anderes Verzeichnis verwendest.

### 3. Training starten

**Wichtig:** Training benötigt zusätzliche Dependencies:

```bash
pip install torch torchvision datasets accelerate
```

Dann starte das Training:

```bash
cd ~/vogel-training-data
python ~/path/to/vogel-video-analyzer/training/train_custom_model.py
```

**Training-Konfiguration:**
- Basis-Modell: `google/efficientnet-b0`
- Epochs: 50 (mit Early Stopping)
- Batch Size: 16
- Learning Rate: 2e-4
- Image Size: 224x224

**Dauer:** Ca. 3-4 Stunden auf Raspberry Pi 5 (abhängig von Dataset-Größe)

Das trainierte Modell wird gespeichert in:
```
~/vogel-models/bird-classifier-YYYYMMDD_HHMMSS/final/
```

### 4. Modell testen

Teste das trainierte Modell auf dem Validation Set:

```bash
python training/test_model.py ~/vogel-models/bird-classifier-YYYYMMDD_HHMMSS/final/
```

Oder teste auf einem einzelnen Bild:

```bash
python training/test_model.py ~/vogel-models/bird-classifier-YYYYMMDD_HHMMSS/final/ /path/to/image.jpg
```

### 5. Custom Modell verwenden

Verwende dein trainiertes Modell mit vogel-video-analyzer:

```bash
vogel-video-analyzer --species-model ~/vogel-models/bird-classifier-YYYYMMDD_HHMMSS/final/ <video>
```

## Empfohlene Dataset-Größe

Für gute Ergebnisse empfehle ich mindestens:
- **Minimum:** 30-50 Bilder pro Vogelart
- **Optimal:** 100+ Bilder pro Vogelart
- **Klassen-Balance:** Versuche ähnliche Anzahl Bilder pro Art zu haben

**Beispiel aus meinem Test-Dataset:**
- Kohlmeise: 353 Bilder
- Kleiber: 45 Bilder
- Blaumeise: 43 Bilder
- Sumpfmeise: 39 Bilder
- Rotkehlchen: 29 Bilder

## Scripts

### `extract_birds.py`

Extrahiert einzelne Vogel-Crops aus Videos mit YOLO Object Detection.

**Optionen:**
- `--model`: YOLO Modell (default: `yolov8n.pt`)
- `--threshold`: Konfidenz-Schwellwert (default: 0.3)
- `--sample-rate`: Verarbeite jedes N-te Frame (default: 10)
- `--output` / `-o`: Output-Verzeichnis

### `organize_dataset.py`

Organisiert extrahierte Bilder in 80/20 Train/Val Split.

**Anpassungen erforderlich:**
- `SOURCE_DIR`: Pfad zu deinen extrahierten Bildern
- `SPECIES_MAPPING`: Deine Vogelarten (Ordnernamen)

### `train_custom_model.py`

Trainiert ein EfficientNet-basiertes Modell auf deinem Dataset.

**Anpassungen erforderlich:**
- `DATA_DIR`: Pfad zum organisierten Dataset
- `OUTPUT_DIR`: Pfad zum Speichern der trainierten Modelle
- `SPECIES`: Liste deiner Vogelarten

### `test_model.py`

Testet ein trainiertes Modell auf Validation-Bildern oder einzelnen Bildern.

## Data Augmentation

Das Training-Script nutzt folgende Augmentations:
- Random Resized Crop (80-100%)
- Random Horizontal Flip (50%)
- Color Jitter (Brightness, Contrast, Saturation, Hue)

Dies hilft dem Modell, robuster gegenüber verschiedenen Lichtverhältnissen und Kameraperspektiven zu werden.

## Tipps

1. **Mehr Daten = Besser:** Sammle Bilder aus verschiedenen Videos, Tageszeiten, Wetterbedingungen
2. **Klassen-Balance:** Versuche ähnliche Anzahl Bilder pro Vogelart zu haben
3. **Qualität:** Entferne unscharfe oder schlecht erkannte Bilder manuell
4. **Checkpoints:** Das Training speichert Checkpoints - bei Unterbrechung kannst du fortsetzen
5. **Monitoring:** Schau dir `~/vogel-models/bird-classifier-*/logs/` an für Training-Verlauf

## Fehlerbehebung

**Problem:** `ModuleNotFoundError: No module named 'torch'`
```bash
~/venv-vogel/bin/pip install torch torchvision datasets accelerate
```

**Problem:** Out of Memory
- Reduziere `BATCH_SIZE` in `train_custom_model.py` (z.B. auf 8)
- Nutze kleineres Modell: `google/mobilenet_v2_1.0_224`

**Problem:** Schlechte Accuracy
- Sammle mehr Trainingsdaten
- Prüfe ob Bilder korrekt klassifiziert sind (falsche Ordner?)
- Erhöhe `NUM_EPOCHS` oder reduziere `early_stopping_patience`

## Lizenz

Diese Scripts sind Teil von vogel-video-analyzer und unter der MIT Lizenz verfügbar.
