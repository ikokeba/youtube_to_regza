# YouTube to REGZA 変換ツール

YouTube動画をREGZA 40V30対応のMP4形式に変換するPythonツールです。

## 概要

このツールは、YouTubeの動画をダウンロードして、REGZA 40V30テレビで再生可能な形式に変換します。変換されたファイルはNASのDLNA共有フォルダに配置することで、テレビで視聴できます。

主な特徴：
- 🎬 YouTube動画の自動ダウンロード（yt-dlp使用）
- 📺 REGZA 40V30仕様への最適化変換（ffmpeg使用）
- 📝 動画タイトル取得と自動ファイル名生成
- ⚙️ 柔軟な設定ファイルシステム
- 🧹 一時ファイルの自動クリーンアップ
- 🪟 Windowsバッチファイル対応

## 機能

### コア機能
- YouTube動画の自動ダウンロード（最高品質）
- REGZA 40V30仕様への最適化変換
- 動画タイトル取得と適切なファイル名生成
- 一時ファイルの自動削除
- 設定ファイルによる柔軟なカスタマイズ

### 高度機能
- 設定ファイルシステム（config.json / config_sample.json）
- 複数解像度対応（640x480 / 1920x1080）
- プログレス表示
- エラーハンドリング

## 変換仕様

### REGZA 40V30推奨設定
- **解像度**: 640x480 (4:3アスペクト比、アスペクト比維持)
- **動画コーデック**: H.264 Baseline Profile Level 3.1
- **フレームレート**: 29.97fps
- **音声コーデック**: AAC LC
- **音声ビットレート**: 128kbps
- **サンプリングレート**: 44.1kHz
- **チャンネル**: ステレオ
- **品質**: CRF 20

### 高品質設定（新テレビ対応）
- **解像度**: 1920x1080 (Full HD)
- **動画コーデック**: H.264 High Profile Level 4.0
- **その他**: 上記と同じ設定

## 必要な環境

- **Python**: 3.11以上
- **パッケージ管理**: [uv](https://github.com/astral-sh/uv)
- **動画変換**: [ffmpeg](https://ffmpeg.org/)
- **OS**: Windows 10/11 (バッチファイル対応)

## インストール

1. **リポジトリをクローン**
```bash
git clone <repository-url>
cd youtube_to_regza
```

2. **依存関係をインストール**
```bash
uv sync
```

3. **ffmpegのインストール確認**
```bash
ffmpeg -version
```
※ ffmpegがインストールされていない場合は、公式サイトからダウンロードしてインストールしてください。

## 使用方法

### 方法1: コマンドライン実行
```bash
uv run python youtube_to_regza.py <YouTube_URL>
```

### 方法2: バッチファイル実行（推奨）
```bash
# バッチファイルをダブルクリック、またはコマンドラインで実行
youtube_to_regza.bat
```

### 使用例

```bash
# コマンドライン使用例
uv run python youtube_to_regza.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 出力ファイル例
# 動画タイトル: Rick Astley - Never Gonna Give You Up
# 生成ファイル: Rick Astley - Never Gonna Give You Up.mp4
```

### バッチファイル使用例
```
========================================
   YouTube to REGZA Converter
========================================

Enter YouTube URL: https://youtu.be/wg0yAiMerhg?si=yHzf1JccVNFfMx7o
Processing: https://youtu.be/wg0yAiMerhg?si=yHzf1JccVNFfMx7o

[変換処理中...]

========================================
Conversion completed!
========================================

Press any key to exit...
```

## プロジェクト構成

```
youtube_to_regza/
├── main.py                 # テスト用メインスクリプト
├── youtube_to_regza.py     # メイン変換スクリプト
├── youtube_to_regza.bat    # Windowsバッチファイル
├── config.json            # ユーザー設定ファイル（自動生成）
├── config_sample.json     # サンプル設定ファイル
├── pyproject.toml         # プロジェクト設定
├── uv.lock               # 依存関係ロックファイル
├── log.md                # 開発ログ
└── README.md             # このファイル
```

## 設定ファイル

### 自動設定ファイル生成
初回実行時に`config_sample.json`から`config.json`が自動生成されます。

### 設定項目

```json
{
    "output_directory": "./output",           // 出力先ディレクトリ
    "temp_directory": "./temp",              // 一時ファイル保存先
    "video_settings": {
        "resolution": "640x480",             // 解像度
        "codec": "libx264",                  // 動画コーデック
        "profile": "baseline",               // H.264プロファイル
        "level": "3.1",                      // H.264レベル
        "framerate": "29.97",                // フレームレート
        "quality": "20",                     // 品質(CRF)
        "audio_codec": "copy"                // 音声コーデック
    },
    "advanced_settings": {
        "auto_cleanup": true,                // 自動クリーンアップ
        "overwrite_existing": true,          // 既存ファイル上書き
        "show_progress": true                // プログレス表示
    }
}
```

### 設定例

#### REGZA 40V30互換設定（推奨）
```json
{
    "output_directory": "自身で設定したディレクトリ",
    "temp_directory": "./temp",
    "video_settings": {
        "resolution": "640x480",
        "codec": "libx264",
        "profile": "baseline",
        "level": "3.1",
        "framerate": "29.97",
        "quality": "20",
        "audio_codec": "copy"
    },
    "advanced_settings": {
        "auto_cleanup": true,
        "overwrite_existing": true,
        "show_progress": true
    }
}
```

#### 高品質設定（新テレビ対応）
```json
{
    "video_settings": {
        "resolution": "1920x1080",
        "profile": "high",
        "level": "4.0"
    }
}
```

## トラブルシューティング

### よくある問題

#### 1. **ffmpegが見つからない**
```bash
# 確認方法
ffmpeg -version

# エラーメッセージ例
'ffmpeg' は、内部コマンドまたは外部コマンド、操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```
**解決方法**:
- [ffmpeg公式サイト](https://ffmpeg.org/download.html)からWindows版をダウンロード
- インストール後、PATH環境変数にffmpegのbinフォルダを追加
- または、ffmpeg.exeをプロジェクトフォルダに直接配置

#### 2. **動画のダウンロードに失敗**
```bash
# エラーメッセージ例
ERROR: [youtube] Video unavailable
```
**解決方法**:
- YouTube URLが正しいことを確認（共有リンクを使用）
- インターネット接続を確認
- 動画が公開設定であることを確認
- yt-dlpを最新版に更新: `uv sync`

#### 3. **変換に失敗**
```bash
# エラーメッセージ例
Error converting video: Command '['ffmpeg', ...]' returned non-zero exit status 1
```
**解決方法**:
- 入力動画が有効であることを確認
- 十分なディスク容量があることを確認（最低2GB推奨）
- 一時ファイルと出力先ディレクトリへの書き込み権限を確認
- 動画ファイルが破損していないことを確認

#### 4. **設定ファイル関連の問題**
```bash
# config.jsonが存在しない場合
Using default settings
```
**解決方法**:
- `config_sample.json`が存在することを確認
- 書き込み権限があることを確認
- 必要に応じて手動で`config.json`を作成

#### 5. **REGZAで再生できない**
**解決方法**:
- REGZA 40V30互換設定を使用していることを確認
- 解像度: 640x480, プロファイル: baseline, レベル: 3.1
- NASのDLNA共有フォルダに配置後、リスキャンを実行
- テレビのファームウェアが最新であることを確認

### 詳細なエラーログ確認
```bash
# 詳細ログを表示する場合
set PYTHONPATH=%PYTHONPATH%;.
uv run python youtube_to_regza.py <URL> 2>&1 | tee conversion.log
```

### サポート情報
問題が解決しない場合は、以下の情報を添えてIssueを作成してください：
- 使用したYouTube URL
- エラーメッセージ全文
- config.jsonの内容
- 使用環境（OS、Pythonバージョン、ffmpegバージョン）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグ報告や機能要望は、GitHubのIssuesページでお知らせください。

プルリクエストも歓迎します！

## 更新履歴

### v0.2.0 (2025-09-16)
- ✅ **設定ファイルシステム実装**
  - `config.json` / `config_sample.json` の導入
  - 自動設定ファイル生成機能
  - 柔軟な設定カスタマイズ
- ✅ **動画タイトル取得機能**
  - YouTube動画タイトルの自動取得
  - ファイル名自動生成（タイトルベース）
  - 特殊文字の自動置換
- ✅ **バッチファイル対応**
  - `youtube_to_regza.bat` の作成
  - ユーザーフレンドリーなGUIインターフェース
  - UTF-8エンコーディング対応
- ✅ **複数解像度対応**
  - REGZA 40V30互換設定（640x480）
  - 高品質設定（1920x1080）
- ✅ **REGZA互換性修正**
  - 古いREGZAでの再生問題を解決
  - Baseline Profile Level 3.1 設定の復元

### v0.1.0 (2025-09-12)
- ✅ **初回リリース**
  - YouTube動画ダウンロード機能（yt-dlp使用）
  - REGZA 40V30仕様変換機能（ffmpeg使用）
  - 基本的なエラーハンドリング
  - uv環境対応
  - Windowsバッチファイル対応

## 技術仕様

### 依存関係
- **Python**: 3.11+
- **yt-dlp**: 2025.9.5+ (YouTubeダウンロード)
- **ffmpeg**: 最新版 (動画変換)
- **uv**: 最新版 (パッケージ管理)

### システム要件
- **OS**: Windows 10/11, macOS, Linux
- **RAM**: 最低2GB（推奨4GB以上）
- **ストレージ**: 動画1本あたり最低2GBの空き容量
- **ネットワーク**: 安定したインターネット接続

### 処理フロー
1. **URL検証** → 2. **動画タイトル取得** → 3. **動画ダウンロード** → 4. **REGZA仕様変換** → 5. **クリーンアップ**

---

**📺 REGZA 40V30で快適に動画を楽しもう！**
