import customtkinter as ctk
import threading
from downloader import Downloader
import tkinter

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.downloader = Downloader()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.label_title = ctk.CTkLabel(self.main_frame, text="YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.entry_url = ctk.CTkEntry(self.main_frame, placeholder_text="Paste YouTube URL here")
        self.entry_url.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.option_type = ctk.CTkOptionMenu(self.main_frame, values=["Video", "Audio (MP3)"])
        self.option_type.grid(row=2, column=0, padx=20, pady=10)

        self.button_download = ctk.CTkButton(self.main_frame, text="Download", command=self.start_download_thread)
        self.button_download.grid(row=3, column=0, padx=20, pady=20)

        self.label_status = ctk.CTkLabel(self.main_frame, text="")
        self.label_status.grid(row=4, column=0, padx=20, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

    def start_download_thread(self):
        url = self.entry_url.get()
        if not url:
            self.label_status.configure(text="Please enter a URL", text_color="red")
            return

        self.button_download.configure(state="disabled")
        self.label_status.configure(text="Downloading...", text_color="white")
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self.download, args=(url,))
        thread.start()

    def download(self, url):
        download_type = self.option_type.get()
        try:
            if download_type == "Video":
                self.downloader.download_video(url, self.progress_hook)
            else:
                self.downloader.download_audio(url, self.progress_hook)
            
            self.after(0, lambda: self.label_status.configure(text="Download Completed!", text_color="green"))
        except Exception as e:
            error_message = str(e)
            self.after(0, lambda: self.label_status.configure(text=f"Error: {error_message}", text_color="red"))
        finally:
            self.after(0, lambda: self.button_download.configure(state="normal"))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%', '').strip()
                # Remove ANSI escape codes if any remain (though nocolor should fix it)
                import re
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                p = ansi_escape.sub('', p)
                
                self.after(0, lambda: self.progress_bar.set(float(p) / 100))
                self.after(0, lambda: self.label_status.configure(text=f"Downloading: {d.get('_percent_str', '').strip()}"))
            except Exception as e:
                print(f"Progress Error: {e}")
                pass
        elif d['status'] == 'finished':
             self.after(0, lambda: self.progress_bar.set(1))
             self.after(0, lambda: self.label_status.configure(text="Processing..."))

if __name__ == "__main__":
    app = App()
    app.mainloop()
