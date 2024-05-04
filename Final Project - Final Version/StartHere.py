import tkinter as TK
from tkinter import messagebox
import subprocess
import pandas as pd
import openpyxl as openpyxl
import os

#defines the locations of files and subfolders

def openEnemyCollect():
    currentDir = os.path.dirname(__file__)
    enemyCollect = os.path.join(currentDir,"SubProcesses", "enemyCollect.py")
    subprocess.Popen(["python",enemyCollect])
    quit()

def openPlayerCollect():
    currentDir = os.path.dirname(__file__)
    playerCollect = os.path.join(currentDir,"SubProcesses", "playerCollect.py")
    subprocess.Popen(["python",playerCollect])
    quit()


#A warning window that allows the user to skip past entering player data
#Since player data doesn't often change

savedFileCheck = TK.Tk()

savedFileCheck.geometry("300x230")
savedFileCheck.title("File Check")
savedFileCheck.configure(background="light gray")

windowText = TK.Label(savedFileCheck, text="Do you have a saved player file?", bg = "light gray", font = "Helvetica 16", wraplength=280)
windowText.place(x=10, y=10, width=280, height=100)

yesButton = TK.Button(savedFileCheck, text = "Yes, I only need to enter enemy information", width = 35, command = lambda: openEnemyCollect())
yesButton.place(x=10, y=110, width=280, height=30)

noButton = TK.Button(savedFileCheck, text = "No, I need to add player information", width = 35, command = lambda: openPlayerCollect())
noButton.place(x=10, y=150, width=280, height=30)

exitButton = TK.Button(savedFileCheck, text = "Actually, I don't feel like doing combat today", width = 35, command = lambda: quit())
exitButton.place(x=10, y=190, width=280, height=30)

savedFileCheck.mainloop()