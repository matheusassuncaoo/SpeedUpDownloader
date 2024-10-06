import customtkinter
from pytube import YouTube
from tkinter import messagebox
import os
import threading
import time

# Constantes
SUPPORTED_PLATFORMS = ["YouTube", "TikTok", "Instagram"]
SUPPORTED_FORMATS = ["MP4", "MP3"]
DEFAULT_RESOLUTIONS = ["8K", "4K", "1440P", "1080p", "720p"]

# Classe de gerenciamento de downloads
class DownloadManager:
    def __init__(self):
        self.platform = None
        self.link = None

    def set_platform(self, platform):
        self.platform = platform

    def set_link(self, link):
        self.link = link

    def download(self, formato, resolucao, progress_callback=None):
        if not self.link:
            raise ValueError("Link não pode ser vazio")
        if self.platform == "YouTube":
            self._download_youtube(formato, resolucao, progress_callback)
        elif self.platform == "Instagram":
            self._download_instagram(formato, progress_callback)
        elif self.platform == "TikTok":
            self._download_tiktok(formato, progress_callback)
        else:
            raise ValueError(f"Plataforma {self.platform} não suportada no momento.")

    def _download_youtube(self, formato, resolucao, progress_callback):
        try:
            yt = YouTube(self.link, on_progress_callback=progress_callback)
            if formato == "MP4":
                video = yt.streams.filter(res=resolucao, file_extension="mp4").first()
            elif formato == "MP3":
                video = yt.streams.filter(only_audio=True).first()

            if not video:
                raise ValueError("Não foi possível encontrar o formato/resolução selecionado!")
            
            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
            video.download(output_path=download_path)

            messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
        except Exception as e:
            raise ValueError(f"Erro ao baixar o vídeo: {str(e)}")

    def _download_instagram(self, formato, progress_callback):
        # Placeholder para o download do Instagram
        raise NotImplementedError("Download do Instagram ainda não implementado")

    def _download_tiktok(self, formato, progress_callback):
        # Placeholder para o download do TikTok
        raise NotImplementedError("Download do TikTok ainda não implementado")

# Funções de UI
def baixar_video():
    try:
        link = link_entry.get()
        if not link:
            raise ValueError("Insira um link válido!")

        btn_download.configure(state="disabled")  # Desativa o botão durante o download

        download_manager.set_link(link)
        formato = archive_options.get()
        resolucao = video_options.get()
        download_manager.set_platform(platform_options.get())

        # Inicia o download em uma nova thread
        thread = threading.Thread(target=download_manager.download, args=(formato, resolucao, on_download_progress))
        thread.start()

        messagebox.showinfo("Sucesso", "Download iniciado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        btn_download.configure(state="normal")  # Reativa o botão após o download

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

def on_download_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_var.set(f"Progresso: {percentage_of_completion:.2f}%")
    app.update_idletasks()

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

# Barra de progresso
progress_var = customtkinter.StringVar()
progress_label = customtkinter.CTkLabel(master=app, textvariable=progress_var, font=("Arial", 12, "normal"))
progress_label.pack(pady=10)

copyright_label = customtkinter.CTkLabel(master=app, text="Desenvolvido Por Matheus Assunção", font=("Arial", 15, "normal"))
copyright_label.pack(pady=10, padx=150)

app.mainloop()
