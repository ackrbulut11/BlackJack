import customtkinter as ctk
from game_logic import *


class BlackJackUI:

    def __init__(self):
        # app frame
        self.root = ctk.CTk()
        self.root.title("BlackJack")
        self.root.geometry("720x400")
        self.root.configure(background = "green")

        self.game = BlackJack()

        # buttons
        self.hit_button = ctk.CTkButton(self.root, text = "Hit", command = self.game.player_hit)
        self.hit_button.grid(row=0, column=0, padx = 30, pady = 20)

        self.stand_button = ctk.CTkButton(self.root, text = "Stand", command = self.game.stand)
        self.stand_button.grid(row=0, column=1, padx = 30, pady = 20)



    def start(self):
        pass

    # run
    def run(self):
        self.root.mainloop()


