import tkinter as tk
from tkinter import Scrollbar, RIGHT, Y
from venmo_api import Client

client = None

# Step 1: Initial Authentication (Username, Password, and optional Device ID)
def authenticate():
    global client
    username = username_entry.get()
    password = password_entry.get()
    device_id = device_id_entry.get()

    try:
        if device_id:
            # Use the device ID to get the access token directly, bypassing 2FA
            access_token = Client.get_access_token(username=username, password=password, device_id=device_id)
            client = Client(access_token)
            result_label.config(text="Login Successful!", fg="green")
        else:
            # Trigger 2FA if no device ID is provided
            access_token = Client.get_access_token(username=username, password=password)
            client = Client(access_token)
            result_label.config(text="Login Successful!", fg="green")
    except Exception as e:
        if '2fa required' in str(e).lower():
            result_label.config(text="2FA Required. Please enter the code sent to your device.", fg="orange")
            two_fa_frame.pack()  # Show the 2FA entry frame
        else:
            result_label.config(text=f"Error: {str(e)}", fg="red")

# Step 2: Provide the 2FA Code
def submit_two_fa_code():
    global client
    username = username_entry.get()
    password = password_entry.get()
    two_fa_code = two_fa_code_entry.get()

    try:
        # Complete 2FA with the provided code
        access_token = Client.get_access_token(username=username, password=password, two_factor_code=two_fa_code)
        client = Client(access_token)
        result_label.config(text="2FA Successful! Logged in.", fg="green")
        two_fa_frame.pack_forget()  # Hide the 2FA frame after successful login
    except Exception as e:
        result_label.config(text=f"Error during 2FA: {str(e)}", fg="red")

# Step 3: Fetch User Data and Transactions, Create Buttons for Each Transaction
def get_user_data():
    if client:
        try:
            myuserid = client.user.get_my_profile().id
            user_id_label.config(text=f"My User ID: {myuserid}")

            transactions = client.user.get_user_transactions(myuserid)
            transactions_text.delete(1.0, tk.END)  # Clear existing content
            transaction_buttons = []

            transaction_count = 1
            while transactions:
                for transaction in transactions:
                    # Display the transaction number, necessary details, and add a button for each transaction
                    button_text = f"{transaction_count}. {transaction.actor.display_name} -> {transaction.target.display_name} | ${transaction.amount} | {transaction.date_completed}"
                    button = tk.Button(transactions_text, text=button_text, anchor="w", justify="left", wraplength=450, command=lambda t=transaction: show_transaction_details(t))
                    transaction_buttons.append(button)
                    transactions_text.window_create(tk.END, window=button)
                    transactions_text.insert(tk.END, "\n\n")
                    transaction_count += 1
                transactions = transactions.get_next_page()
        except Exception as e:
            transactions_text.insert(tk.END, f"Error: {str(e)}\n")
    else:
        result_label.config(text="Please complete authentication first.", fg="red")

# Function to show transaction details in a new window
def show_transaction_details(transaction):
    details_window = tk.Toplevel(root)
    details_window.title(f"Transaction Details: {transaction.id}")

    details_text = tk.Text(details_window, height=20, width=80)
    details_text.pack(padx=10, pady=10)

    details = f"""
Transaction ID: {transaction.id}
Payment ID: {transaction.payment_id}
Date Completed: {transaction.date_completed}
Date Created: {transaction.date_created}
Date Updated: {transaction.date_updated}
Payment Type: {transaction.payment_type}
Amount: {transaction.amount}
Audience: {transaction.audience}
Status: {transaction.status}
Note: {transaction.note}
Device Used: {transaction.device_used}

Actor:
  ID: {transaction.actor.id}
  Username: {transaction.actor.username}
  First Name: {transaction.actor.first_name}
  Last Name: {transaction.actor.last_name}
  Display Name: {transaction.actor.display_name}
  Profile Picture URL: {transaction.actor.profile_picture_url}

Target:
  ID: {transaction.target.id}
  Username: {transaction.target.username}
  First Name: {transaction.target.first_name}
  Last Name: {transaction.target.last_name}
  Display Name: {transaction.target.display_name}
  Profile Picture URL: {transaction.target.profile_picture_url}

Comments: {transaction.comments if transaction.comments else "None"}
    """

    details_text.insert(tk.END, details)

# Create the main window
root = tk.Tk()
root.title("Venmo API GUI")

# Authentication Frame
auth_frame = tk.LabelFrame(root, text="Authentication", padx=10, pady=10)
auth_frame.pack(padx=10, pady=10)

username_label = tk.Label(auth_frame, text="Username:")
username_label.pack()
username_entry = tk.Entry(auth_frame)
username_entry.pack()

password_label = tk.Label(auth_frame, text="Password:")
password_label.pack()
password_entry = tk.Entry(auth_frame, show="*")
password_entry.pack()

device_id_label = tk.Label(auth_frame, text="Device ID (optional):")
device_id_label.pack()
device_id_entry = tk.Entry(auth_frame)
device_id_entry.pack()

login_button = tk.Button(auth_frame, text="Login", command=authenticate)
login_button.pack()

result_label = tk.Label(auth_frame, text="")
result_label.pack()

# 2FA Frame
two_fa_frame = tk.LabelFrame(root, text="Two-Factor Authentication", padx=10, pady=10)
two_fa_code_label = tk.Label(two_fa_frame, text="Enter 2FA Code:")
two_fa_code_label.pack()
two_fa_code_entry = tk.Entry(two_fa_frame)
two_fa_code_entry.pack()

two_fa_button = tk.Button(two_fa_frame, text="Submit 2FA Code", command=submit_two_fa_code)
two_fa_button.pack()

# Initially hide the 2FA frame until it's needed
two_fa_frame.pack_forget()

# User Data Frame
user_data_frame = tk.LabelFrame(root, text="User Data", padx=10, pady=10)
user_data_frame.pack(padx=10, pady=10)

user_id_label = tk.Label(user_data_frame, text="My User ID: ")
user_id_label.pack()

# Add scrollbar to the transactions text widget
scrollbar = Scrollbar(user_data_frame)
scrollbar.pack(side=RIGHT, fill=Y)

transactions_text = tk.Text(user_data_frame, height=20, width=100, yscrollcommand=scrollbar.set)
transactions_text.pack()
scrollbar.config(command=transactions_text.yview)

user_data_button = tk.Button(user_data_frame, text="Get User Data & Transactions", command=get_user_data)
user_data_button.pack()

# Run the main loop
root.mainloop()
