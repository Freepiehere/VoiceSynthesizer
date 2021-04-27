from pydub import AudioSegment
from pydub.silence import split_on_silence
import argparse
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import matplotlib
import matplotlib.pyplot as plt

from pydub.playback import play
from pydub.utils import get_array_type
from pydub.utils import mediainfo
import array
import random
import os

from pdf_to_text import pdfParser
from pdf_to_text import getWordByIndex,getPdfParser,getPageNumberFromIndex,getWordIndexFromPageNumber


class AudioVisualizer:
    def __init__(self,sound_file,pdf_parser,page_number,word_index,start_time=0):
        self.start_time = start_time
        self.end_time = 0
        self.duration = len(sound_file)
        self.sound_file=sound_file
        self.fig = None
        self.mouse_wheel_increment=10
        self.audio_segments = []
        self.segment_labels = []
        self.save_audio_segments = []
        self.display_size = 1000

        self.pdf_parser = pdf_parser
        self.page_number = page_number
        self.word_index=word_index
        self.label = self.get_next_word()

    def initUI(self):
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('scroll_event',self.scroll_event)
        self.fig.canvas.mpl_connect('close_event',self.close_event)
        self.fig.canvas.mpl_connect('key_press_event',self.key_event)
        self.fig.canvas.mpl_connect('button_press_event',self.on_click)
        self.ax = self.fig.add_subplot(111)
        plt.show()
    
    def save_audio_segment(self,save):
        self.audio_segments.append(self.sound_file[self.start_time:self.end_time])
        self.segment_labels.append(self.label.lower())
        self.save_audio_segments.append(save)
    
    def remove_audio_segment(self):
        self.start_time-=len(self.audio_segments[-1])
        del(self.audio_segments[-1])
        del(self.segment_labels[-1])
        del(self.save_audio_segments[-1])
    
    def scroll_event(self,e):
        if (e.button =="down"):
            self.end_time+=self.mouse_wheel_increment
        elif (e.button == "up"):
            self.end_time-=self.mouse_wheel_increment
        else:
            return
        if self.end_time >= self.duration:
            self.end_time = self.duration-1
        elif self.end_time < self.start_time:
            self.end_time = self.start_time
        self.display()
    
    def display(self):
        self.ax.cla()

        sound_clip = self.sound_file[self.start_time:self.end_time]
        bit_depth = sound_clip.sample_width*8
        array_type = get_array_type(bit_depth)

        numeric_array = array.array(array_type,sound_clip._data)
        self.ax.plot(numeric_array)
        plt.title(str(self.page_number)+":"+str(self.word_index)+" "+"\""+self.label+"\"")
        self.fig.canvas.draw()

    def key_event(self,e):
        if (e.key==" " and self.start_time!=self.end_time):
            self.save_audio_segment(True)
            self.start_time = self.end_time
            self.label = self.get_next_word()
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
            self.label = input("insert word label")
            self.display()

    def get_next_word(self):
        self.word_index+=1
        next_word = getWordByIndex(self.pdf_parser, self.page_number, self.word_index)
        if next_word is None:
            self.page_number+=1
            self.word_index=0
            next_word = getWordByIndex(self.pdf_parser, self.page_number, self.word_index)
        return next_word
    
    def get_prev_word(self):
        self.word_index-=1
        if self.word_index<0:
            self.word_index = 0
        word = getWordByIndex(self.pdf_parser, self.page_number, self.word_index)
        if word is None:
            self.page_number+=1
            self.word_index=0
            word = getWordByIndex(self.pdf_parser, self.page_number, self.word_index)
        return word

    def close_event(self,event):
        pass
    
    def on_click(self,event):
        if event.button==1:
            play(self.sound_file[self.start_time:self.end_time])
        elif event.button==3: 
            self.label="space"
            self.save_audio_segment(True)
            self.start_time=self.end_time
            self.display()
        
    def segment_generator(self,save_directory):
        save_index=get_saved_index(save_directory)
        for i,sound_segment in enumerate(self.audio_segments):
            label = self.segment_labels[i]
            filename="%d_%s_.wav" % (i+save_index,label)
            save_path = os.path.join(save_directory,filename)
            yield save_path,sound_segment

def get_saved_index(save_directory):
    filenames = os.listdir(save_directory)
    max_index=0
    for filename in filenames:
        print(filename)
        comps = filename.split("_")
        try:
            save_index = int(comps[0])
        except ValueError: #metadata
            continue 
        if save_index>max_index:
            max_index=save_index
    return max_index+1



def play_audio_segment(sound_file):
    play(sound_file)

def export_audio_samples(av,save_directory):
    for save_path,save_segment in av.segment_generator(save_directory):
        save_segment.export(save_path, format="wav")

def save_word_index(av,pdf_parser,save_path):
    word_index = getWordIndexFromPageNumber(pdf_parser,av)
    with open(save_path,"w+") as f:
        f.write(str(word_index))


def save_start_time(av,save_path):
    save_path = os.path.join(save_directory,"start_time.txt")
    with open(save_path,"w+") as f:
        f.write(str(av.start_time))

def getStartTime(save_directory):
    if not os.path.exists(start_time_file):
        return 0
    f = open(start_time_file,"r")
    start_time = f.readline()
    return int(start_time)

def getStartWordIndex(save_directory):
    if not os.path.exists(start_index_file):
        return 0
    f = open(start_index_file,"r")
    start_index = f.readline()
    try:
        start_index = int(start_index)
    except ValueError as e:
        print(e)
        print("starting from zero")
        start_index=0
    return start_index

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_file",required=True,type=str)
    parser.add_argument("--pdf_file",required=True,type=str)
    
    args = vars(parser.parse_args())
    
    base,filename = os.path.split(args["audio_file"])
    name,ext = os.path.splitext(filename)
    save_directory = os.path.join(base,name)
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    start_filename = "start_time.txt"
    start_time_file = os.path.join(save_directory,start_filename)
    word_index_filename = "word_index.txt"
    start_index_file = os.path.join(save_directory,word_index_filename)
    word_index = getStartWordIndex(start_index_file)
    start_time = getStartTime(start_time_file)

    pdf_parser = getPdfParser(args["pdf_file"])

    page_number,word_index = getPageNumberFromIndex(pdf_parser,word_index)
    
    sound_file = AudioSegment.from_wav(args["audio_file"])

    av = AudioVisualizer(sound_file,pdf_parser,page_number,word_index,start_time)
    av.initUI()
    
    export_audio_samples(av,save_directory)
    save_word_index(av,pdf_parser,start_index_file)
    save_start_time(av,start_time_file)
    print("exit")