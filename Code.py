import tkinter as tk
from tkinter import messagebox
import json
import bcrypt
import time
import base64

def load_passwords(filename, master_key):
    try:
        with open(filename, 'r') as file:
            encrypted_data = file.read()
            if not encrypted_data:
                return {}  # Return empty dictionary if file is empty
            decrypted_data = decrypt(encrypted_data, master_key)
            passwords = json.loads(decrypted_data)
            return passwords
    except FileNotFoundError:
        return {}  # Return empty dictionary if file is not found
    except json.decoder.JSONDecodeError:
        return {}  # Return empty dictionary if JSON decoding fails

def save_passwords(passwords, filename, master_key):
    encrypted_data = encrypt(json.dumps(passwords), master_key)
    with open(filename, "w") as file:
        file.write(encrypted_data)

def encrypt(data, key):
    key_int = int.from_bytes(key.encode('utf-8'), 'big') % 256  # Limit key to range [0, 255]
    encrypted_data = ''.join(chr(ord(c) ^ key_int) for c in data)
    return encrypted_data

def decrypt(data, key):
    key_int = int.from_bytes(key.encode('utf-8'), 'big') % 256  # Limit key to range [0, 255]
    decrypted_data = ''.join(chr(ord(c) ^ key_int) for c in data)
    return decrypted_data

def add_password_page():
    clear_entries()
    add_retrieve_frame.grid_forget()
    add_retrieve_page_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    add_label.grid(row=0, column=0, columnspan=2)
    website_label.grid(row=1, column=0, padx=10, pady=5)
    website_entry.grid(row=1, column=1, padx=10, pady=5)
    username_label.grid(row=2, column=0, padx=10, pady=5)
    username_entry.grid(row=2, column=1, padx=10, pady=5)
    password_label.grid(row=3, column=0, padx=10, pady=5)
    password_entry.grid(row=3, column=1, padx=10, pady=5)
    add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    back_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

def retrieve_password_page():
    clear_entries()
    add_retrieve_frame.grid_forget()
    add_retrieve_page_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    retrieve_label.grid(row=0, column=0, columnspan=2)
    website_label.grid(row=1, column=0, padx=10, pady=5)
    website_entry.grid(row=1, column=1, padx=10, pady=5)
    username_label.grid(row=2, column=0, padx=10, pady=5)
    username_entry.grid(row=2, column=1, padx=10, pady=5)
    retrieve_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
    back_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

def back_to_start():
    add_retrieve_page_frame.grid_forget()
    add_retrieve_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

def clear_entries():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    master_key = master_key_entry.get()
    filename = filename_entry.get()
    stored_passwords = load_passwords(filename, master_key)
    stored_passwords[website] = {"username": username, "password": encrypt(password, master_key)}
    save_passwords(stored_passwords, filename, master_key)
    messagebox.showinfo("Success", "Password added successfully.")

def retrieve_password():
    website = website_entry.get()
    username = username_entry.get()
    master_key = master_key_entry.get()
    filename = filename_entry.get()
    stored_passwords = load_passwords(filename, master_key)
    if stored_passwords:
        if website in stored_passwords and stored_passwords[website]["username"] == username:
            stored_password = stored_passwords[website]["password"]
            messagebox.showinfo("Password", f"Password for {username} at {website} is: {decrypt(stored_password, master_key)}")
        else:
            messagebox.showerror("Error", "No matching password found.")
    else:
        messagebox.showerror("Error", "No passwords stored.")

root = tk.Tk()
root.title("Password Manager")

filename_label = tk.Label(root, text="Enter filename:")
filename_entry = tk.Entry(root)

master_key_label = tk.Label(root, text="Enter master key:")
master_key_entry = tk.Entry(root, show="*")

start_button = tk.Button(root, text="Start", command=lambda: add_retrieve_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew"))

add_retrieve_frame = tk.Frame(root)

add_retrieve_label = tk.Label(add_retrieve_frame, text="Select an option:")
add_retrieve_label.grid(row=0, column=0, columnspan=2)

add_password_button = tk.Button(add_retrieve_frame, text="Add Password", command=add_password_page)
add_password_button.grid(row=1, column=0, padx=10, pady=5)

retrieve_password_button = tk.Button(add_retrieve_frame, text="Retrieve Password", command=retrieve_password_page)
retrieve_password_button.grid(row=1, column=1, padx=10, pady=5)

add_retrieve_page_frame = tk.Frame(root)

add_label = tk.Label(add_retrieve_page_frame, text="Add Password")
retrieve_label = tk.Label(add_retrieve_page_frame, text="Retrieve Password")

website_label = tk.Label(add_retrieve_page_frame, text="Website:")
website_entry = tk.Entry(add_retrieve_page_frame)

username_label = tk.Label(add_retrieve_page_frame, text="Username:")
username_entry = tk.Entry(add_retrieve_page_frame)

password_label = tk.Label(add_retrieve_page_frame, text="Password:")
password_entry = tk.Entry(add_retrieve_page_frame)

add_button = tk.Button(add_retrieve_page_frame, text="Add Password", command=add_password)
retrieve_button = tk.Button(add_retrieve_page_frame, text="Retrieve Password", command=retrieve_password)
back_button = tk.Button(add_retrieve_page_frame, text="Back", command=back_to_start)

filename_label.grid(row=0, column=0, padx=10, pady=5)
filename_entry.grid(row=0, column=1, padx=10, pady=5)
master_key_label.grid(row=1, column=0, padx=10, pady=5)
master_key_entry.grid(row=1, column=1, padx=10, pady=5)
start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()