from PyPDF2 import PdfFileWriter, PdfFileReader
import os


def merge(dir, output):
    pdf_writer = PdfFileWriter()
    pdfFiles=[]

    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            pdfFiles.append(filename)

    firstPage = PdfFileReader(pdfFiles[0]).getPage(0)
    pdf_writer.addPage(firstPage)

    for file in pdfFiles:
        pdfobj = PdfFileReader(file)
        for page in range(1,pdfobj.getNumPages()):
            page = pdfobj.getPage(page)
            pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)

if __name__ == '__main__':
    merge(dir='.',output = 'merge.pdf')