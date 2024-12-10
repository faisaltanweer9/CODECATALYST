import os
import yt_dlp
import shutil


def check_ffmpeg():
    """
    Check if ffmpeg is installed and accessible.
    """
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not in PATH.")
        print("Please install ffmpeg and try again.")
        exit(1)


def download_with_yt_dlp(link, folder_path, quality):
    """
    Downloads a video or playlist using yt-dlp with quality selection.
    """
    print(f"Starting download for: {link}")
    

    if quality == "1":
        format_option = "bestvideo+bestaudio/best"
    elif quality == "2":
        format_option = "bestvideo[height<=720]+bestaudio/best[height<=720]"  
    elif quality == "3":
        format_option = "bestvideo[height<=480]+bestaudio/best[height<=480]" 
    else:
        print("Invalid quality choice. Defaulting to best quality.")
        format_option = "bestvideo+bestaudio/best"

    ydl_opts = {
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'), 
        'format': format_option,
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error downloading with yt-dlp: {e}")


def main():
    """
    Main function for YouTube video/playlist downloader with quality selection.
    """

    check_ffmpeg()


    folder_path = input("Enter the folder path for downloads (default: current directory): ").strip()
    if not folder_path:
        folder_path = os.getcwd()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")


    link = input("Enter YouTube Video/Playlist Link: ").strip()
    if not link.startswith("http"):
        print("Error: Invalid URL. Please enter a valid YouTube link.")
        return


    print("\nSelect Video Quality:")
    print("1. Best Quality (default)")
    print("2. 720p (HD)")
    print("3. 480p (SD)")
    quality = input("Enter your choice (1/2/3): ").strip()

    download_with_yt_dlp(link, folder_path, quality)


if __name__ == "__main__":
    main()
