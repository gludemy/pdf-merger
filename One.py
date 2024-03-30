#!/usr/bin/python
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

from tkinter import Tk, filedialog, messagebox, LabelFrame, Button, GROOVE, TOP
from datetime import date


window = Tk()
window.title("PDF Merger - Gludemy.com")
window.geometry('320x290')
window.configure(bg='#005a95')


# FRAME 1: CHOOSE FILE

# Choose folder that holdes labels
def choose_folder():
    global source_folder
    source_folder = filedialog.askdirectory()
    return source_folder

frame1 = LabelFrame(window, width=30, height=10, bd=1, font="Verdana 9 bold", relief=GROOVE)

btn1 = Button(frame1, bg='#bdd7e9', text='Choose folder', height = 5, width = 30, bd=5, command=choose_folder)
btn1.pack(side=TOP)

frame1.pack(padx=10, pady=10)

# FRAME 2: CONVERT
def create_shipping_label(input_path):
    labels_name_list = os.listdir(input_path)
    pdf_writer = PdfFileWriter()
    for label_name in labels_name_list:
        path = os.path.join(input_path, label_name)
        pdf_reader = PdfFileReader(path)

        for page in range(pdf_reader.getNumPages()):
            current_page = pdf_reader.getPage(page)
            current_page_width = current_page.mediaBox.getWidth()
            current_page_height = current_page.mediaBox.getHeight()
            aspect = current_page_width / current_page_height
            if aspect > 1:
                current_page.rotateCounterClockwise(90)
                pdf_writer.addPage(current_page)
            else:
                pdf_writer.addPage(current_page)
            
    # pop up windows for user to choose where to save!
    todayStr = date.today().strftime("%Y%m%d")
    save_path = filedialog.asksaveasfilename(
        initialfile = 'Labels{}.pdf'.format(todayStr),
        title = "Save as", 
        filetypes = (("pdf files","*.pdf"),("all files","*.*"))
    )
    with open(save_path, "wb") as out_f:
        pdf_writer.write(out_f)
        messagebox.showinfo('Successful', 'Task completed!')

frame2 = LabelFrame(window, width=30, height=10, bd=1, font="Verdana 9 bold", relief=GROOVE)

btn2 = Button(frame2, text='Start', height = 5, width = 30, bd=5, command=lambda:create_shipping_label(source_folder))
btn2.pack(side=TOP)

frame2.pack(padx=10, pady=10)

window.update()
window.minsize(window.winfo_width(), window.winfo_height())
window.mainloop()
