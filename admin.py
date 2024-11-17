import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from customer import BasePage
from data_handler import DataHandler
import config
import random
import utils


class AdminLoginPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Admin Login")
        
        self.email = ctk.StringVar()
        self.password = ctk.StringVar()

        self.instruction = ctk.CTkLabel(master, text="Please enter admin email and password!", font=("Helvetica", 25), text_color="red")
        self.instruction.pack(pady=25)

        self.input_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.input_frame.pack(pady=15)

        self.label_email = ctk.CTkLabel(self.input_frame, text="Email:", font=("Helvetica", 25))
        self.label_email.grid(row=1, column=1, padx=10, pady=10)
        self.entry_email = ctk.CTkEntry(self.input_frame, font=("Helvetica", 18), width=350, height=50, textvariable=self.email)
        self.entry_email.grid(row=1, column=2, padx=10, pady=10)

        self.label_password = ctk.CTkLabel(self.input_frame, text="Password:", font=("Helvetica", 25))
        self.label_password.grid(row=2, column=1, padx=10, pady=10)
        self.entry_password = ctk.CTkEntry(self.input_frame, show="*", font=("Helvetica", 18), width=350, height=50, textvariable=self.password)
        self.entry_password.grid(row=2, column=2, padx=10, pady=10)

        self.login_button = ctk.CTkButton(master, text="Log In", font=("Helvetica", 25), width=200, height=40, command=self.login)
        self.login_button.pack(pady=20)
        self.login_button.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

    def login(self):
        if self.email.get() == config.ADMIN_EMAIL and self.password.get() == config.ADMIN_PASSWORD:
            data_handler = DataHandler()
            db = data_handler.get_customers()

            # master is log_in_page
            self.master.withdraw()
            admin_menu = ctk.CTkToplevel(self.master)
            AdminMenu(admin_menu, db, data_handler)
        else:
            messagebox.showerror(title="Log In Failed!", message="Invalid Email or Password!\nPlease try again!")


class AdminMenu(BasePage):
    def __init__(self, master, db, data_handler) -> None:
        super().__init__(master, "Admin Menu")
        self.db = db
        self.data_handler = data_handler

        self.instruction = ctk.CTkLabel(master, text="Please make a selection!", font=("Helvetica", 25), text_color="red")
        self.instruction.pack(pady=25)

        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.add_customer_btn = ctk.CTkButton(self.button_frame, text="Register Customer", font=("Helvetica", 20), width=400, height=50, command=self.register_customer)
        self.add_customer_btn.grid(row=1, column=1, padx=10, pady=10)

        self.view_customer_btn = ctk.CTkButton(self.button_frame, text="Customer List", width=400, font=("Helvetica", 20), height=50, command=self.view_customer)
        self.view_customer_btn.grid(row=2, column=1, padx=10, pady=10)

        self.exit_btn = ctk.CTkButton(self.button_frame, text="Exit", width=400, height=50, font=("Helvetica", 20), command=self.exit_customer)
        self.exit_btn.grid(row=3, column=1, padx=10, pady=10)

    def register_customer(self):
        self.master.withdraw()
        register_window = ctk.CTkToplevel(self.master)
        RegisterCustomer(register_window, self.db, self.data_handler)

    def view_customer(self):
        self.master.withdraw()
        view_customer_window = ctk.CTkToplevel(self.master)
        ViewCustomer(view_customer_window, self.data_handler)

    def exit_customer(self):
        sys.exit()


class RegisterCustomer(BasePage):
    def __init__(self, master, db, data_handler) -> None:
        super().__init__(master, "Register Customer")
        self.db = db
        self.data_handler = data_handler

        # acc no is automatically set to a random number
        self.account_no = ctk.StringVar(value=str(random.randint(1000, 99999)))
        self.password = ctk.StringVar()
        self.f_name = ctk.StringVar()
        self.l_name = ctk.StringVar()
        self.amount = ctk.DoubleVar()

        self.instruction = ctk.CTkLabel(master, text="Please fill customer details!", font=("Helvetica", 25), text_color="red")
        self.instruction.pack(pady=25)

        # frame to hold inputs
        self.input_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.account_no_label = ctk.CTkLabel(self.input_frame, text="Account Number: ", font=("Helvetica", 25), anchor="e")
        self.account_no_label.grid(row=1, column=1, padx=10, pady=10)
        self.account_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 18), textvariable=self.account_no, state="disabled", width=200)
        self.account_entry.grid(row=1, column=2, padx=10, pady=10)

        self.password_label = ctk.CTkLabel(self.input_frame, text="Password: ", font=("Helvetica", 25), anchor="e")
        self.password_label.grid(row=2, column=1, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 18), textvariable=self.password, width=200)
        self.password_entry.grid(row=2, column=2, padx=10, pady=10)

        self.fname_label = ctk.CTkLabel(self.input_frame, text="First Name: ", font=("Helvetica", 25), anchor="e")
        self.fname_label.grid(row=3, column=1, padx=10, pady=10)
        self.fname_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 18), textvariable=self.f_name, width=200)
        self.fname_entry.grid(row=3, column=2, padx=10, pady=10)

        self.lname_label = ctk.CTkLabel(self.input_frame, text="Last Name: ", font=("Helvetica", 25), anchor="e")
        self.lname_label.grid(row=4, column=1, padx=10, pady=10)
        self.lname_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 18), textvariable=self.l_name, width=200)
        self.lname_entry.grid(row=4, column=2, padx=10, pady=10)

        self.amount_label = ctk.CTkLabel(self.input_frame, text="Initial Amount: ", font=("Helvetica", 25), anchor="e")
        self.amount_label.grid(row=5, column=1, padx=10, pady=10)
        self.amount_entry = ctk.CTkEntry(self.input_frame, font=("Helvetica", 18), textvariable=self.amount, width=200)
        self.amount_entry.grid(row=5, column=2, padx=10, pady=10),

        self.button_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.button_frame.pack(padx=10, pady=20)
        self.register_btn = ctk.CTkButton(self.button_frame, text="Register", width=300, height=45, font=("Helvetica", 18), command=self.register)
        self.register_btn.pack(padx=10, pady=10)
        self.back_btn = ctk.CTkButton(self.button_frame, text="Back", width=300, height=45, font=("Helvetica", 18), command=self.main_menu)
        self.back_btn.pack(padx=10, pady=10)

    def register(self):
        if self.data_handler.username_exists(self.f_name.get(), self.l_name.get()):
            messagebox.showerror("Username Exists!", message="Current username already exists.")
        elif self.data_handler.password_exists(self.password.get()):

            messagebox.showerror("Password Exists!", message="Current password already exists.")
        
        elif self.password.get() and self.f_name.get() and self.l_name.get():

            new_customer = {"account_no": self.account_no.get(), "password": self.password.get(), "f_name": self.f_name.get().upper(), "l_name": self.l_name.get().upper(), "amount": self.amount.get(), "transaction_history": list(), "status": True}
            self.db.append(new_customer)
            self.data_handler.save_data(self.db)

            messagebox.showinfo("Customer Registered!", message="A new customer is registered succesfully!")
            self.main_menu()
                

        else:
            messagebox.showerror("Empty Field Exists!", message="Please fill all the empty fields.")

    def main_menu(self):
        self.master.withdraw()
        self.master.master.deiconify()

        
class ViewCustomer(BasePage):
    def __init__(self, master, data_handler) -> None:
        super().__init__(master, "Customer Management")
        self.data_handler = data_handler

        headers = ["NO", "Account Number", "Password", "First Name", "Last Name", "Amount", "Status", "Actions"]

        self.topic = ctk.CTkLabel(master, text="Customer Management", font=("Helvetica", 28, "bold"), text_color="red")
        self.topic.pack(pady=25)

        self.list_frame = ctk.CTkFrame(master, width=1200, height=400)
        self.list_frame.pack(pady=10, padx=10)
        self.list_frame.pack_propagate(False)

        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 17), rowheight=30)  # Set row font size and height
        style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))
        style.configure("Treeview", rowheight=80)

        self.tree = ttk.Treeview(self.list_frame, columns=headers, show='headings', height=10, yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=100, anchor=tk.CENTER)

        self.tree.column("Account Number", width=200)
        self.tree.column("Password", width=150)
        self.tree.column("First Name", width=150)
        self.tree.column("Last Name", width=150)
        self.tree.column("Amount", width=150)
        self.tree.column("Status", width=150)
        self.tree.column("Actions", width=180)

        self.tree.bind("<Button-1>", self.handle_click)  # Handle clicks on action links

        self.load_customers()

        button_frame = ctk.CTkFrame(master, fg_color="transparent")
        button_frame.pack(pady=10)

        return_btn = ctk.CTkButton(button_frame, text="Back", width=300, height=40, font=("Helvetica", 18), command=self.main_menu)
        return_btn.pack(side=tk.LEFT, padx=10)

        refresh_btn = ctk.CTkButton(button_frame, text="Refresh", width=300, height=40, font=("Helvetica", 18), command=self.refresh_customers)
        refresh_btn.pack(side=tk.LEFT, padx=10)

    def load_customers(self):
     
        self.data_handler.refresh_customers()
        customers = self.data_handler.get_customers()[::-1]

        for index, customer in enumerate(customers, start=1):
            status = "Active" if customer["status"] else "Locked"
            values = (index, customer["account_no"], customer["password"], customer["f_name"], customer["l_name"], customer["amount"], status, "Edit | Delete")
            self.tree.insert('', tk.END, values=values)

    def handle_click(self, event):
   
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = int(self.tree.identify_column(event.x).replace("#", ""))
            row_id = self.tree.identify_row(event.y)
            if col == 8:  # Actions column
                self.open_action_menu(row_id)

    def open_action_menu(self, row_id):
        action_popup = tk.Menu(self.tree, tearoff=0)
        font_style = (("Helvetica", 16))
        action_popup.add_command(label="Edit", command=lambda: self.edit_customer(row_id), font=font_style)
        action_popup.add_command(label="Delete", command=lambda: self.confirm_delete(row_id), font=font_style)
        action_popup.post(self.tree.winfo_pointerx(), self.tree.winfo_pointery())

    def refresh_customers(self):

        self.data_handler.refresh_customers()
        self.tree.delete(*self.tree.get_children())
        self.load_customers()

    def edit_customer(self, row_id):
        customer_data = self.tree.item(row_id)["values"]
        account_no, password, f_name, l_name, amount, status = customer_data[1:7]
        status_bool = (status == "Active")

        edit_window = ctk.CTkToplevel(self.master)
        edit_window.title("Edit Customer")
        edit_window.geometry("350x300")
        edit_window.resizable(False, False)

        ctk.CTkLabel(edit_window, text="Account Number").grid(row=0, column=0, padx=10, pady=5)
        acc_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=account_no), state="disabled", width=200)
        acc_entry.grid(row=0, column=1)

        ctk.CTkLabel(edit_window, text="Password").grid(row=1, column=0, pady=5)
        pass_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=password), width=200)
        pass_entry.grid(row=1, column=1)

        ctk.CTkLabel(edit_window, text="First Name").grid(row=2, column=0, pady=5)
        first_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=f_name), width=200)
        first_entry.grid(row=2, column=1)

        ctk.CTkLabel(edit_window, text="Last Name").grid(row=3, column=0, pady=5)
        last_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=l_name), width=200)
        last_entry.grid(row=3, column=1)

        ctk.CTkLabel(edit_window, text="Amount").grid(row=4, column=0, pady=5)
        amount_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=amount), width=200)
        amount_entry.grid(row=4, column=1)

        ctk.CTkLabel(edit_window, text="Status").grid(row=5, column=0, pady=5)
        status_check = ctk.CTkCheckBox(edit_window, text="", variable=tk.BooleanVar(value=status_bool))
        status_check.grid(row=5, column=1)

        save_btn = ctk.CTkButton(edit_window, text="Save", command=lambda: self.save_changes(row_id, pass_entry.get(), first_entry.get(), last_entry.get(), amount_entry.get(), status_check.get(), edit_window))
        save_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def save_changes(self, row_id, password, f_name, l_name, amount, status, edit_window):
  
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
        customer_data = self.tree.item(row_id)["values"]
        account_no = str(customer_data[1]) # convert acc_no to str

        if messagebox.askyesno('Delete Account', f'Confirm to delete account number {account_no}?'):
            db = self.data_handler.get_customers()
            db = [customer for customer in db if customer["account_no"] != account_no]
     
            self.data_handler.save_data(db)
            self.refresh_customers()
            messagebox.showinfo("Deleted", f"Account Number '{account_no}' deleted successfully.")

    def main_menu(self):
        self.master.destroy()
        self.master.master.deiconify()


root = ctk.CTk()
AdminLoginPage(root)
root.mainloop()