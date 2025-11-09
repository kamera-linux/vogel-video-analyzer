# 🐦 Vogel Video Analyzer

**言語:** [🇬🇧 English](README.md) | [🇩🇪 Deutsch](README.de.md) | [🇯🇵 日本語](README.ja.md)

<p align="left">
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/vogel-video-analyzer.svg"></a>
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/vogel-video-analyzer.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <a href="https://pypi.org/project/vogel-video-analyzer/"><img alt="PyPI Status" src="https://img.shields.io/pypi/status/vogel-video-analyzer.svg"></a>
  <a href="https://pepy.tech/project/vogel-video-analyzer"><img alt="Downloads" src="https://static.pepy.tech/badge/vogel-video-analyzer"></a>
</p>

**YOLOv8ベースの鳥コンテンツ検出・定量化のための動画解析ツール**

最先端のYOLOv8物体検出を使用して、動画内の鳥の存在を検出・定量化するための強力なコマンドラインツールおよびPythonライブラリ。

---

## ✨ 特徴

- 🤖 **YOLOv8による検出** - 事前学習済みモデルによる正確な鳥検出
- 🦜 **種の識別** - Hugging Faceモデルを使用した鳥の種の識別（オプション）
- 📊 **詳細な統計** - フレームごとの分析と鳥コンテンツのパーセンテージ
- 🎯 **セグメント検出** - 鳥が存在する連続した時間帯を識別
- ⚡ **パフォーマンス最適化** - 設定可能なサンプリングレートで高速処理
- 📄 **JSONエクスポート** - アーカイブやさらなる分析のための構造化レポート
- 🗑️ **スマート自動削除** - 鳥コンテンツのない動画ファイルまたはフォルダを削除
- 📝 **ログサポート** - バッチ処理ワークフロー用の構造化ログ
- 🐍 **ライブラリ & CLI** - スタンドアロンツールとして、またはPythonプロジェクトに統合

---

## 🚀 クイックスタート

### インストール

#### 推奨：仮想環境を使用

```bash
# venvのインストール（必要な場合、Debian/Ubuntu）
sudo apt install python3-venv

# 仮想環境の作成
python3 -m venv ~/venv-vogel

# アクティベート
source ~/venv-vogel/bin/activate  # Windows: ~/venv-vogel\Scripts\activate

# パッケージのインストール（基本）
pip install vogel-video-analyzer

# 種の識別サポート付きでインストール（オプション）
pip install vogel-video-analyzer[species]
```

#### 直接インストール

```bash
# 基本インストール
pip install vogel-video-analyzer

# 種の識別サポート付き
pip install vogel-video-analyzer[species]
```

### 基本的な使い方

```bash
# 単一の動画を分析
vogel-analyze video.mp4

# 鳥の種を識別
vogel-analyze --identify-species video.mp4

# 日本語で出力
vogel-analyze --language ja video.mp4

# より高速な分析（5フレームごと）
vogel-analyze --sample-rate 5 video.mp4

# JSONにエクスポート
vogel-analyze --output report.json video.mp4

# 鳥コンテンツ0%の動画ファイルのみを削除
vogel-analyze --delete-file *.mp4

# 鳥コンテンツ0%のフォルダ全体を削除
vogel-analyze --delete-folder ~/Videos/*/*.mp4

# ディレクトリのバッチ処理
vogel-analyze ~/Videos/Birds/**/*.mp4
```

---

## 📖 使用例

### コマンドラインインターフェース

#### 基本的な分析
```bash
# デフォルト設定で単一の動画を分析
vogel-analyze bird_video.mp4

# カスタム信頼度閾値
vogel-analyze --threshold 0.4 bird_video.mp4

# 5フレームごとにサンプリングして高速化
vogel-analyze --sample-rate 5 bird_video.mp4
```

#### 種の識別

**⚠️ 実験的機能:** 事前学習済みモデルは、ヨーロッパの庭園の鳥を外来種として誤認識する可能性があります。地域の鳥種を正確に識別するには、カスタムモデルのトレーニングを検討してください（[カスタムモデルトレーニング](#-カスタムモデルトレーニング)を参照）。

**インストール：**
```bash
pip install vogel-video-analyzer[species]
```

初回実行時、モデル（約100-300MB）が自動的にダウンロードされ、今後の使用のためにローカルにキャッシュされます。

#### カスタムモデルの使用

特定の鳥種でより高い精度を得るために、ローカルでトレーニングされたモデルを使用できます：

```bash
# カスタムモデルを使用
vogel-analyze --identify-species --species-model ~/vogel-models/my-model/ video.mp4

# カスタム信頼度閾値を使用（デフォルト：0.3）
vogel-analyze --identify-species \
  --species-model ~/vogel-models/my-model/ \
  --species-threshold 0.5 \
  video.mp4
```

**閾値ガイドライン：**
- `0.1-0.2` - 検出を最大化（探索的）
- `0.3-0.5` - バランス型（推奨）
- `0.6-0.9` - 高信頼度のみ

詳細については、[カスタムモデルトレーニング](#-カスタムモデルトレーニング)セクションを参照してください。

#### 高度なオプション
```bash
# カスタム閾値とサンプルレート
vogel-analyze --threshold 0.4 --sample-rate 10 video.mp4

# 信頼度調整を伴う種の識別
vogel-analyze --identify-species --species-threshold 0.4 video.mp4
```

#### バッチ処理
```bash
# 複数の動画
vogel-analyze video1.mp4 video2.mp4 video3.mp4

# ディレクトリ内のすべてのMP4ファイル
vogel-analyze ~/Videos/Birdhouse/*.mp4

# 再帰的（すべてのサブディレクトリ）
vogel-analyze ~/Videos/Birds/**/*.mp4
```

#### 自動削除
```bash
# 鳥コンテンツのない動画ファイルを削除
vogel-analyze --delete-file --sample-rate 5 *.mp4

# 鳥コンテンツのないフォルダ全体を削除
vogel-analyze --delete-folder --sample-rate 5 ~/Videos/*/*.mp4

# 削除前にプレビュー（削除なしで実行）
vogel-analyze --sample-rate 5 ~/Videos/*/*.mp4
```

#### レポートのエクスポート
```bash
# JSON形式で保存
vogel-analyze --output report.json video.mp4

# 種の識別とJSON
vogel-analyze --identify-species --output analysis.json video.mp4
```

#### ロギング
```bash
# コンソール出力をログファイルに保存
vogel-analyze --log *.mp4

# ログの場所：/var/log/vogel-kamera-linux/YYYY/KWXX/TIMESTAMP_analyze.log
```

---

## 🎓 カスタムモデルトレーニング

**独自の鳥種に対して高精度を実現！**

事前学習済みモデルは世界中の鳥種でトレーニングされており、地域の種を誤認識する可能性があります。最良の結果を得るには、特定のバードハウスのセットアップでカスタムモデルをトレーニングしてください。

**カスタムモデルの利点：**
- あなたの特定の鳥種に対する高精度
- あなたのカメラのセットアップと照明条件でトレーニング
- 正しく識別された鳥に対する信頼度スコア >0.9

### クイックスタート

トレーニングツールは現在、スタンドアロンパッケージとして利用可能です：**[vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)**

**1. トレーニングパッケージのインストール：**
```bash
pip install vogel-model-trainer
```

**2. 動画から鳥の画像を抽出：**
```bash
vogel-trainer extract ~/Videos/kohlmeise.mp4 \
  --folder ~/vogel-training-data/ \
  --bird kohlmeise \
  --sample-rate 3
```

**3. データセットを整理（80/20 train/val 分割）：**
```bash
vogel-trainer organize \
  --source ~/vogel-training-data/ \
  --output ~/vogel-training-data/organized/
```

**4. モデルをトレーニング（Raspberry Pi 5で約3-4時間必要）：**
```bash
vogel-trainer train
```

**5. トレーニングされたモデルを使用：**
```bash
vogel-analyze --identify-species \
  --species-model ~/vogel-models/bird-classifier-*/final/ \
  video.mp4
```

### 推奨データセットサイズ

- **最小：** 鳥種ごとに30-50枚の画像
- **最適：** 鳥種ごとに100枚以上の画像
- **バランス：** 各種で同程度の画像数

### 完全なドキュメント

詳細については、**[vogel-model-trainer ドキュメント](https://github.com/kamera-linux/vogel-model-trainer)**を参照してください：
- 完全なトレーニングワークフロー
- より高い精度のための反復トレーニング
- 高度な使用法とトラブルシューティング
- パフォーマンスのヒントとベストプラクティス

---

## 📚 ドキュメント

- **GitHubリポジトリ：** [vogel-video-analyzer](https://github.com/kamera-linux/vogel-video-analyzer)
- **PyPIパッケージ：** [vogel-video-analyzer](https://pypi.org/project/vogel-video-analyzer/)
- **トレーニングツール：** [vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)
- **親プロジェクト：** [vogel-kamera-linux](https://github.com/kamera-linux/vogel-kamera-linux)

---

## 🔧 技術仕様

### 依存関係

**コア：**
- Python ≥ 3.8
- OpenCV (cv2)
- Ultralytics YOLOv8
- NumPy

**種の識別（オプション）：**
- Transformers (Hugging Face)
- PyTorch
- Pillow

### サポートされる動画形式

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- その他のOpenCVがサポートする形式

### パフォーマンス

- **CPU処理：** Raspberry Pi 5でテスト済み
- **サンプリング：** 設定可能（デフォルト：5フレームごと）
- **メモリ使用量：** 標準のビデオ解析で約500MB-1GB
- **速度：** フルHDビデオの場合、リアルタイムの5-10倍の速度（`--sample-rate 5`使用時）

---

## 🤝 コントリビューション

コントリビューションを歓迎します！以下をお願いします：

1. リポジトリをフォーク
2. 機能ブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを開く

詳細については、[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

---

## 📝 ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下でライセンスされています。

---

## 🙏 謝辞

- **YOLOv8** - [Ultralytics](https://github.com/ultralytics/ultralytics)による物体検出
- **事前学習済み鳥種モデル** - [Hugging Face](https://huggingface.co/)コミュニティ
- **vogel-kamera-linux** - 親プロジェクト

---

## 📧 サポート

- **Issues：** [GitHub Issues](https://github.com/kamera-linux/vogel-video-analyzer/issues)
- **ディスカッション：** [GitHub Discussions](https://github.com/kamera-linux/vogel-video-analyzer/discussions)

---

**このツールを楽しんでいただけましたら、⭐をつけてください！**
