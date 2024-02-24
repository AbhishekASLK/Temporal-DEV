import tkinter as tk
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import *
import time
import math

class AudioAuraFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        pygame.mixer.init()
        self.n = 0
        self.list_of_songs = ['modules/songs/Husn-Slowed-Reverb.mp3','modules/songs/Core2Web-Theme-Song.mp3','modules/songs/Ve-Haaniyaan.mp3',]
        self.list_of_covers = ['modules/images/husn_cover.jpg','modules/images/core2web_cover.png','modules/images/haaniya_cover.jpg',]

        # Tkinter widgets
        self.setup_widgets()

    def setup_widgets(self):

        

        self.paused = False 

        # Album cover image
        image1 = Image.open(self.list_of_covers[self.n]).resize((250,250))
        image2 = image1.resize((500, 500))
        self.album_cover = ImageTk.PhotoImage(image2)
        self.album_cover_label = tk.Label(self, image=self.album_cover)
        self.album_cover_label.pack(pady=50)

        # Song name label
        stripped_string = self.list_of_songs[self.n][14:]
        self.song_name_label = tk.Label(self, font=('arial', 20, 'bold'),text=stripped_string, bg='#222222', fg='white')
        self.song_name_label.pack()

        # Play button
        self.play_button = customtkinter.CTkButton(master=self,fg_color="green", text='Play',font=('arial', 30, 'bold'), width=200,height=50,command=self.play_music)
        self.play_button.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

        # Next Button
        self.next_song_button = customtkinter.CTkButton(master=self,fg_color="green", text='Next',font=('arial', 30, 'bold'), width=200,height=50, command=self.skip_forward)
        self.next_song_button.place(relx=0.8, rely=0.7, anchor=tk.CENTER)

        # Pause button
        self.pause_button = customtkinter.CTkButton(master=self, fg_color="red", text='Pause', font=('arial', 30, 'bold'), width=200, height=50, command=self.pause_music)
        self.pause_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

        # Back Button
        self.back_song_button = customtkinter.CTkButton(master=self,fg_color="green", text='Prev', font=('arial', 30, 'bold'), width=200,height=50,command=self.skip_back)
        self.back_song_button.place(relx=0.2, rely=0.7, anchor=tk.CENTER)

        # Volume slider
        self.volume_slider = customtkinter.CTkSlider(master=self,from_=0, to=1, command=self.volume, width=250)
        self.volume_slider.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

        # Progress bar
        self.progressbar = customtkinter.CTkProgressBar(master=self, progress_color='#32a85a', width=400,height=20)
        self.progressbar.place(relx=.5, rely=.85, anchor=tk.CENTER)

    def get_album_cover(self, song_name):
        image1 = Image.open(song_name)
        image2 = image1.resize((500, 500))
        load = ImageTk.PhotoImage(image2)
        self.album_cover_label.configure(image=load)
        self.album_cover_label.image = load

    def progress(self, song_len):
        while self.playing:
            time.sleep(.1)
            progress = pygame.mixer.music.get_pos() / (song_len * 1000)  # Progress as a fraction
            self.progressbar.set(progress)

    def threading(self):
        self.playing = True
        t1 = Thread(target=self.progress, args=(pygame.mixer.Sound(self.list_of_songs[self.n]).get_length(),))
        t1.start()

    def play_music(self):
        self.playing = False
        current_song = self.n
        if self.n > len(self.list_of_songs)-1:
            self.n = 0
            current_song = 0
        song_name = self.list_of_songs[current_song]
        album_image = self.list_of_covers[current_song]
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(.5)
        self.get_album_cover(album_image)
        self.threading()

    def pause_music(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False
            self.pause_button.configure(text='Pause', fg_color='red')  # Change button text to "Pause"


    def skip_forward(self):
        self.playing = False
        self.n+=1
        if self.n == len(self.list_of_songs):
            self.n=0
        self.song_name_label.config(text=self.list_of_songs[self.n][14:])
        self.play_music()

    def skip_back(self):
        self.playing = False
        self.n -= 1
        if self.n < 0:
            self.n = len(self.list_of_songs)-1
        self.song_name_label.config(text=self.list_of_songs[self.n][14:])
        self.album_cover_label.config(text=self.list_of_songs[self.n][14:])
        self.play_music()

    def volume(self, value):
        pygame.mixer.music.set_volume(value)


if __name__ == "__main__":
    root = customtkinter.CTk()
    music_player_frame = AudioAuraFrame(root)
    music_player_frame.pack(expand=True, fill="both")
    root.mainloop()
