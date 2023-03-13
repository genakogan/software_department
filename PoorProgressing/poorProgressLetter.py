# Genady Kogan
import io
import tkinter
import pandas as pd
from tkinter import font as tkFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfReader, PdfWriter
import os

try:
    os.mkdir("PoorProgressing/results")
    print("Directory "+ "PoorProgressing/results "+"created successfully")
except OSError as error: 
    print(error)    
def nameWidth(stusentName):
    """
    Function return width of student name
    """
    tkinter.Frame().destroy()  # Enough to initialize resources
    arial36b = tkFont.Font(family='DejaVu', size=11)
    width = arial36b.measure("")
    return width


def pageSize(pdf):
    """
    Function return page size, for example RectangleObject([0, 0, 595.32, 841.92])
    """
    existing_pdf = PdfFileReader(open("PoorProgressing/test.pdf", "rb"))
    size = existing_pdf.pages[0].mediabox
    return size  
def get_dataSet():
    """
    function load data from csv file
    return ['ת.ז','שם'], data lenght
    """
    # load dataset
    df = pd.read_csv('poorStudents.csv', encoding="ISO-8859-8")

    # convert df[['ת.ז','מקצוע']] to string
    df = df[['ת.ז', 'שם']].astype(str)
   
    return df


from io import BytesIO
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def modifyFile():
    """
    Function modify PDF file for student 
    add: student name and student ID
    """
    df = get_dataSet()
   
    for i in range(len(df)-2):
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Registers a font, including setting up info for accelerated stringWidth
        pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSansCondensed.ttf'))
        can.setFont("DejaVu", 11)

        # String rotation
        text = df['שם'][i][::-1]

        # Draws a string in the current text styles.
        for txt in text.split('\n'):

            # Student name
            # Draws a string aligned on the first '.' (or other pivot character)
            can.drawAlignedString(400-nameWidth(text), 694, text=text)

        # student id
        can.drawAlignedString(485, 677, df['ת.ז'][i])
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)

        # create a new PDF with Reportlab
        new_pdf = PdfReader(packet)

        # read your existing PDF
        existing_pdf = PdfReader("PoorProgressing/test.pdf")
        output = PdfWriter()

        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

        # finally, write "output" to a real file
        #outputStream = open(df['שם'][i]+".pdf", "wb")
        if not os.path.exists("PoorProgressing/results"):
            os.makedirs("PoorProgressing/results")
        outputStream = open(os.path.join("PoorProgressing/results",df['שם'][i]+".pdf"), "wb")
        output.write(outputStream)
        outputStream.close()




if __name__ == "__main__":
    modifyFile()
