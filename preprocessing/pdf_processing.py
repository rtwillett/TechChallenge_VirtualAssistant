import PyPDF2

class PDFExtractor:
    
    def __init__(self, read_filepath:str, save_filepath):
        
        self.read_filepath = read_filepath
        self.save_filepath = save_filepath
        self.reader = self.load_file()
                
    def calculate_page_length(self) -> int:
        # printing number of( pages in pdf file
        return len(self.reader.pages)
        
    def load_file(self): 
        
        import PyPDF2
        
        # Creating a pdf file object
        self.pdffile = open(self.read_filepath, 'rb')

        # Creating a pdf reader object
        reader = PyPDF2.PdfReader(self.pdffile)
        
        return reader
    
    def extract_page(self, p:int) -> str:
    
        # Creating a page object
        pageObj = self.reader.pages[p]
        return pageObj.extract_text()
    
    def write_page(self, p:int):
        
        page_text = self.extract_page(p)
        
        
        # Opening and Closing a file "MyFile.txt" for object name file1.
        file = open(self.save_filepath,"a")
        file.write(page_text)
        file.close()
        
        return None

    def write_all_pages(self, n:int = 0):
        
        if n == 0:
            page_limit = self.calculate_page_length()
        else: 
            page_limit = n
        
        for p in range(page_limit):
            self.write_page(p)
            
        self.close()
            
    def close(self) -> None:
        
        self.pdffile.close()
        
        return None