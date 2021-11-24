import tkinter
from tkinter import *

width = 600
height = 400
bgColor = "#F0F7F4"
primaryColor = "#a2e3c4"
secondaryColor = "#3c493f"
neutralLightColor = "#b3bfb8"
neutralDarkColor = "#7e8d85"


# When passing a method as a command in the constructor of a widget, it does not
def onGenerateClicked():
    print("clicked via command instead of bind")
    mywin.setRecipeName("silly")


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


window = Tk()
mywin = MyWindow(window)
window.title('Whats for dinner?')
window.geometry(f"{width}x{height}+10+10")
window.configure(bg=bgColor)
window.mainloop()
