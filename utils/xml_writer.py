"""
word index
page index
sentance index
part of phrase
punctuation

<>
    <>
    word index
    page index
    sentence index
    part of phrase
    attached puncutation
    <>
</>
"""

import spacy
import xml.etree.ElementTree as ET

class xmlWriter:
    def __init__(self,filename):
        self.audio_path = filename
        self.fields = ["word_index","page_index","sentence_index","part_of_phrase","punctuation"]
        self.root = self.open_file(filename)

    def get_save_path(self):
        save_directory,filename = os.path.split(self.audio_path)
        name,ext = os.path.splitext(filename)
        save_filename = name + ".xml"
        save_path = os.path.join(save_directory,save_filename)
        return save_path

    def save_file(self):
        save_data = ET.tostring(self.root)
        with open(self.get_save_path,"wb") as f:
            f.write(save_data)

    def add_sample(self,save_packet):
        samples = self.root.find('samples')
        sample = ET.SubElement(samples, "sample")
        for key in save_packet:
            elem = ET.SubElement(sample,key)
            elem.text = save_packet[key]

    def open_file(self,filename):
        if os.path.exists(filename):
            tree = ET.ElementTree(file=filename)
            root = tree.getroot()
        else:
            root = ET.Element("data")
            path = ET.SubElement(root, "audio_path")
            path.text = self.audio_path
            samples = ET.SubElement(root,"samples")
        return root
        
    
