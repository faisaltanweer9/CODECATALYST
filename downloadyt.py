import os
import yt_dlp
import shutil


def check_ffmpeg():
    """
    Check if ffmpeg is installed and accessible.
    """
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not in PATH.")
        print("Visit https://ffmpeg.org/download.html to install it.")
        exit(1)


def check_yt_dlp():
    """
    Check if yt-dlp is installed.
    """
    try:
        import yt_dlp
    except ImportError:
        print("Error: yt-dlp is not installed.")
        print("Please install it using: pip install yt-dlp")
        exit(1)


def download_with_yt_dlp(link, folder_path, quality, audio_only):
    """
    Downloads a video or playlist using yt-dlp with quality selection.
    If audio_only is True, it downloads as MP3.
    """
    print(f"Starting download for: {link}")
    
    # Format options based on quality choice
    if audio_only:
        # For MP3 audio-only download
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
        format_option = "bestvideo[height<=144]+bestaudio/best[height<=144]"  # 144p quality option
        output_format = "mp4"
    else:
        print("Invalid quality choice. Defaulting to best quality.")
        format_option = "bestvideo+bestaudio/best"
        output_format = "mp4"

    # yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),  # Save video with title
        'format': format_option,  # Selected quality format
        'merge_output_format': output_format,  # Merge video and audio into the specified format
        'noplaylist': True,  # Download single video by default
        'progress_hooks': [lambda d: print(f"Downloading: {d['filename']} - {d['_percent_str']} complete")],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error downloading with yt-dlp: {e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Error: {e}\n")
        print("Error details saved in error_log.txt.")


def main():
    """
    Main function for YouTube video/playlist downloader with quality selection.
    """

    # Check if ffmpeg and yt-dlp are installed
    check_ffmpeg()
    check_yt_dlp()

    # Get folder path for downloads
    folder_path = input("Enter the folder path for downloads (default: current directory): ").strip()
    if not folder_path:
        folder_path = os.getcwd()

    # Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")

    # Get YouTube link
    link = input("Enter YouTube Video/Playlist Link: ").strip()
    if not link.startswith("http"):
        print("Error: Invalid URL. Please enter a valid YouTube link.")
        return

    # Quality selection
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

    # If MP3 is selected, set audio_only flag
    audio_only = True if quality == "5" else False

    # Start downloading
    download_with_yt_dlp(link, folder_path, quality, audio_only)

    # Notify the user that the download is complete
    print("\nAll downloads completed successfully! Check your folder.")

    
if __name__ == "__main__":
    main()
