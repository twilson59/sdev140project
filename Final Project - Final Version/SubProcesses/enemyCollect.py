import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import openpyxl as openpyxl

#Initializing a pandas dataframe
enemyDataTable = pd.DataFrame({
        "Character Name" : [],
        "Initiative Total" : [],
        "Initiative Bonus" : [],
        "Dice Roll" : [],
        "Dexterity Bonus" : [],
        "Dexterity Score" : [],
        "Hit Points" : [],
        "Bad" : None,
        "Good" : None,
        "Spell Effects" : None,
        "Spell Expirations" : None 
    })

#Defining file and folder locations
currentDir = os.path.dirname(__file__)
parentDir = os.path.dirname(currentDir)
oldEnemyFile = os.path.join(parentDir,"SpreadSheets","enemyData.xlsx")
if os.path.exists(oldEnemyFile):
        os.remove(oldEnemyFile)


def clearFields():
    entryEnemyName.delete(0, tk.END)
    entryEnemyInitiativeBonus.delete(0, tk.END)
    entryEnemyDexterityBonus.delete(0, tk.END)
    entryEnemyDexterityScore.delete(0, tk.END)
    entryEnemyHitPoints.delete(0, tk.END)

def saveBadGuys(enemyName, initiativeBonus, dexterityBonus, dexterityScore, hitPoints):

    global enemyDataTable

    #Error checking by both data type, and ranges

    enemyName = str(enemyName).strip()
    if len(enemyName) > 64:
        messagebox.showerror("Error", "You enemy name is too long!")
        entryEnemyName.delete(0, tk.END)
        return

    try: enemyInitiativeBonus = int(initiativeBonus)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your initiative bonus!")
        entryEnemyInitiativeBonus.delete(0, tk.END)
        return
    
    if enemyInitiativeBonus < -10 or enemyInitiativeBonus > 20:
        messagebox.showerror("Error", "Your Initiative bonus is out of range.")
        entryEnemyInitiativeBonus.delete(0, tk.END)
        return

    try: enemyDexterityBonus = int(dexterityBonus)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity bonus!")
        entryEnemyDexterityBonus.delete(0, tk.END)
        return
    
    if enemyDexterityBonus < -10 or enemyDexterityBonus > 10:
        messagebox.showerror("Error", "Your Dexterity bonus is out of range.")
        entryEnemyDexterityBonus.delete(0, tk.END)
        return

    try: enemyDexterityScore = int(dexterityScore)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity score!")
        entryEnemyDexterityScore.delete(0, tk.END)
        return
    
    if enemyDexterityScore < 1 or enemyDexterityScore > 30:
        messagebox.showerror("Error", f"A Dexterity score of {enemyDexterityScore} is out of range.")
        entryEnemyDexterityScore.delete(0, tk.END)
        return
    
    try: enemyHitPoints = int(hitPoints)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your Hit Points!")
        entryEnemyHitPoints.delete(0, tk.END)
        return
    
    if enemyHitPoints < 1 or enemyHitPoints > 1500:
        messagebox.showerror("Error", f"{enemyHitPoints} Hit Points is out of range.")
        entryEnemyHitPoints.delete(0, tk.END)
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
     
    enemyDataTable = pd.concat([newEnemyDataTable, enemyDataTable], ignore_index=True)

    messagebox.showinfo("Saved", "Enemy Information Saved")
    clearFields()

#Checking for a 0 length file
def combineFiles(enemyDataTable):
    if len(enemyDataTable) <1:
        messagebox.showerror("Error","You didn't enter any enemy information!")
        clearFields()
        return
    

#Writing the data table to an Excel file
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    fileName = "enemyData.xlsx"
    savedFile = os.path.join(parentDir,"SpreadSheets", fileName)
    with pd.ExcelWriter(savedFile, engine="openpyxl") as fileWriter:
        enemyDataTable.to_excel(fileWriter, index=False)
    combineAndDice = os.path.join(currentDir, "combineAndDice.py")
    subprocess.Popen(["python", combineAndDice])
    quit()


enemyDataWindow = tk.Tk()

enemyDataWindow.geometry("400x390")
enemyDataWindow.title("Add Enemy Data")
enemyDataWindow.configure(background="tomato")

labelHeader = tk.Label(enemyDataWindow, text = "Adding Enemy Info", background="tomato", font="Helvetica 14", wraplength=380)
labelHeader.place(x=10, y=10, width=380, height=50)

labelEnemyName = tk.Label(enemyDataWindow, text = "Enemy Name: ", background="tomato", font="Helvetica 12")
labelEnemyName.place(x=10, y=70, width=150, height=30)
labelenemyInitiativeBonus = tk.Label(enemyDataWindow, text = "Initiative Bonus: ", background="tomato", font="Helvetica 12")
labelenemyInitiativeBonus.place(x=10, y=110, width=150, height=30)
labelenemyDexterityBonus = tk.Label(enemyDataWindow, text = "Dexterity Bonus: ", background="tomato", font="Helvetica 12")
labelenemyDexterityBonus.place(x=10, y=150, width=150, height=30)
labelenemyDexterityScore = tk.Label(enemyDataWindow, text = "Dexterity Score: ", background="tomato", font="Helvetica 12")
labelenemyDexterityScore.place(x=10, y=190, width=150, height=30)
labelenemyHitPoints = tk.Label(enemyDataWindow, text = "Hit Points: ", background="tomato", font="Helvetica 12")
labelenemyHitPoints.place(x=10, y=230, width=150, height=30)


entryEnemyName = tk.Entry(enemyDataWindow, font="Helvetica 12")
entryEnemyName.place(x=160, y=70, width=230, height=30)
entryEnemyInitiativeBonus = tk.Entry(enemyDataWindow, font="Helvetica 12")
entryEnemyInitiativeBonus.place(x=160, y=110, width=230, height=30)
entryEnemyDexterityBonus = tk.Entry(enemyDataWindow, font="Helvetica 12")
entryEnemyDexterityBonus.place(x=160, y=150, width=230, height=30)
entryEnemyDexterityScore = tk.Entry(enemyDataWindow, font="Helvetica 12")
entryEnemyDexterityScore.place(x=160, y=190, width=230, height=30)
entryEnemyHitPoints = tk.Entry(enemyDataWindow, font="Helvetica 12")
entryEnemyHitPoints.place(x=160, y=230, width=230, height=30)

commitButton = tk.Button(enemyDataWindow, text = "Add Enemy", font="Helvetica 12", command = lambda: saveBadGuys(entryEnemyName.get(),
                                                                                                                entryEnemyInitiativeBonus.get(),
                                                                                                                entryEnemyDexterityBonus.get(),
                                                                                                                entryEnemyDexterityScore.get(),
                                                                                                                entryEnemyHitPoints.get()
                                                                                                                ))
                                                                                #Passing user inputs as arguments

commitButton.place(x=10, y=280, width= 185, height=40)

resetButton = tk.Button(enemyDataWindow, text = "Reset Fields", font="Helvetica 12", command = lambda: clearFields)
resetButton.place(x=205, y=280, width= 185, height=40)

doneButton = tk.Button(enemyDataWindow, text = "Done Adding Enemies", font="Helvetica 12 bold", command = lambda: combineFiles(enemyDataTable))
doneButton.place(x=10, y=340, width= 380, height=40)



enemyDataWindow.mainloop()