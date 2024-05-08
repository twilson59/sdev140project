import tkinter as TK
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import random
import openpyxl as openpyxl

#Initializing the incrementation variable
active = 0

#Loading excel files as data tables
currentDir = os.path.dirname(__file__)
parentDir = os.path.dirname(currentDir)
sheets = os.path.join(parentDir, "SpreadSheets")
enemyFile = os.path.join(parentDir,sheets,"enemyData.xlsx")
playerFile = os.path.join(parentDir,sheets,"playerData.xlsx")

#concatenating the two data tables into one, with a try: except: block if a file is missing
try: 
    playerData = pd.read_excel(playerFile)
except FileNotFoundError:
    messagebox.showerror("Error","Your Player data file is missing.  Please create one!")
    subprocess.Popen(["python", "playerCollect.py"])
    exit(1)
    
try:
    enemyData = pd.read_excel(enemyFile)
except FileNotFoundError:
    messagebox.showerror("Error","Your Enemy data file is missing.  Please create one!")
    subprocess.Popen(["python", "enemyCollect.py"])
    exit(1)

tableInitiativeList = pd.concat([playerData, enemyData], ignore_index=True)

#.loc[active, "Character name"]  Goes to the location referenced as Row, Column
#This will iterate through the table and run for each row that contains data
activeCharacter = tableInitiativeList.loc[active, "Character Name"]

#Simulates a 20-sided dice roll
def hurlTheDice():
    global entryDiceRoll
    diceRoll = random.randint(1,20)
    entryDiceRoll.delete(0, "end")
    entryDiceRoll.insert("end", diceRoll)
    rollAndWrite.update()

def saveDiceRoll(diceRollValue):
    global active
    global activeCharacter
    global tableInitiativeList
    
    #Error checking becuase I allow either program generation of random numbers, or manual input
    try:
        diceRollValue = int(diceRollValue)
    except ValueError:
        messagebox.showerror("Error", "You entered something besides a whole number as your dice roll!")
        entryDiceRoll.delete(0, TK.END)
        return
    
    #I could have combined this into an or statement, but I wanted to tell the user exactly what was wrong
    if diceRollValue > 20:
        messagebox.showerror("Error", "You entered a dice roll higher than 20!")
        entryDiceRoll.delete(0, TK.END)
        return
    
    if diceRollValue < 1:
        messagebox.showerror("Error", "You entered a dice roll less than 1!")
        entryDiceRoll.delete(0, TK.END)
        return

#Puts the value of the dice roll into the data dable
#and then adds the contents of two columns, and writes the result to the column where it's needed
    tableInitiativeList.loc[active, "Dice Roll"] = diceRollValue
    tableInitiativeList.loc[active, "Initiative Total"] = diceRollValue + tableInitiativeList.loc[active, "Initiative Bonus"]

#increases my control variable
    active = active + 1

#If the variable representing the row is within the row numbers of the data table it updates the data table
    if active < len(tableInitiativeList):
        messagebox.showinfo("Done", "Initiative roll saved!")
        activeCharacter = tableInitiativeList.loc[active, "Character Name"]
        entryDiceRoll.delete(0, TK.END)
        currentPlayer.config(text=f"Roll a d20 for \n {activeCharacter}'s initiative")
        rollAndWrite.update()    
    else:
#once the table is full, confrims that you're done, does a multi-level descending sort, and opens the next window
        messagebox.showinfo("Done", "All initiatives entered!")
        tableInitiativeList = tableInitiativeList.sort_values(
            by=["Initiative Total", "Initiative Bonus", "Dexterity Bonus", "Dexterity Score", "Dice Roll", "Hit Points", "Character Name"],
            ascending=[False, False, False, False, False, False, False])
        openCombat(tableInitiativeList)
        
#searches the dice roll column of the data table, returns to the previous screen if any of them are blank or NaN
def openCombat(tableInitiativeList):
    if (tableInitiativeList['Dice Roll'] == "").any() or (tableInitiativeList['Dice Roll'].isna().any()):
        messagebox.showerror("Error","You didn't enter a dice roll for everyone!")
        return
    
#Writes the data table to an excel file    
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    fileName = "initiativeList.xlsx"
    savedFile = os.path.join(parentDir,"SpreadSheets", fileName)
    with pd.ExcelWriter(savedFile, engine="openpyxl") as fileWriter:
        tableInitiativeList.to_excel(fileWriter, index=False)
    combatWindow = os.path.join(currentDir, "combatWindow.py")
    subprocess.Popen(["python", combatWindow])
    quit()


    
    





rollAndWrite = TK.Tk()

rollAndWrite.geometry("260x390")
rollAndWrite.title("Roll some dice!")
rollAndWrite.configure(background="lime green")


currentPlayer = TK.Label(rollAndWrite, text=f"Roll a d20 for \n {activeCharacter}'s initiative" , bg = "lime green", font = "Helvetica 14", wraplength=240)
currentPlayer.place(x=10, y=10, width=240, height=60)

entryDiceRoll = TK.Entry(rollAndWrite, justify="center", width=4, font=("Helvetica", 72))
entryDiceRoll.place(x=10, y=80, width=240, height=120)

rollForMeButton = TK.Button(rollAndWrite, text = "Roll for me!", font = "Helvetica 14", command = lambda: hurlTheDice())
rollForMeButton.place(x=10, y=210, width=240, height=80)

commitButton = TK.Button(rollAndWrite, text = "Confirm Roll", height=5, width=20, font = "Helvetica 14", command = lambda: saveDiceRoll(entryDiceRoll.get()))
commitButton.place(x=10, y=300, width=240, height=80)

rollAndWrite.mainloop()