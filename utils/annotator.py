import argparse
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib
import matplotlib.pyplot as plt

from mp3_to_amplitude import getAudioData,getNumbericArray
from pydub.playback import play
import random
import os

from pdf_to_text import pdfParser
from pdf_to_text import getWordByIndex,getPdfParser,getPageNumberFromIndex,getWordIndexFromPageNumber


class AudioAnnotator:
    def __init__(self,audio_store,):
        self.fig = None
        self.audio_store = audio_store

    def initUI(self):
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('scroll_event',self.scroll_event)
        self.fig.canvas.mpl_connect('key_press_event',self.key_event)
        self.fig.canvas.mpl_connect('button_press_event',self.on_click)
        self.fig.canvas.mpl_connect('close_event',self.close_event)
        self.ax = self.fig.add_subplot(111)
        plt.show()
    
    def display(self):
        self.ax.cla()

        sound_clip = self.sound_file[self.start_time:self.end_time]
        numeric_array = getNumbericArray(sound_clip)
        self.ax.plot(numeric_array)

        plt.title(str(self.page_number)+":"+str(self.word_index)+" "+"\""+self.label+"\"")
        self.fig.canvas.draw()
    
    def scroll_event(self,e):
        if (e.button =="down"):
            end_time = self.audio_store.get_end_time()
            end_time += self.mouse_wheel_increment
            self.audio_store.set_end_time(end_time)
        elif (e.button == "up"):
            end_time = self.audio_store.get_end_time()
            end_time -= self.mouse_wheel_increment
            self.audio_store.set_end_time(end_time)
        else:
            return
        if self.end_time >= self.duration:
            self.end_time = self.duration-1
        elif self.end_time < self.start_time:
            self.end_time = self.start_time
        self.display()

    def key_event(self,e):
        if (e.key==" " and self.start_time!=self.end_time):
            self.audio_store.save_audio_segment()
            end_time = self.audio_store.get_end_time()
            self.audio_store.set_start_time(end_time)
            self.audio_store.set_label("")
            self.display()
        elif(e.key=="backspace"):
            self.remove_audio_segment()
            self.display()
        elif(e.key=="left"):
            self.label=self.get_prev_word()
            self.display()
        elif(e.key=="right"):
            self.label=self.get_next_word()
            self.display()
        elif(e.key=="up"):
            self.page_number+=1
            self.label = self.get_next_word()
            self.display()
        elif(e.key=="down"):
            self.page_number-=1
            self.page_number = max(0,self.page_number)
            self.display()
        elif(e.key=="i"):
    
    def on_click(self,event):
        if event.button==1:
            play(self.sound_file[self.start_time:self.end_time])
        elif event.button==3:
            self.label="space"
            self.save_audio_segment(True)
            self.start_time=self.end_time
            self.display()

    def close_event(self,event):
        pass
      