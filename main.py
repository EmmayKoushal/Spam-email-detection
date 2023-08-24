import sys
import os
from tkinter import *

window=Tk()

window.title("Malicious URL detecting Tool from emails")
window.geometry('550x200')

def run():
    os.system('python3 detection.py')

btn = Button(window, text="Start Tool", bg="black", fg="white",command=run)
btn.grid(column=100, row=10)

window.mainloop()
