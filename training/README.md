# Training Custom Bird Species Classifier

Dieses Verzeichnis enthält Scripts zum Trainieren eines eigenen Bird Species Classifiers für deine spezifischen Vogelarten.

## Warum ein Custom Model?

Die vortrainierten Modelle (wie `chriamue/bird-species-classifier`) wurden auf globalen Datensätzen trainiert und klassifizieren oft europäische Gartenvögel falsch als exotische Arten. Ein Custom Model, trainiert auf deinen eigenen Vogelhaus-Videos, liefert wesentlich bessere Ergebnisse (96%+ Accuracy).

## 📋 Workflow-Übersicht

1. **Bilder extrahieren** → `extract_birds.py`
2. **Dataset organisieren** → `organize_dataset.py`
3. **Modell trainieren** → `train_custom_model.py`
4. **Modell testen** → `test_model.py`
5. **Modell verwenden** → `vogel-analyze --species-model <path>`

## 🎯 Schritt 1: Bilder aus Videos extrahieren

Das neue `extract_birds.py` unterstützt 3 Modi:

### Option A: Manuelle Sortierung (empfohlen für erste Extraktion)

```bash
# Wenn du WEISST welche Art im Video ist
python training/extract_birds.py kohlmeise_video.mp4 \
  --folder ~/vogel-training-data/ \
  --bird kohlmeise \
  --threshold 0.5 \
  --sample-rate 3
```

→ Erstellt automatisch `~/vogel-training-data/kohlmeise/` mit 224x224px Bildern

### Option B: Auto-Sortierung (für iteratives Training)

```bash
# Mit deinem trainierten Modell
python training/extract_birds.py gemischtes_video.mp4 \
  --folder ~/vogel-training-data/ \
  --species-model ~/vogel-models/bird-classifier-TIMESTAMP/final/ \
  --threshold 0.6 \
  --sample-rate 2
```

→ Klassifiziert automatisch und sortiert in Species-Ordner

### Option C: Wildcards & Batch-Processing

```bash
# Alle Videos in einem Ordner
python training/extract_birds.py "~/Videos/Vogelhaus/*.mp4" \
  --folder ~/vogel-training-data/ \
  --bird kohlmeise

# Rekursiv alle Unterverzeichnisse
python training/extract_birds.py ~/Videos/ \
  --folder ~/vogel-training-data/ \
  --species-model ~/vogel-models/bird-classifier-*/final/ \
  --recursive
```

### Wichtige Parameter

| Parameter | Default | Beschreibung |
|-----------|---------|--------------|
| `--threshold` | 0.5 | YOLO Detection Threshold (höher = bessere Qualität) |
| `--sample-rate` | 3 | Analysiere jeden N-ten Frame (niedriger = mehr Bilder) |
| `--no-resize` | - | Behalte Original-Größe (Standard: 224x224px) |
| `--bird` | - | Manuelle Species (erstellt Unterordner) |
| `--species-model` | - | Auto-Klassifizierung mit Custom Model |

### Beispiel-Workflow (erste Sammlung)

```bash
# 5 verschiedene Vogelarten extrahieren
python training/extract_birds.py ~/Videos/kohlmeise_*.mp4 \
  --folder ~/vogel-training-data/ --bird kohlmeise

python training/extract_birds.py ~/Videos/blaumeise_*.mp4 \
  --folder ~/vogel-training-data/ --bird blaumeise

python training/extract_birds.py ~/Videos/rotkehlchen_*.mp4 \
  --folder ~/vogel-training-data/ --bird rotkehlchen

python training/extract_birds.py ~/Videos/kleiber_*.mp4 \
  --folder ~/vogel-training-data/ --bird kleiber

python training/extract_birds.py ~/Videos/sumpfmeise_*.mp4 \
  --folder ~/vogel-training-data/ --bird sumpfmeise
```

**Ergebnis:**
```
vogel-training-data/
├── kohlmeise/
│   ├── kohlmeise1_20251108_143000_a1b2c3d4_f001234_c0.85.jpg
│   └── ... (353 Bilder)
├── blaumeise/
│   └── ... (43 Bilder)
├── rotkehlchen/
│   └── ... (29 Bilder)
├── kleiber/
│   └── ... (45 Bilder)
└── sumpfmeise/
    └── ... (39 Bilder)
```

## 📊 Schritt 2: Dataset organisieren

```bash
python training/organize_dataset.py \
  --source ~/vogel-training-data/ \
  --output ~/vogel-training-data/organized/ \
  --train-ratio 0.8
```

**Was macht das Script:**
- Findet automatisch alle Species-Ordner
- 80/20 Train/Val Split mit Random Shuffling
- Kopiert Bilder in `train/` und `val/` Struktur
- Unterstützt alte (`species_video*/`) und neue (`species/`) Strukturen

**Output:**
```
organized/
├── train/
│   ├── kohlmeise/     (282 Bilder)
│   ├── blaumeise/     ( 34 Bilder)
│   ├── rotkehlchen/   ( 23 Bilder)
│   ├── kleiber/       ( 36 Bilder)
│   └── sumpfmeise/    ( 31 Bilder)
└── val/
    ├── kohlmeise/     ( 71 Bilder)
    ├── blaumeise/     (  9 Bilder)
    ├── rotkehlchen/   (  6 Bilder)
    ├── kleiber/       (  9 Bilder)
    └── sumpfmeise/    (  8 Bilder)
```

## 🚀 Schritt 3: Training starten

### Dependencies installieren

```bash
pip install torch torchvision datasets accelerate transformers
```

### Training starten

```bash
python training/train_custom_model.py
```

**Training-Konfiguration (optimiert):**
- **Basis-Modell:** `google/efficientnet-b0` (8.5M Parameter)
- **Epochs:** 50 (Early Stopping nach 7 Epochen ohne Verbesserung)
- **Batch Size:** 16
- **Learning Rate:** 2e-4 mit Cosine Annealing
- **Image Size:** 224x224px
- **Data Augmentation:**
  - RandomResizedCrop (70-100% scale)
  - RandomRotation (±15°)
  - RandomAffine (Translation)
  - ColorJitter (Brightness/Contrast/Saturation)
  - GaussianBlur (Fokus-Variationen)
- **Regularization:**
  - Weight Decay: 0.01
  - Label Smoothing: 0.1

**Dauer:** Ca. 3-4 Stunden auf Raspberry Pi 5 (500 Bilder, 5 Arten)

**Output:**
```
~/vogel-models/bird-classifier-20251108_143000/
├── checkpoints/          (Zwischenstände)
├── logs/                 (TensorBoard Logs)
└── final/               (Finales Modell - DAS BRAUCHST DU!)
    ├── config.json
    ├── model.safetensors
    └── preprocessor_config.json
```

### Training läuft:
```
Epoch 1/50
  Loss: 1.234, Accuracy: 45.2%
  
Epoch 5/50
  Loss: 0.456, Accuracy: 85.3%
  
Epoch 12/50 ⭐ BEST
  Loss: 0.123, Accuracy: 96.88%
  Val Accuracy per Species:
    - Blaumeise:   100.0%
    - Kleiber:     100.0%
    - Rotkehlchen: 100.0%
    - Sumpfmeise:  100.0%
    - Kohlmeise:    83.3%

Early stopping triggered at epoch 19
```

## ✅ Schritt 4: Modell testen

```bash
# Test auf einzelnem Bild
python training/test_model.py \
  ~/vogel-models/bird-classifier-20251108_143000/final/ \
  /path/to/bird.jpg
```

**Output:**
```
🖼️  Testing: bird.jpg
   🐦 Predicted: kohlmeise (98.5% confidence)
```

**Hinweis:** Validation-Set Testing hat aktuell einen Bug. Nutze Single-Image Testing.

## 🎯 Schritt 5: Custom Modell verwenden

### In vogel-analyze

```bash
vogel-analyze --identify-species \
  --species-model ~/vogel-models/bird-classifier-20251108_143000/final/ \
  --species-threshold 0.3 \
  vogelhaus_video.mp4
```

### Für weitere Extraktion (iteratives Training)

```bash
# Nutze dein trainiertes Modell für Auto-Sortierung
python training/extract_birds.py "~/Videos/neue_videos/*.mp4" \
  --folder ~/vogel-training-data/iteration2/ \
  --species-model ~/vogel-models/bird-classifier-20251108_143000/final/ \
  --threshold 0.6
```

## 🔄 Iteratives Training für höhere Genauigkeit

1. **Initiales Training** mit manuell sortierten Bildern
2. **Auto-Extraktion** mit trainiertem Modell aus neuen Videos
3. **Manuelles Review** der auto-sortierten Bilder
4. **Neues Training** mit erweitertem Dataset
5. **Wiederhole** bis gewünschte Accuracy erreicht

### Beispiel 2. Iteration:

```bash
# 1. Auto-Extraktion mit bestehendem Modell
python training/extract_birds.py ~/Videos/neue_aufnahmen/*.mp4 \
  --folder ~/vogel-training-data/iteration2/ \
  --species-model ~/vogel-models/bird-classifier-20251108_143000/final/

# 2. Review und Korrektur der Klassifizierungen
#    (Verschiebe falsch klassifizierte Bilder manuell)

# 3. Kombiniere mit alten Daten
mkdir ~/vogel-training-data/combined/
cp -r ~/vogel-training-data/kohlmeise ~/vogel-training-data/combined/
cp -r ~/vogel-training-data/iteration2/kohlmeise/* ~/vogel-training-data/combined/kohlmeise/
# ... für alle Species

# 4. Neues Training
python training/organize_dataset.py --source ~/vogel-training-data/combined/
python training/train_custom_model.py

# Ergebnis: Noch bessere Accuracy! 🎉
```

## 📈 Erfahrungswerte

### Datenmengen (Minimum für gute Ergebnisse):
- **Minimum:** ~20-30 Bilder pro Art
- **Gut:** ~50-100 Bilder pro Art
- **Optimal:** 100+ Bilder pro Art

### Trainingsergebnisse (509 Bilder, 5 Arten):
- **Validation Accuracy:** 96.88%
- **Per-Species Accuracy:**
  - Blaumeise: 100.0% (9/9 val images)
  - Kleiber: 100.0% (9/9)
  - Rotkehlchen: 100.0% (6/6)
  - Sumpfmeise: 100.0% (8/8)
  - Kohlmeise: 83.3% (59/71) ← Größte Klasse, schwieriger

### Tipps für bessere Ergebnisse:

1. **Vielfalt in Trainingsda ten:**
   - Verschiedene Lichtverhältnisse
   - Verschiedene Posen (seitlich, frontal, von oben)
   - Verschiedene Jahreszeiten (Federkleid ändert sich!)

2. **Klassen-Balance:**
   - Versuche ähnliche Anzahl Bilder pro Art zu haben
   - Kohlmeise (353 Bilder) vs Rotkehlchen (29 Bilder) = unbalanciert

3. **Qualität über Quantität:**
   - Lieber 50 gute, klare Bilder als 200 unscharfe
   - Threshold 0.5-0.6 für hochwertige Extraktion
   - Sample-Rate 2-3 für gute Abdeckung ohne Duplikate

4. **Monitoring:**
   - Per-Class Accuracy beachten
   - Confusion Matrix anschauen (welche Arten werden verwechselt?)
   - Bei niedriger Accuracy: Mehr Daten für diese Art sammeln

## 🛠️ Utility Scripts

### Bilder resizen

Falls du alte Bilder auf 224x224 konvertieren willst:

```bash
python ~/vogel-training-data/resize_images.py \
  --source ~/vogel-training-data/old_data/ \
  --output ~/vogel-training-data/old_data_resized/ \
  --size 224
```

## 📁 Dateien-Übersicht

| Script | Beschreibung |
|--------|--------------|
| `extract_birds.py` | Extrahiert Vogel-Crops aus Videos (224x224px) |
| `organize_dataset.py` | Organisiert Bilder in Train/Val Split |
| `train_custom_model.py` | Trainiert Custom EfficientNet Model |
| `test_model.py` | Testet trainierte Modelle |
| `README.md` | Diese Dokumentation |

## ⚠️ Bekannte Probleme

1. **test_model.py Validation Set Bug:**
   - Validation-Set Testing funktioniert nicht korrekt
   - **Workaround:** Nutze Single-Image Testing

2. **Memory Usage:**
   - Training benötigt ~2-3 GB RAM
   - Bei OOM Errors: Batch Size reduzieren

3. **Training auf CPU:**
   - Raspberry Pi 5: ~3-4 Stunden für 500 Bilder
   - Keine GPU-Beschleunigung verfügbar

## 🚀 Nächste Schritte

Nach erfolgreichem Training:

1. **Teste auf echten Videos** mit `vogel-analyze`
2. **Sammle Feedback** über Fehlklassifizierungen
3. **Iteriere** mit mehr Trainingsdaten
4. **Erweitere** um neue Vogelarten

Viel Erfolg beim Training! 🐦✨
