from io import BytesIO
from tkinter import *
import tkinter
import os
from tkinter import filedialog
from pdf2image import convert_from_path
import numpy as np
from tkPDFViewer import tkPDFViewer as pdf
import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

root = Tk()
root.title('PDF-Genie')
root.geometry('1000x1200+10+20')

my_menu = Menu(root)
root.config(menu=my_menu)

welcomeLabel = Label(root, text="Welcome to PDF Genie",
                     font=('Didot bold', 60), pady=20, padx=20).pack()

descLabel = Label()


def on_click():
   pass


def convertToJpeg(im):
    with BytesIO() as f:
        im.save(f, format='JPEG')
        return f.getvalue()


def open_pdf():
    open_file = filedialog.askopenfilename(initialdir=os.getcwd(
    ), title="Open PDF File", filetypes=(("PDF Files", "*.pdf"),))
    if open_file:
        # v1 = pdf.ShowPdf()
        # v2 = v1.pdf_view(root,pdf_location=open(open_file,'r'),width=85,height=100)
        # v2.pack(pady=(0,0))
        images = convert_from_path(open_file)

        pil_img = images[0].convert('RGB')
        cv_image = np.array(pil_img)
        cv_image = cv_image[:, :, ::-1]
        print(cv_image.shape)
        r = cv2.selectROI(cv_image)

        # Crop image
        cropped_image = cv_image[int(r[1]):int(r[1]+r[3]),
                                 int(r[0]):int(r[0]+r[2])]
        img = Image.fromarray(cropped_image, 'RGB')
        img = img.convert('L')                             # grayscale

        img = img.filter(ImageFilter.MedianFilter())       # a little blur
        img = img.point(lambda x: 0 if x < 140 else 255)

        text = pytesseract.image_to_string(img)
        print(text)
        resLabel = Label(root, text=text, font=(
            'Helvetica', 20), pady=20, padx=20)
        resLabel.pack()


def save_temp():
    pass


# Adding a Button
myButton1 = Button(root, text="Create Template", command=open_pdf).pack()


file_menu = Menu(my_menu, tearoff=False)
template_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label='Create Template', command=open_pdf)
file_menu.add_command(label='Save Template', command=save_temp)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)
my_menu.add_cascade(label="Templates", menu=template_menu)
template_menu.add_command(label="Template-1")

j = 1
Templates = [{"temp_name": "Temp-1", "selection": {"name": {"x": 23, "y": 45}}},
             {"temp_name": "Temp-2", "selection": {"name": {"x": 13, "y": 55}}}]
print(Templates)

root.menubutton_1 = Menubutton(root, text='Templates', relief='raised')
root.menubutton_1.menu = Menu(root.menubutton_1)
root.menubutton_1.pack()
root.user_choice = IntVar()
root.file_menu = Menu(root.menubutton_1, tearoff=0)
for i in Templates:
    S = root.file_menu.add_radiobutton(label=i.get(
        "temp_name"), variable=root.user_choice, value=i)
    j += 1
root.menubutton_1.config(menu=root.file_menu)

root.mainloop()
