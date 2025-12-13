# 🐦 Vogel Video Analyzer

![Vogel Video Analyzer Banner](assets/banner.png)

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
- 📊 **HTMLレポート（v0.5.0+）** - チャートとサムネイル付きのインタラクティブなビジュアルレポート
  - 時系列の鳥検出を示すアクティビティタイムライン
  - 種の分布チャート
  - 最良の検出のサムネイルギャラリー
  - デスクトップとモバイル対応のレスポンシブデザイン
  - 自己完結型HTMLファイル（外部依存関係なし）
- 🎬 **動画注釈** - バウンディングボックスと種ラベル付きの注釈動画を作成（v0.3.0+）
- 📊 **詳細な統計** - フレームごとの分析と鳥コンテンツのパーセンテージ
- 🎯 **セグメント検出** - 鳥が存在する連続した時間帯を識別
- ⚡ **パフォーマンス最適化** - 設定可能なサンプリングレートで高速処理
- 📄 **JSONエクスポート** - アーカイブやさらなる分析のための構造化レポート
- 🗑️ **スマート自動削除** - 鳥コンテンツのない動画ファイルまたはフォルダを削除
- 📝 **ログサポート** - バッチ処理ワークフロー用の構造化ログ
- 🐍 **ライブラリ & CLI** - スタンドアロンツールとして、またはPythonプロジェクトに統合

---

## 🎓 独自の種分類器をトレーニングしませんか？

**[vogel-model-trainer](https://github.com/kamera-linux/vogel-model-trainer)** を使用して、動画からトレーニングデータを抽出し、地域の鳥種用のカスタムモデルを構築できます！

**カスタムモデルをトレーニングする理由は？**
- 事前学習済みモデルは、ヨーロッパの庭鳥を異国の種として誤認識することがよくあります
- カスタムモデルは、あなた固有の鳥に対して90%以上の精度を達成します
- あなたのカメラ設定と照明条件でトレーニングされます

👉 **[vogel-model-trainerを始める →](https://github.com/kamera-linux/vogel-model-trainer)**

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

# パッケージのインストール
pip install vogel-video-analyzer
```

#### 直接インストール

```bash
pip install vogel-video-analyzer
```

### 基本的な使い方

```bash
# 単一の動画を分析
vogel-analyze video.mp4

# 鳥の種を識別
vogel-analyze --identify-species video.mp4

# HTMLレポートを生成（v0.5.0+）
vogel-analyze --language en --identify-species --species-model kamera-linux/german-bird-classifier --species-threshold 0.80 --html-report report.html --sample-rate 15 --max-thumbnails 12 video.mp4
# サンプルを見る: https://htmlpreview.github.io/?https://github.com/kamera-linux/vogel-video-analyzer/blob/main/examples/html_report_example.html

# バウンディングボックスと種ラベル付きの注釈動画を作成（v0.3.0+）
vogel-analyze --identify-species \
  --annotate-video \
  video.mp4
# 出力：video_annotated.mp4（自動）

# 複合出力：JSON + HTMLレポート
vogel-analyze --identify-species -o data.json --html-report report.html video.mp4

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

初回実行時にモデル（約100-300MB）が自動的にダウンロードされ、以降はローカルにキャッシュされます。

**🚀 GPU アクセラレーション：** 種の識別は、利用可能な場合は自動的にCUDA（NVIDIA GPU）を使用し、推論を大幅に高速化します。GPUが検出されない場合は、CPUにフォールバックします。

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

#### 動画注釈（v0.3.0+）

バウンディングボックスと種ラベル付きの注釈動画を作成：

```bash
# 基本的な注釈（自動出力パス）
vogel-analyze --identify-species \
  --annotate-video \
  input.mp4
# 出力：input_annotated.mp4

# カスタムモデルと高速処理
vogel-analyze --identify-species \
  --species-model kamera-linux/german-bird-classifier \
  --sample-rate 3 \
  --annotate-video \
  my_video.mp4
# 出力：my_video_annotated.mp4

# カスタム出力パス（単一動画のみ）
vogel-analyze --identify-species \
  --annotate-video \
  --annotate-output custom_output.mp4 \
  input.mp4

# 複数の動画を同時処理
vogel-analyze --identify-species \
  --annotate-video \
  --multilingual \
  *.mp4
# 作成：video1_annotated.mp4, video2_annotated.mp4, など
```

**機能：**
- 📦 検出された鳥の周りに**バウンディングボックス**（緑色）
- 🏷️ 信頼度スコア付きの**種ラベル**
- 🌍 **多言語ラベル**（英語、ドイツ語、日本語）
- ⏱️ フレーム番号と時間を表示する**タイムスタンプオーバーレイ**
- 📊 **リアルタイム進行状況**インジケーター
- 🎵 **音声保持**（元の動画から自動的にマージ）


**パフォーマンスのヒント：**
- より高速な処理には`--sample-rate 2`以上を使用（Nフレームごとに注釈）
- 出力動画は元の解像度とフレームレートを維持
- 処理時間は動画の長さと種分類の複雑さによる

#### 動画サマリー（v0.3.1+）

鳥の活動がないセグメントをスキップして圧縮動画を作成：

```bash
# デフォルト設定での基本的なサマリー
vogel-analyze --create-summary video.mp4
# 出力：video_summary.mp4

# カスタム閾値
vogel-analyze --create-summary \
  --skip-empty-seconds 5.0 \
  --min-activity-duration 1.0 \
  video.mp4

# カスタム出力パス（単一動画のみ）
vogel-analyze --create-summary \
  --summary-output custom_summary.mp4 \
  video.mp4

# 複数の動画を同時処理
vogel-analyze --create-summary *.mp4
# 作成：video1_summary.mp4, video2_summary.mp4, など

# 高速処理との組み合わせ
vogel-analyze --create-summary \
  --sample-rate 10 \
  video.mp4
```

**機能：**
- ✂️ **スマートセグメント検出** - 鳥の活動期間を自動的に識別
- 🎵 **音声保持** - 完璧な音声同期を維持（ピッチ/速度変更なし）
- ⚙️ **設定可能な閾値**：
  - `--skip-empty-seconds`（デフォルト：3.0）- スキップする鳥なしセグメントの最小期間
  - `--min-activity-duration`（デフォルト：2.0）- 保持する鳥の活動の最小期間
- 📊 **圧縮統計** - オリジナルとサマリーの期間を表示
- ⚡ **高速処理** - ffmpeg concat を使用（再エンコードなし）
- 📁 **自動パス生成** - `<original>_summary.mp4` として保存

**動作の仕組み：**
1. フレームごとに動画を分析して鳥の存在を検出
2. 鳥のいる/いない連続セグメントを識別
3. 期間の閾値に基づいてセグメントをフィルタリング
4. ffmpeg を使用して音声付きでセグメントを連結
5. 圧縮統計を返す

**出力例：**
```
🔍 鳥の活動についてビデオを分析しています：video.mp4...
   📊 30.0 FPSで18000フレームを分析しています...
   ✅ 分析完了 - 1250フレームで鳥を検出

📊 鳥の活動セグメントが識別されました
   📊 保持するセグメント：8
   ⏱️  オリジナル期間：0:10:00
   ⏱️  サマリー期間：0:02:45
   📉 圧縮：72.5% 短縮

🎬 要約ビデオを作成中：video_summary.mp4...
   ✅ 要約ビデオが正常に作成されました
   📁 video_summary.mp4
```

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

## 🔍 技術詳細

### 検出アルゴリズム

- **対象クラス:** 鳥（COCOクラス14）
- **推論:** フレームごとのYOLOv8検出
- **セグメント検出:** 最大2秒の間隔で連続する鳥フレームをグループ化
- **パフォーマンス:** 30fps動画でsample-rate=5の場合、約5倍の高速化

### 種の識別（GPU最適化）

- **GPUバッチ処理:** フレームごとにすべての鳥のクロップを同時に処理（v0.4.4+）
  - フレーム内で検出されたすべての鳥に対する単一バッチ推論
  - 最大8つのクロップを並列処理（`batch_size=8`）
  - 逐次処理と比較して最大8倍高速
  - 「pipelines sequentially on GPU」警告を排除
- **デバイス選択:** CUDA（NVIDIA GPU）の自動検出とCPUフォールバック
- **モデル読み込み:** Hugging Face Hubからダウンロード（約100-300MB、ローカルキャッシュ）
- **閾値フィルタリング:** 設定可能な信頼度閾値（デフォルト: 0.3）
- **多言語サポート:** 英語、ドイツ語、日本語の鳥の名前（39種）

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
