import json
from tkinter import *
from tkinter import messagebox
import string
import secrets
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password_length = 12  # You can adjust the length of the password
    password = ''.join(secrets.choice(characters) for _ in range(password_length))
    entry_password.delete(0, END)
    entry_password.insert(0, password)
    pyperclip.copy(password)  # This copies the password to the clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = entry_website.get().lower()
    email = entry_email.get()
    password = entry_password.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password} \nDo you want to save?")

    if is_ok:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = new_data
        else:
            data.update(new_data)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

        entry_website.delete(0, END)
        entry_password.delete(0, END)

        messagebox.showinfo(title="Success", message="Password saved successfully!")

# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website = entry_website.get().lower()

    if len(website) == 0:
        messagebox.showwarning(title="Oops", message="Please enter the website name to search!")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message="No data file found!")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Not Found", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(window, width=200, height=200, highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website_label = Label(window, text="Website:", highlightthickness=0)
website_label.grid(column=0, row=1, sticky="E")

entry_website = Entry(window, width=21)
entry_website.grid(column=1, row=1, sticky="W")
entry_website.focus()

search_button = Button(window, text="Search", width=14, command=search_password)
search_button.grid(column=2, row=1, sticky="W")

email_label = Label(window, text="Email/Username:", highlightthickness=0)
email_label.grid(column=0, row=2, sticky="E")

entry_email = Entry(window, width=35)
entry_email.grid(column=1, row=2, columnspan=2, sticky="W")

password_label = Label(window, text="Password:", highlightthickness=0)
password_label.grid(column=0, row=3, sticky="E")

entry_password = Entry(window, width=21)
entry_password.grid(column=1, row=3, sticky="W")

generate_button = Button(window, text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="W")

add_button = Button(window, text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

# Entries

window.mainloop()
