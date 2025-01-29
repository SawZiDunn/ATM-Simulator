import customtkinter as ctk
from tkinter import messagebox, ttk
import utils
from data_handler import DataHandler
import sys
from transaction import BasePage, Transfer, Deposit, Withdraw

 
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
        account_number = self.entry_account.get().strip()
        password = self.entry_password.get().strip()

        data_handler = DataHandler()
        db = data_handler.get_customers()
        
        user = next((user for user in db if user['account_no'] == account_number and str(user['password']) == password), None)
        
        if user:
            self.entry_account.delete(0, ctk.END)
            self.entry_password.delete(0, ctk.END)
            self.master.withdraw()
            main_menu_window = ctk.CTkToplevel(self.master)
            UserMenu(main_menu_window, user, db, data_handler.save_data)
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

        text = "Your account is locked!\nYou wont be able to make transactions!\nPlease contact our back for further information."
        self.locked_acc_message = ctk.CTkLabel(master, text=text, font=("Helvetica", 22, "bold"), text_color="red", width=200)
        if not current_user["status"]:
            self.locked_acc_message.pack(pady=10)
        

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

        self.exit_button = ctk.CTkButton(master, text="Exit", font=("Helvetica", 12), width=180, height=35, fg_color="red", command=lambda: sys.exit(1))
        self.exit_button.pack(pady=10)

    def show_balance(self):
        self.master.withdraw()
        balance_window = ctk.CTkToplevel(self.master)
        Balance(balance_window, self.master, self.current_user)

    def withdraw_money(self):
        if not self.current_user["status"]:
            messagebox.showwarning("Account Locked!", "Your account is locked!\nYou cannot make withdrawal.")
        else:
            self.master.withdraw()
            withdraw_window = ctk.CTkToplevel(self.master)
            Withdraw(withdraw_window, self.current_user, self.db, self.save_data, self.master)

    def deposit_money(self):
        if not self.current_user["status"]:
            messagebox.showwarning("Account Locked!", "Your account is locked!\nYou cannot make deposit.")
        else:
            self.master.withdraw()
            deposit_window = ctk.CTkToplevel(self.master)
            Deposit(deposit_window, self.current_user, self.db, self.save_data, self.master)

    def transfer_money(self):
        if not self.current_user["status"]:
            messagebox.showwarning("Account Locked!", "Your account is locked!\nYou cannot make transfer.")
        else:
            self.master.withdraw()
            self.transfer_window = ctk.CTkToplevel(self.master)
            Transfer(self.transfer_window, self.current_user, self.db, self.save_data, self.master)

    def show_history(self):
        self.master.withdraw()
        transaction_history_window = ctk.CTkToplevel(self.master)
        TransactionHistory(transaction_history_window, self.current_user, self.db, self.master)

    def log_out(self):
        self.master.destroy()
        self.master.master.deiconify()


class Balance(BasePage):
    def __init__(self, master, parent, current_user):
        super().__init__(master, "Balance Inquiry")
        self.parent = parent

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
            command=lambda: self.go_back(self.parent),
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

    def go_back(self, parent):
        return super().go_back(parent)


class TransactionHistory(BasePage):
    def __init__(self, master, current_user, db, parent):
        super().__init__(master, "Transaction History")
        self.current_user = current_user
        self.db = db
        self.parent = parent

        # Title label
        title_label = ctk.CTkLabel(master, text="Transaction History", font=("Arial", 25, "bold"))
        title_label.pack(pady=20)

        if current_user["transaction_history"]:
            # Scrollable table for transaction list
            self.table_frame = ctk.CTkFrame(master, width=1200, height=400)
            self.table_frame.pack(padx=10, pady=10)
            self.table_frame.pack_propagate(False)

            # Add scrollbars
            self.scrollbar = ttk.Scrollbar(self.table_frame, orient=ctk.VERTICAL)
            self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

            self.table = ttk.Treeview(self.table_frame, columns=("Description", "Date", "Amount"), show="headings", height=10, yscrollcommand=self.scrollbar.set)
            self.table.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
            self.table.configure(yscrollcommand=self.scrollbar.set)

            style = ttk.Style()
            style.configure("Treeview", font=("Helvetica", 17), rowheight=70)  # Set row font size and height
            style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))
            style.configure("Treeview", rowheight=60)

            # defining column widths
            self.table.column("Description", width=400, anchor=ctk.CENTER)
            self.table.column("Date", width=300, anchor=ctk.CENTER)
            self.table.column("Amount", width=200, anchor=ctk.CENTER)

            # defining column headings
            self.table.heading("Description", text="Description")
            self.table.heading("Date", text="Date")
            self.table.heading("Amount", text="Amount")

            # Define row styles for positive and negative transactions
            self.table.tag_configure("positive", foreground="green")
            self.table.tag_configure("negative", foreground="red")

            # Add transactions to the table with the most recent one at the top
            transaction_history = self.current_user["transaction_history"][::-1]
            for transaction in transaction_history:
                description, date, amount = transaction
                formatted_amount = f"+{amount:,.2f} Baht" if amount >= 0 else f"{amount:,.2f} Baht"
                tag = "positive" if amount >= 0 else "negative"
                self.table.insert("", "end", values=(description, date, formatted_amount), tags=(tag,))
        else:
            initial_label = ctk.CTkLabel(master, text="No Transaction History!", font=("Arial", 18, "bold"), text_color="red")
            initial_label.pack(pady=20)

        # frame to hold buttons
        button_frame = ctk.CTkFrame(master, fg_color="transparent")
        button_frame.pack(pady=10)

        back_button = ctk.CTkButton(button_frame, text="Back to Menu", command=lambda: self.go_back(self.parent), width=300, height=30)
        back_button.grid(row=0, column=0, padx=10)

        print_button = ctk.CTkButton(button_frame, text="Print Transaction History", command=lambda: utils.print_transaction_history(self.current_user), width=300, height=30)
        print_button.grid(row=0, column=1, padx=10)

    def go_back(self, parent):
        return super().go_back(parent)


