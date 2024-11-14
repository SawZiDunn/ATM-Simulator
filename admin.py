import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from CTkMessagebox import CTkMessagebox
from customer import BasePage
from data_handler import DataHandler
import config
import random



class AdminLoginPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Admin Login")
        
        self.email = ctk.StringVar()
        self.password = ctk.StringVar()

        self.instruction = ctk.CTkLabel(master, text="Please enter admin email and password!", font=("Helvetica", 18))
        self.instruction.pack(pady=25)

        self.input_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.label_email = ctk.CTkLabel(self.input_frame, text="Email:", font=("Helvetica", 18))
        self.label_email.grid(row=1, column=1, padx=10, pady=10)
        self.entry_email = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), width=300, height=40, textvariable=self.email)
        self.entry_email.grid(row=1, column=2, padx=10, pady=10)

        self.label_password = ctk.CTkLabel(self.input_frame, text="Password:", font=("Helvetica", 18))
        self.label_password.grid(row=2, column=1, padx=10, pady=10)
        self.entry_password = ctk.CTkEntry(self.input_frame, show="*", font=("Helvetica", 12), width=300, height=40, textvariable=self.password)
        self.entry_password.grid(row=2, column=2, padx=10, pady=10)

        self.login_button = ctk.CTkButton(master, text="Log In", font=("Helvetica", 16), fg_color="blue", width=200, height=40, command=self.login)
        self.login_button.pack(pady=20)
        self.login_button.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

    def login(self):
        if self.email.get() == config.ADMIN_EMAIL and self.password.get() == config.ADMIN_PASSWORD:
            data_handler = DataHandler()
            db = data_handler.get_customers()

            self.master.withdraw()
            self.admin_menu = ctk.CTkToplevel(self.master)
            AdminMenu(self.admin_menu, db, data_handler)
        else:
            CTkMessagebox(title="Log In Failed!", message="Invalid Email or Password!\nPlease try again!")


class AdminMenu(BasePage):
    def __init__(self, master, db, data_handler) -> None:
        super().__init__(master, "Admin Menu")
        self.db = db
        self.data_handler = data_handler

        self.instruction = ctk.CTkLabel(master, text="Please make a selection!", font=("Helvetica", 18))
        self.instruction.pack(pady=25)

        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.add_customer_btn = ctk.CTkButton(self.button_frame, text="Register Customer", font=("Helvetica", 18), width=200, height=40, command=self.register_customer)
        self.add_customer_btn.grid(row=1, column=1, padx=10, pady=10)

        self.view_customer_btn = ctk.CTkButton(self.button_frame, text="Customer List", width=200, font=("Helvetica", 18), height=40, command=self.view_customer)
        self.view_customer_btn.grid(row=2, column=1, padx=10, pady=10)

        self.exit_btn = ctk.CTkButton(self.button_frame, text="Exit", width=200, height=40, font=("Helvetica", 18), command=self.exit_customer)
        self.exit_btn.grid(row=3, column=1, padx=10, pady=10)

    def register_customer(self):
        self.master.withdraw()
        self.register_window = ctk.CTkToplevel(self.master)
        data_handler = DataHandler()
        db = data_handler.get_customers()
        RegisterCustomer(self.register_window, data_handler=data_handler, db=db)


    def view_customer(self):
        self.master.withdraw()
        self.view_customer_window = ctk.CTkToplevel(self.master)
        ViewCustomer(self.view_customer_window, self.data_handler)

    def exit_customer(self):
        sys.exit()

class RegisterCustomer(BasePage):
    def __init__(self, master, db, data_handler) -> None:
        super().__init__(master, "Register Customer")
        self.db = db
        self.data_handler = data_handler

        self.account_no = ctk.StringVar(value=str(random.randint(1000, 99999)))
        self.password = ctk.StringVar()
        self.f_name = ctk.StringVar()
        self.l_name = ctk.StringVar()
        self.amount = ctk.DoubleVar()

        self.instruction = ctk.CTkLabel(master, text="Please fill customer details!", font=("Helvetica", 18))
        self.instruction.pack(pady=25)

        # frame to hold inputs
        self.input_frame = ctk.CTkFrame(master)
        self.input_frame.pack(pady=10)

        self.account_no_label = ctk.CTkLabel(self.input_frame, text="Account Number: ", font=("Helvetica", 18))
        self.account_no_label.grid(row=1, column=1, padx=10, pady=10)
        self.account_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), textvariable=self.account_no, state="disabled")
        self.account_entry.grid(row=1, column=2, padx=10, pady=10)

        self.password_label = ctk.CTkLabel(self.input_frame, text="Password: ", font=("Helvetica", 18))
        self.password_label.grid(row=2, column=1, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), textvariable=self.password)
        self.password_entry.grid(row=2, column=2, padx=10, pady=10)

        self.fname_label = ctk.CTkLabel(self.input_frame, text="First Name: ", font=("Helvetica", 18))
        self.fname_label.grid(row=3, column=1, padx=10, pady=10)
        self.fname_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), textvariable=self.f_name)
        self.fname_entry.grid(row=3, column=2, padx=10, pady=10)

        self.lname_label = ctk.CTkLabel(self.input_frame, text="Last Name: ", font=("Helvetica", 18))
        self.lname_label.grid(row=4, column=1, padx=10, pady=10)
        self.lname_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), textvariable=self.l_name)
        self.lname_entry.grid(row=4, column=2, padx=10, pady=10)

        self.amount_label = ctk.CTkLabel(self.input_frame, text="Initial Amount: ", font=("Helvetica", 18))
        self.amount_label.grid(row=5, column=1, padx=10, pady=10)
        self.amount_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 12), textvariable=self.amount)
        self.amount_entry.grid(row=5, column=2, padx=10, pady=10)

        self.register_btn = ctk.CTkButton(master, text="Register", width=200, height=40, font=("Helvetica", 12), command=self.register)
        self.register_btn.pack(padx=10, pady=10)
        self.back_btn = ctk.CTkButton(master, text="Back", width=200, height=40, font=("Helvetica", 12), command=self.main_menu)
        self.back_btn.pack(padx=10, pady=10)

    def register(self):
        new_customer = {"account_no": self.account_no.get(), "password": self.password.get(), "f_name": self.f_name.get(), "l_name": self.l_name.get(), "amount": self.amount.get(), "transaction_history": list(),"status": True}
        self.db.append(new_customer)
        self.data_handler.save_data(self.db)

        CTkMessagebox(message="A new customer is registered succesfully!")
        self.master.withdraw()
        self.master.master.deiconify()
        # print(DATA_HANDLER.get_customers())

    def main_menu(self):
        self.master.withdraw()
        self.master.master.deiconify()

        
class ViewCustomer(BasePage):
    def __init__(self, master, data_handler) -> None:
        super().__init__(master, "Customer Management")
        self.data_handler = data_handler

        headers = ["NO", "Account Number", "Password", "First Name", "Last Name", "Amount", "Status", "Actions"]

        self.list_frame = ctk.CTkFrame(master, width=800)
        self.list_frame.pack(pady=10, padx=10)

        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.list_frame, columns=headers, show='headings', height=10, yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=100, anchor=tk.CENTER)

        self.tree.column("Account Number", width=150)
        self.tree.column("Password", width=150)
        self.tree.column("First Name", width=150)
        self.tree.column("Last Name", width=150)
        self.tree.column("Amount", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("Actions", width=200)

        self.tree.bind("<Button-1>", self.handle_click)  # Handle clicks on action links

        self.load_customers()

        button_frame = ctk.CTkFrame(master)
        button_frame.pack(pady=10)

        return_btn = ctk.CTkButton(button_frame, text="Back", width=200, height=40, font=("Helvetica", 12), command=self.main_menu)
        return_btn.pack(side=tk.LEFT, padx=10)

        refresh_btn = ctk.CTkButton(button_frame, text="Refresh", width=200, height=40, font=("Helvetica", 12), command=self.refresh_customers)
        refresh_btn.pack(side=tk.LEFT, padx=10)

    def load_customers(self):
        """Load customers and add Edit/Delete links."""
        self.data_handler.refresh_customers()
        customers = self.data_handler.get_customers()
        for index, customer in enumerate(customers, start=1):
            status = "Active" if customer["status"] else "Locked"
            values = (index, customer["account_no"], customer["password"], customer["f_name"], customer["l_name"], customer["amount"], status, "Edit | Delete")
            self.tree.insert('', tk.END, values=values)

    def handle_click(self, event):
        """Handle click events on Treeview items."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = int(self.tree.identify_column(event.x).replace("#", ""))
            row_id = self.tree.identify_row(event.y)
            if col == 8:  # Actions column
                self.open_action_menu(row_id)

    def open_action_menu(self, row_id):
        """Determine whether to edit or delete based on click position."""
        action_popup = tk.Menu(self.tree, tearoff=0)
        action_popup.add_command(label="Edit", command=lambda: self.edit_customer(row_id))
        action_popup.add_command(label="Delete", command=lambda: self.confirm_delete(row_id))
        action_popup.post(self.tree.winfo_pointerx(), self.tree.winfo_pointery())

    def refresh_customers(self):
        """Reload the customer list."""
        self.data_handler.refresh_customers()
        self.tree.delete(*self.tree.get_children())
        self.load_customers()

    def edit_customer(self, row_id):
        """Open an Edit Customer window."""
        customer_data = self.tree.item(row_id)["values"]
        account_no, password, f_name, l_name, amount, status = customer_data[1:7]
        status_bool = (status == "Active")

        edit_window = ctk.CTkToplevel(self.master)
        edit_window.title("Edit Customer")

        ctk.CTkLabel(edit_window, text="Account Number").grid(row=0, column=0, padx=10, pady=5)
        acc_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=account_no), state="disabled")
        acc_entry.grid(row=0, column=1)

        ctk.CTkLabel(edit_window, text="Password").grid(row=1, column=0)
        pass_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=password))
        pass_entry.grid(row=1, column=1)

        ctk.CTkLabel(edit_window, text="First Name").grid(row=2, column=0)
        first_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=f_name))
        first_entry.grid(row=2, column=1)

        ctk.CTkLabel(edit_window, text="Last Name").grid(row=3, column=0)
        last_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=l_name))
        last_entry.grid(row=3, column=1)

        ctk.CTkLabel(edit_window, text="Amount").grid(row=4, column=0)
        amount_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=amount))
        amount_entry.grid(row=4, column=1)

        ctk.CTkLabel(edit_window, text="Status").grid(row=5, column=0)
        status_check = ctk.CTkCheckBox(edit_window, text="", variable=tk.BooleanVar(value=status_bool))
        status_check.grid(row=5, column=1)

        save_btn = ctk.CTkButton(edit_window, text="Save", command=lambda: self.save_changes(row_id, pass_entry.get(), first_entry.get(), last_entry.get(), amount_entry.get(), status_check.get(), edit_window))
        save_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def save_changes(self, row_id, password, f_name, l_name, amount, status, edit_window):
        """Save edited customer data."""
        customer_data = self.tree.item(row_id)["values"]
        account_no = str(customer_data[1]) # convert acc_no to str
        db = self.data_handler.get_customers()
    
        for customer in db:
            if customer["account_no"] == account_no:
                customer["password"] = password
                customer["f_name"] = f_name
                customer["l_name"] = l_name
                customer["amount"] = float(amount)
                customer["status"] = status
        self.data_handler.save_data(db)
        self.refresh_customers()
        edit_window.destroy()
        messagebox.showinfo("Success", "Customer updated successfully!")

    def confirm_delete(self, row_id):
        """Prompt to confirm deletion."""
        customer_data = self.tree.item(row_id)["values"]
        account_no = str(customer_data[1]) # convert acc_no to str

        if messagebox.askyesno('Delete', f'Confirm delete account {account_no}?'):
            db = self.data_handler.get_customers()
            print(account_no, type(account_no))
            print(db)
            db = [customer for customer in db if customer["account_no"] != account_no]
     
            self.data_handler.save_data(db)
            self.refresh_customers()
            print(self.data_handler.get_customers())
    
            messagebox.showinfo("Deleted", f"Customer {account_no} deleted successfully.")

    def main_menu(self):
        """Return to the main menu."""
        self.master.destroy()
        self.master.master.deiconify()

root = ctk.CTk()
AdminLoginPage(root)
root.mainloop()