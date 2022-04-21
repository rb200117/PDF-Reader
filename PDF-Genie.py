from mimetypes import common_types
from tkinter import *
import PyPDF2
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf
import os

root = Tk()
root.title('PDF-Genie')
root.geometry('500x500')

my_menu = Menu(root)
root.config(menu=my_menu)

my_text = Text(root, height=30, width=60)
my_text.pack(pady=10)


def clear_text_box():
    my_text.delete(1.0, END)


def open_pdf():
    open_file = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Open PDF File",
        filetypes=(("PDF Files", "*.pdf"),)
    )
    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        page = pdf_file.getPage(0)
        # page_stuff = page.extractText()
        # my_text.insert(1.0,page_stuff)
        v1 = pdf.ShowPdf()
        v2 = v1.pdf_view(root, pdf_location=open())


def save_pdf():
    pass


file_menu = Menu(my_menu, tearoff=False)
template_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label='Create Template', command=open_pdf)
file_menu.add_command(label='Save Template', command=save_pdf)
file_menu.add_command(label='Clear', command=clear_text_box)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)
my_menu.add_cascade(label="Templates", menu=template_menu)
template_menu.add_command(label="Template-1")


root.mainloop()
