import os
import yt_dlp
import shutil
from tqdm import tqdm
import re

# Features of the Script:
# Video and Playlist Downloading
# Quality Options
# Duplicate Check
# Progress Bar Integration
# Folder Management
# Space Usage Calculation
# Error Logging

def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not in PATH.")
        print("Visit https://ffmpeg.org/download.html to install it.")
        exit(1)


def check_yt_dlp():
    try:
        import yt_dlp
    except ImportError:
        print("Error: yt-dlp is not installed.")
        print("Please install it using: pip install yt-dlp")
        exit(1)


def calculate_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
    size_in_mb = total_size / (1024 * 1024)
    size_in_gb = total_size / (1024 * 1024 * 1024)
    return total_size, size_in_mb, size_in_gb


def download_with_yt_dlp(link, folder_path, quality, audio_only, existing_files):
    print(f"Starting download for: {link}")

    if audio_only:
        format_option = "bestaudio/best"
        output_format = "mp3"
    elif quality == "1":
        format_option = "bestvideo+bestaudio/best"
        output_format = "mp4"
    elif quality == "2":
        format_option = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        output_format = "mp4"
    elif quality == "3":
        format_option = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        output_format = "mp4"
    elif quality == "4":
        format_option = "bestvideo[height<=144]+bestaudio/best[height<=144]"
        output_format = "mp4"
    else:
        print("Invalid quality choice. Defaulting to best quality.")
        format_option = "bestvideo+bestaudio/best"
        output_format = "mp4"

    ydl_opts = {
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
        'format': format_option,
        'merge_output_format': output_format,
        'noplaylist': False,
    }

    with tqdm(total=100, desc="Downloading", unit="%", dynamic_ncols=True) as pbar:
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0.0%')
                percent_clean = re.sub(r'\x1b\[[0-9;]*m', '', percent_str)
                try:
                    progress = float(percent_clean.strip('%'))
                    pbar.n = progress
                    pbar.refresh()
                except ValueError:
                    print(f"Error parsing progress: {percent_str}")

        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            print("\nDownload completed successfully!")
        except Exception as e:
            print(f"Error downloading with yt-dlp: {e}")
            with open("error_log.txt", "a") as log_file:
                log_file.write(f"Error: {e}\n")
            print("Error details saved in error_log.txt.")


def main():
    check_ffmpeg()
    check_yt_dlp()

    folder_path = input("Enter the folder path for downloads (default: current directory): ").strip()
    if not folder_path:
        folder_path = os.getcwd()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")

    existing_files = set(os.listdir(folder_path))

    link = input("Enter YouTube Video/Playlist Link: ").strip()
    if not link.startswith("http"):
        print("Error: Invalid URL. Please enter a valid YouTube link.")
        return

    print("\nSelect Video Quality:")
    print("1. Best Quality (default)")
    print("2. 720p (HD)")
    print("3. 480p (SD)")
    print("4. 144p (Lowest quality)")
    print("5. MP3 (Audio only)")
    quality = input("Enter your choice (1/2/3/4/5): ").strip()

    while quality not in ["1", "2", "3", "4", "5"]:
        print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        quality = input("Enter your choice (1/2/3/4/5): ").strip()

    audio_only = True if quality == "5" else False

    download_with_yt_dlp(link, folder_path, quality, audio_only, existing_files)

    total_size, size_in_mb, size_in_gb = calculate_folder_size(folder_path)
    print(f"\nTotal space used by downloaded videos:")
    print(f" - {total_size} bytes")
    print(f" - {size_in_mb:.2f} MB")
    print(f" - {size_in_gb:.2f} GB")

    print("\nAll downloads completed successfully! Check your folder.")


if __name__ == "__main__":
    main()

