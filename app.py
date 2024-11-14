import customtkinter as ctk
from customer import LoginPage

class ATM:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.log_in_page = LoginPage(self.root)
        self.root.mainloop()



if __name__ == "__main__":
    ATM()

