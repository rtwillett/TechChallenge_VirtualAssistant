class DocProcessingInterface:
    
    def __init__(self, raw_dir, proc_dir):
        self.raw_dir = raw_dir
        self.proc_dir = proc_dir
        
        self.find_dir_div()
    
    def find_dir_div(self):
        """
        Checks the processed and raw directories and finds documents 
        """
        
        from glob import glob
        
        # Get the filepaths and filenames in the raw documents directory
        self.raw_docs = glob(f'{self.raw_dir}*.pdf')
        self.raw_docs_filenames = [self.extract_filename(f) for f in self.raw_docs]
        
        # Get the filepaths and filenames in the processed directory
        self.proc_docs = glob(f'{self.proc_dir}/*.txt')
        self.proc_docs_filenames = [self.extract_filename(f) for f in self.proc_docs]
        
        # Find the files in the raw folder that are missing in the processed folder
        self.staged_docs = list(set(self.raw_docs_filenames) - set(self.proc_docs_filenames) - set([""]))
        
        staged_filepaths = [i if self.extract_filename(i) in self.staged_docs else "" for i in self.raw_docs]
        self.staged_filepaths = [i for i in staged_filepaths if i.strip() != ""]
    
    def extract_filename(self, filepath:str) -> str:
        try:
            return filepath.split("/")[-1].split(".")[0].strip()
        except: 
            return ""