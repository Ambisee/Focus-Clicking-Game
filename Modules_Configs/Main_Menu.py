# --- Modules --- #
from tkinter import *
from tkinter import messagebox

try:
    from Modules_Configs import Game, Scores, config
except ModuleNotFoundError:
    import Scores
    import Game
    import config

# --- Main Menu  Window --- #
class MainMenu:
    def __init__(self):
        # WINDOW
        self.mwin = Tk()
        self.mwin.title("Focus Clicking Game")
        self.mwin.resizable(height=False, width=False)
        self.mwin.protocol("WM_DELETE_WINDOW", self.mwin.quit)
        config.mainwin = self.mwin

        # WIDGETS
        self.welcome_label = Label(self.mwin, text="WHACK A MOLE", font=("System", 30), fg="Purple")
        self.no_label = Label(self.mwin, text="Insert number of rounds to click :", font=("Courier", 10))
        self.no_entry = Entry(self.mwin, width=50)
        self.button = Button(self.mwin, text="Start Game", font=("Courier", 15), bg='grey', fg='white', command=self.btn_func, height=1, width=11)
        self.button2 = Button(self.mwin, text="Scores", font=("Courier", 15), bg='grey', fg='white', command=self.openScores, height=1, width=11)

        self.welcome_label.grid(row=0, column=0, columnspan=3)
        self.no_label.grid(row=1, column=0, padx=5, pady=10)
        self.no_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=10)
        self.button.grid(row=2, column=0, columnspan=3)
        self.button2.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # POSITION
        mwin = self.mwin
        mwin.update()
        posx = int(mwin.winfo_screenwidth() / 2 - mwin.winfo_reqwidth() / 2)
        posy = int(mwin. winfo_screenheight() / 2 - mwin.winfo_reqheight() / 2)
        mwin.geometry("+{}+{}".format(posx, posy))

        self.mwin.bind("<Return>", self.kb_btn_func)
        self.mwin.mainloop()

    def get_no_rounds(self):
        # Get number of rounds the player wants
        max = 1000
        try:
            noor = int(self.no_entry.get())
        except:
            messagebox.showerror("! Error !", f"Please insert a valid number ( Max. {max} ).")
            return

        if noor <= 0 or noor > max:
            messagebox.showerror("! Error !", f"Please insert a valid number ( Max. {max} ).")
            return

        return noor

    def kb_btn_func(self, event):
        # Keyboard shortcut for btn_func
        self.btn_func()

    def btn_func(self):
        # Set number of rounds and time, proceed to game
        config.noor = self.get_no_rounds()
        config.noor_c = config.noor
        if config.noor == None:
            return

        self.no_entry.delete(0, END)
        self.mwin.withdraw()
        Game.Game()
    
    def openScores(self):
        self.mwin.withdraw()
        Scores.Scores()

if __name__ == '__main__':
    if input("Debug (Y/N) ? : ").lower() == 'y':
        x = Tk()
        x.withdraw()
        MainMenu().mwin.deiconify()
        x.mainloop()