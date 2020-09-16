from tkinter import *
from tkinter import messagebox
from random import choice

# --- Main Menu --- #
class MainMenu:
    def __init__(self):
        # WINDOW
        self.mwin = Tk()
        self.mwin.title("Focus Clicking Game")
        self.mwin.resizable(height=False, width=False)

        # WIDGETS
        self.welcome_label = Label(self.mwin, text="FOCUS CLICKING GAME", font=("System", 30), fg="Purple")
        self.no_label = Label(self.mwin, text="Insert number of rounds to click :", font=("Courier", 10))
        self.no_entry = Entry(self.mwin, width=50)
        self.button = Button(self.mwin, text="Start Game", font=("Courier", 15), command=self.btn_func)

        self.welcome_label.grid(row=0, column=0, columnspan=3)
        self.no_label.grid(row=1, column=0, padx=5, pady=10)
        self.no_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=10)
        self.button.grid(row=2, column=0, columnspan=3)

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
        global noor, noor_c, mistake, m, s, ms

        noor = self.get_no_rounds()
        noor_c = noor
        if noor == None:
            return

        m = 0
        s = 0
        ms = -1
        mistake = 0

        self.mwin.withdraw()
        y = Game()

# --- Game --- #

# Buttons
button_list = []

class GameButtons:
    def __init__(self, root, r, c, cmd=None):
        self.button = Button(root, text="X", font=("", 30), height=2, width=5, command=cmd, bg="White")
        self.button.grid(row=r, column=c, padx=5, pady=5)
        button_list.append(self)

    def clicked(self):
        # Check whether player clicked the right button
        global noor, mistake

        if self.button['bg'] == "Green":
            noor -=1
            if noor != 0:
                self.button.configure(bg="White")
                tlist = button_list.copy()
                tlist.remove(self)
                nextb = choice(tlist)
                nextb.button.configure(bg="Green")
        else:
            mistake += 1


# Game Window
class Game(GameButtons):
    def __init__(self):
        global mistake, m, s, ms

        # WINDOW
        self.win = Toplevel()
        self.win.resizable(height=False, width=False)
        self.framel = Frame(self.win)
        self.frameb = Frame(self.win)
        self.framel.grid(row=0, column=0, pady=10)
        self.frameb.grid(row=1, column=0, padx=30)
        self.win.protocol("WM_DELETE_WINDOW", self.win.quit)
        self.win.withdraw()

        # WIDGETS
        self.inst = Label(self.framel, text="Press all of the GREEN button as fast as possible", font=("Arial", 15))
        self.mistake = Label(self.framel, text="Mistake = " + str(mistake), font=("Courier", 12))
        self.time = Label(self.framel,text=f"{m} : {s} : {ms}",font=("Courier",12))

        self.r0c0 = GameButtons(self.frameb, 0, 0, lambda: self.b_click(self.r0c0))
        self.r0c1 = GameButtons(self.frameb, 0, 1, lambda: self.b_click(self.r0c1))
        self.r0c2 = GameButtons(self.frameb, 0, 2, lambda: self.b_click(self.r0c2))
        self.r1c0 = GameButtons(self.frameb, 1, 0, lambda: self.b_click(self.r1c0))
        self.r1c1 = GameButtons(self.frameb, 1, 1, lambda: self.b_click(self.r1c1))
        self.r1c2 = GameButtons(self.frameb, 1, 2, lambda: self.b_click(self.r1c2))
        self.r2c0 = GameButtons(self.frameb, 2, 0, lambda: self.b_click(self.r2c0))
        self.r2c1 = GameButtons(self.frameb, 2, 1, lambda: self.b_click(self.r2c1))
        self.r2c2 = GameButtons(self.frameb, 2, 2, lambda: self.b_click(self.r2c2))

        self.inst.grid(row=0, column=0, columnspan=2, padx=10)
        self.mistake.grid(row=1, column=0, pady=5)
        self.time.grid(row=1, column=1, pady=5)

        # POSITION
        win = self.win
        win.update()
        posx = int(win.winfo_screenwidth() / 2 - win.winfo_reqwidth() / 2)
        posy = int(win.winfo_screenheight() / 2 - win.winfo_reqheight() / 2)
        win.geometry(f"+{posx}+{posy}")

        # INITIAL FUNCTIONS
        self.win.deiconify()
        self.stop = False
        init_b = choice(button_list)
        init_b.button.configure(bg="Green")
        self.start_timer()

    def start_timer(self):
        # Start the timer
        global m, s, ms

        if self.stop == False:
            ms += 1
            if ms == 1000:
                ms = 0
                s += 1
            if s == 60:
                s = 0
                m += 1
            self.time['text'] = f"{m} : {s} : {ms}"

            self.win.after(1, self.start_timer)

    def b_click(self, b):
        # Update number of mistake, check whether victory or defeat condition met
        global mistake, noor

        GameButtons.clicked(b)
        self.mistake['text'] = "Mistake = " + str(mistake)

        if noor == 0:
            self.stop = True
            self.win.destroy()
            del self
            y = Results()
            y.win.deiconify()

# --- Results --- #

# Result Window
class Results(Game):
    def __init__(self):
        global mistake, m, s, ms

        self.time = f"{m} : {s} : {ms}"

        # WINDOW
        self.win = Toplevel()
        self.win.resizable(height=False, width=False)
        self.win.protocol("WM_DELETE_WINDOW", self.win.quit)
        self.upframe = Frame(self.win)
        self.downframe = Frame(self.win)
        self.upframe.grid(row=0, column=0)
        self.downframe.grid(row=1, column=0)
        self.win.withdraw()

        # WIDGETS
        self.title = Label(self.upframe, text="RESULTS", font=("System", 30), fg="Yellow", bg="Purple")
        self.mistake = Label(self.upframe, text="Total Mistakes = " + str(mistake), font=("System", 15), fg="Blue")
        self.time = Label(self.upframe, text="Time = " + self.time, font=("System", 15), fg="Blue")

        self.n_label = Label(self.upframe, text="Insert Name : ")
        self.n_entry = Entry(self.upframe, width=50)
        self.submit = Button(self.upframe, text="Save Result", command=self.submit_score)
        self.scorelist = Listbox(self.upframe, width=70)

        self.retry = Button(self.downframe, text="Retry", font=("Courier", 15), command=self.retry)
        self.delete_score = Button(self.downframe, text="Delete Score", font=("Courier", 15), command=self.del_s)
        self.quitb = Button(self.downframe, text="Quit", font=("Courier", 15), command=self.win.quit)

        self.title.grid(row=0, column=0, padx=10, pady=5, columnspan=3)
        self.mistake.grid(row=1, column=0, padx=10, pady=5, columnspan=3)
        self.time.grid(row=2, column=0, padx=10, columnspan=3)
        self.n_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.n_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
        self.submit.grid(row=4, column=0, padx=5, pady=5, columnspan=3)
        self.scorelist.grid(row=5, column=0, padx=10, pady=5, columnspan=3)
        self.retry.grid(row=0, column=0, padx=5, pady=10)
        self.delete_score.grid(row=0, column=1, padx=5, pady=10)
        self.quitb.grid(row=0, column=2, padx=5, pady=10)

        # POSITION
        win = self.win
        win.update()
        posx = int(win.winfo_screenwidth() / 2 - win.winfo_reqwidth() / 2)
        posy = int(win.winfo_screenheight() / 2 - win.winfo_reqheight() / 2)
        win.geometry(f"+{posx}+{posy}")

        # INITIAL FUNCTIONS
        self.print_score()

    def print_score(self):
        # Print out the scoreboard on the GUI
        self.scorelist.delete(0, END)
        with open("Scores.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                nl = line.replace("\n", "")
                lines.remove(line)
                lines.append(nl)

        for line in lines:
            split_l = line.split(',')
            save = ScoreItem(split_l[0], split_l[1], split_l[2], split_l[3])
            save.post(self.scorelist)

    def submit_score(self):
        # Submit and reprint the current score
        global mistake, noor_c, m, s, ms

        name = self.n_entry.get()
        time = f"{m}:{s}:{ms}"

        if name != "":
            with open("Scores.txt", 'a') as f:
                f.write(f"{name},{time},{mistake},{noor_c}\n")
            self.print_score()
            self.submit['state'] = "disabled"
            self.n_entry.delete(0, END)
            self.n_entry['state'] = "disabled"
        else:
            messagebox.showerror("! Error !", "Please enter at least one character in the entry bar.")

    def retry(self):
        # Return to the main menu
        self.win.destroy()
        button_list.clear()
        MainMenu()

    def del_s(self):
        # Delete a score on the scoreboard
        del_obj = self.scorelist.get(ANCHOR)

        if del_obj == "":
            return

        x = messagebox.askyesno("Confirmation", "Do you wish to delete this score?")
        if x == False:
            return

        self.scorelist.delete(ANCHOR)
        del_obj = del_obj.replace("Name = ", "")
        del_obj = del_obj.replace(" Time = ", "")
        del_obj = del_obj.replace(" Mistakes = ", "")
        del_obj = del_obj.replace(" No. of Rounds = ", "")

        with open("Scores.txt", "r") as f:
            lines = f.readlines()
        with open("Scores.txt", "w") as f:
            for line in lines:
                if del_obj not in line:
                    f.write(line)

# Save Score
class ScoreItem:
    def __init__(self, name, time, mistake, noor):
        self.name = name
        self.time = time
        self.mistake = mistake
        self.noor = noor

    def post(self, listbox):
        # Post score on the scoreboard
        listbox.insert(END, f"Name = {self.name}, Time = {self.time}, Mistakes = {self.mistake}, No. of Rounds = {self.noor}")


if __name__ == "__main__":
    MainMenu()