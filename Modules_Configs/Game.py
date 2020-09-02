# --- Modules --- #
from tkinter import *
from random import choice

if __name__ == "__main__":
    print("Game Module - Part of 'Focus Clicking Game'.")
    print("Uses - Displays Game Window.")
else:
    try:
        from Modules_Configs import config, Results
    except ModuleNotFoundError:
        import config
        import Results

# --- Game Window --- #
# Game Buttons
class GameButtons:
    def __init__(self, root, r, c, cmd=None):
        self.button = Button(root, text="X", font=("", 30), height=2, width=5, command=cmd, bg="White")
        self.button.grid(row=r, column=c, padx=5, pady=5)
        config.button_list.append(self)

    def clicked(self):
        # Check whether player clicked the right button
        if self.button['bg'] == "Green":
            config.noor -=1
            if config.noor != 0:
                self.button.configure(bg="White")
                tlist = config.button_list.copy()
                tlist.remove(self)
                nextb = choice(tlist)
                nextb.button.configure(bg="Green")
        else:
            config.mistake += 1

# Window
class Game(GameButtons):
    def __init__(self):
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
        self.mistake = Label(self.framel, text="Mistake = " + str(config.mistake), font=("Courier", 12))
        self.time = Label(self.framel,text=f"{config.m} : {config.s} : {config.ms}",font=("Courier",12))

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
        self.win.focus_force()
        self.stop = False
        init_b = choice(config.button_list)
        init_b.button.configure(bg="Green")
        self.start_timer()

    def start_timer(self):
        # Start the timer
        if self.stop == False:
            config.ms += 1
            if config.ms == 1000:
                config.ms = 0
                config.s += 1
            if config.s == 60:
                config.s = 0
                config.m += 1
            self.time['text'] = f"{config.m} : {config.s} : {config.ms}"

            self.win.after(1, self.start_timer)

    def b_click(self, b):
        # Update number of mistake, check whether victory or defeat condition met
        GameButtons.clicked(b)
        self.mistake['text'] = "Mistake = " + str(config.mistake)

        if config.noor == 0:
            self.stop = True
            self.win.destroy()
            del self
            y = Results.Results()
            y.win.deiconify()
