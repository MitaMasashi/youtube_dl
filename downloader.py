import yt_dlp
import os
import imageio_ffmpeg

class Downloader:
    def __init__(self, download_folder="downloads"):
        self.download_folder = download_folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    def download_video(self, url, progress_hook=None):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'nocolor': True,
            'ffmpeg_location': self.ffmpeg_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_audio(self, url, progress_hook=None):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'nocolor': True,
            'ffmpeg_location': self.ffmpeg_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def get_info(self, url):
        with yt_dlp.YoutubeDL() as ydl:
            return ydl.extract_info(url, download=False)
