import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import openpyxl as openpyxl

#Initializing the structure of my dataframe

playerDataTable = pd.DataFrame({
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

#Defininig folder and file locations
def openStartPage():
    currentDir = os.path.dirname(__file__)  #gets path of the folder where the script is running
    parentDir = os.path.dirname(currentDir) #gets the folder in which the current folder is located
    startFile = os.path.join(parentDir, "StartHere.py")  #location of the start script
    subprocess.Popen(["python",startFile])  #opens the file
    quit()

#locating and deleting the existing player data if requested
def wipePlayerData():
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    sheetsDir = os.path.join(parentDir, "SpreadSheets")
    oldPlayerFile = os.path.join(parentDir,sheetsDir,"playerData.xlsx")
    if os.path.exists(oldPlayerFile):
        os.remove(oldPlayerFile)
    warning.destroy()
    playerDataWindow.deiconify()

#Clears the text boxes
def clearFields():
    entryCharacterName.delete(0, tk.END)
    entryInitiativeBonus.delete(0, tk.END)
    entryDexterityBonus.delete(0, tk.END)
    entryDexterityScore.delete(0, tk.END)
    entryHitPoints.delete(0, tk.END)

def clearDexInit():
    entryInitiativeBonus.delete(0, tk.END)
    entryDexterityBonus.delete(0, tk.END)

def clearDexAndBonus():
    entryDexterityBonus.delete(0, tk.END)
    entryDexterityScore.delete(0, tk.END)


def initDexCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified):

    bonusWarningWindow = tk.Tk()
    bonusWarningWindow.geometry("280x210")
    bonusWarningWindow.title("Warning!")
    bonusWarningWindow.config(bg="mistyrose")
    bonusWarningWindowText1 = tk.Label(bonusWarningWindow, wraplength=240, font="helvetica 12 bold", bg="mistyrose", 
                                    text=f"You entered an initiative bonus of {initiativeBonus}, and a dexterity bonus of {dexterityBonus}.\n\nThey seem a little far apart, are you sure you entered the correct info?")
    bonusWarningWindowText1.place(x=10, y=10, width=260, height=110)

    confirmButton = tk.Button(bonusWarningWindow, text="That is correct", command= lambda: [savePlayer(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, "Y", dexVerified), bonusWarningWindow.withdraw()])
    confirmButton.place(x=10, y=130, height=30, width=260)

    cancelButton = tk.Button(bonusWarningWindow, text="Oops, I need to correct that", command= lambda: [clearDexInit(), bonusWarningWindow.withdraw()])
    cancelButton.place(x=10, y=170, height=30, width=260)


def dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified):

    dexBonusWarningWindow = tk.Tk()
    dexBonusWarningWindow.geometry("280x310")
    dexBonusWarningWindow.title("Warning!")
    dexBonusWarningWindow.config(bg="mistyrose")
    dexBonusWarningWindowText1 = tk.Label(dexBonusWarningWindow, wraplength=240, font="helvetica 12 bold", bg="mistyrose", 
                                    text=f"You entered an dexterity bonus of {dexterityBonus}, and a dexterity score of {dexterityScore}.\n\nThey don't seem to match, are you sure you entered the correct info?")
    dexBonusWarningWindowText1.place(x=10, y=10, width=260, height=210)

    confirmButton = tk.Button(dexBonusWarningWindow, text="That is correct", command= lambda: [savePlayer(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, "Y"), dexBonusWarningWindow.withdraw()])
    confirmButton.place(x=10, y=230, height=30, width=260)

    cancelButton = tk.Button(dexBonusWarningWindow, text="Oops, I need to correct that", command= lambda: [clearDexAndBonus(), dexBonusWarningWindow.withdraw()])
    cancelButton.place(x=10, y=270, height=30, width=260)



def savePlayer(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified):

    global playerDataTable
#A LOT of error checking

    characterName = str(name).strip()
    if len(characterName) > 64:
        messagebox.showerror("Error", "You character name is too long!")
        entryCharacterName.delete(0, tk.END)
        return

#Fails and returns if input is a non-integer
    try: initiativeBonus = int(entryInitiativeBonus.get())
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your initiative bonus!")
        entryInitiativeBonus.delete(0, tk.END)
        return

#Minimum and maximum range
#These two steps are repeated for each entry    
    if initiativeBonus < -10 or initiativeBonus > 20:
        messagebox.showerror("Error", f"An Initiative bonus of {initiativeBonus} is out of range.")
        entryInitiativeBonus.delete(0, tk.END)
        return

    try: dexterityBonus = int(entryDexterityBonus.get())
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity bonus!")
        entryDexterityBonus.delete(0, tk.END)
        return
    
    if dexterityBonus < -5 or dexterityBonus > 6:
        messagebox.showerror("Error", f"A Dexterity bonus of {dexterityBonus} is out of range.")
        entryDexterityBonus.delete(0, tk.END)
        return

    try: dexterityScore = int(entryDexterityScore.get())
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity score!")
        entryDexterityScore.delete(0, tk.END)
        return
    
    if dexterityScore < 1 or dexterityScore > 24:
        messagebox.showerror("Error", f"A Dexterity score of {dexterityScore} is out of range.")
        entryDexterityScore.delete(0, tk.END)
        return
    
    try: hitPoints = int(entryHitPoints.get())
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your Hit Points!")
        entryHitPoints.delete(0, tk.END)
        return
    
    if hitPoints < 1 or hitPoints > 800:
        messagebox.showerror("Error", f"{hitPoints} Hit Points is out of range.")
        entryHitPoints.delete(0, tk.END)
        return
    
    if abs(initiativeBonus-dexterityBonus) >= 2 and initVerified != "Y":
        initDexCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        return
    else:
        initVerified = "Y"

    if dexVerified != "Y":
        if dexterityScore == 24 and dexterityBonus != 7:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore >= 22 and dexterityScore < 24 and dexterityBonus != 6:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore >= 20 and dexterityScore < 22 and dexterityBonus != 5:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)   
        elif dexterityScore >= 18 and dexterityScore < 20 and dexterityBonus != 4:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore >= 16 and dexterityScore < 18 and dexterityBonus != 3:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore >= 14 and dexterityScore < 16 and dexterityBonus != 2:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore >= 12 and dexterityScore < 14 and dexterityBonus != 1:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore >= 10 and dexterityScore < 12 and dexterityBonus != 0:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)      
        elif dexterityScore <= 9 and dexterityScore > 7 and dexterityBonus != -1:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore <= 7 and dexterityScore > 5 and dexterityBonus != -2:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore <= 5 and dexterityScore > 3 and dexterityBonus != -3:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore <= 3 and dexterityScore > 1 and dexterityBonus != -4:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        elif dexterityScore == 1 and dexterityBonus != -5:
            dexBonusCompare(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
        else: writeToTable(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints)
    else: writeToTable(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints)
    

    
    #provides initial data for the table
def writeToTable(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints):
    global playerDataTable
    diceRoll = 0
    initiativeTotal = initiativeBonus + diceRoll

    #writes the input to the data table
    newPlayerDataTable = pd.DataFrame({
        "Character Name" : [name],
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
    
    playerDataTable = pd.concat([newPlayerDataTable, playerDataTable], ignore_index=True)

    #confirmation pop up
    messagebox.showinfo("Saved", "Player Information Saved")
    clearFields()
    

    #Keeps you from continuing if you don't enter any data
def openEnemyCollect(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified):
    if name != "" and initiativeBonus != "" and dexterityBonus != "" and dexterityScore != "" and hitPoints != "":
        savePlayer(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints, initVerified, dexVerified)
    elif name != "" or initiativeBonus != "" or dexterityBonus !="" or dexterityScore != "" or hitPoints !="":
        messagebox.showerror("Error","You didn't fill in all the fields!")
        clearFields()
        return
    
    if len(playerDataTable) <1:
        messagebox.showerror("Error","You didn't enter any player information!")
        clearFields()
        return
    
    #Gets the file path needed and writes the data table to an Excel file
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    sheetsDir = os.path.join(parentDir, "SpreadSheets")
    playerFile = os.path.join(parentDir,sheetsDir, "playerData.xlsx")
    with pd.ExcelWriter(playerFile, engine="openpyxl") as fileWriter:
        playerDataTable.to_excel(fileWriter, index=False)
    enemyCollect = os.path.join(currentDir, "enemyCollect.py")
    subprocess.Popen(["python", enemyCollect])
    quit()

warning = tk.Tk()
warning.geometry("300x150")
warning.title("Warning!")
warning.configure(background="red")

warningText = tk.Label(warning, text="Warning! Any existing player data will be deleted!", bg = "red", font = "Helvetica 16 bold", wraplength=280, anchor="w")
warningText.place(x=10, y=10, width=280, height=100)

yesButton = tk.Button(warning, text = "Yes, continue", width = 35, command = lambda: wipePlayerData())
yesButton.place(x=10, y=110, width=135, height=30)

noButton = tk.Button(warning, text = "No, go back.", width = 35, command = lambda: openStartPage())
noButton.place(x=155, y=110, width=135, height=30)


playerDataWindow = tk.Tk()
playerDataWindow.withdraw()

playerDataWindow.geometry("400x390")
playerDataWindow.title("Add Player Data")
playerDataWindow.configure(background="light blue")

labelHeader = tk.Label(playerDataWindow, text = "Adding Character Info", background="light blue", font="Helvetica 14", wraplength=380)
labelHeader.place(x=10, y=10, width=380, height=50)

labelCharacterName = tk.Label(playerDataWindow, text = "Character Name: ", background="light blue", font="Helvetica 12")
labelCharacterName.place(x=10, y=70, width=150, height=30)
labelInitiativeBonus = tk.Label(playerDataWindow, text = "Initiative Bonus: ", background="light blue", font="Helvetica 12")
labelInitiativeBonus.place(x=10, y=110, width=150, height=30)
labelDexterityBonus = tk.Label(playerDataWindow, text = "Dexterity Bonus: ", background="light blue", font="Helvetica 12")
labelDexterityBonus.place(x=10, y=150, width=150, height=30)
labelDexterityScore = tk.Label(playerDataWindow, text = "Dexterity Score: ", background="light blue", font="Helvetica 12")
labelDexterityScore.place(x=10, y=190, width=150, height=30)
labelHitPoints = tk.Label(playerDataWindow, text = "Hit Points: ", background="light blue", font="Helvetica 12")
labelHitPoints.place(x=10, y=230, width=150, height=30)

entryCharacterName = tk.Entry(playerDataWindow, font="Helvetica 12")
entryCharacterName.place(x=160, y=70, width=230, height=30)
entryInitiativeBonus = tk.Entry(playerDataWindow, font="Helvetica 12")
entryInitiativeBonus.place(x=160, y=110, width=230, height=30)
entryDexterityBonus = tk.Entry(playerDataWindow, font="Helvetica 12")
entryDexterityBonus.place(x=160, y=150, width=230, height=30)
entryDexterityScore = tk.Entry(playerDataWindow, font="Helvetica 12")
entryDexterityScore.place(x=160, y=190, width=230, height=30)
entryHitPoints = tk.Entry(playerDataWindow, font="Helvetica 12")
entryHitPoints.place(x=160, y=230, width=230, height=30)

commitButton = tk.Button(playerDataWindow, text = "Add Character", font="Helvetica 12", command = lambda: savePlayer(entryCharacterName.get(),
                                                                                                                    entryInitiativeBonus.get(), 
                                                                                                                    entryDexterityBonus.get(),
                                                                                                                    entryDexterityScore.get(),
                                                                                                                    entryHitPoints.get(),
                                                                                                                    "N",
                                                                                                                    "N"
                                                                                                                    ))
                                                                                #Passes user input to the function
commitButton.place(x=10, y=280, width= 185, height=40)

resetButton = tk.Button(playerDataWindow, text = "Reset Fields", font="Helvetica 12", command = lambda: clearFields)
resetButton.place(x=205, y=280, width= 185, height=40)

doneButton = tk.Button(playerDataWindow, text = "Done Adding Characters", font="Helvetica 12 bold", command = lambda: openEnemyCollect(entryCharacterName.get(),
                                                                                                                                       entryInitiativeBonus.get(), 
                                                                                                                                       entryDexterityBonus.get(), 
                                                                                                                                       entryDexterityScore.get(), 
                                                                                                                                       entryHitPoints.get(),
                                                                                                                                       "N",
                                                                                                                                       "N"
                                                                                                                                       ))
doneButton.place(x=10, y=340, width= 380, height=40)

playerDataWindow.mainloop()