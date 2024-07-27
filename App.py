import customtkinter
from pytube import YouTube
from tkinter import messagebox
import os
import threading

# Constantes
SUPPORTED_PLATFORMS = ["YouTube", "TikTok", "Instagram", "Facebook"]
SUPPORTED_FORMATS = ["MP4", "MP3", "WAV", "AVI"]
DEFAULT_RESOLUTIONS = ["8K", "4K", "1440P", "1080p", "720p"]

class DownloadManager:
    def __init__(self):
        self.platform = None
        self.link = None

    def set_platform(self, platform):
        self.platform = platform

    def set_link(self, link):
        self.link = link

    def download(self, formato, resolucao):
        if not self.link:
            raise ValueError("Link não pode ser vazio")
        if self.platform == "YouTube":
            self._download_youtube(formato, resolucao)
        # Adicione outros métodos de download de plataformas aqui

    def _download_youtube(self, formato, resolucao):
        try:
            yt = YouTube(self.link)
            if formato == "MP4":
                video = yt.streams.filter(res=resolucao, file_extension="mp4").first()
            elif formato == "MP3":
                video = yt.streams.filter(only_audio=True).first()

            if not video:
                raise ValueError("Não foi possível encontrar o formato/resolução selecionado!")

            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
            video.download(output_path=download_path)
        except Exception as e:
            raise e

# Funções de UI
def baixar_video():
    try:
        link = link_entry.get()
        if not link:
            raise ValueError("Insira um link válido!")

        download_manager.set_link(link)
        formato = archive_options.get()
        resolucao = video_options.get()
        download_manager.set_platform(platform_options.get())

        thread = threading.Thread(target=download_manager.download, args=(formato, resolucao))
        thread.start()

        messagebox.showinfo("Sucesso", "Download iniciado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def update_video_options(event=None):
    try:
        link = link_entry.get()
        if not link:
            raise ValueError("Insira um link válido!")
        
        download_manager.set_link(link)
        yt = YouTube(link)
        resolutions = list(set(stream.resolution for stream in yt.streams.filter(progressive=True) if stream.resolution))
        if resolutions:
            video_options.configure(values=resolutions)
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar resoluções disponíveis!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Inicializando o gerenciador de downloads
download_manager = DownloadManager()

# Configurações da UI
customtkinter.set_appearance_mode("Dark")
app = customtkinter.CTk()
app.title("Speed Up Downloader")
app.geometry("800x500")

# Layout da aplicação
titulo_label = customtkinter.CTkLabel(master=app, text="Speed Up Downloader", font=("Arial", 24, "bold"))
titulo_label.pack(pady=20)

link_entry = customtkinter.CTkEntry(master=app, placeholder_text="Insira o seu link...", width=694)
link_entry.pack(pady=10)
link_entry.bind("<Return>", update_video_options)

platform_options = customtkinter.CTkComboBox(master=app, values=SUPPORTED_PLATFORMS, fg_color="#3E3E3E")
platform_options.pack(pady=5, fill="x")

video_options = customtkinter.CTkComboBox(master=app, values=DEFAULT_RESOLUTIONS, fg_color="#3E3E3E")
video_options.pack(pady=5, fill="x")

archive_options = customtkinter.CTkComboBox(master=app, values=SUPPORTED_FORMATS, fg_color="#3E3E3E")
archive_options.pack(pady=5, fill="x")

btn_download = customtkinter.CTkButton(master=app, text="Download", corner_radius=30, bg_color="transparent", fg_color="#006C38", hover_color="#004A27", command=baixar_video)
btn_download.pack(pady=15)

copyright_label = customtkinter.CTkLabel(master=app, text="Desenvolvido Por Matheus Assunção", font=("Arial", 15, "normal"))
copyright_label.pack(pady=10, padx=150)

app.mainloop()
