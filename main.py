from __future__ import print_function
import tkinter
from tkinter import *
import os.path
from datetime import datetime

# My Custom Classes
from mapping import *
from classes import Recipe

# Sheets API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# region variables
width = 600
height = 400
bgColor = "#F0F7F4"
primaryColor = "#a2e3c4"
secondaryColor = "#3c493f"
neutralLightColor = "#b3bfb8"
neutralDarkColor = "#7e8d85"
recipeList = []


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

# region helper methods
def parseDatime(dateString):
    try:
        parsedDate = datetime.strptime(dateString, "%Y-%m-%d")
    except ValueError:
        parsedDate = ''
    return parsedDate


# endregion



def main():
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
                                range=RECIPE_COLUMN_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Found Data:')
        for row in values:
            dateStr = row[FIELD_DATE_COOKED]
            parsedDate = parseDatime(dateStr)

            recipe = Recipe(row[FIELD_ID],
                            row[FIELD_NAME],
                            row[FIELD_LINK],
                            row[FIELD_NOTES],
                            parsedDate,
                            row[FIELD_CORE_INGREDIENT],
                            row[FIELD_CUISINE])
            recipeList.append(recipe)

        print(recipeList[0])


if __name__ == '__main__':
    main()

# window = Tk()
# mywin = MyWindow(window)
# window.title('Whats for dinner?')
# window.geometry(f"{width}x{height}+10+10")
# window.configure(bg=bgColor)
# window.mainloop()
