import tkinter as tk
from tkinter import messagebox
from tkinter import Entry
from tkinter import Button
from tkinter import ttk
import pandas as pd
import openpyxl as openpyxl
from PIL import ImageTk, Image
import os
'''
A few notes that I didn't feel like repeating a bunch throughout my code:

I use a a lot of similar code to prevent windows to keep from being destoyed,
is the syntax  %windowName%.protocol("WM_DELETE_WINDOW", %functionName%)
it intercepts a close command and instead will withdraw() the window

(0. tk.END) and .set("") are also used a lot to clear the content of text boxes when windows are closed
I added them as parts of the commands that each button was tied to, it made for cleaner
window initialization since old data was no longer displayed

Lastly, every button has a lambda: after the command = 
This keeps the function from trying to collect data or pre-execute any commands before the button
is clicked.  WIthout it, my error checking would pop on the fields which had text boxes becuase it would
collect an empty text box, pass the empty string to the next function, then the next function would
being executing and fail.
'''


#importing my excel file, converting it back to a datatable
currentDir = os.path.dirname(__file__)
parentDir = os.path.dirname(currentDir)
sheets = os.path.join(parentDir, "SpreadSheets")
table = os.path.join(parentDir,sheets,"initiativeList.xlsx")

#defining variables that are accessed at the top level
active = 0
roundCounter = 1
tableInitiativeList = pd.read_excel(table)
playerList = tableInitiativeList['Character Name'].str.strip().to_list()



#refresh the data in the main window
#This function gets called a lot!
def updateMainWIndow():
    global active
    global prettyListOfEffects
    global playerList
    global roundCounter
    global windowPlayerList
    global windowActivePlayer

#pandas has a to_list function that will write all of the contents of a column or row to a list
    playerList = tableInitiativeList['Character Name'].str.strip().to_list()

#I had to set the datatype of the column so that it could accept lists as input
    tableInitiativeList['Spell Effects'] = tableInitiativeList['Spell Effects'].astype(object)
#Checks the row, column location, and creates a list that looks good for display purposes
#Or writes it as "None"
    currentActiveEffects = tableInitiativeList.at[active, 'Spell Effects']
    if isinstance(currentActiveEffects, list):
        prettyListOfEffects = ', '.join(currentActiveEffects)
        if len(prettyListOfEffects) == 0:
            prettyListOfEffects = "None"
    else:
        prettyListOfEffects = "None"

#Updates the .config of the window to show changes each time they are made
    windowPlayerList.config(text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\n Combat round: {roundCounter}")
    windowActivePlayer = tk.Label(combatWindow)
    windowActivePlayer.config(text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}\n\n Active Effects: {prettyListOfEffects}")  
    windowActivePlayer.config(bg = "white", font = "Helvetica 14 bold", justify="center", wraplength=375)
    windowActivePlayer.place(x=200, y=10, width=395, height=400)


def victoryScreen():

#loading my image
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    imagesDir = os.path.join(parentDir, "Images")
    victoryPath = os.path.join(imagesDir,"Victory.jpg")

    victoryImageUploaded = Image.open(victoryPath)
    victoryImage = ImageTk.PhotoImage(victoryImageUploaded)   

    victoryScreenWindow = tk.Toplevel()
    victoryScreenWindow.geometry("376x470")
    victoryScreenWindow.title("Victory!")
    victoryScreenWindow.config(background="light gray")

#defining it as a function so it doesn't get lost
    victoryScreenWindow.victoryImage = victoryImage

    victoryScreenLabelOne = tk.Label(victoryScreenWindow, image=victoryImage)
    victoryScreenLabelOne.place(x=10, y=10, height=356, width=356)

    victoryScreenLabelTwo = tk.Label(victoryScreenWindow, text="Victory is yours!", font="helvetica 20 bold", bg="light gray")
    victoryScreenLabelTwo.place(x=10, y=376, height=30, width=356)

    exitButton = tk.Button(victoryScreenWindow, text="Congratulations to me!", font="helvetica 12 bold", command=lambda: quit())
    exitButton.place(x=10, y=416, width = 356, height=40)


def defeatScreen():
#This is pretty much a carbon copy of the victory screen
    currentDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(currentDir)
    imagesDir = os.path.join(parentDir, "Images")
    defeatPath = os.path.join(imagesDir,"Defeat.jpg")



    defeatImageUploaded = Image.open(defeatPath)
    defeatImage = ImageTk.PhotoImage(defeatImageUploaded)

    defeatScreenWindow = tk.Toplevel()
    defeatScreenWindow.geometry("376x470")
    defeatScreenWindow.title("Defeat!")
    defeatScreenWindow.config(background="light gray")

    defeatScreenWindow.defeatImage = defeatImage

    defeatScreenLabelOne = tk.Label(defeatScreenWindow, image=defeatImage)
    defeatScreenLabelOne.place(x=10, y=10, height=356, width=356)

    defeatScreenLabelTwo = tk.Label(defeatScreenWindow, text="You have tasted defeat!", font="helvetica 20 bold", bg="light gray")
    defeatScreenLabelTwo.place(x=10, y=376, height=30, width=356)

    exitButton = tk.Button(defeatScreenWindow, text="I give up!", font="helvetica 12 bold", command=lambda: quit())
    exitButton.place(x=10, y=416, width = 356, height=40)




def addCombatant(alignment, combatantAddWindowName, combatantAddWindowInitiative):
    global tableInitiativeList

#Error checking
    if combatantAddWindowName == "":
        messagebox.showerror("Error",f"Name cannot be blank")
        return

    if combatantAddWindowName > 64:
        messagebox.showerror("Error",f"Name is too long")
        return      

    try: 
        combatantAddWindowInitiative = int(combatantAddWindowInitiative)
    except ValueError:
        messagebox.showerror("Error",f"Please enter a whole number for your initiative")
        return
    if combatantAddWindowInitiative > 30:
        messagebox.showerror("Error",f"{combatantAddWindowInitiative} is too high")
        return
    if combatantAddWindowInitiative < -10:
        messagebox.showerror("Error",f"{combatantAddWindowInitiative} is too low")
        return

#Creates a row with the user's input, then concatenates it with the main data table
    if alignment == 1:
        newRow = pd.Series({'Character Name': combatantAddWindowName,'Initiative Total': combatantAddWindowInitiative, 'Good':1})
        tableInitiativeList = pd.concat([tableInitiativeList, newRow.to_frame().T], ignore_index=True)
    else:
        newRow = pd.Series({'Character Name': combatantAddWindowName,'Initiative Total': combatantAddWindowInitiative, 'Bad':1})
        tableInitiativeList = pd.concat([tableInitiativeList, newRow.to_frame().T], ignore_index=True)

#Then resorts the list, and re-indexes it    
    tableInitiativeList = tableInitiativeList.sort_values(
            by=["Initiative Total"], ascending=[False])
    tableInitiativeList = tableInitiativeList.reset_index(drop=True)

#Updates the displayed data    
    updateMainWIndow()


#Adds spell effects to the player table
def addToTable(roundSelection, effectAddWindowTextBox, effectAddListBox, persistentEffect):
    global tableInitiativeList

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()
    
    effectName = effectAddWindowTextBox
    tableInitiativeList['Spell Effects'] = tableInitiativeList['Spell Effects'].astype(object)
    tableInitiativeList['Spell Expirations'] = tableInitiativeList['Spell Expirations'].astype(object)

#error checking
    if len(effectName) < 1:
        messagebox.showerror("Error", "Effect name cannot be blank.")
        return
    
    if len(effectName) > 64:
        messagebox.showerror("Error", "Effect name is too long.")
        return
    
    if persistentEffect == 0 and roundSelection == "":
        messagebox.showerror("Error", "Please select your duration.")
        return
    
    if persistentEffect == 1:
        valueRoundSelection = 9999
    if roundSelection == "1 Round":
        valueRoundSelection = len(playerList)
    if roundSelection == "1 Minute":
        valueRoundSelection = len(playerList) * 10
    if roundSelection == "10 Minutes":
        valueRoundSelection = len(playerList) * 100

    turnsLeft = valueRoundSelection

    selectedCombatants = effectAddListBox
    selectedCombatantsRows = list(selectedCombatants)

    if len(selectedCombatants) < 1:

        messagebox.showerror("Error", "Please select your targets.")
        return() 

    for index in selectedCombatantsRows:
        rowToEdit = index
#I have to store the iterable as a different variable, pandas will not let you refer to a row number
#by a variable that iterates in a for list, and i couldn't use index
#Checks to see if the cell contains a list
        if isinstance(tableInitiativeList.loc[rowToEdit, 'Spell Effects'], list):
#also, if you want to add to a cell, then write the cell back to a table, you have to use the .copy() function            
            currentEffects = tableInitiativeList.loc[rowToEdit, 'Spell Effects'].copy()
#If the cell contains a list, appends the list
            currentEffects.append(effectName)
#Writes the cell back to the table
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = currentEffects
#If the cell does not contain a list, and the list of effects(from user input) is a list, it writes the list to the cell
        elif isinstance(effectName, list):
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectName
#Else, else...It converts the string to a list, and writes it to a cell        
        else:   
            effectName = [effectName]
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectName

#That same process is repeated here, excet that it is writing list(s) with numberical values to
#a column that counts down, the effects will be removed from the list in a later function   
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
    updateMainWIndow()


          

    


    
def nextCombatant():
    global active
    global roundCounter
    global tableInitiativeList
    playerList = tableInitiativeList['Character Name'].str.strip().to_list()

#Increases my turn counters, resets the turn counter at the end of the list
#and will increase the round counter after going through each player
    active += 1
    if active >= len(playerList):
        active = 0
        roundCounter += 1

#Creating my ilst of effects that looks good for display
    tableInitiativeList['Spell Effects'] = tableInitiativeList['Spell Effects'].astype(object)
    currentActiveEffects = tableInitiativeList.at[active, 'Spell Effects']
    if isinstance(currentActiveEffects, list):
        prettyListOfEffects = ', '.join(currentActiveEffects)
        if len(prettyListOfEffects) == 0:
            prettyListOfEffects = "None"    
    else:
        prettyListOfEffects = "None"
    
#Reduce counts is what counts down as mentioned previously
    reduceCounts()
    updateMainWIndow()
#used for debugging, will be commented out when I submit
   # print(tableInitiativeList)


def reduceCounts():
    global tableInitiativeList

#Used a control variable rather than a for list, it made more sense to me since i have a loop in a loop
    loopCounter = len(tableInitiativeList)

#Starts at row 0
    index = 0
    while index < loopCounter:
        rowToEdit = index
#looks for a list, copies the two cells so they can be manipulated
        if isinstance(tableInitiativeList.at[rowToEdit, 'Spell Expirations'], list):
            countdown = tableInitiativeList.at[rowToEdit, 'Spell Expirations'].copy()
            effectListItems = tableInitiativeList.at[rowToEdit, 'Spell Effects'].copy()

#Goes through the list items in the cell
            pos = 0
            while pos < len(countdown):
#Redcues the numerical value by 1
                countdown[pos] = countdown[pos] - 1
#If a countdown reaches 0 it removes the list item at that position
#Then it removes the effect at the same list position in the neighboring column
#which contains the name of the effect 
                if countdown[pos] == 0:
                    countdown.pop(pos)
                    effectListItems.pop(pos)
#if nothing is removed, moves on to the next list item
                else:
                    pos = pos + 1
#writes the cells back to the table
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = countdown
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectListItems
#basically the same process, but if the list only contains an numerical value, not a list
#it doesn't mess with list position, it just empties the neighboring column since it will only
#have a single entry
        elif isinstance(tableInitiativeList.at[rowToEdit, 'Spell Expirations'],int):
            countdown = tableInitiativeList.at[rowToEdit, 'Spell Expirations'].copy()
            effectListItems = tableInitiativeList.at[rowToEdit, 'Spell Effects'].copy()
            countdown = countdown - 1
            if countdown <= 0:
                countdown = None
                effectListItems = None
            tableInitiativeList.at[rowToEdit, 'Spell Expirations'] = countdown
            tableInitiativeList.at[rowToEdit, 'Spell Effects'] = effectListItems
        index += 1
    updateMainWIndow()


def openSpellRemoveWindowOne():

    #Keeps the window from getting destroyed
    def spellRemoveWindowOneResetAndMinimize():
        spellRemoveWindowOneDropdown.set("")
        spellRemoveWindowOne.withdraw()

    #This searches my list of tuples, and returns the index from the tuple
    #This index corresponds to a row in the master initiative table
    #Then it launches the second part of the process
    def runNameSearch(nameToSearch):
        for item in spellRemoveWindowOneplayerListBeta:
            if item[1] == nameToSearch:
                masterTableRow = item[0]
                break
        openSpellRemoveWindowTwo(masterTableRow, nameToSearch)
        spellRemoveWindowOne.withdraw()

    # Initialize the lists to a empty lists
    spellRemoveWindowOneplayerListBeta = []
    spellRemoveWindowOneplayerListBetaNamesOnly = []

    #This creates a tuple that contains the index and player name IF the player has an active condition
    #It also creates a list of just the names for the combobox
    #also, enumerate lets me refer to an iterable as a row index
    spellRemoveWindowOneplayerListAlpha = tableInitiativeList['Character Name'].str.strip().to_list()
    for row, name in enumerate(spellRemoveWindowOneplayerListAlpha):
        if isinstance(tableInitiativeList.at[row, "Spell Effects"], list):
            if len(tableInitiativeList.at[row, 'Spell Effects']) > 0:
                spellRemoveWindowOneplayerListBeta.append((row, name))
                spellRemoveWindowOneplayerListBetaNamesOnly.append((name))

    #Makes sure there are effects that can be removed
    #Pops an error message and kills the function if not
    if len(spellRemoveWindowOneplayerListBeta) < 1:
        messagebox.showerror("Warning","There are no current active effects to remove!")
        return

    spellRemoveWindowOne = tk.Tk()

    spellRemoveWindowOne.geometry("200x145")
    spellRemoveWindowOne.title("Remove a spell effect from someone")



    spellRemoveWindowOneText = tk.Label(spellRemoveWindowOne, text="Who is losing the effect?")
    spellRemoveWindowOneText.place(x=10, y=10, width = 180, height=20)

    spellRemoveWindowOneDropdown = ttk.Combobox(spellRemoveWindowOne, state="readonly", values=spellRemoveWindowOneplayerListBetaNamesOnly)
    spellRemoveWindowOneDropdown.place(x=10, y=35, width=180, height=20)

    yesButton = tk.Button(spellRemoveWindowOne, text = "Confirm", command =lambda: [runNameSearch(spellRemoveWindowOneDropdown.get()),
                                                                                    spellRemoveWindowOneDropdown.set(""),
                                                                                    spellRemoveWindowOne.withdraw(),
                                                                                    updateMainWIndow()
                                                                                    ])
    #send user input to the next function
    yesButton.place(x=10, y=65, width=180, height=30)

    noButton = tk.Button(spellRemoveWindowOne, text = "Cancel", command = lambda:[spellRemoveWindowOneDropdown.set(""),
                                                                                  spellRemoveWindowOne.withdraw(),
                                                                                  updateMainWIndow()
                                                                                  ])
    noButton.place(x=10, y=105, width=180, height=30)

    spellRemoveWindowOne.protocol("WM_DELETE_WINDOW", spellRemoveWindowOneResetAndMinimize)


def openSpellRemoveWindowTwo(masterTableRow, nameToSearch):
    
    def spellRemoveWindowTwoResetAndMinimize():
        spellRemoveWindowTwoDropdown.set("")
        spellRemoveWindowTwo.withdraw()
    

#uses the index passed from the previous function to choose a row, column location and create a variable
    activeEffectsList = tableInitiativeList.at[masterTableRow, 'Spell Effects']

    spellRemoveWindowTwo = tk.Tk()
    spellRemoveWindowTwo.geometry("200x160")
    spellRemoveWindowTwo.title("Select the effect to remove")

    spellRemoveWindowTwoText = tk.Label(spellRemoveWindowTwo, text=f"Which effect is \n{nameToSearch} losing?")
    spellRemoveWindowTwoText.place(x=10, y=10, width = 190, height=30)

#loads a combobox with the list values
    spellRemoveWindowTwoDropdown = ttk.Combobox(spellRemoveWindowTwo, values=activeEffectsList)
    spellRemoveWindowTwoDropdown.place(x=10, y=50, width=180, height=20)

    yesButton=tk.Button(spellRemoveWindowTwo, text = "Confirm", command = lambda: [openSpellRemoveWindowThree(nameToSearch, 
                                                                                    masterTableRow, 
                                                                                    spellRemoveWindowTwoDropdown.current()),
                                                                                   spellRemoveWindowTwo.withdraw(),
                                                                                   updateMainWIndow()
                                                                                   ])
#uses current(), similar to get() and passes to the third and final function
#since current returns the index position of the item selected, it will correspond to
#the same list position within the cell that the list was created from
    
    yesButton.place(x=10, y=80, width=180, height=30)
 

    noButton = tk.Button(spellRemoveWindowTwo, text = "Cancel", command = lambda: [spellRemoveWindowTwoDropdown.set(""),
                                                                                   spellRemoveWindowTwo.withdraw(),
                                                                                   updateMainWIndow()
                                                                                   ])
    noButton.place(x=10, y=120, width=180, height=30)

    spellRemoveWindowTwo.protocol("WM_DELETE_WINDOW", spellRemoveWindowTwoResetAndMinimize)

def openSpellRemoveWindowThree(nameToSearch, tableRow, listPosition):

#reads my data table and creates the copies I'm going to modify    

    selectedEffectList = tableInitiativeList.at[tableRow, 'Spell Effects'].copy()
    selectedEffectDuration = tableInitiativeList.at[tableRow, 'Spell Expirations'].copy()
    effectGettingRemoved = selectedEffectList[listPosition]
#uses .pop() to remove the items from the lists within the cells
    selectedEffectList.pop(listPosition)
    selectedEffectDuration.pop(listPosition)
#And writes the updated cells back to the table
    tableInitiativeList.at[tableRow, 'Spell Effects'] = selectedEffectList
    tableInitiativeList.at[tableRow, 'Spell Expirations'] = selectedEffectDuration

    messagebox.showinfo("Notice",f"{nameToSearch} is no longer {effectGettingRemoved}")

def openEffectAddWindow():
    availableRounds = ["1 Round", "1 Minute", "10 Minutes"]

    def effectAddWindowResetAndMinimize():
        effectAddWindowTextBox.delete(0, tk.END)
        roundSelection.set(""),
        longEffectCheck.deselect(),
        effectAddListBox.selection_clear(0, tk.END),
        effectAddWindow.withdraw()
    
    #The underscore allows unlimited positional arguments to be passed
    #it was the only way to make these functions work
    def listBoxClear(_):
        effectAddListBox.selection_clear(0, tk.END)

    def uncheckLongEffect(_):
        longEffectCheck.deselect()
        effectAddListBox.selection_clear(0, tk.END)
    
    def clearRoundDropdown(_):
        roundSelection.set("")
        effectAddListBox.selection_clear(0, tk.END)

    effectAddWindow = tk.Tk()
    effectAddWindow.geometry("200x580")
    effectAddWindow.title("Add a spell or effect")

    effectAddWindowText1 = tk.Label(effectAddWindow, text=f"It's Round {roundCounter}, Turn {active+1}!", font="Helvetica 12 bold") 
    effectAddWindowText1.place(x=10, y=10, width=180, height=40)

    effectAddWindowText2 = tk.Label(effectAddWindow, text="Enter effect name") 
    effectAddWindowText2.place(x=10, y=60, width=180, height=15)

    effectAddWindowTextBox = tk.Entry(effectAddWindow)
    effectAddWindowTextBox.place(x=10, y=85, width=180, height=20)
    #Clears the listbox when you click in the text box
    effectAddWindowTextBox.bind("<Button-1>", listBoxClear)

    effectAddWindowText3 = tk.Label(effectAddWindow, text="How long will this effect last?") 
    effectAddWindowText3.place(x=10, y=120, width=180, height=20)


    roundSelection = ttk.Combobox(effectAddWindow, values=availableRounds, state="readonly")    
    roundSelection.place(x=10, y=145, width=180, height=20)
    #unchecks the box if you click the dropdown
    roundSelection.bind("<Button-1>", uncheckLongEffect)

#Becuase this window is not the .mainloop() window
#I had to specifiy the window location in the IntVar arguments
    persistentEffect = tk.IntVar(effectAddWindow)  
    longEffectCheck = tk.Checkbutton(effectAddWindow, text="This effect will persist until cancelled", onvalue=1, offvalue=0, variable=persistentEffect, wraplength=180)
    longEffectCheck.place(x=10, y=175, width=180, height=30)
    #Clears the dropdown if you check the box
    longEffectCheck.bind("<Button-1>", clearRoundDropdown)
    
    effectAddWindowText2 = tk.Label(effectAddWindow, text="Select Targets") 
    effectAddWindowText2.place(x=10, y=215, width=180, height=20)

    effectAddListBox = tk.Listbox(effectAddWindow, selectmode=tk.MULTIPLE)
    effectAddListBox.place(x=10, y=240, width=180, height=210)
    for item in playerList:
        effectAddListBox.insert(tk.END, item)

    saveCloseButton = tk.Button(effectAddWindow, text = "Confirm and close", width = 35, command= lambda:[addToTable(roundSelection.get(), 
                                                                                        effectAddWindowTextBox.get(), 
                                                                                        effectAddListBox.curselection(), 
                                                                                        persistentEffect.get()),
                                                                                        effectAddWindowTextBox.delete(0, tk.END),
                                                                                        roundSelection.set(""),
                                                                                        longEffectCheck.deselect(),
                                                                                        effectAddListBox.selection_clear(0, tk.END),
                                                                                        effectAddWindow.withdraw(),
                                                                                        updateMainWIndow()
                                                                                        ])   
#Does a bunch of .gets to pass data to the next function                                                                                        
    saveCloseButton.place(x=10, y=460, width=180, height=30)

    saveOpenButton = tk.Button(effectAddWindow, text = "Confirm and add another", width = 35, command= lambda:[addToTable(roundSelection.get(), effectAddWindowTextBox.get(), effectAddListBox.curselection(), persistentEffect.get()),
                                                                                        effectAddWindowTextBox.delete(0, tk.END),
                                                                                        roundSelection.set(""),
                                                                                        longEffectCheck.deselect(),
                                                                                        effectAddListBox.selection_clear(0, tk.END),
                                                                                        updateMainWIndow()
                                                                                        ])                                                                                       
    saveOpenButton.place(x=10, y=500, width=180, height=30)

    cancelButton = tk.Button(effectAddWindow, text = "Cancel", width = 35, command= lambda:[cancelEffectAddWindow,
                                                                                    effectAddWindowTextBox.delete(0, tk.END),
                                                                                    roundSelection.set(""),
                                                                                    longEffectCheck.deselect(),
                                                                                    effectAddListBox.selection_clear(0, tk.END),
                                                                                    updateMainWIndow(),
                                                                                    effectAddWindow.withdraw()
                                                                                    ])
    cancelButton.place(x=10, y=540, width=180, height=30)



    def cancelEffectAddWindow():
        effectAddWindow.withdraw()
    
    effectAddWindow.protocol("WM_DELETE_WINDOW", effectAddWindowResetAndMinimize)  




def openCombatantRemoveWindow():

    def combatantRemoveWindowResetAndMinimize():
        playerListDropdown.set("")
        combatantRemoveWindow.withdraw()

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()

    combatantRemoveWindow = tk.Tk()
    combatantRemoveWindow.geometry("200x145")
    combatantRemoveWindow.title("Remove someone from the initiative list")



    combatantRemoveWindowText = tk.Label(combatantRemoveWindow, text="Select who/what to remove")
    combatantRemoveWindowText.place(x=10, y=10, width = 180, height=20)

    playerListDropdown = ttk.Combobox(combatantRemoveWindow, values=playerList, state="readonly")
    playerListDropdown.place(x=10, y=35, width=180, height=20)

    yesButton = tk.Button(combatantRemoveWindow, text = "Confirm", command = lambda: [removeCombatant(playerListDropdown.current()),
                                                                                playerListDropdown.set(""),
                                                                                combatantRemoveWindow.withdraw(),
                                                                                updateMainWIndow()
                                                                                ])
    #.current gets a list index, since the list is generated from the data table
    #The list index will match the data table row
    yesButton.place(x=10, y=65, width=180, height=30)

    noButton = tk.Button(combatantRemoveWindow, text = "Cancel", command = lambda: [playerListDropdown.set(""),
                                                                                combatantRemoveWindow.withdraw(),
                                                                                updateMainWIndow()
                                                                                ])
    noButton.place(x=10, y=105, width=180, height=30)

    combatantRemoveWindow.protocol("WM_DELETE_WINDOW", combatantRemoveWindowResetAndMinimize)




def removeCombatant(rowToRemove):
    global active
    global tableInitiativeList

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()

    tableInitiativeList = tableInitiativeList.drop(index=rowToRemove).reset_index(drop=True)

#Does a summation of the Good and Bad columns, and will load a victory or
#Defeat screen if one of the columns reaches 0    
    goodCount=int(tableInitiativeList["Good"].sum())
    badCount=int(tableInitiativeList["Bad"].sum())

    if badCount == 0:
        victoryScreen()

    if goodCount == 0:
        defeatScreen()

    if active >= len(playerList):
        active = len(playerList) -1
        if active < 0:
            active = 0
    
    if active < len(playerList):
        active = 0

    playerList = tableInitiativeList['Character Name'].str.strip().to_list()
    tableInitiativeList['Spell Effects'] = tableInitiativeList['Spell Effects'].astype(object)
    currentActiveEffects = tableInitiativeList.at[active, 'Spell Effects']

#Recreates my list of effects for the main window
    currentActiveEffects = tableInitiativeList.at[active, 'Spell Effects']
    if isinstance(currentActiveEffects, list):
        prettyListOfEffects = ', '.join(currentActiveEffects)
        if len(prettyListOfEffects) == 0:
            prettyListOfEffects = "None"
    else:
        prettyListOfEffects = "None"

    updateMainWIndow()






def openCombatantAddWindow():

    def combatantAddWindowResetAndMinimize():
        combatantAddWindowName.delete(0, tk.END)
        combatantAddWindowInitiative.delete(0, tk.END)
        combatantAddWindow.withdraw()

    combatantAddWindow = tk.Tk()
    combatantAddWindow.geometry("200x230")
    combatantAddWindow.title("Add someone to the initiative list")

    

    combatantAddWindowLabel1 = tk.Label(combatantAddWindow, text="Enter Name") 
    combatantAddWindowLabel1.place(x=10, y=10, width=180, height=20)

    combatantAddWindowName = tk.Entry(combatantAddWindow)
    combatantAddWindowName.place(x=10, y=35, width=180, height=20)

    combatantAddWindowLabel2 = tk.Label(combatantAddWindow, text="Enter Initiative Total") 
    combatantAddWindowLabel2.place(x=10, y=65, width=180, height=20)

    combatantAddWindowInitiative = tk.Entry(combatantAddWindow)
    combatantAddWindowInitiative.place(x=10, y=90, width=180, height=20)

    alignment = tk.IntVar(combatantAddWindow) #had to specify which window

#uses radio buttons to specifiy if it's an enemy or ally
#since the variable is the same, it will only allow one to be selected
    combatantAddWindowRadioAlly = tk.Radiobutton(combatantAddWindow, text="Ally", variable=alignment, value=1)
    combatantAddWindowRadioAlly.place(x=10, y=120, width=80, height=20)

    combatantAddWindowRadioEnemy = tk.Radiobutton(combatantAddWindow, text="Enemy", variable=alignment, value=0)
    combatantAddWindowRadioEnemy.place(x=100, y=120, width=80, height=20)





    saveButton = tk.Button(combatantAddWindow, text = "Confirm", width = 35, command= lambda: [(alignment.get(), 
                                                                                            combatantAddWindowName.get(), 
                                                                                            combatantAddWindowInitiative.get()),
                                                                                            combatantAddWindowName.delete(0, tk.END),
                                                                                            combatantAddWindowInitiative.delete(0, tk.END),
                                                                                            updateMainWIndow(),
                                                                                            combatantAddWindow.withdraw()
                                                                                            ])
    #more get()s to pass data to the next function                                                                                           
    saveButton.place(x=10, y=150, width=180, height=30)

    cancelButton = tk.Button(combatantAddWindow, text = "Cancel", width = 35, command=lambda: [combatantAddWindowName.delete(0, tk.END),
                                                                                            combatantAddWindowInitiative.delete(0, tk.END),
                                                                                            combatantAddWindow.withdraw(),
                                                                                            updateMainWIndow()
                                                                                            ])
    cancelButton.place(x=10, y=190, width=180, height=30)

    combatantAddWindow.protocol("WM_DELETE_WINDOW", combatantAddWindowResetAndMinimize)





combatWindow = tk.Tk()





combatWindow.geometry("605x500")
combatWindow.title("Fight!")
combatWindow.configure(background="gray")


windowPlayerList = tk.Label(combatWindow)
windowPlayerList.place(x=10, y=10, width=180, height=400)

windowActivePlayer = tk.Label(combatWindow)
windowActivePlayer.place(x=200, y=10, width=395, height=400)

updateMainWIndow()
windowPlayerList.config(text=f"Initiative Order\n\n{'\n'.join(playerList)}\n\nCombat round: {roundCounter}",bg = "white", bd = 2, font = "Helvetica")
windowActivePlayer.config(text=f"Active combatant\n\n{playerList[active]}\n\n Combat round: {roundCounter}  Turn: {active+1}\n\n Active Effects: {prettyListOfEffects}")  
windowActivePlayer.config(bg = "white", font = "Helvetica 14 bold", justify="center", wraplength=375)



nextButton = tk.Button(combatWindow, text = "Next combatant!", command = nextCombatant, font="bold")
nextButton.place(x=10, y=420, width=180, height=75)

addASpell = tk.Button(combatWindow, text = "Add a spell or condition to the list.", wraplength=90, command = lambda: openEffectAddWindow())
addASpell.place(x=200, y=420, width=95, height=75)

removeASpell = tk.Button(combatWindow, text = "Remove a spell or condition from the list.", wraplength=90, command = lambda: openSpellRemoveWindowOne())
removeASpell.place(x=300, y=420, width=95, height=75)

addAnEnemy = tk.Button(combatWindow, text = "Add a combatant to the list.", wraplength=90, command = lambda: openCombatantAddWindow())
addAnEnemy.place(x=400, y=420, width=95, height=75)

removeFromOrder = tk.Button(combatWindow, text = "Remove someone from the list.", wraplength=90, command = lambda: openCombatantRemoveWindow())
removeFromOrder.place(x=500, y=420, width=95, height=75)






combatWindow.mainloop()
