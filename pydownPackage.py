from pytube import YouTube
from pytube import Playlist
from tkinter import filedialog
from pytube.cli import on_progress

class Playlist():
    def __init__(self, url):
        self.path = filedialog.askdirectory()
        self.url = url
        self.p = Playlist(url)

    def download(self):
        for video in self.p.videos:
            print("-----------------------------------------------")
            print("                   LETÖLTÉS                    ")
            print("\nADATOK:")
            print("URL: ", video.watch_url)
            print("A videó neve: ", video.title)
            print("Feltöltő: ", video.author)
            print("Feltöltés dátuma: ", video.publish_date)
            print("Megtekintések száma: ", video.views)
            print("feltöltő csatornájának URL-je: ", video.channel_url)

            print("\nLETÖLTÉS: ")
            try:
                yd = video.streams.get_highest_resolution()
                yd.download(path)
            except:
                print("Sikertelen letöltés.")
            print("-----------------------------------------------\n")

class Video():
    def __init__(self, url):
        self.url = url
        self.path = filedialog.askdirectory()
        self.yt = YouTube(self.url, on_progress_callback=on_progress)

    def download(self):
        print("-----------------------------------------------")
        print("                   LETÖLTÉS                    ")
        print("\nADATOK:")
        print("URL: ", self.yt.watch_url)
        print("A videó neve: ", self.yt.title)
        print("Feltöltő: ", self.yt.author)
        print("Feltöltés dátuma: ", self.yt.publish_date)
        print("Megtekintések száma: ", self.yt.views)
        print("feltöltő csatornájának URL-je: ", self.yt.channel_url)

        self.yd = self.yt.streams.get_highest_resolution()
        self.yd.download(self.path)

p = Playlist('https://www.youtube.com/playlist?list=PLK6G4JP74vhGW6uJKPMw6nKTQYz9rLkhi')
p.download()