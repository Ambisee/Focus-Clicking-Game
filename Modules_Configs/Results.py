# --- Modules --- #
from tkinter import *
from tkinter import messagebox

if __name__ == "__main__":
    print("Results Module - Part of 'Focus Clicking Game'.")
    print("Uses - Display Results Window.")
else:
    try:
        from Modules_Configs import config
    except ModuleNotFoundError:
        import config

# --- Results Window --- #
# Window
class Results:
    def __init__(self):
        self.time = f"{config.m} : {config.s} : {config.ms}"

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
        self.mistake = Label(self.upframe, text="Total Mistakes = " + str(config.mistake), font=("System", 15), fg="Blue")
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
        self.win.focus_force()

    def print_score(self):
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
        name = self.n_entry.get()
        time = f"{config.m}:{config.s}:{config.ms}"

        if name != "":
            with open("Scores.txt", 'a') as f:
                f.write(f"{name},{time},{config.mistake},{config.noor_c}\n")
            self.print_score()
            self.submit['state'] = "disabled"
            self.n_entry.delete(0, END)
            self.n_entry['state'] = "disabled"
        else:
            messagebox.showerror("! Error !", "Please enter at least one character in the entry bar.")

    def retry(self):
        self.win.destroy()

        config.m = 0
        config.s = 0
        config.ms = 0
        config.mistake = 0
        config.noor = 0
        config.noor_c = 0
        config.button_list.clear()

        config.mainwin.deiconify()

    def pass_f(self):
        pass

    def del_s(self):
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

# Save Score
class ScoreItem:
    def __init__(self, name, time, mistake, noor):
        self.name = name
        self.time = time
        self.mistake = mistake
        self.noor = noor

    def post(self, listbox):
        listbox.insert(END, f"Name = {self.name}, Time = {self.time}, Mistakes = {self.mistake}, No. of Rounds = {self.noor}")