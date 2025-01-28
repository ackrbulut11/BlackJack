import customtkinter as ctk

def startUI():

    def hit():
        pass

    def stand():
        run = ctk.CTkLabel(app, text= "run" )
        run.pack(padx = 10, pady=10)

    # system
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # app frame
    app = ctk.CTk()
    app.title("BlackJack")
    app.geometry("720x480")

    # buttons
    hit = ctk.CTkButton(app, text = "Hit", command=hit)
    hit.grid(row=0, column=0, padx = 30, pady = 20)

    stand = ctk.CTkButton(app, text = "Stand", command=stand)
    stand.grid(row=0, column=1, padx = 30, pady = 20)

    # run
    app.mainloop()

startUI()



