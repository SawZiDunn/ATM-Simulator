import customtkinter as ctk
import pickle
from tkinter import messagebox, ttk
import utils
from data_handler import DataHandler

class BasePage:
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)

        window_width = 1200
        window_height = 800
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(master, text="Ladkrabang Bank ATM", font=("Helvetica", 50, "bold"))
        self.label.pack(pady=25)


class LoginPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "ATM Login")

        self.instruction = ctk.CTkLabel(master, text="Please enter bank account number and password!", font=("Helvetica", 25))
        self.instruction.pack(pady=25)

        self.label_account = ctk.CTkLabel(master, text="Bank Account No:", font=("Helvetica", 25))
        self.label_account.pack(pady=10)
        self.entry_account = ctk.CTkEntry(master, font=("Helvetica", 18), width=350, height=50)
        self.entry_account.pack(pady=5)

        self.label_password = ctk.CTkLabel(master, text="Password:", font=("Helvetica", 25))
        self.label_password.pack(pady=5)
        self.entry_password = ctk.CTkEntry(master, show="*", font=("Helvetica", 18), width=350, height=50)
        self.entry_password.pack(pady=5)

        self.login_button = ctk.CTkButton(master, text="Log In", font=("Helvetica", 25), fg_color="blue", width=200, height=40, command=self.login)
        self.login_button.pack(pady=20)
        self.login_button.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

    def login(self):
        account_number = self.entry_account.get()
        password = self.entry_password.get()

        data_handler = DataHandler()
        self.db = data_handler.get_customers()
        
        user = next((user for user in self.db if user['account_no'] == account_number and str(user['password']) == password), None)
        
        if user:
            self.entry_account.delete(0, ctk.END)
            self.entry_password.delete(0, ctk.END)
            self.master.withdraw()
            main_menu_window = ctk.CTkToplevel(self.master)
            self.current_user = user
            UserMenu(main_menu_window, self.current_user, self.db, data_handler.save_data)
        else:
            messagebox.showerror("Login Failed", "Invalid account number or password.")
    

class UserMenu(BasePage):
    def __init__(self, master, current_user, db, save_data):
        super().__init__(master, "User Menu")
        self.current_user = current_user
        self.db = db
        self.save_data = save_data

        self.main_menu_header = ctk.CTkLabel(master, text="User Main Menu", font=("Helvetica", 25, "bold"), width=200)
        self.main_menu_header.pack(pady=10)

        self.intro = ctk.CTkLabel(master, text=f"Hello, {current_user["f_name"]} {current_user["l_name"]}", font=("Helvetica", 25), width=200)
        self.intro.pack(pady=10)

        # frame to hold 4 buttons
        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.balance_button = ctk.CTkButton(self.button_frame, text="Balance", font=("Helvetica", 18), width=150, height=40, command=self.show_balance)
        self.balance_button.grid(row=0, column=0, padx=15, pady=10)

        self.withdraw_button = ctk.CTkButton(self.button_frame, text="Withdraw", font=("Helvetica", 18), width=150, height=40, command=self.withdraw_money)
        self.withdraw_button.grid(row=1, column=0, padx=15, pady=10)

        self.deposit_button = ctk.CTkButton(self.button_frame, text="Deposit", font=("Helvetica", 18), width=150, height=40, command=self.deposit_money)
        self.deposit_button.grid(row=0, column=1, padx=15, pady=10)

        self.transfer_button = ctk.CTkButton(self.button_frame, text="Transfer", font=("Helvetica", 18), width=150, height=40, command=self.transfer_money)
        self.transfer_button.grid(row=1, column=1, padx=15, pady=10)

        self.history_button = ctk.CTkButton(master, text="Transaction History", font=("Helvetica", 18), width=180, height=35, command=self.show_history)
        self.history_button.pack(pady=15)

        self.logout_button = ctk.CTkButton(master, text="Log Out", font=("Helvetica", 12), width=180, height=35, fg_color="red", command=self.log_out)
        self.logout_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(master, text="Exit", font=("Helvetica", 12), width=180, height=35, fg_color="red", command=master.quit)
        self.exit_button.pack(pady=10)

    def show_balance(self):
        self.master.withdraw()
        balance_window = ctk.CTkToplevel(self.master)
        Balance(balance_window, self.current_user)

    def withdraw_money(self):
        self.master.withdraw()
        withdraw_window = ctk.CTkToplevel(self.master)
        Withdraw(withdraw_window, self.current_user, self.db, self.save_data, self.master)

    def deposit_money(self):
        self.master.withdraw()
        deposit_window = ctk.CTkToplevel(self.master)
        Deposit(deposit_window, self.current_user, self.db, self.save_data, self.master)

    def transfer_money(self):
        self.master.withdraw()
        self.transfer_window = ctk.CTkToplevel(self.master)
        Transfer(self.transfer_window, self.current_user, self.db, self.save_data, self.master)

    def show_history(self):
        self.master.withdraw()
        self.transaction_history_window = ctk.CTkToplevel(self.master)
        TransactionHistory(self.transaction_history_window, self.current_user, self.db, self.master)
        

    def log_out(self):
        self.master.destroy()
        self.master.master.deiconify()


class Balance(BasePage):
    def __init__(self, master, current_user):
        super().__init__(master, "Balance Inquiry")

        main_frame = ctk.CTkFrame(master, fg_color="transparent")
        main_frame.pack(pady=20)

        ctk.CTkLabel(main_frame, text="Your current Balance is: ", font=("Helvetica", 23)).grid(row=0, column=0, columnspan=2, pady=20)

        self.balance_var = ctk.StringVar(value=current_user["amount"])
        ctk.CTkLabel(
            main_frame,
            text=f"{self.balance_var.get()} Baht",
            font=('Helvetica', 24, 'bold')
        ).grid(row=1, column=0, columnspan=2, pady=10)
        
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=30)
        
        
        ctk.CTkButton(
            button_frame, 
            text="Back", 
            command=self.go_to_main_menu,
            width=150, height=40
        ).grid(row=0, column=0, padx=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Print Balance Receipt", 
            command=lambda: utils.print_balance_slip(current_user),
            width=150, height=40
        ).grid(row=0, column=1, padx=10)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def go_to_main_menu(self):
        self.master.withdraw()
        self.master.master.deiconify()

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

        # for amount buttons
        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(pady=20)

        amounts = [500, 1000, 2000, 5000, 10000, 20000]
        row, col = 0, 0
        for amount in amounts:
            ctk.CTkButton(self.button_frame, text=str(amount), font=("Helvetica", 15), width=100, height=35,
                          command=lambda amt=amount: self.set_amount(amt)).grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.deposit_button = ctk.CTkButton(master, text="Deposit", command=self.deposit, width=150, height=30)
        self.deposit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(master, text="Back", command=self.go_back, width=150, height=30)
        self.back_button.pack()


    def set_amount(self, amt):
        self.amount_entry.delete(0, ctk.END)
        self.amount_entry.insert(0, amt)

    def deposit(self):
        amount = float(self.amount_entry.get())
        self.current_user['amount'] += amount
        text = ("Deposit", utils.get_current_time(), amount)
        self.current_user["transaction_history"].append(text)
        messagebox.showinfo("Deposit Success", f"${amount} deposited successfully.")
        self.save_data(self.db)

        result = messagebox.askyesno("Get Deposit Slip", "Would you like to take deposit slip?")
        if result:
            utils.print_deposit_slip(self.current_user, amount)

        self.go_back()

    def go_back(self):
        self.master.destroy()
        self.parent.deiconify()

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

        self.amount_entry = ctk.CTkEntry(main_frame, font=("Helvetica", 12), width=200)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=10)

        # for amount buttons
        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(pady=20)

        amounts = [500, 1000, 2000, 5000, 10000, 20000]
        row, col = 0, 0
        for amount in amounts:
            ctk.CTkButton(self.button_frame, text=str(amount), font=("Helvetica", 12), width=90, height=35,
                          command=lambda amt=amount: self.set_amount(amt)).grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.withdraw_button = ctk.CTkButton(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.back_button = ctk.CTkButton(master, text="Back", command=self.go_back)
        self.back_button.pack()
        
        

    def set_amount(self, amount):
        """Set the amount in the entry field"""
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, str(amount))

    def withdraw(self):
        amount = float(self.amount_entry.get())
        if amount <= self.current_user['amount']:
            self.current_user['amount'] -= amount
            # transactin history logic
            text = ("Withdrawal", utils.get_current_time(), +amount)
            self.current_user["transaction_history"].append(text)
            messagebox.showinfo("Withdraw Success", f"${amount} withdrawn successfully.")
            self.save_data(self.db)
            result = messagebox.askyesno("Get Withdrawal Slip", "Would you like to take withdrawal slip?")
            if result:
                utils.print_withdrawal_slip(self.current_user, amount)
            self.go_back()
        else:
            messagebox.showerror("Insufficient Funds", "Not enough balance.")

    def go_back(self):
        self.master.destroy()
        self.parent.deiconify()

class TransactionHistory(BasePage):
    def __init__(self, master, current_user, db, parent):
        super().__init__(master, "Transaction History")
        self.current_user = current_user
        self.db = db
        self.parent = parent

        # Title label
        title_label = ctk.CTkLabel(master, text="Transaction History", font=("Arial", 25, "bold"))
        title_label.pack(pady=20)

        # Scrollable table for transaction list
        self.table_frame = ctk.CTkFrame(master, width=1200)
        self.table_frame.pack(padx=10, pady=10)

        # Add scrollbars
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=ctk.VERTICAL)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
        

        self.table = ttk.Treeview(self.table_frame, columns=("Description", "Date", "Amount"), show="headings", height=10, yscrollcommand=self.scrollbar.set)
        self.table.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.table.configure(yscrollcommand=self.scrollbar.set)

        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 17), rowheight=30)  # Set row font size and height
        style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))
        style.configure("Treeview", rowheight=40)

        # Set column widths
        self.table.column("Description", width=300, anchor=ctk.CENTER)
        self.table.column("Date", width=300, anchor=ctk.CENTER)
        self.table.column("Amount", width=200, anchor=ctk.CENTER)

        # Set column headings
        self.table.heading("Description", text="Description")
        self.table.heading("Date", text="Date")
        self.table.heading("Amount", text="Amount")
        

        # Add transactions to the table
        transaction_history = self.current_user["transaction_history"]
        for transaction in transaction_history:
            self.table.insert("", "end", values=(transaction[0], transaction[1], f"{transaction[2]:,.2f} Baht"))

        # Buttons
        button_frame = ctk.CTkFrame(master, fg_color="transparent")
        button_frame.pack(pady=10)

        back_button = ctk.CTkButton(button_frame, text="Back to Menu", command=self.go_back, width=300, height=30)
        back_button.grid(row=0, column=0, padx=10)

        print_button = ctk.CTkButton(button_frame, text="Print Transaction History", command=lambda: utils.print_transaction_history(self.current_user), width=300, height=30)
        print_button.grid(row=0, column=1, padx=10)

    def go_back(self):
        self.master.destroy()
        self.parent.deiconify()


class Transfer(BasePage):
    def __init__(self, master, current_user, db, save_data, parent):
        super().__init__(master, "Transfer")
        self.current_user = current_user
        self.db = db
        self.save_data = save_data
        self.parent = parent

        self.transfer_header = ctk.CTkLabel(master, text="Transfer Money", font=("Helvetica", 18, "bold"))
        self.transfer_header.pack(pady=10)

        # frame for input
        self.input_frame = ctk.CTkFrame(master)
        self.input_frame.pack(pady=10)

        self.account_label = ctk.CTkLabel(self.input_frame, text="Account No:", font=("Helvetica", 12))
        self.account_label.grid(row=0, column=0, padx=5, pady=10, sticky=ctk.E)
        self.account_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), width=200)
        self.account_entry.grid(row=0, column=1, padx=5, pady=10)

        self.amount_label = ctk.CTkLabel(self.input_frame, text="Transfer Amount:", font=("Helvetica", 12))
        self.amount_label.grid(row=1, column=0, padx=5, pady=10, sticky=ctk.E)
        self.amount_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), width=200)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=10)

        # for amount buttons
        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(pady=20)

        amounts = [500, 1000, 2000, 5000, 10000, 20000]
        row, col = 0, 0
        for amount in amounts:
            ctk.CTkButton(self.button_frame, text=str(amount), font=("Helvetica", 12), width=90, height=35,
                          command=lambda amt=amount: self.set_amount(amt)).grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # frame for menu and transfer
        self.action_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.action_frame.pack(pady=20)

        self.main_menu_button = ctk.CTkButton(self.action_frame, text="Main Menu", font=("Helvetica", 12), width=150, height=35, command=self.go_to_main_menu)
        self.main_menu_button.grid(row=0, column=0, padx=10, pady=10)

        self.transfer_button = ctk.CTkButton(self.action_frame, text="Transfer", font=("Helvetica", 12), width=150, height=35, command=self.make_transfer)
        self.transfer_button.grid(row=0, column=1, padx=10, pady=10)

    def set_amount(self, amount):

        self.amount_entry.delete(0, ctk.END)
        self.amount_entry.insert(0, str(amount))

    def go_to_main_menu(self):
        self.master.destroy()
        self.parent.deiconify()

    def make_transfer(self):
        recipient_account = self.account_entry.get()
        amount = float(self.amount_entry.get())
        recipient = next((user for user in self.db if user['account_no'] == recipient_account), None)

        if recipient:
            if recipient["account_no"] == self.current_user["account_no"]:
                messagebox.showwarning("Transfer Failed", "You cannot transfer to your own account!")
            elif amount <= self.current_user['amount']:
                self.current_user['amount'] -= amount
                recipient['amount'] += amount
                # transaction history logic
                # for current_user
                text = (f"Transfer to {recipient["f_name"]} {recipient["l_name"]}", utils.get_current_time(), -amount)
                self.current_user["transaction_history"].append(text)
                # for recipient
                text = (f"Transfer from {self.current_user["f_name"]} {self.current_user["l_name"]}", utils.get_current_time(), amount)
                recipient["transaction_history"].append(text)

                messagebox.showinfo("Transfer Success", f"${amount} transferred to {recipient_account}.")
                self.save_data(self.db)

                result = messagebox.askyesno("Get Transfer Slip", "Would you like to take transfer slip?")
                if result:
                    utils.print_transfer_slip(self.current_user, recipient, amount)
                self.go_to_main_menu()

            else:
                messagebox.showerror("Insufficient Funds", "Not enough balance.")
        else:
            messagebox.showerror("Transfer Failed", "Recipient account not found.")