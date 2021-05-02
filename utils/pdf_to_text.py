import PyPDF2
import argparse
import string

class pdfParser(PyPDF2.PdfFileReader):
    def get_page_number(self,target_text):
        i=0
        while i in range(self.numPages):
            if self.text_in_page(i,target_text):
                return i
            i+=1
        return i

    def text_in_page(self,page_number,target_text):
        lines = self.get_page_lines(page_number)
        for line in lines:
            if target_text in line:
                return True
        return False
    
    def get_line_location(self,target_text,lines):
        for i,line in enumerate(lines):
            if target_text in line:
                return i
        return -1
    
    def get_page_lines(self,page_number):
        pageObj = self.getPage(page_number)
        text = pageObj.extractText()
        lines = text.splitlines()
        return lines
    
    def split_words_on_line(self,line):
        new_line = line.split(" ")
        new_line = [i for i in new_line if i]
        return new_line

    """
    HAS ERROR NOT INCLUDING COLLOQUIAL PUNCTIATION
    """
    def count_words_in_line(self,line):
        new_line=self.split_words_on_line(line)
        if new_line:
            del new_line[0]
        for j in range(len(new_line)):
            new_line[j] = ''.join([i for i in new_line[j] if not i.isdigit()])
        new_line = [i for i in new_line if i]

        print(new_line,len(new_line))
        return len(new_line)
    
    def count_words_in_page(self,lines):
        sum = 0
        for line in lines:
            sum += self.count_words_in_line(line)
        return sum
    
    def count_words_in_range(self,start_page,end_page):
        sum=0
        for page_number in range(end_page-start_page):
            page_lines = self.get_page_lines(start_page+page_number)
            sum += self.count_words_in_page((page_lines))
        return sum  

def getPdfParser(pdf_file):
    pdfFileObj = open(pdf_file,"rb")
    pdf_parser = pdfParser(pdfFileObj)
    return pdf_parser

punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
def getWordByIndex(pdfReader,pdf_page,index):
    page_lines = pdfReader.get_page_lines(pdf_page)

    i=0
    for line in page_lines:
        words = pdfReader.split_words_on_line(line)
        for word in words:
            if i==index:
                return_string=word
                for ele in return_string:
                    if ele in punc:
                        return_string=return_string.replace(ele,"")
                return return_string
            i+=1
    return None

def getPageNumberFromIndex(pdf_parser,word_index):
    page_number=0
    word_sum=0
    while page_number < pdf_parser.numPages:
        page_lines = pdf_parser.get_page_lines(page_number)
        i=0
        for line in page_lines:
            words = pdf_parser.split_words_on_line(line)
            for word in words:
                if word_sum==word_index:
                    return page_number,i
                i+=1
                word_sum+=1
        page_number+=1

def getWordIndexFromPageNumber(pdf_parser,av):
    index=0
    page_number = av.page_number
    word_index = av.word_index
    # iterate through the second to last page
    # word_index contains current position in last page
    for page in range(page_number-1):
        page_lines = pdf_parser.get_page_lines(page)
        for line in page_lines:
            words = pdf_parser.split_words_on_line(line)
            index+=len(words)
    return index+word_index




if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_pdf",type=str,required=True)
    args = vars(ap.parse_args())
    filename = args["input_pdf"]

    
    target_text = "P R O C E E D I N G S"
    first_page_number = pdfReader.get_page_number(target_text)
    page_number = first_page_number
    page_text = pdfReader.getPage(page_number)
    
    page_lines = pdfReader.get_page_lines(page_number)
    page_position = pdfReader.get_line_location(target_text,page_lines)+1

    target_text = "(Whereupon, at 11:44 a.m., the case"
    final_page_number = pdfReader.get_page_number(target_text)
    word_count = pdfReader.count_words_in_range(first_page_number,final_page_number)
    print(word_count)
    
    pdfFileObj.close()  