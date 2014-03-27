import subprocess
from multiprocessing import Pool, cpu_count

from PyPDF2 import PdfFileMerger

class PDF:
    def __init__(self, config):
        self.conf = config

    def pdfmerge(self, file_list, pdfname):
        "Merge a list of PDF files."

        merger = PdfFileMerger()

        for f in file_list:
            if type(f) == str:
                fo = open(f, "rb")
                merger.append(fileobj = fo)

            elif type(f).__name__ == "Revue":
                for act in f.acts:
                    for m in act.materials:
                        merger.append(os.path.join(m.category, "{}.pdf".format(m.file_name[:-4])))
            
            elif type(f).__name__ == "Actor":
                print(f.name)
                for role in f.roles:
                    merger.append(os.path.join(role.material.category, "{}.pdf".format(role.material.file_name[:-4])))


        output = open(pdfname, "wb")
        merger.write(output)
    

    def parallel_pdfmerge(self, file_list):
        "Merge a list of lists of PDF files in parallel."

        if type(file_list[0]) == str:
            # Each element is a file path.
            with Pool(processes = cpu_count()) as pool:
                result = pool.map(generate_pdf_from_file, file_list)

