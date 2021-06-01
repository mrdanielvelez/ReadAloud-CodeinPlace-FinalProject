import os, pyttsx3, tkinter as tk
import PyPDF3
from tkinter.font import BOLD
from tkinter import Canvas, filedialog
from tkPDFViewer import tkPDFViewer as pdf
from gtts import gTTS, tts
from playsound import playsound
from tkinter import *

root = tk.Tk()
root.title("Read Aloud: Turn Your PDF Files into Audiobooks  [Stanford Code in Place 2021 Python Project by Daniel Velez]")
root.iconbitmap("ReadAloud_icon.ico")

canvas = tk.Canvas(root, height=800, width=800, bg="#3F5A36", highlightbackground="#3F5A36", highlightthickness=2)
canvas.create_text(400, 45, text="Turn any PDF into an Audiobook", font=("Helvetica", 21, BOLD), justify="center", fill="white")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Holds string of one PDF file path
FILENAME = []

# PDF Status Indicators in a List of Booleans
PDF_STATUS = [False]

# Prevents duplicate Read Aloud Buttons
READ_ALOUD_STATUS = [False]

def pdf_opened():
    if PDF_STATUS[-1]:
        return True
    return False


# Opens PDF/EPUB file for viewing and displays its name + extension
def add_file():
    if not pdf_opened():
        for widget in frame.winfo_children():
            widget.destroy()
        filename = filedialog.askopenfilename(initialdir="/clear", title="Select a File", filetypes=(("PDF files", "*.pdf"), ("All Files", "*.*")))
        close_button()
        label = tk.Label(frame, text=filename_from_path(filename))
        label.pack()
        FILENAME.append(filename)
        open_pdf(filename)

# Open File Button
open_file = tk.Button(root, text="Open a File", padx=30, pady=5, fg="white", bg="#5C1010", justify="center", command=add_file)
open_file.pack()

# Returns "file name + .extension" 
def filename_from_path(file):
    file_split = file.split("/")
    return file_split[-1]

# Starts Text-to-Speech Process
def generate_tts():
    if PDF_STATUS[-1]:
        audio_reader = pyttsx3.init()
        with open(FILENAME[-1], "rb") as file:
            my_pdf = PyPDF3.PdfFileReader(file)
            pages = my_pdf.numPages
            my_text = ""
            for num in range(pages):
                page = my_pdf.getPage(num)
                my_text += page.extractText()
        global audiobook_name
        audiobook_name = filename_from_path(FILENAME[-1]).split(".")[0].title() + " Audiobook.mp3"
        audio_reader.save_to_file(my_text, audiobook_name)
        audio_reader.runAndWait()
        popup_msg(f"Successfully generated MP3 file \"{audiobook_name}\"")

        
# Generates popup window after creating MP3 file
def popup_msg(msg):
    popup = tk.Tk()
    popup.title("Read Aloud")
    popup.iconbitmap("ReadAloud_icon.ico")
    popup.geometry("1000x100")
    popup.config(bg="darkgreen")
    label = tk.Label(popup, text=msg, font="Helvetica 18")
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="OK", command=popup.destroy)
    B1.pack(pady=5, padx=5)
    popup.mainloop()

# Opens PDF in frame
def open_pdf(file):
    pdf_var = pdf.ShowPdf()
    # Clears any previous PDF images before loading new file
    pdf_var.img_object_li.clear()
    set_pdf = pdf_var.pdf_view(frame, file_location = file, width = 120, height = 120)
    set_pdf.pack()
    # Creates read aloud button
    if not READ_ALOUD_STATUS[-1]:
        read_aloud = tk.Button(root, text="Generate Audiobook", padx=5, pady=12, fg="white", bg="#4B1B5B", justify="center", command=generate_tts)
        read_aloud.pack()
        READ_ALOUD_STATUS.append(True)
    PDF_STATUS.append(True)

def close_button():
    close_file = tk.Button(frame, text="Close File", padx=20, pady=7, fg="white", bg="black", command=close)
    close_file.pack()

def close():
    for widget in frame.winfo_children():
        widget.destroy()
    FILENAME.clear()
    PDF_STATUS.append(False)

root.mainloop()