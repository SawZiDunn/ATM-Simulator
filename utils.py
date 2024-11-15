from datetime import datetime
from tkinter import filedialog

def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def print_balance_slip(current_user):
        file_name = f"balance_slip_{current_user["f_name"]}_{current_user["l_name"]}"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=file_name)

        if file_path:
            try:
                with open(file_path, "w") as output_file:
                    output_file.write("Balance Slip\n")
                    output_file.write("----------------\n\n")
                    output_file.write(f"Name: {current_user["f_name"]} {current_user["l_name"]}\n\n")
                    output_file.write(f"Account Number: {current_user["account_no"]}\n\n")
                    output_file.write(f"Balance: {current_user["amount"]} Baht\n\n")
                    output_file.write(f"Date: {get_current_time()}")

            except Exception as e:
                print(f"An error occurred: {e}")
def print_transfer_slip(current_user, recipient, amount):
        file_name = f"transfer_slip_{current_user["f_name"]}_{current_user["l_name"]}"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=file_name)

        if file_path:
            try:
                with open(file_path, "w") as output_file:
                    output_file.write("Receipt\n")
                    output_file.write("----------------\n\n")
                    output_file.write(f"Transaction: Transfer\n\n")
                    output_file.write(f"Sender: {current_user["f_name"]} {current_user["l_name"]}\n\n")
                    output_file.write(f"Sender Account Number: {current_user["account_no"]}\n\n")
                    output_file.write(f"Recipient: {recipient["f_name"]} {recipient["l_name"]}\n\n")
                    output_file.write(f"Recipient Account Number: {recipient["account_no"]}\n\n")
                    output_file.write(f"Amount: {amount} Baht\n\n")
                    output_file.write(f"Balance: {current_user["amount"]} Baht\n\n")
                    output_file.write(f"Date: {get_current_time()}")

            except Exception as e:
                print(f"An error occurred: {e}")

def print_deposit_slip(current_user, amount):
        file_name = f"deposit_slip_{current_user["f_name"]}_{current_user["l_name"]}"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=file_name)

        if file_path:
            try:
                with open(file_path, "w") as output_file:
                    output_file.write("Receipt\n")
                    output_file.write("----------------\n\n")
                    output_file.write(f"Transaction: Deposit\n\n")
                    output_file.write(f"Name: {current_user["f_name"]} {current_user["l_name"]}\n\n")
                    output_file.write(f"Account Number: {current_user["account_no"]}\n\n")
                    output_file.write(f"Amount: {amount} Baht\n\n")
                    output_file.write(f"Balance: {current_user["amount"]} Baht\n\n")
                    output_file.write(f"Date: {get_current_time()}")

            except Exception as e:
                print(f"An error occurred: {e}")

def print_withdrawal_slip(current_user, amount):
        file_name = f"withdrawal_slip_{current_user["f_name"]}_{current_user["l_name"]}"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=file_name)

        if file_path:
            try:
                with open(file_path, "w") as output_file:
                    output_file.write("Receipt\n")
                    output_file.write("----------------\n\n")
                    output_file.write(f"Transaction: Withdrawal\n\n")
                    output_file.write(f"Name: {current_user["f_name"]} {current_user["l_name"]}\n\n")
                    output_file.write(f"Account Number: {current_user["account_no"]}\n\n")
                    output_file.write(f"Amount: {amount} Baht\n\n")
                    output_file.write(f"Balance: {current_user["amount"]} Baht\n\n")
                    output_file.write(f"Date: {get_current_time()}")

            except Exception as e:
                print(f"An error occurred: {e}")

def print_transaction_history(current_user):
     
     file_name = f"transaction_history_{current_user["f_name"]}_{current_user["l_name"]}"
     
     file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=file_name)
     if file_path:
        try:
            with open(file_path, "w") as output_file:
            
                output_file.write("Transaction History\n")
                output_file.write("=" * 110 + "\n\n")  # Adjusted for longer width
                output_file.write(f"Name: {current_user['f_name']} {current_user['l_name']}\n")
                output_file.write(f"Account Number: {current_user['account_no']}\n\n")
                
            
                output_file.write(f"{'Date':<30}{'Description':<30}{'Amount':>20}     \n")
                output_file.write("-" * 110 + "\n")
                
     
                for each in current_user["transaction_history"]:
                    date, description, amount = each[1], each[0], each[2]
                    output_file.write(f"{date:<30}{description:<30}{amount:>20.2f} Baht\n")
                
            
                print("Transaction history saved successfully!")
        
        except Exception as e:
            print(f"An error occurred: {e}")