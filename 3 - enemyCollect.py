import tkinter as TK
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import random
import openpyxl as openpyxl


enemyDataTable = pd.DataFrame()

if os.path.exists("enemyData.xlsx"):
    os.remove("enemyData.xlsx")

def clearFields():
    entryEnemyName.delete(0, TK.END)
    entryEnemyInitiativeBonus.delete(0, TK.END)
    entryEnemyDexterityBonus.delete(0, TK.END)
    entryEnemyDexterityScore.delete(0, TK.END)
    entryEnemyHitPoints.delete(0, TK.END)

def saveBadGuys():

    global enemyDataTable

    enemyName = str(entryEnemyName.get()).strip()

    try: enemyInitiativeBonus = int(entryEnemyInitiativeBonus.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your initiative bonus!")
        entryEnemyInitiativeBonus.delete(0, TK.END)
        return
    
    if enemyInitiativeBonus < -10 or enemyInitiativeBonus > 20:
        messagebox.showwarning("Stop", "Your Initiative bonus is out of range.")
        entryEnemyInitiativeBonus.delete(0, TK.END)
        return

    try: enemyDexterityBonus = int(entryEnemyDexterityBonus.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your dexterity bonus!")
        entryEnemyDexterityBonus.delete(0, TK.END)
        return
    
    if enemyDexterityBonus < -10 or enemyDexterityBonus > 10:
        messagebox.showwarning("Stop", "Your Dexterity bonus is out of range.")
        entryEnemyDexterityBonus.delete(0, TK.END)
        return

    try: enemyDexterityScore = int(entryEnemyDexterityScore.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your dexterity score!")
        entryEnemyDexterityScore.delete(0, TK.END)
        return
    
    if enemyDexterityScore < 1 or enemyDexterityScore > 30:
        messagebox.showwarning("Stop", f"A Dexterity score of {enemyDexterityScore} is out of range.")
        entryEnemyDexterityScore.delete(0, TK.END)
        return
    
    try: enemyHitPoints = int(entryEnemyHitPoints.get())
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your Hit Points!")
        entryEnemyHitPoints.delete(0, TK.END)
        return
    
    if enemyHitPoints < 1 or enemyHitPoints > 1500:
        messagebox.showwarning("Stop", f"{enemyHitPoints} Hit Points is out of range.")
        entryEnemyHitPoints.delete(0, TK.END)
        return
    
    enemyDiceRoll = 0
    enemyInitiativeTotal = enemyInitiativeBonus + enemyDiceRoll


  
    newEnemyDataTable = pd.DataFrame({
        "Character Name" : [enemyName],
        "Initiative Total" : [enemyInitiativeTotal],
        "Initiative Bonus" : [enemyInitiativeBonus],
        "Dice Roll" : [enemyDiceRoll],
        "Dexterity Bonus" : [enemyDexterityBonus],
        "Dexterity Score" : [enemyDexterityScore],
        "Hit Points" : [enemyHitPoints],
        "Bad" : 1,
        "Good" : 0,
        "Spell Effects" : None,
        "Spell Expirations" : None
    })
    newEnemyDataTable['Spell Effects'] = newEnemyDataTable['Spell Effects'].astype(object)
    newEnemyDataTable['Spell Expirations'] = newEnemyDataTable['Spell Expirations'].astype(object)
    
    
    enemyDataTable = pd.concat([newEnemyDataTable, enemyDataTable], ignore_index=True)

    messagebox.showinfo("Saved", "Enemy Information Saved")
    clearFields()

def combineFiles():
    with pd.ExcelWriter("enemyData.xlsx", engine="openpyxl") as fileWriter:
        enemyDataTable.to_excel(fileWriter, index=False)
    workingDir = os.path.join(os.getcwd(), "FinalProject", "4 - combineAndDice.py")
    subprocess.Popen(["python", workingDir])
    enemyDataWindow.quit()


enemyDataWindow = TK.Tk()

enemyDataWindow.geometry("250x350")
enemyDataWindow.title("Add Enemy Data")
enemyDataWindow.configure(background="red")

labelEnemyName = TK.Label(enemyDataWindow, height = 2, width = 15, text = "Enemy Name: ")
labelEnemyName.grid(row = 1, column = 0, padx = 2, pady = 2)
labelenemyInitiativeBonus = TK.Label(enemyDataWindow, height = 2, width = 15, text = "Initiative Bonus: ")
labelenemyInitiativeBonus.grid(row = 2, column = 0, padx = 2, pady = 2)
labelenemyDexterityBonus = TK.Label(enemyDataWindow, height = 2, width = 15, text = "Dexterity Bonus: ")
labelenemyDexterityBonus.grid(row = 3, column = 0, padx = 2, pady = 2)
labelenemyDexterityScore = TK.Label(enemyDataWindow, height = 2, width = 15, text = "Dexterity Score: ")
labelenemyDexterityScore.grid(row = 4, column = 0, padx = 2, pady = 2)
labelenemyHitPoints = TK.Label(enemyDataWindow, height = 2, width = 15, text = "Hit Points: ")
labelenemyHitPoints.grid(row = 5, column = 0, padx = 2, pady = 2)


entryEnemyName = TK.Entry(enemyDataWindow)
entryEnemyName.grid(row = 1, column = 1, padx = 2, pady = 2)
entryEnemyInitiativeBonus = TK.Entry(enemyDataWindow)
entryEnemyInitiativeBonus.grid(row = 2, column = 1, padx = 2, pady = 2)
entryEnemyDexterityBonus = TK.Entry(enemyDataWindow)
entryEnemyDexterityBonus.grid(row = 3, column = 1, padx = 2, pady = 2)
entryEnemyDexterityScore = TK.Entry(enemyDataWindow)
entryEnemyDexterityScore.grid(row = 4, column = 1, padx = 2, pady = 2)
entryEnemyHitPoints = TK.Entry(enemyDataWindow)
entryEnemyHitPoints.grid(row = 5, column = 1, padx = 2, pady = 2)

commitButton = TK.Button(enemyDataWindow, text = "Add Enemy", command = saveBadGuys)
commitButton.grid(row = 6, column = 0, padx = 2, pady = 2)

resetButton = TK.Button(enemyDataWindow, text = "Reset Fields", command = clearFields)
resetButton.grid(row = 6, column = 1, padx = 2, pady = 2)

doneButton = TK.Button(enemyDataWindow, text = "Done Adding Enemies", command = combineFiles)
doneButton.grid(row = 7, columnspan = 2, padx = 2, pady = 2)



enemyDataWindow.mainloop()