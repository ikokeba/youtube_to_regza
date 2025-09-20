import subprocess
import sys
import os
import json
import re
import time
from pathlib import Path
from tqdm import tqdm

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
        # yt-dlpの進捗表示を有効にしてダウンロード
        subprocess.run([
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", temp_output,
            "--progress",  # 進捗表示を有効化
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
    
    cmd.append(output_file)
    
    try:
        # tqdmを使用した進捗表示
        if advanced_settings.get("show_progress", True):
            print("Converting video... (This may take several minutes)")
            # ffmpegの進捗をパースしてtqdmで表示
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
            
            # 進捗バーを初期化
            pbar = tqdm(total=100, desc="Converting", unit="%")
            
            duration_seconds = None
            
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # ffmpegの進捗情報をパース
                    try:
                        # duration情報を探す
                        if "Duration:" in output:
                            duration_str = output.split("Duration: ")[1].split(",")[0]
                            # HH:MM:SS.mmm形式を秒に変換
                            time_parts = duration_str.split(":")
                            duration_seconds = float(time_parts[0]) * 3600 + float(time_parts[1]) * 60 + float(time_parts[2])
                            pbar.set_description(f"Converting (Duration: {duration_str})")
                        elif "time=" in output and duration_seconds:
                            time_str = output.split("time=")[1].split(" ")[0]
                            time_parts = time_str.split(":")
                            current_seconds = float(time_parts[0]) * 3600 + float(time_parts[1]) * 60 + float(time_parts[2])
                            progress = (current_seconds / duration_seconds) * 100
                            pbar.n = min(progress, 100)
                            pbar.refresh()
                    except (ValueError, IndexError):
                        pass
            
            pbar.close()
            
            # プロセスの終了を待つ
            return_code = process.wait()
            if return_code != 0:
                raise subprocess.CalledProcessError(return_code, cmd)
        else:
            subprocess.run(cmd, check=True)
        
        print(f"Converted to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting video: {e}")
        sys.exit(1)
    finally:
        if advanced_settings.get("auto_cleanup", True) and os.path.exists(input_file):
            try:
                # ファイルが使用中の場合、少し待ってから再試行
                import time
                for attempt in range(3):
                    try:
                        os.remove(input_file)
                        print(f"Cleaned up temporary file: {input_file}")
                        break
                    except PermissionError:
                        if attempt < 2:  # 最後の試行でない場合
                            time.sleep(1)  # 1秒待機
                        else:
                            print(f"Warning: Could not delete temporary file {input_file} (file may be in use)")
            except Exception as e:
                print(f"Warning: Error cleaning up temporary file {input_file}: {e}")

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
    
    # 同時実行対応: タイムスタンプとプロセスIDを含む一意なファイル名
    timestamp = int(time.time() * 1000)  # ミリ秒のタイムスタンプ
    process_id = os.getpid()
    temp_file = temp_dir / f"temp_video_{timestamp}_{process_id}.mp4"
    
    # 動画タイトルを取得してファイル名を生成
    print("Getting video title...")
    title = get_video_title(youtube_url)
    output_file = output_dir / f"{title}.mp4"
    print(f"Video title: {title}")
    print(f"Output file: {output_file}")

    # 既存の出力ファイルがあれば削除
    if config["advanced_settings"].get("overwrite_existing", True) and output_file.exists():
        try:
            # ファイルが使用中の場合、少し待ってから再試行
            for attempt in range(3):
                try:
                    output_file.unlink()
                    print(f"Removed existing file: {output_file}")
                    break
                except PermissionError:
                    if attempt < 2:  # 最後の試行でない場合
                        time.sleep(1)  # 1秒待機
                    else:
                        print(f"Warning: Could not remove existing file {output_file} (file may be in use)")
                        print("Continuing with conversion...")
        except Exception as e:
            print(f"Warning: Error removing existing file {output_file}: {e}")
            print("Continuing with conversion...")

    # 動画ダウンロード（進捗表示付き）
    print("Downloading video...")
    download_youtube_video(youtube_url, str(temp_file))

    # REGZA仕様に変換
    convert_to_regza_spec(str(temp_file), str(output_file), config)

    print(f"REGZA-compatible MP4 created: {output_file}")
    print("Place this file in your NAS DLNA shared folder and rescan.")

if __name__ == "__main__":
    main()