
from pydub import AudioSegment
import array
from pydub.utils import get_array_type
from pydub.utils import mediainfo

def getAudioData(filepath):
    sound_file = AudioSegment.from_wav(filepath)
    return sound_file

def getNumbericArray(sound_clip):
    bit_depth = sound_clip.sample_width*8
    array_type = get_array_type(bit_depth)

    numeric_array = array.array(array_type,sound_clip._data)

class AudioStore:
    def __init__(self,sound_file,start_time):
        self.start_time = start_time
        self.end_time = start_time
        
        self.sound_file=sound_file
        self.mouse_wheel_increment=10
        
        self.saved_segments = []
        self.segment_labels = []
        self.display_size = 1000
        
        self.page_number = page_number
        self.word_index=word_index
        self.label=None
        self.fig = None
    
    def get_end_time(self):
        return self.end_time
    
    def set_end_time(self,end_time):
        end_time = max(self.start_time,end_time)
        end_time = min(self.duration,end_time)
        self.end_time = end_time
    
    def get_start_time(self):
        return self.start_time

    def set_start_time(self,start_time):
        start_time = max(0,self.start_time)
        start_time = min(self.duration,start_time)
        self.start_time = start_time
    
    def set_label(self,label):
        self.label = label

    def save_audio_segment(self):
        self.saved_segments.append(self.sound_file[self.start_time:self.end_time])
        self.segment_labels.append(self.label.lower())
    
    def remove_audio_segment(self):
        self.label = input("insert word label")
        self.display()

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
        self.start_time-=len(self.saved_segments[-1])
        del(self.saved_segments[-1])
        del(self.segment_labels[-1])
        del(self.save_saved_segments[-1])
  
    def segment_generator(self,save_directory):
        save_index=get_saved_index(save_directory)
        for i,sound_segment in enumerate(self.saved_segments):
            label = self.segment_labels[i]
            filename="%d_%s_.wav" % (i+save_index,label)
            save_path = os.path.join(save_directory,filename)
            yield save_path,sound_segment

def export_audio_samples(av,save_directory):
    for save_path,save_segment in av.segment_generator(save_directory):
        save_segment.export(save_path, format="wav")

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
    word_index_filename = "word_position.txt"
    start_index_file = os.path.join(save_directory,word_index_filename)
    page_number,word_index = getStartWordIndex(start_index_file)
    start_time = getStartTime(start_time_file)

    pdf_parser = getPdfParser(args["pdf_file"])

    print(page_number,word_index)
    sound_file = getAudioData(args["audio_file"])

    av = AudioVisualizer(sound_file,pdf_parser,page_number,word_index,start_time)
    av.initUI()
    
    export_audio_samples(av,save_directory)
    save_word_index(av,start_index_file)
    save_start_time(av,start_time_file)
    print("exit")