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

def savePlayer(name, initiativeBonus, dexterityBonus, dexterityScore, hitPoints):


#A LOT of error checking
    global playerDataTable
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
    
    if dexterityBonus < -6 or dexterityBonus > 6:
        messagebox.showerror("Error", f"A Dexterity bonus of {dexterityBonus} is out of range.")
        entryDexterityBonus.delete(0, tk.END)
        return

    try: dexterityScore = int(entryDexterityScore.get())
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dexterity score!")
        entryDexterityScore.delete(0, tk.END)
        return
    
    if dexterityScore < 1 or dexterityScore > 30:
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
    
    #provides initial data for the table
    diceRoll = 0
    initiativeTotal = initiativeBonus + diceRoll

    #writes the input to the data table
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
    
    playerDataTable = pd.concat([newPlayerDataTable, playerDataTable], ignore_index=True)

    #confirmation pop up
    messagebox.showinfo("Saved", "Player Information Saved")
    clearFields()
    

    #Keeps you from continuing if you don't enter any data
def openEnemyCollect(playerDataTable):
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
                                                                                                                    entryHitPoints.get()))
                                                                                #Passes user input to the function
commitButton.place(x=10, y=280, width= 185, height=40)

resetButton = tk.Button(playerDataWindow, text = "Reset Fields", font="Helvetica 12", command = lambda: clearFields)
resetButton.place(x=205, y=280, width= 185, height=40)

doneButton = tk.Button(playerDataWindow, text = "Done Adding Characters", font="Helvetica 12 bold", command = lambda: openEnemyCollect(playerDataTable))
doneButton.place(x=10, y=340, width= 380, height=40)

playerDataWindow.mainloop()