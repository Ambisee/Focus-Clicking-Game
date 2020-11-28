# --- Modules --- #
from tkinter import *
from tkinter import messagebox

try:
    from Modules_Configs import config, Results
except ModuleNotFoundError:
    import config
    import Results

# --- Scores Window --- #
class Scores:
    def __init__(self):
        # WINDOW
        self.win = Toplevel()
        self.win.title("Whack A Mole - Scoreboard")
        self.win.resizable(height=False, width=False)
        self.win.protocol("WM_DELETE_WINDOW", self.win.quit)
        self.upframe = Frame(self.win)
        self.downframe = Frame(self.win)
        self.upframe.grid(row=0, column=0)
        self.downframe.grid(row=1, column=0)

        # WIDGETS
        self.title = Label(self.upframe, text="SCORES", font=("System", 30), fg="Yellow", bg="Purple")
        self.scorelist = Listbox(self.upframe, width=70)
        self.delete_score = Button(self.downframe, text="Delete Score", font=("Courier", 15), command=self.del_s)
        self.returnb = Button(self.downframe, text="Return", font=("Courier", 15), command=self.returnToMain)

        self.title.grid(row=0, column=0, padx=10, pady=5, columnspan=3)
        self.scorelist.grid(row=5, column=0, padx=10, pady=5, columnspan=3)
        self.delete_score.grid(row=0, column=1, padx=5, pady=10)
        self.returnb.grid(row=0, column=2, padx=5, pady=10)

        # POSITION
        win = self.win
        win.update()
        posx = int(win.winfo_screenwidth() / 2 - win.winfo_reqwidth() / 2)
        posy = int(win.winfo_screenheight() / 2 - win.winfo_reqheight() / 2)
        win.geometry(f"+{posx}+{posy}")

        # INITIAL FUNCTIONS
        self.print_score()
        self.win.focus_force()

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
            save = Results.ScoreItem(split_l[0], split_l[1], split_l[2], split_l[3])
            save.post(self.scorelist)

    def del_s(self):
        # Delete a score on the scoreboard
        del_obj = self.scorelist.get(ANCHOR)

        if del_obj == "":
            return

        x = messagebox.askyesno("Confirmation","Do you wish to delete this score?")
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

    def returnToMain(self):
        self.win.destroy()
        del self
        config.mainwin.deiconify()

if __name__ == '__main__':
    if input("Debug (Y/N) ? : ").lower() == 'y':
        x = Tk()
        x.withdraw()
        Scores().win.deiconify()
        x.mainloop()