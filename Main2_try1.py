# importing required libraries
import os
import sys
import threading
from pathlib import Path

import validators
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineSettings, QWebEngineDownloadItem, QWebEngineScript, QWebEngineScriptCollection, QWebEngineHistory
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtTextToSpeech import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence
from pytube import YouTube
from tkinter import filedialog
from tkinter import *

# Download
import requests
import shutil

# Notifications
from winotify import Notification, audio

path = str(Path(__file__).parent / "icon.png")

def send_notification(title, message):
    toast = Notification(
        app_id = "Cat Surf",
        title=title,
        msg=message,
        duration="long",
        icon=path)
    toast.set_audio(audio.Default, loop=False)
    toast.show()

#Geek
# main window
class CustomWebEnginePage(QWebEnginePage):
    external_windows = []

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            w = QWebEngineView()
            w.setUrl(url)
            w.show()

            self.external_windows.append(w)
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

class MainWindow(QMainWindow):
 
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        self.setWindowTitle("Cat Surf V2")
        self.setWindowIcon(QIcon("./pics/icon.png"))
        self.setGeometry(200,200, 1400,800)
        self.showMaximized()

        self.browser = QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self))

        self.browser.page().fullScreenRequested.connect(self.FullscreenRequest)
        self.browser.page().profile().downloadRequested.connect(self.on_downloadRequested)

        # creating a tab widget
        self.tabs = QTabWidget()
 
        # making document mode true
        self.tabs.setDocumentMode(True)
 
        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)
 
        # making tabs closeable 
        self.tabs.setTabsClosable(True)
 
        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
 
        # making tabs as central widget
        self.setCentralWidget(self.tabs)
 
        # creating a status bar
        self.status = QStatusBar()
 
        # setting status bar to the main window
        self.setStatusBar(self.status)
 
        # creating a tool bar for navigation
        navtb = QToolBar("Navigation")
        navtb.setMovable(False)
        
        # adding tool bar tot he main window
        self.addToolBar(navtb)
 
        # creating back action
        path = str(Path(__file__).parent / "back.png")
        back_btn = QAction(QIcon(path), "Vissza", self)
 
        # setting status tip
        back_btn.setStatusTip("Visszal??p??s az el??z?? oldalra")
 
        # adding action to back button
        # making current tab to go back
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
 
        # adding this to the navigation tool bar
        navtb.addAction(back_btn)
 
        # similarly adding next button
        path = str(Path(__file__).parent / "forward.png")
        next_btn = QAction(QIcon(path), "El??re", self)
        next_btn.setStatusTip("A k??vetkez?? oldalra l??p??s ->")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
 
        # similarly adding reload button
        path = str(Path(__file__).parent / "reload3.png")
        reload_btn = QAction(QIcon(path), "??jrat??lt??s", self)
        reload_btn.setStatusTip("Az oldal ??jrat??lt??se")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
 
        # creating home action
        path = str(Path(__file__).parent / "home3.png")
        home_btn = QAction(QIcon(path), "F??oldal", self)
        home_btn.setStatusTip("Ugr??s a f??oldalra")
 
        # adding action to home button
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # Vide?? let??lt??se

        # adding a separator
        navtb.addSeparator()
 
        # creating a line edit widget for URL
        self.urlbar = QLineEdit()
 
        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 
        # adding line edit to tool bar
        navtb.addWidget(self.urlbar)

        more_opt = QAction("Be??ll??t??sok", self)
        more_opt.setStatusTip("B??ng??sz?? be??ll??t??sok")

        more_opt.triggered.connect(self.settings)
        navtb.addAction(more_opt)
 
        downloadV = QAction("Vide?? let??lt??se", self)
        downloadV.triggered.connect(self.download_video_thread)
        downloadV.setStatusTip('Ezzel a funkci??val let??lthetsz vide??kat a YouTube-r??l, Shortcut: Ctrl + Shift + V')

        self.download_video_shortcut = QShortcut(QKeySequence('Ctrl+Shift+V'), self)
        self.download_video_shortcut.activated.connect(self.download_video_thread)

        extBtn = QPushButton("B??v??tm??nyek")

        navtb.addWidget(extBtn)

        menu = QMenu()
        menu.addAction(downloadV)
        extBtn.setMenu(menu)

        menu.triggered.connect(lambda action: print("A vide??t a b??ng??sz?? a PyDown API seg??ts??g??vel t??lt??tte le a YouTuber??l.\n Copyright (c) 2022. All rights reserved TheSpaceknight"))

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Le??ll??tja az oldal friss??t??s??t")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
 
        # creating first tab
        self.add_new_tab(QUrl('https://foxresearch.hu/catsurf/index.html'), '??j oldal')
 
        # showing all the components
        self.show()
 
        # setting window title
        self.setWindowTitle("Cat Surf V2")

        self.tabs.setDocumentMode(True)

        # F??gg??leges links??v
        linkbar = self.addToolBar("Linkbar")
        linkbar.setOrientation(QtCore.Qt.Vertical)
        linkbar.setMovable(False)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, linkbar)

        path = str(Path(__file__).parent / "google.png")
        google_link = QAction(QIcon(path), "Google", self)
        google_link.triggered.connect(self.Open_google)
        linkbar.addAction(google_link)

        path = str(Path(__file__).parent / "youtube.png")
        youtube_link = QAction(QIcon(path), "YouTube", self)
        youtube_link.triggered.connect(self.Open_youtube)
        linkbar.addAction(youtube_link)

        path = str(Path(__file__).parent / "netflix.png")
        netflix_link = QAction(QIcon(path), "Netflix", self)
        netflix_link.triggered.connect(self.Open_netflix)
        linkbar.addAction(netflix_link)

        path = str(Path(__file__).parent / "facebook.png")
        facebook_link = QAction(QIcon(path), "Facebook", self)
        facebook_link.triggered.connect(self.Open_facebook)
        linkbar.addAction(facebook_link)

        path = str(Path(__file__).parent / "wikipedia.png")
        wiki_link = QAction(QIcon(path), "Wikip??dia", self)
        wiki_link.triggered.connect(self.Open_wikipedia)
        linkbar.addAction(wiki_link)

        path = str(Path(__file__).parent / "gmail.png")
        gmail_link = QAction(QIcon(path), "Gmail", self)
        gmail_link.triggered.connect(self.Open_gmail)
        linkbar.addAction(gmail_link)

        path = str(Path(__file__).parent / "google_maps.png")
        google_maps_link = QAction(QIcon(path), "Google Maps", self)
        google_maps_link.triggered.connect(self.Open_googlemaps)
        linkbar.addAction(google_maps_link)

        path = str(Path(__file__).parent / "twitter.png")
        twitter_link = QAction(QIcon(path), "Twitter", self)
        twitter_link.triggered.connect(self.Open_twitter)
        linkbar.addAction(twitter_link)

        path = str(Path(__file__).parent / "apple.png")
        apple_link = QAction(QIcon(path), "Apple", self)
        apple_link.triggered.connect(self.Open_apple)
        linkbar.addAction(apple_link)

        path = str(Path(__file__).parent / "stackoverflow.png")
        stacko_link = QAction(QIcon(path), "Stackoverflow", self)
        stacko_link.triggered.connect(self.Open_stackoverflow)
        linkbar.addAction(stacko_link)

        path = str(Path(__file__).parent / "github.png")
        github_link = QAction(QIcon(path), "Github", self)
        github_link.triggered.connect(self.Open_github)
        linkbar.addAction(github_link)

        path = str(Path(__file__).parent / "outlook.png")
        outlook_link = QAction(QIcon(path), "Outlook", self)
        outlook_link.triggered.connect(self.Open_outlook)
        linkbar.addAction(outlook_link)

        path = str(Path(__file__).parent / "onedrive.png")
        onedrive_link = QAction(QIcon(path), "Onedrive", self)
        onedrive_link.triggered.connect(self.Open_onedrive)
        linkbar.addAction(onedrive_link)

    def Open_google(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com/"))
    def Open_youtube(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.youtube.com/"))
    def Open_netflix(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.netflix.com/hu/"))
    def Open_facebook(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.facebook.com"))
    def Open_wikipedia(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.wikipedia.org"))
    def Open_gmail(self):
        self.tabs.currentWidget().setUrl(QUrl("https://gmail.com/"))
    def Open_googlemaps(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.googlemaps.com"))
    def Open_twitter(self):
        self.tabs.currentWidget().setUrl(QUrl("https://twitter.com/home"))
    def Open_apple(self):
        self.tabs.currentWidget().setUrl(QUrl("https://apple.com/hu"))
    def Open_stackoverflow(self):
        self.tabs.currentWidget().setUrl(QUrl("https://stackoverflow.com/"))
    def Open_github(self):
        self.tabs.currentWidget().setUrl(QUrl("https://github.com/"))
    def Open_outlook(self):
        self.tabs.currentWidget().setUrl(QUrl("https://outlook.hu/"))
    def Open_onedrive(self):
        self.tabs.currentWidget().setUrl(QUrl("https://onedrive.com/"))

    def history(self):
        with open("history.txt", mode='r') as file:
            lines = file.readlines()
            for line in lines:
                self.urlbar.setText(line.strip())

    def settings(self):
        pass

    def download_video(self):
        if "https://www.youtube.com/watch?v=" in self.urlbar.text():
            path = str(Path.home() / "Downloads")
            yt = YouTube(self.urlbar.text())
            print("-----------------------------------------------")
            print("                   LET??LT??S                    ")
            print("\nADATOK:")
            print("URL: ", yt.watch_url)
            print("A vide?? neve: ", yt.title)
            print("Felt??lt??: ", yt.author)
            print("Felt??lt??s d??tuma: ", yt.publish_date)
            print("Megtekint??sek sz??ma: ", yt.views)
            print("felt??lt?? csatorn??j??nak URL-je: ", yt.channel_url)

            yd = yt.streams.get_highest_resolution()
            yd.download(path)

    def download_video_thread(self):
        x = threading.Thread(target=self.download_video)
        x.start()

    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self, download):
        try:
            old_path = download.url().path()  # download.path()
            suffix = QtCore.QFileInfo(old_path).suffix()
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save File", old_path, "*.*" # + suffix
            )
            if path:
                download.setPath(path)
                download.accept()
        except:
            pass

    @QtCore.pyqtSlot("QWebEngineFullScreenRequest")
    def FullscreenRequest(self, request):
        request.accept()
        if request.toggleOn():
            self.browser.setParent(None)
            self.browser.showFullScreen()
        else:
            self.setCentralWidget(self.browser)
            self.browser.showNormal()
 
    # method for adding new tab
    def add_new_tab(self, qurl = None, label ="Blank"):
 
        # if url is blank
        if qurl is None:
            # creating a google url
            qurl = QUrl('https://foxresearch.hu/catsurf/index.html')
 
        # creating a QWebEngineView object
        browser = QWebEngineView()
 
        # setting url to browser
        browser.setUrl(qurl)
 
        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabIcon(i, browser.icon())
        browser.iconChanged.connect(lambda icon, browser=browser:
                                    self.update_tab_icon(browser, icon))
 
        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
 
        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
 
        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()
 
    # when tab is changed
    def current_tab_changed(self, i):
 
        # get the curl
        qurl = self.tabs.currentWidget().url()
 
        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        # update the title
        self.update_title(self.tabs.currentWidget())
 
    # when tab is closed
    def close_current_tab(self, i):
 
        # if there is only one tab
        if self.tabs.count() == 1:
            # do nothing
            self.close()
 
        # else remove the tab
        self.tabs.removeTab(i)
 
    # method for updating the title
    def update_title(self, browser):
 
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return
 
        # get the page title
        title = self.tabs.currentWidget().page().title()
 
        # set the window title
        self.setWindowTitle("% s - Cat Surf" % title)
 
    # action to go to home
    def navigate_home(self):
 
        # go to google
        self.tabs.currentWidget().setUrl(QUrl("https://foxresearch.hu/catsurf/index.html"))
 
    # method for navigate to url
    def navigate_to_url(self):
 
        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())

        """
        if "https://" in self.urlbar.text() or "http://" in self.urlbar.text():
            if exception == 0:
                if ".hu" in self.urlbar.text() or ".com" in self.urlbar.text() or ".net" in self.urlbar.text() or ".org" in self.urlbar.text():
                    q = QUrl(self.urlbar.text())

        if "https://" not in self.urlbar.text() or "http://" not in self.urlbar.text():
            if ".hu" not in self.urlbar.text() or ".com" not in self.urlbar.text() or ".net" not in self.urlbar.text() or ".org" not in self.urlbar.text():
                q = QUrl("https://duckduckgo.com/?q=" + self.urlbar.text() + "&t=h_&ia=web")
        """
        if self.urlbar.text() == "":
            q = QUrl("https://duckduckgo.com/?t=h_")

        # set the url
        self.tabs.currentWidget().setUrl(q)

        with open("history.txt", "a+") as file:
            file.write(self.urlbar.text() + "\n")

    # method to update the url
    def update_urlbar(self, q, browser = None):
 
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
 
            return
 
        # set text to the url bar
        self.urlbar.setText(q.toString())
 
        # set cursor position
        self.urlbar.setCursorPosition(0)

    def update_tab_icon(self, browser, icon):
        index = self.tabs.indexOf(browser)
        self.tabs.setTabIcon(index, icon)

# creating a PyQt5 application
app = QApplication(sys.argv)
 
# setting name to the application
app.setApplicationName("Cat Surf")
 
# creating MainWindow object
window = MainWindow()
path = str(Path(__file__).parent / "icon.png")
window.setWindowIcon(QIcon(path))

send_notification("A Cat Surf elindult.", "Sikeres ind??t??s")

# loop
app.exec_()