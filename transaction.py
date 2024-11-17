from tkinter import messagebox
import customtkinter as ctk
import utils


class BasePage:
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
        self.setup_window()
        self.create_header()

    def setup_window(self):
        window_width, window_height = 1200, 800
        screen_width, screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def create_header(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        label = ctk.CTkLabel(self.master, text="Ladkrabang Bank ATM", font=("Helvetica", 50, "bold"))
        label.pack(pady=25)

    # to go back to the previous parent page
    def go_back(self, parent):
        self.master.destroy()
        parent.deiconify()

    # default buttons to add amoun for deposit, withdraw, and transfer
    def add_button_frame(self, master, entry):
        button_frame = ctk.CTkFrame(master, fg_color="transparent")
        button_frame.pack(pady=20)

        amounts = [500, 1000, 2000, 5000, 10000, 20000]
        row, col = 0, 0
        for amount in amounts:
            ctk.CTkButton(button_frame, text=str(amount), font=("Helvetica", 15), width=100, height=35,
                          command=lambda amt=amount: self.set_amount(amt, entry)).grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def set_amount(self, amt, amount_entry):
        amount_entry.delete(0, ctk.END)
        amount_entry.insert(0, amt)


class Deposit(BasePage):
    def __init__(self, master, current_user, db, save_data, parent):
        super().__init__(master, "Deposit")
        self.current_user = current_user
        self.db = db
        self.save_data = save_data
        self.parent = parent

        main_frame = ctk.CTkFrame(master, fg_color="transparent")
        main_frame.pack(pady=20)

        ctk.CTkLabel(main_frame, text="Current Balance: " , font=("Helvetica", 23)).grid(row=0, column=0, columnspan=2, pady=10)

        self.balance_var = ctk.StringVar(value=current_user["amount"])
        ctk.CTkLabel(
            main_frame, 
            text=f"{self.balance_var.get()} Baht", 
            font=('Helvetica', 24, 'bold')
        ).grid(row=1, column=0, columnspan=2, pady=10)

        self.amount_entry = ctk.CTkEntry(main_frame, font=("Helvetica", 18), width=200, height=35)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=10)
        self.add_button_frame(master, self.amount_entry)

        self.deposit_button = ctk.CTkButton(master, text="Deposit", command=self.deposit, width=150, height=30)
        self.deposit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(master, text="Back", command=lambda: self.go_back(self.parent), width=150, height=30)
        self.back_button.pack()

    def deposit(self):
        amount = self.amount_entry.get().strip()
        if utils.validate_amount(amount):
            amount = float(amount)
            self.current_user['amount'] += amount
            text = ("Deposit", utils.get_current_time(), amount)
            self.current_user["transaction_history"].append(text)
            messagebox.showinfo("Deposit Success", f"{amount} Baht deposited successfully.")
            self.save_data(self.db)

            result = messagebox.askyesno("Get Deposit Slip", "Would you like to take deposit slip?")
            if result:
                utils.print_deposit_slip(self.current_user, amount)

            self.go_back(self.parent)
        return

    def go_back(self, parent):
        return super().go_back(parent)


class Withdraw(BasePage):
    def __init__(self, master, current_user, db, save_data, parent):
        super().__init__(master, "Cash Withdraw")
        
        self.current_user = current_user
        self.db = db
        self.save_data = save_data
        self.parent = parent
        
        main_frame = ctk.CTkFrame(master, fg_color="transparent")
        main_frame.pack(pady=20)

        ctk.CTkLabel(main_frame, text="Current Balance: " , font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)

        self.balance_var = ctk.StringVar(value=current_user["amount"])
        ctk.CTkLabel(
            main_frame, 
            textvariable=self.balance_var, 
            font=('Helvetica', 24, 'bold')
        ).grid(row=1, column=0, columnspan=2, pady=10)

        self.amount_entry = ctk.CTkEntry(main_frame, font=("Helvetica", 18), width=200)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=10)

        self.add_button_frame(master, self.amount_entry)

        self.withdraw_button = ctk.CTkButton(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.back_button = ctk.CTkButton(master, text="Back", command=lambda: self.go_back(parent))
        self.back_button.pack()

    def withdraw(self):
        amount = self.amount_entry.get().strip()
        if utils.validate_amount(amount):
            amount = float(amount)
            if amount <= self.current_user['amount']:
                self.current_user['amount'] -= amount
                # transactin history logic
                text = ("Withdrawal", utils.get_current_time(), -amount)
                self.current_user["transaction_history"].append(text)
                messagebox.showinfo("Withdraw Success", f"{amount} Baht withdrawn successfully.")
                self.save_data(self.db)
                result = messagebox.askyesno("Get Withdrawal Slip", "Would you like to take withdrawal slip?")
                if result:
                    utils.print_withdrawal_slip(self.current_user, amount)
                self.go_back(self.parent)
            else:
                messagebox.showerror("Insufficient Funds", "Not enough balance.")
        return

    def go_back(self, parent):
        return super().go_back(parent)

class Transfer(BasePage):
    def __init__(self, master, current_user, db, save_data, parent):
        super().__init__(master, "Transfer")
        self.current_user = current_user
        self.db = db
        self.save_data = save_data
        self.parent = parent

        self.transfer_header = ctk.CTkLabel(master, text="Transfer Money", font=("Helvetica", 25, "bold"), text_color="red")
        self.transfer_header.pack(pady=10)

        # frame for input
        self.input_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.account_label = ctk.CTkLabel(self.input_frame, text="Account No:", font=("Helvetica", 16))
        self.account_label.grid(row=0, column=0, padx=5, pady=10, sticky=ctk.E)
        self.account_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), width=200)
        self.account_entry.grid(row=0, column=1, padx=5, pady=10)

        self.amount_label = ctk.CTkLabel(self.input_frame, text="Transfer Amount:", font=("Helvetica", 16))
        self.amount_label.grid(row=1, column=0, padx=5, pady=10, sticky=ctk.E)
        self.amount_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), width=200)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=10)

        self.add_button_frame(master, self.amount_entry)

        # frame for menu and transfer
        self.action_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.action_frame.pack(pady=20)

        self.main_menu_button = ctk.CTkButton(self.action_frame, text="Main Menu", font=("Helvetica", 12), width=150, height=35, command=lambda: self.go_back(parent))
        self.main_menu_button.grid(row=0, column=0, padx=10, pady=10)

        self.transfer_button = ctk.CTkButton(self.action_frame, text="Transfer", font=("Helvetica", 12), width=150, height=35, command=self.make_transfer)
        self.transfer_button.grid(row=0, column=1, padx=10, pady=10)

    def make_transfer(self):
        recipient_account = self.account_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if utils.validate_amount(amount):
            amount = float(amount)
            recipient = next((user for user in self.db if user['account_no'] == recipient_account), None)

            if recipient:
                if recipient["account_no"] == self.current_user["account_no"]:
                    messagebox.showwarning("Transfer Failed", "You cannot transfer to your own account!")
                elif amount <= 0:
                    messagebox.showerror("Invalid Amount", "Transfer amount must be greater than zero.")
                elif amount <= self.current_user['amount']:
                    self.current_user['amount'] -= amount
                    recipient['amount'] += amount
                    # transaction history logic
                    # for current_user
                    text = (
                    f"Transfer to {recipient['f_name']} {recipient['l_name']}", utils.get_current_time(), -amount)
                    self.current_user["transaction_history"].append(text)
                    # for recipient
                    text = (f"Transfer from {self.current_user['f_name']} {self.current_user['l_name']}",
                            utils.get_current_time(), amount)
                    recipient["transaction_history"].append(text)

                    messagebox.showinfo("Transfer Success",
                                        f"{amount} Baht transferred to Account Number: {recipient_account}.")
                    self.save_data(self.db)

                    result = messagebox.askyesno("Get Transfer Slip", "Would you like to take transfer slip?")
                    if result:
                        utils.print_transfer_slip(self.current_user, recipient, amount)
                    self.go_back(self.parent)

                else:
                    messagebox.showerror("Insufficient Funds", "Not enough balance.")
            else:
                messagebox.showerror("Transfer Failed", "Recipient account not found.")

    def go_back(self, parent):
        return super().go_back(parent)

