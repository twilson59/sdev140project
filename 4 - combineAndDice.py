import tkinter as TK
from tkinter import messagebox
import subprocess
import os
import pandas as pd
import random
import openpyxl as openpyxl

active = 0

if os.path.exists("playerData.xlsx") and os.path.exists("enemyData.xlsx"):
    playerData = pd.read_excel("playerData.xlsx")
    enemyData = pd.read_excel("enemyData.xlsx")
    combinedData = pd.concat([playerData, enemyData], ignore_index=True)
    with pd.ExcelWriter("initiativeList.xlsx", engine="openpyxl") as fileWriter:
        combinedData.to_excel(fileWriter, index=False)

tableInitiativeList = pd.read_excel("initiativeList.xlsx")
activeCharacter = tableInitiativeList.loc[active, "Character Name"]

def hurlTheDice():
    diceRoll = random.randint(1,20)
    entryDiceRoll.delete(0, TK.END)
    entryDiceRoll.insert(TK.END, diceRoll)

def saveDiceRoll():
    global active
    global activeCharacter
    global tableInitiativeList
    diceRollValue = entryDiceRoll.get()
    
    try:
        diceRollValue = int(diceRollValue)
    except ValueError:
        messagebox.showwarning("Stop", "You entered something besides a whole number as your dice roll!")
        entryDiceRoll.delete(0, TK.END)
        return
    
    if diceRollValue > 20 or diceRollValue < 1:
        messagebox.showwarning("Stop", "You entered a dice roll higher than 20!")
        entryDiceRoll.delete(0, TK.END)
        return

    tableInitiativeList.loc[active, "Dice Roll"] = diceRollValue
    tableInitiativeList.loc[active, "Initiative Total"] = diceRollValue + tableInitiativeList.loc[active, "Initiative Bonus"]

    active = active + 1

    if active < len(tableInitiativeList):
        messagebox.showinfo("Done", "Initiative roll saved!")
        activeCharacter = tableInitiativeList.loc[active, "Character Name"]
        entryDiceRoll.delete(0, TK.END)
        currentPlayer.config(text=f"Entering an initiative roll for\n {activeCharacter}")
        rollAndWrite.update()    
    else:
        messagebox.showinfo("Done", "All initiatives entered!")
        tableInitiativeList = tableInitiativeList.sort_values(
            by=["Initiative Total", "Initiative Bonus", "Dexterity Bonus", "Dexterity Score", "Dice Roll", "Hit Points", "Character Name"],
            ascending=[False, False, False, False, False, False, False])
        openCombat()
        

def openCombat():
    with pd.ExcelWriter("initiativeList.xlsx", engine="openpyxl") as fileWriter:
        tableInitiativeList.to_excel(fileWriter, index=False)
    workingDir = os.path.join(os.getcwd(), "FinalProject", "5 - displayListAndActiveInfo.py")
    subprocess.Popen(["python", workingDir])
    rollAndWrite.quit()


    
    





rollAndWrite = TK.Tk()

rollAndWrite.geometry("225x350")
rollAndWrite.title("Roll some dice!")
rollAndWrite.configure(background="green")


currentPlayer = TK.Label(rollAndWrite, text=f"Entering an initiative roll for\n {activeCharacter}" , bg = "white", bd = 2, font = "Helvetica", height = 3, width = 30, wraplength=250)
currentPlayer.grid(row = 0, column = 0, padx = 2, pady = 2, columnspan= 3)
rollAndWrite.grid_rowconfigure(0, weight= 1)
rollAndWrite.grid_columnconfigure(0, weight= 1)



entryDiceRoll = TK.Entry(rollAndWrite, justify="center", width=4, font=("Helvetica", 72))
entryDiceRoll.grid(row=1, column=0, padx=2, pady=2)
rollAndWrite.columnconfigure(0, weight=1)

rollForMeButton = TK.Button(rollAndWrite, text = "Roll for me!", height=5, width=20, command = hurlTheDice)
rollForMeButton.grid(row=3, column=0, padx=2, pady=2)

commitButton = TK.Button(rollAndWrite, text = "Confirm Roll", height=5, width=20, command = saveDiceRoll)
commitButton.grid(row=4, column=0, padx=2, pady=2)

rollAndWrite.mainloop()