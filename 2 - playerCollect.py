import tkinter as TK
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import random
import openpyxl as openpyxl

playerDataTable = pd.DataFrame()

def openStartPage():
    workingDir = os.path.join(os.getcwd(), "FinalProject", "1 - savedDataFile.py")
    subprocess.Popen(["python", workingDir])
    warning.destroy()
    playerDataWindow.destroy()


def wipePlayerData():
    if os.path.exists("playerData.xlsx"):
        os.remove("playerData.xlsx")
    warning.destroy()
    playerDataWindow.deiconify()


def clearFields():
    entryCharacterName.delete(0, TK.END)
    entryInitiativeBonus.delete(0, TK.END)
    entryDexterityBonus.delete(0, TK.END)
    entryDexterityScore.delete(0, TK.END)
    entryHitPoints.delete(0, TK.END)

def savePlayer():

    global playerDataTable

    characterName = str(entryCharacterName.get()).strip()

    try: initiativeBonus = int(entryInitiativeBonus.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your initiative bonus!")
        entryInitiativeBonus.delete(0, TK.END)
        return
    
    if initiativeBonus < -10 or initiativeBonus > 20:
        messagebox.showwarning("Stop", f"An Initiative bonus of {initiativeBonus} is out of range.")
        entryInitiativeBonus.delete(0, TK.END)
        return

    try: dexterityBonus = int(entryDexterityBonus.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your dexterity bonus!")
        entryDexterityBonus.delete(0, TK.END)
        return
    
    if dexterityBonus < -6 or dexterityBonus > 6:
        messagebox.showwarning("Stop", f"A Dexterity bonus of {dexterityBonus} is out of range.")
        entryDexterityBonus.delete(0, TK.END)
        return

    try: dexterityScore = int(entryDexterityScore.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your dexterity score!")
        entryDexterityScore.delete(0, TK.END)
        return
    
    if dexterityScore < 1 or dexterityScore > 30:
        messagebox.showwarning("Stop", f"A Dexterity score of {dexterityScore} is out of range.")
        entryDexterityScore.delete(0, TK.END)
        return
    
    try: hitPoints = int(entryHitPoints.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your Hit Points!")
        entryHitPoints.delete(0, TK.END)
        return
    
    if hitPoints < 1 or hitPoints > 800:
        messagebox.showwarning("Stop", f"{hitPoints} Hit Points is out of range.")
        entryHitPoints.delete(0, TK.END)
        return
    
    diceRoll = 0
    initiativeTotal = initiativeBonus + diceRoll


    newPlayerDataTable = pd.DataFrame({
        "Character Name" : [characterName],
        "Initiative Total" : [initiativeTotal],
        "Initiative Bonus" : [initiativeBonus],
        "Dice Roll" : [diceRoll],
        "Dexterity Bonus" : [dexterityBonus],
        "Dexterity Score" : [dexterityScore],
        "Hit Points" : [hitPoints],
        "Bad" : 0,
        "Good" : 1,
        "Spell Effects" : None,
        "Spell Expirations" : None 
    })
    newPlayerDataTable['Spell Effects'] = newPlayerDataTable['Spell Effects'].astype(object)
    newPlayerDataTable['Spell Expirations'] = newPlayerDataTable['Spell Expirations'].astype(object)
    
    playerDataTable = pd.concat([newPlayerDataTable, playerDataTable], ignore_index=True)

    messagebox.showinfo("Saved", "Player Information Saved")
    clearFields()
    


def openEnemyCollect():
    global combinedData
    with pd.ExcelWriter("playerData.xlsx", engine="openpyxl") as fileWriter:
        playerDataTable.to_excel(fileWriter, index=False)
    workingDir = os.path.join(os.getcwd(), "FinalProject", "3 - enemyCollect.py")
    subprocess.Popen(["python", workingDir])
    playerDataWindow.quit()

warning = TK.Tk()
warning.title("Warning!")

warningText = TK.Label(warning, text="If you continue, any existing player data will be deleted.", bg = "white", bd = 2, font = "Helvetica", height = 3, width = 30, wraplength=250)
warningText.grid(row = 0, column = 0, padx = 2, pady = 2, columnspan= 3)
warningText.grid_rowconfigure(0, weight= 1)
warningText.grid_columnconfigure(0, weight= 1)

yesButton = TK.Button(warning, text = "Yes, continue", width = 35, command = wipePlayerData)
yesButton.grid(row = 7, column = 0, padx = 2, pady = 2, columnspan= 3)
warningText.grid_rowconfigure(7, weight= 1)

noButton = TK.Button(warning, text = "No, go back.", width = 35, command = openStartPage)
noButton.grid(row = 8, column = 0, padx = 2, pady = 2, columnspan= 3)
warningText.grid_rowconfigure(8, weight= 1)    


playerDataWindow = TK.Tk()
playerDataWindow.withdraw()

playerDataWindow.geometry("250x300")
playerDataWindow.title("Add Player Data")
playerDataWindow.configure(background="blue")

labelCharacterName = TK.Label(playerDataWindow, height = 2, width = 15, text = "Character Name: ")
labelCharacterName.grid(row = 1, column = 0, padx = 2, pady = 2)
labelInitiativeBonus = TK.Label(playerDataWindow, height = 2, width = 15, text = "Initiative Bonus: ")
labelInitiativeBonus.grid(row = 2, column = 0, padx = 2, pady = 2)
labelDexterityBonus = TK.Label(playerDataWindow, height = 2, width = 15, text = "Dexterity Bonus: ")
labelDexterityBonus.grid(row = 3, column = 0, padx = 2, pady = 2)
labelDexterityScore = TK.Label(playerDataWindow, height = 2, width = 15, text = "Dexterity Score: ")
labelDexterityScore.grid(row = 4, column = 0, padx = 2, pady = 2)
labelHitPoints = TK.Label(playerDataWindow, height = 2, width = 15, text = "Hit Points: ")
labelHitPoints.grid(row = 5, column = 0, padx = 2, pady = 2)

entryCharacterName = TK.Entry(playerDataWindow)
entryCharacterName.grid(row = 1, column = 1, padx = 2, pady = 2)
entryInitiativeBonus = TK.Entry(playerDataWindow)
entryInitiativeBonus.grid(row = 2, column = 1, padx = 2, pady = 2)
entryDexterityBonus = TK.Entry(playerDataWindow)
entryDexterityBonus.grid(row = 3, column = 1, padx = 2, pady = 2)
entryDexterityScore = TK.Entry(playerDataWindow)
entryDexterityScore.grid(row = 4, column = 1, padx = 2, pady = 2)
entryHitPoints = TK.Entry(playerDataWindow)
entryHitPoints.grid(row = 5, column = 1, padx = 2, pady = 2)

commitButton = TK.Button(playerDataWindow, text = "Add Character", command = savePlayer)
commitButton.grid(row = 6, column = 0, padx = 2, pady = 2)

resetButton = TK.Button(playerDataWindow, text = "Reset Fields", command = clearFields)
resetButton.grid(row = 6, column = 1, padx = 2, pady = 2)

doneButton = TK.Button(playerDataWindow, text = "Done Adding Characters", command = openEnemyCollect)
doneButton.grid(row = 7, columnspan = 2, padx = 2, pady = 2)

playerDataWindow.mainloop()