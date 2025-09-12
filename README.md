# YouTube to REGZA 変換ツール

YouTube動画をREGZA 40V30対応のMP4形式に変換するPythonツールです。

## 概要

このツールは、YouTubeの動画をダウンロードして、REGZA 40V30テレビで再生可能な形式に変換します。変換されたファイルはQNAP NASのDLNA共有フォルダに配置することで、テレビで視聴できます。

## 機能

- YouTube動画の自動ダウンロード（最高品質）
- REGZA 40V30仕様への最適化変換
- 一時ファイルの自動削除
- シンプルなコマンドライン操作

## 変換仕様

- **解像度**: 640x480 (アスペクト比維持)
- **動画コーデック**: H.264 Baseline Profile Level 3.1
- **フレームレート**: 29.97fps
- **音声コーデック**: AAC
- **音声ビットレート**: 128kbps
- **サンプリングレート**: 44.1kHz
- **チャンネル**: ステレオ
- **品質**: CRF 20

## 必要な環境

- Python 3.11以上
- [uv](https://github.com/astral-sh/uv) (パッケージ管理)
- [ffmpeg](https://ffmpeg.org/) (動画変換エンジン)

## インストール

1. リポジトリをクローン
```bash
git clone <repository-url>
cd youtube_to_regza
```

2. 依存関係をインストール
```bash
uv sync
```

## 使用方法

```bash
uv run python youtube_to_regza.py <YouTube_URL>
```

### 使用例

```bash
# 動画を変換
uv run python youtube_to_regza.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 出力ファイル: output_regza.mp4
```

## 出力ファイル

変換が完了すると、`output_regza.mp4`ファイルが生成されます。このファイルをQNAP NASのDLNA共有フォルダに配置し、テレビでリスキャンすることで視聴できます。

## トラブルシューティング

### よくある問題

1. **ffmpegが見つからない**
   - ffmpegがインストールされていることを確認
   - PATH環境変数にffmpegが含まれていることを確認

2. **動画のダウンロードに失敗**
   - YouTube URLが正しいことを確認
   - インターネット接続を確認
   - yt-dlpが最新版であることを確認

3. **変換に失敗**
   - 入力動画が有効であることを確認
   - 十分なディスク容量があることを確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグ報告や機能要望は、GitHubのIssuesページでお知らせください。

## 更新履歴

- v1.0.0 (2025-09-12): 初回リリース
  - YouTube動画ダウンロード機能
  - REGZA 40V30仕様変換機能
  - 基本的なエラーハンドリング
