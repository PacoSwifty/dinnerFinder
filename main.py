from __future__ import print_function
import tkinter
from tkinter import *
import os.path
from datetime import datetime
import random
import webbrowser

# My Custom Classes
from mapping import *
from classes import Recipe

# Sheets API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# region variables
fullRecipeList = []
filteredRecipeList = []
uniqueCuisines = []
uniqueIngredients = []
currentlySelectedCuisine = OPTION_ANY
currentlySelectedIngredient = OPTION_ANY
currentRecipe = Recipe("", "", "", "", None, "", "")
service = None
# todo: set this to true when not in debug mode
enforceDate = False


# endregion

# region UI handlers
def onGenerateClicked():
    global currentRecipe
    currentRecipe = pickRandomRecipe()
    if currentRecipe is not None:
        mywin.setRecipeName(currentRecipe.name)
        mywin.setNotes(currentRecipe.notes)
        mywin.setUrl(currentRecipe.url)

    # If it's the first time running / numResults is empty, go ahead and display the count'
    if not mywin.numResults.cget("text"):
        mywin.setNumResults(f"Picking from {len(filteredRecipeList)} out of {len(fullRecipeList)} total recipes")


def onConfirmCookedClicked():
    markRecipeAsCooked()


def onUrlClicked():
    webbrowser.open_new(currentRecipe.url)


def onCuisineSelected(selectedCuisine):
    global currentlySelectedCuisine
    currentlySelectedCuisine = selectedCuisine
    filteredRecipeList.clear()
    for recipe in fullRecipeList:
        if currentlySelectedIngredient == OPTION_ANY:
            if selectedCuisine == OPTION_ANY or recipe.cuisine == selectedCuisine:
                filteredRecipeList.append(recipe)
        else:
            if (
                    selectedCuisine == OPTION_ANY or recipe.cuisine == selectedCuisine) and recipe.coreIngredient == currentlySelectedIngredient:
                filteredRecipeList.append(recipe)
    print(f"Cuisine Selected: {selectedCuisine}")
    print(f"Found {len(filteredRecipeList)} recipes matching that criteria.")
    mywin.setNumResults(f"Picking from {len(filteredRecipeList)} out of {len(fullRecipeList)} total recipes")


def onIngredientSelected(selectedIngredient):
    global currentlySelectedIngredient
    currentlySelectedIngredient = selectedIngredient
    filteredRecipeList.clear()
    for recipe in fullRecipeList:
        if currentlySelectedCuisine == OPTION_ANY:
            if selectedIngredient == OPTION_ANY or recipe.coreIngredient == selectedIngredient:
                filteredRecipeList.append(recipe)
        else:
            if (
                    selectedIngredient == OPTION_ANY or recipe.coreIngredient == selectedIngredient) and recipe.cuisine == currentlySelectedCuisine:
                filteredRecipeList.append(recipe)
    print(f"Ingredient Selected: {selectedIngredient}")
    print(f"Found {len(filteredRecipeList)} recipes matching that criteria.")
    mywin.setNumResults(f"Picking from {len(filteredRecipeList)} out of {len(fullRecipeList)} total recipes")


# endregion

# region UI Initializer
class MyWindow:
    def __init__(self, win):
        # Create the views
        self.title = Label(win,
                           text="What Should We Eat?",
                           font=("Arial", 18),
                           wraplength=TEXT_WRAP_WIDTH,
                           bg=BG_COLOR, fg=SECONDARY_COLOR)

        self.recipeName = Label(win,
                                text="Click Below to Begin",
                                font=("Arial", 24),
                                wraplength=TEXT_WRAP_WIDTH,
                                bg=BG_COLOR, fg=SECONDARY_COLOR)

        self.notes = Label(win,
                           text="",
                           font=("Arial", 14),
                           wraplength=TEXT_WRAP_WIDTH,
                           justify="center",
                           bg=BG_COLOR, fg=SECONDARY_COLOR)

        self.url = Label(win,
                         text="",
                         font=("Ariel", 12),
                         wraplength=TEXT_WRAP_WIDTH,
                         bg=BG_COLOR, fg=NEUTRAL_DARK_COLOR)

        self.numResults = Label(win,
                                text="",
                                font=("Ariel", 10),
                                bg=BG_COLOR, fg=NEUTRAL_DARK_COLOR)

        self.generateButton = Button(win,
                                     text="Random Meal",
                                     padx=20, pady=5,
                                     font=("Arial", 14),
                                     bd=4,
                                     fg=PRIMARY_COLOR, bg=SECONDARY_COLOR,
                                     activebackground=NEUTRAL_DARK_COLOR, activeforeground=PRIMARY_COLOR,
                                     command=onGenerateClicked)

        self.confirmCookedButton = Checkbutton(win,
                                               text="We Cooked It!",
                                               padx=4, pady=2,
                                               font=("Arial", 10),
                                               bd=10,
                                               fg=SECONDARY_COLOR, bg=BG_COLOR,
                                               activebackground=BG_COLOR, activeforeground=SECONDARY_COLOR,
                                               command=onConfirmCookedClicked)

        # Setting up OptionMenu dropdowns
        self.selectedCuisineVariable = StringVar(win)
        self.selectedCuisineVariable.set(uniqueCuisines[0])
        self.selectedIngredientVariable = StringVar(win)
        self.selectedIngredientVariable.set(uniqueIngredients[0])

        # Place the views
        self.title.place(x=100, y=50)
        self.title.pack(side=TOP, pady=15)
        self.recipeName.pack(side=TOP)
        self.notes.pack(side=TOP, pady=20)
        self.url.pack(side=TOP)
        self.url.bind("<Button-1>", lambda e: onUrlClicked())

        # Cuisine and ingredient pickers
        dropDownHolder = Frame(win, bg=BG_COLOR)
        self.cuisineOptions = OptionMenu(dropDownHolder, self.selectedCuisineVariable, *uniqueCuisines,
                                         command=onCuisineSelected)
        self.ingredientOptions = OptionMenu(dropDownHolder, self.selectedIngredientVariable, *uniqueIngredients,
                                            command=onIngredientSelected)
        self.cuisineOptions.config(width=20, fg=PRIMARY_COLOR, bg=SECONDARY_COLOR, activebackground=NEUTRAL_DARK_COLOR,
                                   activeforeground=PRIMARY_COLOR)
        self.ingredientOptions.config(width=20, fg=PRIMARY_COLOR, bg=SECONDARY_COLOR,
                                      activebackground=NEUTRAL_DARK_COLOR, activeforeground=PRIMARY_COLOR)
        self.cuisineOptions.pack(in_=dropDownHolder, side=LEFT, padx=20, pady=10)
        self.ingredientOptions.pack(in_=dropDownHolder, side=RIGHT, padx=20, pady=10)

        self.confirmCookedButton.pack(side=BOTTOM, pady=10)
        self.numResults.pack(side=BOTTOM, pady=10)
        dropDownHolder.pack(side=BOTTOM, fill=NONE, expand=FALSE)
        self.generateButton.pack(side=BOTTOM, pady=2)

    def setRecipeName(self, text):
        self.recipeName.config(text=text)

    def setNotes(self, text):
        self.notes.config(text=text)

    def setUrl(self, text):
        self.url.config(text=text)

    def setNumResults(self, text):
        self.numResults.config(text=text)

    def disableCookedCheckbox(self):
        self.confirmCookedButton.config(state=DISABLED)


# endregion

# region Logic Methods
def parseDatetime(dateString):
    try:
        parsedDate = datetime.strptime(dateString, "%Y-%m-%d")
    except ValueError:
        parsedDate = ''
    return parsedDate


def convertDateToString(timeStamp):
    stringifiedDate = timeStamp.strftime("%Y-%m-%d")
    print(f"Converted datetime to this string: {stringifiedDate}")
    return stringifiedDate


def pickRandomRecipe():
    if filteredRecipeList:
        return random.choice(filteredRecipeList)
    else:
        mywin.setRecipeName("Sorry, we're out of recipes!")
        mywin.setNotes("")
        mywin.setUrl("")
        print("ERROR! THERE WERE NO AVAILABLE RECIPES!")


def getRecipesFromSheet():
    global filteredRecipeList
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=RECIPE_SPREADSHEET_ID,
                                range=RECIPE_COLUMN_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Found Data:')
        global uniqueCuisines
        global uniqueIngredients
        uniqueCuisines.clear()
        uniqueIngredients.clear()
        fullRecipeList.clear()
        filteredRecipeList.clear()

        uniqueCuisines.append(OPTION_ANY)
        uniqueIngredients.append(OPTION_ANY)
        for row in values:
            dateStr = row[FIELD_DATE_COOKED]
            parsedDate = parseDatetime(dateStr)

            if parsedDate != '':
                difference = datetime.now() - parsedDate
                # Don't add recipes that have been cooked within the last two weeks
                if difference.days < NO_REPEAT_THRESHOLD and enforceDate:
                    continue

            recipe = Recipe(row[FIELD_ID],
                            row[FIELD_NAME],
                            row[FIELD_URL],
                            row[FIELD_NOTES],
                            parsedDate,
                            row[FIELD_CORE_INGREDIENT],
                            row[FIELD_CUISINE])
            fullRecipeList.append(recipe)

            if recipe.cuisine not in uniqueCuisines:
                uniqueCuisines.append(recipe.cuisine)

            if recipe.coreIngredient not in uniqueIngredients:
                uniqueIngredients.append(recipe.coreIngredient)

        filteredRecipeList = fullRecipeList.copy()
        uniqueIngredients.sort()
        uniqueCuisines.sort()


def markRecipeAsCooked():
    mywin.disableCookedCheckbox()
    # This will update the entire row based on the state of the current recipe
    values = [
        [
            currentRecipe.id, currentRecipe.name, currentRecipe.url, currentRecipe.notes,
            convertDateToString(datetime.now()), currentRecipe.coreIngredient, currentRecipe.cuisine
        ]
    ]
    body = {
        'values': values
    }
    service.spreadsheets().values().update(
        spreadsheetId=RECIPE_SPREADSHEET_ID,
        range=f"A{currentRecipe.id}:G{currentRecipe.id}",
        valueInputOption="RAW",
        body=body
    ).execute()


# endregion


def main():
    global service
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    getRecipesFromSheet()


if __name__ == '__main__':
    main()

window = Tk()
mywin = MyWindow(window)
window.title('Whats for dinner?')
window.geometry(f"{WIDTH}x{HEIGHT}+10+10")
window.configure(bg=BG_COLOR)
window.mainloop()
