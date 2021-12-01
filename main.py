from __future__ import print_function
import tkinter
from tkinter import *
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

# region variables
width = 600
height = 400
bgColor = "#F0F7F4"
primaryColor = "#a2e3c4"
secondaryColor = "#3c493f"
neutralLightColor = "#b3bfb8"
neutralDarkColor = "#7e8d85"
recipes = {}


# endregion

# region UI handlers
# When passing a method as a command in the constructor of a widget, it does not
def onGenerateClicked():
    print("clicked via command instead of bind")
    mywin.setRecipeName("silly")


# endregion

# region UI Initializer
class MyWindow:
    def __init__(self, win):
        # Create the views
        self.name_var = tkinter.StringVar()

        self.title = Label(win,
                           text="What Should We Eat?",
                           font=("Arial", 24),
                           bg=bgColor, fg=secondaryColor)

        self.recipeName = Label(win,
                                text="Turkish Delight",
                                font=("Arial", 14),
                                bg=bgColor, fg=secondaryColor)

        self.notes = Label(win,
                           text="Notes: don't overprove it you bellend",
                           font=("Arial", 12),
                           bg=bgColor, fg=secondaryColor)

        self.generateButton = Button(win,
                                     text="Random Meal",
                                     padx=20, pady=5,
                                     font=("Arial", 14),
                                     bd=4,
                                     fg=primaryColor, bg=secondaryColor,
                                     activebackground=neutralDarkColor, activeforeground=primaryColor,
                                     command=onGenerateClicked)

        # Place the views
        self.title.place(x=100, y=50)
        self.title.pack(side=TOP, pady=15)
        self.recipeName.pack(side=TOP)
        self.notes.pack(side=TOP)
        self.generateButton.pack(side=BOTTOM, pady=50)

    def setRecipeName(self, text):
        self.recipeName.config(text=text)

    def setNotes(self, text):
        self.notes.config(text=text)


# endregion

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
RECIPE_SPREADSHEET_ID = '1PsAx6wrv1d1-Ya2SQsOeBvwGAOouIPj0HcpWzh_xNDE'
SAMPLE_RANGE_NAME = 'A2:G'
FIELD_ID = 0
FIELD_NAME = 1
FIELD_LINK = 2
FIELD_NOTES = 3
FIELD_DATE_COOKED = 4
FIELD_CORE_INGREDIENT = 5
FIELD_CUISINE = 6


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=RECIPE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Found Data:')
        for row in values:
            recipeId = row[FIELD_ID]
            recipe = {
                "id": recipeId,
                "name": row[FIELD_NAME],
                "link": row[FIELD_LINK],
                "notes": row[FIELD_NOTES],
                "dateCooked": row[FIELD_DATE_COOKED],
                "coreIngredient": row[FIELD_CORE_INGREDIENT],
                "cuisine": row[FIELD_CUISINE]
            }
            recipes[recipeId] = recipe
            # Print columns A and E, which correspond to indices 0 and 4.
        print(recipes)


if __name__ == '__main__':
    main()

# window = Tk()
# mywin = MyWindow(window)
# window.title('Whats for dinner?')
# window.geometry(f"{width}x{height}+10+10")
# window.configure(bg=bgColor)
# window.mainloop()
