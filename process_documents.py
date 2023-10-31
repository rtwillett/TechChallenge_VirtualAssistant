from interfaces.directory_interfaces import DocProcessingInterface
from preprocessing.pdf_processing import PDFExtractor

def extract_files(interface) -> None:
    for filepath in interface.staged_filepaths:

        print(f"Extracting text from ...... {filepath}")
        
        extraction_fp = f"{interface.proc_dir}{interface.extract_filename(filepath)}.txt"

        pdfreader = PDFExtractor(read_filepath= filepath, save_filepath= extraction_fp)
        pdfreader.write_all_pages()
    
        return None
    
if __name__ == "__main__":

    interface = DocProcessingInterface(raw_dir="./documents_raw/", proc_dir="./documents_processed/")
    extract_files(interface)