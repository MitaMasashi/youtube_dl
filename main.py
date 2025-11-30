import customtkinter as ctk
import threading
from downloader import Downloader
import tkinter

ctk.set_appearance_mode("Dark") # Use dark mode for better contrast with gold
ctk.set_default_color_theme("green") # Base theme, but we will override

# Color Palette
DEEP_GREEN = "#1A4D2E"
BRIGHT_GOLD = "#FFD700"
TEXT_COLOR = "#FFFFFF"
HOVER_GOLD = "#E6C200"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("600x450")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Set window background color
        self.configure(fg_color=DEEP_GREEN)

        self.downloader = Downloader()

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent") # Transparent to show window bg
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.label_title = ctk.CTkLabel(
            self.main_frame, 
            text="YouTube Downloader", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=BRIGHT_GOLD
        )
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 20))

        self.entry_url = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Paste YouTube URL here",
            border_color=BRIGHT_GOLD,
            fg_color="#2C5F3F", # Slightly lighter green for input
            text_color=BRIGHT_GOLD,
            placeholder_text_color="#A0C0A0"
        )
        self.entry_url.grid(row=1, column=0, padx=20, pady=15, sticky="ew")

        self.option_type = ctk.CTkOptionMenu(
            self.main_frame, 
            values=["Video", "Audio (MP3)"],
            fg_color=BRIGHT_GOLD,
            button_color=HOVER_GOLD,
            button_hover_color=BRIGHT_GOLD,
            text_color=DEEP_GREEN,
            dropdown_fg_color=DEEP_GREEN,
            dropdown_text_color=BRIGHT_GOLD,
            dropdown_hover_color="#2C5F3F"
        )
        self.option_type.grid(row=2, column=0, padx=20, pady=15)

        self.button_download = ctk.CTkButton(
            self.main_frame, 
            text="Download", 
            command=self.start_download_thread,
            fg_color=BRIGHT_GOLD,
            text_color=DEEP_GREEN,
            hover_color=HOVER_GOLD,
            font=ctk.CTkFont(weight="bold")
        )
        self.button_download.grid(row=3, column=0, padx=20, pady=20)

        self.label_status = ctk.CTkLabel(self.main_frame, text="", text_color=BRIGHT_GOLD)
        self.label_status.grid(row=4, column=0, padx=20, pady=10)

        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            progress_color=BRIGHT_GOLD,
            border_color=BRIGHT_GOLD
        )
        self.progress_bar.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

    def start_download_thread(self):
        url = self.entry_url.get()
        if not url:
            self.label_status.configure(text="Please enter a URL", text_color="#FF5555")
            return

        self.button_download.configure(state="disabled")
        self.label_status.configure(text="Downloading...", text_color=BRIGHT_GOLD)
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
            
            self.after(0, lambda: self.label_status.configure(text="Download Completed!", text_color=BRIGHT_GOLD))
        except Exception as e:
            error_message = str(e)
            self.after(0, lambda: self.label_status.configure(text=f"Error: {error_message}", text_color="#FF5555"))
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
