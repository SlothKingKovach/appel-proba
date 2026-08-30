import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from yt_dlp import YoutubeDL

def get_app_folder():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS

    return os.path.dirname(
        os.path.abspath(__file__)
    )


APP_FOLDER = get_app_folder()

FFMPEG_PATH = os.path.join(
    APP_FOLDER,
    "ffmpeg.exe"
)
    
class VideoDownloaderApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Gramhoe / Tnjitter / Tiketoke skidavač")
        self.root.geometry("650x400")
        self.root.resizable(False, False)

        self.download_folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        self.url_var = tk.StringVar()

        self.folder_var = tk.StringVar(
            value=self.download_folder
        )

        self.status_var = tk.StringVar(
            value="Zapeto ki puška"
        )

        self.quality_var = tk.StringVar(
            value="Imdabes"
        )

        self.create_widgets()


    def create_widgets(self):

        main = ttk.Frame(
            self.root,
            padding=20
        )

        main.pack(
            fill="both",
            expand=True
        )


        # -------------------------
        # LINK
        # -------------------------

        ttk.Label(
            main,
            text="Linak"
        ).pack(anchor="w")

        self.url_entry = ttk.Entry(
            main,
            textvariable=self.url_var
        )

        self.url_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        # -------------------------
        # FOLDER
        # -------------------------

        ttk.Label(
            main,
            text="Di ćeš ga"
        ).pack(anchor="w")

        folder_frame = ttk.Frame(main)

        folder_frame.pack(
            fill="x",
            pady=(5, 15)
        )

        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            state="readonly"
        )

        self.folder_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            folder_frame,
            text="Di ćeš ga",
            command=self.choose_folder
        ).pack(
            side="left",
            padx=(10, 0)
        )


        # -------------------------
        # KVALITET
        # -------------------------

        ttk.Label(
            main,
            text="Quality"
        ).pack(anchor="w")

        self.quality_combo = ttk.Combobox(
            main,
            textvariable=self.quality_var,
            state="readonly",
            values=[
                "Imdabes",
                "1080p",
                "720p",
                "480p",
                "360p"
            ]
        )

        self.quality_combo.pack(
            fill="x",
            pady=(5, 15)
        )


        # -------------------------
        # PROGRESS BAR
        # -------------------------

        ttk.Label(
            main,
            text="Linija mrdanja"
        ).pack(anchor="w")

        self.progress = ttk.Progressbar(
            main,
            mode="determinate",
            maximum=100
        )

        self.progress.pack(
            fill="x",
            pady=(5, 5)
        )

        self.percent_label = ttk.Label(
            main,
            text="0%"
        )

        self.percent_label.pack(
            anchor="e"
        )


        # -------------------------
        # STATUS
        # -------------------------

        self.status_label = ttk.Label(
            main,
            textvariable=self.status_var
        )

        self.status_label.pack(
            anchor="w",
            pady=(10, 10)
        )


        # -------------------------
        # DOWNLOAD BUTTON
        # -------------------------

        self.download_button = ttk.Button(
            main,
            text="Duzni",
            command=self.start_download
        )

        self.download_button.pack(
            fill="x",
            ipady=5
        )


        # Fokus automatski na polje za link

        self.url_entry.focus()


    # -------------------------
    # IZBOR FOLDERA
    # -------------------------

    def choose_folder(self):

        folder = filedialog.askdirectory(
            initialdir=self.folder_var.get()
        )

        if folder:
            self.folder_var.set(folder)


    # -------------------------
    # POCETAK DOWNLOADA
    # -------------------------

    def start_download(self):

        url = self.url_var.get().strip()

        if not url:

            messagebox.showwarning(
                "Kurac skidaš prazno",
                "Meti linak majmune"
            )

            return


        self.progress["value"] = 0

        self.percent_label.config(
            text="0%"
        )

        self.status_var.set(
            "Idemo ludilo..."
        )

        self.download_button.config(
            state="disabled"
        )


        thread = threading.Thread(
            target=self.download_video,
            args=(url,),
            daemon=True
        )

        thread.start()


    # -------------------------
    # PROGRESS
    # -------------------------

    def update_progress(self, data):

        if data["status"] == "downloading":

            total = (
                data.get("total_bytes")
                or data.get(
                    "total_bytes_estimate"
                )
            )

            downloaded = data.get(
                "downloaded_bytes",
                0
            )


            if total:

                percent = (
                    downloaded / total * 100
                )

                self.root.after(
                    0,
                    lambda: self.set_progress(
                        percent
                    )
                )


            speed = data.get(
                "_speed_str",
                ""
            )

            eta = data.get(
                "_eta_str",
                ""
            )


            status_text = (
                f"Preuzimanje... {speed}"
            )


            if eta:

                status_text += (
                    f" | Saće: {eta}"
                )


            self.root.after(
                0,
                lambda: self.status_var.set(
                    status_text
                )
            )


        elif data["status"] == "finished":

            self.root.after(
                0,
                lambda: self.status_var.set(
                    "Procesuiramo uopaaa..."
                )
            )


    # -------------------------
    # POSTAVLJANJE PROCENTA
    # -------------------------

    def set_progress(
        self,
        percent
    ):

        self.progress["value"] = percent

        self.percent_label.config(
            text=f"{percent:.1f}%"
        )


    # -------------------------
    # DOWNLOAD
    # -------------------------

    def download_video(
        self,
        url
    ):

        try:

            os.makedirs(
                self.folder_var.get(),
                exist_ok=True
            )


            # -------------------------
            # IZBOR KVALITETA
            # -------------------------

            quality = (
                self.quality_var.get()
            )


            if quality == "Imdabes":

                video_format = (
                    "bestvideo+bestaudio/best"
                )

            else:

                height = quality.replace(
                    "p",
                    ""
                )


                video_format = (
                    f"bestvideo[height<={height}]"
                    f"+bestaudio/"
                    f"best[height<={height}]"
                )


            # -------------------------
            # YT-DLP OPTIONS
            # -------------------------

            options = {

                "format": video_format,


                "outtmpl": os.path.join(
                    self.folder_var.get(),
                    "%(title)s.%(ext)s"
                ),


                "merge_output_format": "mp4",

                "ffmpeg_location": FFMPEG_PATH,

                "noplaylist": True,


                "progress_hooks": [
                    self.update_progress
                ],


                "quiet": True,


                "no_warnings": True,

            }


            # -------------------------
            # POKRETANJE DOWNLOADA
            # -------------------------

            with YoutubeDL(
                options
            ) as ydl:


                info = ydl.extract_info(
                    url,
                    download=True
                )


                title = info.get(
                    "title",
                    "Video"
                )


            # -------------------------
            # GOTOVO
            # -------------------------

            self.root.after(
                0,
                lambda: self.download_finished(
                    title
                )
            )


        except Exception as e:


            error_message = str(e)


            self.root.after(
                0,
                lambda: self.download_error(
                    error_message
                )
            )


    # -------------------------
    # USPESAN DOWNLOAD
    # -------------------------

    def download_finished(
        self,
        title
    ):

        self.progress["value"] = 100

        self.percent_label.config(
            text="100%"
        )


        self.status_var.set(
            "Na!"
        )


        self.download_button.config(
            state="normal"
        )


        messagebox.showinfo(
            "Eto ga",
            f"Braomajstore!\n\n{title}"
        )


    # -------------------------
    # GRESKA
    # -------------------------

    def download_error(
        self,
        error
    ):

        self.status_var.set(
            "Ne mere"
        )


        self.download_button.config(
            state="normal"
        )


        messagebox.showerror(
            "Prc!",
            f"Ne mere jer jebiga.\n\n{error}"
        )


# -------------------------
# POKRETANJE PROGRAMA
# -------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = VideoDownloaderApp(
        root
    )

    root.mainloop()