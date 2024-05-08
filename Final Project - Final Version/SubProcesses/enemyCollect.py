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

def wipeEnemyData():
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    oldEnemyFile = os.path.join(parentDir,"SpreadSheets","enemyData.xlsx")
    if os.path.exists(oldEnemyFile):
        os.remove(oldEnemyFile)
    enemyDataWindow.deiconify()


def clearFields():
    entryEnemyName.delete(0, tk.END)
    entryEnemyInitiativeBonus.delete(0, tk.END)
    entryEnemyDexterityBonus.delete(0, tk.END)
    entryEnemyDexterityScore.delete(0, tk.END)
    entryEnemyHitPoints.delete(0, tk.END)

def clearDexInit():
    entryEnemyInitiativeBonus.delete(0, tk.END)
    entryEnemyDexterityBonus.delete(0, tk.END)

def clearDexAndBonus():
    entryEnemyDexterityBonus.delete(0, tk.END)
    entryEnemyDexterityScore.delete(0, tk.END)

def initDexCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified):

    bonusWarningWindow = tk.Tk()
    bonusWarningWindow.geometry("280x210")
    bonusWarningWindow.title("Warning!")
    bonusWarningWindow.config(bg="mistyrose")
    bonusWarningWindowText1 = tk.Label(bonusWarningWindow, wraplength=240, font="helvetica 12 bold", bg="mistyrose", 
                                    text=f"You entered an initiative bonus of {enemyInitiativeBonus}, and a dexterity bonus of {enemyDexterityBonus}.\n\nThey seem a little far apart, are you sure you entered the correct info?")
    bonusWarningWindowText1.place(x=10, y=10, width=260, height=110)

    confirmButton = tk.Button(bonusWarningWindow, text="That is correct", command= lambda: [saveEnemy(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, "Y", dexVerified), bonusWarningWindow.withdraw()])
    confirmButton.place(x=10, y=130, height=30, width=260)

    cancelButton = tk.Button(bonusWarningWindow, text="Oops, I need to correct that", command= lambda: [clearDexInit(), bonusWarningWindow.withdraw()])
    cancelButton.place(x=10, y=170, height=30, width=260)

def dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified):

    dexBonusWarningWindow = tk.Tk()
    dexBonusWarningWindow.geometry("280x310")
    dexBonusWarningWindow.title("Warning!")
    dexBonusWarningWindow.config(bg="mistyrose")
    dexBonusWarningWindowText1 = tk.Label(dexBonusWarningWindow, wraplength=240, font="helvetica 12 bold", bg="mistyrose", 
                                    text=f"You entered an dexterity bonus of {enemyDexterityBonus}, and a dexterity score of {enemyDexterityScore}.\n\nThey seem a little far apart, are you sure you entered the correct info?")
    dexBonusWarningWindowText1.place(x=10, y=10, width=260, height=210)

    confirmButton = tk.Button(dexBonusWarningWindow, text="That is correct", command= lambda: [saveEnemy(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, "Y"), dexBonusWarningWindow.withdraw()])
    confirmButton.place(x=10, y=230, height=30, width=260)

    cancelButton = tk.Button(dexBonusWarningWindow, text="Oops, I need to correct that", command= lambda: [clearDexAndBonus(), dexBonusWarningWindow.withdraw()])
    cancelButton.place(x=10, y=270, height=30, width=260)

def saveEnemy(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified):



    #Error checking by both data type, and ranges

    enemyName = str(enemyName).strip()
    if len(enemyName) > 64:
        messagebox.showerror("Error", "You enemy name is too long!")
        entryEnemyName.delete(0, tk.END)
        return

    try: enemyInitiativeBonus = int(enemyInitiativeBonus)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your initiative bonus!")
        entryEnemyInitiativeBonus.delete(0, tk.END)
        return
    
    if enemyInitiativeBonus < -10 or enemyInitiativeBonus > 20:
        messagebox.showerror("Error", "Your Initiative bonus is out of range.")
        entryEnemyInitiativeBonus.delete(0, tk.END)
        return

    try: enemyDexterityBonus = int(enemyDexterityBonus)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity bonus!")
        entryEnemyDexterityBonus.delete(0, tk.END)
        return
    
    if enemyDexterityBonus < -10 or enemyDexterityBonus > 10:
        messagebox.showerror("Error", "Your Dexterity bonus is out of range.")
        entryEnemyDexterityBonus.delete(0, tk.END)
        return

    try: enemyDexterityScore = int(enemyDexterityScore)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity score!")
        entryEnemyDexterityScore.delete(0, tk.END)
        return
    
    if enemyDexterityScore < 1 or enemyDexterityScore > 30:
        messagebox.showerror("Error", f"A Dexterity score of {enemyDexterityScore} is out of range.")
        entryEnemyDexterityScore.delete(0, tk.END)
        return
    
    try: enemyHitPoints = int(enemyHitPoints)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your Hit Points!")
        entryEnemyHitPoints.delete(0, tk.END)
        return
    
    if enemyHitPoints < 1 or enemyHitPoints > 1500:
        messagebox.showerror("Error", f"{enemyHitPoints} Hit Points is out of range.")
        entryEnemyHitPoints.delete(0, tk.END)
        return
    
    if abs(enemyInitiativeBonus-enemyDexterityBonus) >= 2 and initVerified !="Y":
        initDexCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        return
    else: initVerified = "Y"


    if dexVerified != "Y":
        if enemyDexterityScore == 30 and enemyDexterityBonus != 10:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 28 and enemyDexterityScore < 30 and enemyDexterityBonus != 9:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 26 and enemyDexterityScore < 28 and enemyDexterityBonus != 8:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 24 and enemyDexterityScore < 26 and enemyDexterityBonus != 7:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 22 and enemyDexterityScore < 24 and enemyDexterityBonus != 6:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 20 and enemyDexterityScore < 22 and enemyDexterityBonus != 5:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 18 and enemyDexterityScore < 20 and enemyDexterityBonus != 4:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 16 and enemyDexterityScore < 18 and enemyDexterityBonus != 3:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 14 and enemyDexterityScore < 16 and enemyDexterityBonus != 2:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 12 and enemyDexterityScore < 14 and enemyDexterityBonus != 1:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore >= 10 and enemyDexterityScore < 12 and enemyDexterityBonus != 0:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)      
        elif enemyDexterityScore <= 9 and enemyDexterityScore > 7 and enemyDexterityBonus != -1:
           dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore <= 7 and enemyDexterityScore > 5 and enemyDexterityBonus != -2:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore <= 5 and enemyDexterityScore > 3 and enemyDexterityBonus != -3:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore <= 3 and enemyDexterityScore > 1 and enemyDexterityBonus != -4:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        elif enemyDexterityScore == 1 and enemyDexterityBonus != -5:
            dexBonusCompare(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints, initVerified, dexVerified)
        else: writeToTable(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints)
    else:
        writeToTable(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints)





def writeToTable(enemyName, enemyInitiativeBonus, enemyDexterityBonus, enemyDexterityScore, enemyHitPoints):
    global enemyDataTable
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
def combineFiles(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified):
    if initVerified == "Q":
        writeToExcel()
    if name != "" and initiativeBonus != "" and dexterityBonus != "" and dexterityScore != "" and hitPoints != "":
        saveEnemy(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
    elif name != "" or initiativeBonus != "" or dexterityBonus !="" or dexterityScore != "" or hitPoints !="" or initVerified !="N" or dexVerified !="N":
        messagebox.showerror("Error","Didn't fill in all the fields!")
        clearFields()
        return
    elif len(enemyDataTable) <1:
        messagebox.showerror("Error","You didn't enter any enemy information!")
        clearFields()
        return
    else:
        writeToExcel()    

    

#Writing the data table to an Excel file
def writeToExcel():
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    fileName = "enemyData.xlsx"
    savedFile = os.path.join(parentDir,"SpreadSheets", fileName)
    with pd.ExcelWriter(savedFile, engine="openpyxl") as fileWriter:
        enemyDataTable.to_excel(fileWriter, index=False)
    combineAndDice = os.path.join(currentDir, "combineAndDice.py")
    subprocess.Popen(["python", combineAndDice])
    quit()

warning = tk.Tk()
warning.geometry("300x190")
warning.title("Warning!")
warning.configure(background="red")

warningText = tk.Label(warning, text="Warning! Any existing enemy data will be deleted!", bg = "red", font = "Helvetica 16 bold", wraplength=280, anchor="w")
warningText.place(x=10, y=10, width=280, height=100)

yesButton = tk.Button(warning, text = "Yes, continue", width = 35, command = lambda: [wipeEnemyData(), warning.withdraw()])
yesButton.place(x=10, y=110, width=280, height=30)

noButton = tk.Button(warning, text = "Keep it and move to the next step.", width = 35, command = lambda: [combineFiles("","","","","","Q","Q"), warning.withdraw()])
noButton.place(x=10, y=150, width=280, height=30)


enemyDataWindow = tk.Tk()
enemyDataWindow.withdraw()
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

commitButton = tk.Button(enemyDataWindow, text = "Add Enemy", font="Helvetica 12", command = lambda: saveEnemy(entryEnemyName.get(),
                                                                                                                entryEnemyInitiativeBonus.get(),
                                                                                                                entryEnemyDexterityBonus.get(),
                                                                                                                entryEnemyDexterityScore.get(),
                                                                                                                entryEnemyHitPoints.get(),
                                                                                                                "N",
                                                                                                                "N"
                                                                                                                ))
                                                                                #Passing user inputs as arguments

commitButton.place(x=10, y=280, width= 185, height=40)

resetButton = tk.Button(enemyDataWindow, text = "Reset Fields", font="Helvetica 12", command = lambda: clearFields)
resetButton.place(x=205, y=280, width= 185, height=40)

doneButton = tk.Button(enemyDataWindow, text = "Done Adding Enemies", font="Helvetica 12 bold", command = lambda: combineFiles(entryEnemyName.get(), 
                                                                                                                               entryEnemyInitiativeBonus.get(), 
                                                                                                                               entryEnemyInitiativeBonus.get(), 
                                                                                                                               entryEnemyDexterityScore.get(), 
                                                                                                                               entryEnemyHitPoints.get(),
                                                                                                                               "N",
                                                                                                                               "N"
                                                                                                                               ))
doneButton.place(x=10, y=340, width= 380, height=40)



enemyDataWindow.mainloop()