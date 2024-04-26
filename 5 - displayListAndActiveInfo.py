import tkinter as TK
from tkinter import messagebox
from tkinter import Entry
from tkinter import Button
from tkinter import OptionMenu
from tkinter import ttk
import subprocess
import os
import pandas as pd
import random
import openpyxl as openpyxl

active = 0
roundCounter = 1
effectName = None
effectEntryWindow = None
tableInitiativeList = pd.read_excel("initiativeList.xlsx")
playerList = tableInitiativeList['Character Name'].str.strip().to_list()


def cancelEffectAddWindow():
    effectAddWindow.withdraw()


def closeItemRemoveWindow():
    itemRemoveWindow.withdraw()
    return

def openItemRemoveWindow():

    itemRemoveWindow.deiconify()


def setRemovedItem():
    global itemToRemove
    global tableInitiativeList

    userSelection = playerListDropdown.get()
    itemToRemove = tableInitiativeList.index[tableInitiativeList['Character Name'] == userSelection][0]
    itemRemoveWindow.withdraw()
    removeEffect()
    
def removeEffect():
    global active
    global playerList
    global tableInitiativeList
    global itemToRemove

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()
    playerListDropdown['values'] = playerList

    tableInitiativeList = tableInitiativeList.drop(index=itemToRemove).reset_index(drop=True)
    
    goodCount=int(tableInitiativeList["Good"].sum())
    badCount=int(tableInitiativeList["Bad"].sum())

    if badCount == 0:
        messagebox.showinfo("Stop", "You have slain the last enemy.")
        quit()
    
    if goodCount == 0:
        messagebox.showinfo("Stop", "The last hero has fallen.")
        quit()
    
    if len(playerList) == 1:
        messagebox.showinfo("Stop", "You only have one combatant left.\nI think it's safe to say combat is done.")
        quit()

    if active >= len(playerList):
        active = len(playerList) -1
        if active < 0:
            active = 0

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()
    playerListDropdown['values'] = playerList
    windowPlayerList.config(text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\n Combat round: {roundCounter}")
    windowActivePlayer.config(text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}")


def nextCombatant():
    global active
    global roundCounter
    global playerList
    global tableInitiativeList


    active += 1
    if active >= len(playerList):
        active = 0
        roundCounter += 1

    windowPlayerList.config(text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\n Combat round: {roundCounter}")
    windowActivePlayer.config(text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}")
    
    reduceCounts()
    print(tableInitiativeList)

    return

def reduceCounts():
    global tableInitiativeList
    print("List Before")
    print(tableInitiativeList)

    loopCounter = len(tableInitiativeList)

    index = 0
    while index < loopCounter:
        rowToEdit = index
        if isinstance(tableInitiativeList.at[rowToEdit, 'Spell Expirations'], list):
            activeList = tableInitiativeList.at[rowToEdit, 'Spell Expirations'].copy()
            effectListItems = tableInitiativeList.at[rowToEdit, 'Spell Effects'].copy()
            pos = 0
            while pos < len(activeList):
                activeList[pos] = activeList[pos] - 1 
                if activeList[pos] == 0:
                    activeList.pop(pos)
                    effectListItems.pop(pos)
                else:
                    pos = pos + 1
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = activeList
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectListItems
        elif isinstance(tableInitiativeList.at[rowToEdit, 'Spell Expirations'], int):
            count = tableInitiativeList.at[rowToEdit, 'Spell Expirations']
            count = count - 1
            if count <= 0:
                count = None
                effectListItems = None
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = count
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectListItems
        index += 1

    print("List after")
    print(tableInitiativeList)

def addEffect():
    global roundList
    global roundCounter
    global active
    global turnList
    global playerListDropdown

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()
    playerListDropdown['values'] = playerList
    
    roundList = []
    for item in range(roundCounter, roundCounter +20):
        roundList.append(item)

    turnList = []
    for item in range(1, len(playerList) +1):
        turnList.append(item)

    openEffectAddWindow()        

'''
def saveEffect():
    global effectName
    global effectEntryWindow
    global playerList
    global tableInitiativeList

    effectName = nameTextBox.get()

    newRow = pd.Series({'Character Name': effectName,'Good': 0,'Bad': 0})

    tableInitiativeList = pd.concat([tableInitiativeList.iloc[:active+1], pd.DataFrame([newRow]), tableInitiativeList.iloc[active+1:]], ignore_index=True)
      
    playerList = tableInitiativeList['Character Name'].str.strip().to_list()
    windowPlayerList.config(text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\n Combat round: {roundCounter}")
    windowActivePlayer.config(text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}")
    effectEntryWindow.destroy()
'''


def addSomeone():
    global effectName
    global effectEntryWindow
    global playerList
    global tableInitiativeList


    #effectName = nameTextBox.get()

    newRow = pd.Series({'Character Name': effectName,'Good': 0,'Bad': 0})

    tableInitiativeList = pd.concat([tableInitiativeList.loc[:active+1], pd.DataFrame([newRow]), tableInitiativeList.loc[active+1:]], ignore_index=True)
    
    windowPlayerList.config(text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\n Combat round: {roundCounter}")
    windowActivePlayer.config(text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}")
    effectEntryWindow.withdraw()





def addToTable():
    global selectedCombatants
    global tableInitiativeList
    global roundSelection
    global playerList
    global effectAddWindow
    global effectAddListBox
    
    effectAddWindow.withdraw()
    
    effectName = effectAddWindowTextBox.get()
    tableInitiativeList['Spell Effects'] = tableInitiativeList['Spell Effects'].astype(object)
    tableInitiativeList['Spell Expirations'] = tableInitiativeList['Spell Expirations'].astype(object)

   

    if len(effectName) < 1:
        messagebox.showerror("Error", "Effect name cannot be blank.")
        return()    
    
    valueRoundSelection = int(roundSelection.get())
    valueTurnSelection = int(turnSelection.get())
    turnsLeft = valueRoundSelection * int(len(playerList)) + valueTurnSelection
    turnsLeft = int(turnsLeft)

    selectedCombatants = effectAddListBox.curselection()
    selectedCombatantsRows = list(selectedCombatants)

    if len(selectedCombatants) < 1:
        messagebox.showerror("Error", "Please select your targets.")
        return() 


    for index in selectedCombatantsRows:
        rowToEdit = index
        if isinstance(tableInitiativeList.loc[rowToEdit, 'Spell Effects'], list):
            currentEffects = tableInitiativeList.loc[rowToEdit, 'Spell Effects'].copy()
            currentEffects.append(effectName)
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = currentEffects
        elif isinstance(effectName, list):
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectName
        else:   
            effectName = [effectName]
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectName
            

    for index in selectedCombatantsRows:
        rowToEdit = index
        if isinstance(tableInitiativeList.loc[rowToEdit, 'Spell Expirations'], list):
            currentCountdowns = tableInitiativeList.loc[rowToEdit, 'Spell Expirations'].copy()
            currentCountdowns.append(turnsLeft)
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = currentCountdowns
        elif isinstance(turnsLeft, list):
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = turnsLeft
        else:   
            turnsLeft = [turnsLeft]
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = turnsLeft
            


#Combat window starts here

combatWindow = TK.Tk()

combatWindow.geometry("600x500")
combatWindow.title("Addition")
combatWindow.configure(background="gray")

windowPlayerList = TK.Label(combatWindow, text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\nCombat round: {roundCounter}",bg = "white", bd = 2, font = "Helvetica", anchor = "w")
windowPlayerList.place(anchor="nw", x=5, y=5, width=190, height=400)


windowActivePlayer = TK.Label(combatWindow, text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}", 
                              bg = "white", bd = 2, font = "Helvetica", height = 15, width = 40, justify="center")
windowActivePlayer.place(x=200, y=5, width=395, height=400)


nextButton = TK.Button(combatWindow, text = "Next combatant!", command = nextCombatant)
nextButton.place(x=5, y=410, width=190, height=85)

addASpell = TK.Button(combatWindow, text = "Add a spell or condition to the list.", wraplength=125, command = addEffect)
addASpell.place(x=200, y=410, width=130, height=85)

addAnEnemy = TK.Button(combatWindow, text = "Add a combatant to the list.", wraplength=125, command = addSomeone)
addAnEnemy.place(x=332, y=410, width=130, height=85)

removeFromOrder = TK.Button(combatWindow, text = "Remove something from the list.", wraplength=125, command = openItemRemoveWindow)
removeFromOrder.place(x=464, y=410, width=130, height=85)
#Combat Window Ends Here



#Item removal Window starts here
itemRemoveWindow = TK.Tk()
itemRemoveWindow.withdraw()
itemRemoveWindow.geometry("200x200")
itemRemoveWindow.title("Remove something from the initiative list")

itemRemoveWindowText = TK.Label(itemRemoveWindow, text="Select who/what to remove")
itemRemoveWindowText.place(x=5, y=5, width = 190)

userSelection = TK.StringVar()
playerListDropdown = ttk.Combobox(itemRemoveWindow, values=playerList)
playerListDropdown.set(playerList[0])
playerListDropdown.place(x=5, y=25, width=190)

yesButton = TK.Button(itemRemoveWindow, text = "Confirm", width = 10, command = setRemovedItem)
yesButton.place(x=5, y=50)

noButton = TK.Button(itemRemoveWindow, text = "Cancel", width = 10, command = closeItemRemoveWindow)
noButton.place(x=115, y=50)
#Item removal Window ends here

'''
#Item add window starts here
effectAddWindow = TK.Tk()
effectAddWindow.withdraw()
effectAddWindow.geometry("200x200")
effectAddWindow.title("Add a spell or effect")

effectAddWindowText = TK.Label(effectAddWindow, text="Enter Effect Name") 
effectAddWindowText.place(x=5, y=5, width=190)

effectAddWindowTextBox = Entry(effectAddWindow)
effectAddWindowTextBox.place(x=5, y=25, width=190)

saveButton = TK.Button(effectAddWindow, text = "Save", width = 35, command=saveEffect)
saveButton.place(x=5, y=30, width=190)
#Item add window ends here
'''

#Item add window starts here
def openEffectAddWindow():
    global effectAddWindowTextBox
    global roundSelection
    global turnSelection
    global effectAddListBox
    global effectAddWindow

    effectAddWindow = TK.Tk()
    effectAddWindow.geometry("200x435")
    effectAddWindow.title("Add a spell or effect")
    effectAddWindow.overrideredirect(True)

    effectAddWindowText = TK.Label(effectAddWindow, text="Enter Effect Name") 
    effectAddWindowText.place(x=5, y=5, width=190, height=20)

    effectAddWindowTextBox = TK.Entry(effectAddWindow)
    effectAddWindowTextBox.place(x=5, y=30, width=190, height=20)

    effectAddWindowText3 = TK.Label(effectAddWindow, text=f"It's Round {roundCounter}, Turn {active+1}\n When will this effect expire?") 
    effectAddWindowText3.place(x=5, y=55, width=190, height=40)

    roundList = []
    for item in range(roundCounter, roundCounter +20):
        roundList.append(item)

    effectAddWindowText4 = TK.Label(effectAddWindow, text=f"Round:") 
    effectAddWindowText4.place(x=5, y=100, width=40, height=20)

    roundSelection = TK.StringVar()
    roundDropDown = ttk.Combobox(effectAddWindow, values=roundList, textvariable=roundSelection)
    roundSelection.set(roundList[0])
    roundDropDown.place(x=50, y=100, width=40, height=20)


    turnList = []
    for item in range(1, len(playerList) +1):
        turnList.append(item)

    effectAddWindowText5 = TK.Label(effectAddWindow, text=f"Turn:") 
    effectAddWindowText5.place(x=95, y=100, width=40, height=20)

    turnSelection = TK.StringVar()
    turnDropDown = ttk.Combobox(effectAddWindow, values=turnList, textvariable=turnSelection)
    turnSelection.set(turnList[0])
    turnDropDown.place(x=140, y=100, width=40, height=20)

    effectAddWindowText2 = TK.Label(effectAddWindow, text="Select Targets") 
    effectAddWindowText2.place(x=5, y=125, width=190, height=20)

    effectAddListBox = TK.Listbox(effectAddWindow, selectmode=TK.MULTIPLE)
    effectAddListBox.place(x=5, y=150, width=190, height=220)
    for item in playerList:
        effectAddListBox.insert(TK.END, item)

    saveButton = TK.Button(effectAddWindow, text = "Save", width = 35, command=addToTable)
    saveButton.place(x=5, y=375, width=190)

    cancelButton = TK.Button(effectAddWindow, text = "Cancel", width = 35, command=cancelEffectAddWindow)
    cancelButton.place(x=5, y=405, width=190)




combatWindow.mainloop()