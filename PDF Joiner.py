import PyPDF2
from pathlib import Path
import sys
import os

def debug(*values, end_pause=False, comment = ""):
    if "-debug" in sys.argv:
        if len(values) == 0:
            print(comment)
        else:
            if len(values) == 1:
                print(comment, " ", values[0])
            else:
                print(comment, " ", values)
        if end_pause == True:
            a = input("Script finished. Press ENTER to exit. ")
    #this function invoked only if command line argument is provided
    #used only to print intermediate values to terminal


if "-py" in sys.argv: #python works with path somewhat differently
    #so that's a kostyl' (sorry if u read this)
    #load important stuff
    path_to_script = os.path.realpath(__file__) #get path to file location
    current_path = Path(path_to_script).parent #remove the name of the file
    os.chdir(current_path) #change directory to match the current location
    
else:
    current_path = Path(os.getcwd())

debug(current_path, comment = "Path:")

files_in_dir = [p for p in current_path.glob("*.pdf")]

#now we need to delete old Combined.pdf file
filenames = [file.name for file in files_in_dir] #names of all pdf files in work dir
debug(filenames, comment = "All pdf files (before deletion): ") 
debug("Combined.pdf" in filenames, comment = "combined already created: ") 

#if Combined.pdf is not deleted b4 creating a new one, the old one will be with blank pages
if "Combined.pdf" in filenames:
    combined_file_index = filenames.index("Combined.pdf") #get index for combined.pdf in 2 parralel arrays
    combined_file_path = files_in_dir[combined_file_index] #get path of a resulting pdf
    try:
        os.remove(combined_file_path) #trash this pdf
        files_in_dir.pop(combined_file_index)
        filenames.pop(combined_file_index)
    except FileNotFoundError:
        debug(comment="Combined.pdf is not found!")
        debug(comment="Programm goes on.")
    else:
        debug(comment="Combined.pdf is removed.")

debug(filenames, comment = "PDF files found (after deletion):", )

pages = [] #list of pages scanned
for file in files_in_dir:
    with open(file, "rb") as pdf_file:
        data = PyPDF2.PdfFileReader(pdf_file) #the file stored in a variable
        pages_qty = data.numPages #get qty to work with a list of pages
        for page_number in range(pages_qty): 
            page = data.getPage(page_number) #we'll extract each page one by one
            pages.append(page) #and put into a list
    

        with open("Combined.pdf", "wb") as output:
            writer = PyPDF2.PdfFileWriter()
            for a_page in pages: #each page will be added into resulting file
                writer.addPage(a_page)
                writer.write(output)
            
            # try:
            #     writer.write(output)
            # except PyPDF2.utils.PdfReadError:
            #     pass


debug(end_pause=True)

