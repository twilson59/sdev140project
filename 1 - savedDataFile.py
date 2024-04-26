import tkinter as TK
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import random
import openpyxl as openpyxl

def openEnemyCollect():
    workingDir = os.path.join(os.getcwd(), "FinalProject", "3 - enemyCollect.py")
    subprocess.Popen(["python", workingDir])
    savedFileCheck.quit()

def openPlayerCollect():
    workingDir = os.path.join(os.getcwd(), "FinalProject", "2 - playerCollect.py")
    subprocess.Popen(["python", workingDir])
    savedFileCheck.quit()

savedFileCheck = TK.Tk()

savedFileCheck.geometry("300x300")
savedFileCheck.title("Addition")
savedFileCheck.configure(background="gray")

windowText = TK.Label(savedFileCheck, text="Do you have a saved player file?", bg = "white", bd = 2, font = "Helvetica", height = 3, width = 30, wraplength=250)
windowText.grid(row = 0, column = 0, padx = 2, pady = 2, columnspan= 3)
savedFileCheck.grid_rowconfigure(0, weight= 1)
savedFileCheck.grid_columnconfigure(0, weight= 1)

noButton = TK.Button(savedFileCheck, text = "No, I need to add player information", width = 35, command = openPlayerCollect)
noButton.grid(row = 6, column = 0, padx = 2, pady = 2, columnspan= 3)
savedFileCheck.grid_rowconfigure(6, weight= 1)

yesButton = TK.Button(savedFileCheck, text = "Yes, I only need to enter enemy information", width = 35, command = openEnemyCollect)
yesButton.grid(row = 7, column = 0, padx = 2, pady = 2, columnspan= 3)
savedFileCheck.grid_rowconfigure(7, weight= 1)

noButton = TK.Button(savedFileCheck, text = "Actually, I don't feel like doing combat today.", width = 35, command = quit)
noButton.grid(row = 8, column = 0, padx = 2, pady = 2, columnspan= 3)
savedFileCheck.grid_rowconfigure(8, weight= 1)

savedFileCheck.mainloop()