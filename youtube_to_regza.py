import subprocess
import sys
import os
import json
import re
from pathlib import Path

def load_config():
    """設定ファイルを読み込み"""
    config_file = Path("config.json")
    sample_config_file = Path("config_sample.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"Loaded config from {config_file}")
            return config
        except json.JSONDecodeError as e:
            print(f"Error parsing config.json: {e}")
            print("Using default settings...")
    elif sample_config_file.exists():
        print(f"config.json not found. Copying from {sample_config_file}")
        try:
            with open(sample_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            print(f"Created config.json from sample")
            return config
        except Exception as e:
            print(f"Error creating config.json: {e}")
    
    # デフォルト設定
    default_config = {
        "output_directory": "./",
        "temp_directory": "./",
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
            "auto_cleanup": True,
            "overwrite_existing": True,
            "show_progress": True
        }
    }
    print("Using default settings")
    return default_config

def get_video_title(url):
    """YouTube動画のタイトルを取得"""
    try:
        result = subprocess.run([
            "yt-dlp",
            "--print", "title",
            url
        ], capture_output=True, text=True, check=True)
        title = result.stdout.strip()
        # ファイル名に使用できない文字を置換
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        # 長すぎる場合は切り詰め
        if len(title) > 100:
            title = title[:100]
        return title
    except subprocess.CalledProcessError as e:
        print(f"Error getting video title: {e}")
        return "unknown_video"

def download_youtube_video(url, temp_output="temp_video.mp4"):
    """YouTube動画を最高品質のMP4でダウンロード"""
    try:
        subprocess.run([
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", temp_output,
            url
        ], check=True)
        print(f"Downloaded video to {temp_output}")
        return temp_output
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)

def convert_to_regza_spec(input_file, output_file, config):
    """REGZA 40V30仕様に変換"""
    video_settings = config["video_settings"]
    advanced_settings = config["advanced_settings"]
    
    # 出力ディレクトリを作成
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 解像度を解析
    resolution = video_settings["resolution"]
    width, height = resolution.split('x')
    
    # ffmpegコマンドを構築
    cmd = [
        "ffmpeg", "-i", input_file,
        "-c:v", video_settings["codec"],
        "-profile:v", video_settings["profile"],
        "-level:v", video_settings["level"],
        "-r", video_settings["framerate"],
        "-x264opts", "cabac=0:ref=1",
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        "-pix_fmt", "yuv420p",
        "-crf", video_settings["quality"],
        "-c:a", video_settings["audio_codec"]
    ]
    
    # プログレス表示設定
    if advanced_settings.get("show_progress", True):
        cmd.extend(["-progress", "pipe:1"])
    
    cmd.append(output_file)
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Converted to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting video: {e}")
        sys.exit(1)
    finally:
        if advanced_settings.get("auto_cleanup", True) and os.path.exists(input_file):
            os.remove(input_file)
            print(f"Cleaned up temporary file: {input_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python youtube_to_regza.py <YouTube_URL>")
        sys.exit(1)

    # 設定ファイルを読み込み
    config = load_config()
    
    youtube_url = sys.argv[1]
    temp_dir = Path(config["temp_directory"])
    output_dir = Path(config["output_directory"])
    
    # ディレクトリを作成
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_file = temp_dir / "temp_video.mp4"
    
    # 動画タイトルを取得してファイル名を生成
    print("Getting video title...")
    title = get_video_title(youtube_url)
    output_file = output_dir / f"{title}.mp4"
    print(f"Video title: {title}")
    print(f"Output file: {output_file}")

    # 既存の出力ファイルがあれば削除
    if config["advanced_settings"].get("overwrite_existing", True) and output_file.exists():
        output_file.unlink()
        print(f"Removed existing file: {output_file}")

    # 動画ダウンロード
    download_youtube_video(youtube_url, str(temp_file))

    # REGZA仕様に変換
    convert_to_regza_spec(str(temp_file), str(output_file), config)

    print(f"REGZA-compatible MP4 created: {output_file}")
    print("Place this file in your QNAP NAS DLNA shared folder and rescan.")

if __name__ == "__main__":
    main()