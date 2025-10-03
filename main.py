from tkinter import *
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
def password_gen():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list+=[random.choice(letters) for l in range(nr_letters)]
    password_list+=[random.choice(symbols) for s in range(nr_symbols)]
    password_list+=[random.choice(numbers) for n in range(nr_numbers)]

    # for char in range(nr_letters):
    #   password_list.append(random.choice(letters))
    #
    # for char in range(nr_symbols):
    #   password_list += random.choice(symbols)
    #
    # for char in range(nr_numbers):
    #   password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    # for char in password_list:
    #   password += char
    password_entry.delete(0,END)
    password_entry.insert(0,password)
    # print(f"Your password is: {password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website=website_entry.get().lower()
    user=user_entry.get().lower()
    password=password_entry.get().lower()
    account={website:{
        "mail":user,
        "password":password
    }}
    if len(website_entry.get()) == 0 or len(user_entry.get())==0 or     len(password_entry.get())==0:
        messagebox.showerror(title="Oops",message="Please don't leave any fields empty!")
    else:
        is_ok=messagebox.askokcancel(title=website,message=f"These are the details entered: \nEmail: {user} \nPassword : {password} \n Is it ok to save ?")

        if is_ok:
            try:
                with open("data.json","r") as file:
                    data=json.load(file)
            except:
                with open("data.json", "w") as file:
                    json.dump(account, file, indent=4)
            else:
                data.update(account)
                with open("data.json","w") as file:
                    json.dump(data,file,indent=4)
            finally:
                website_entry.delete(0,END)
                password_entry.delete(0,END)

def find_password():
    try:
        searched_web=website_entry.get().lower()
        with open("data.json","r") as file:
            data=json.load(file)
            print(data[searched_web])
            searched_email=data[searched_web]["mail"]
            searched_password=data[searched_web]["password"]
            messagebox.showinfo(title=searched_web,message=f"Email: {searched_email}\nPassword:{searched_password}")
    except:
        messagebox.showinfo(title="Error",message=f"No data {searched_web} file found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#f0f0f0")

# Logo
canvas = Canvas(window, width=200, height=200, bg="#f0f0f0", highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(window, text="Website:", font=("Arial", 12), bg="#f0f0f0")
website_label.grid(column=0, row=1, pady=5, sticky=E)

user_label = Label(window, text="Email/Username:", font=("Arial", 12), bg="#f0f0f0")
user_label.grid(column=0, row=2, pady=5, sticky=E)

password_label = Label(window, text="Password:", font=("Arial", 12), bg="#f0f0f0")
password_label.grid(column=0, row=3, pady=5, sticky=E)

# Entries
website_entry = Entry(window, width=21, font=("Arial", 12))
website_entry.grid(column=1, row=1, sticky=W, padx=(0, 5))
website_entry.focus()

user_entry = Entry(window, width=35, font=("Arial", 12))
user_entry.grid(column=1, row=2, columnspan=2, sticky=W)
user_entry.insert(0, "safak_senel@hotmail.com")

password_entry = Entry(window, width=21, font=("Arial", 12))
password_entry.grid(column=1, row=3, sticky=W, padx=(0, 5))

# Buttons
gen_button = Button(window, text="Generate Password", command=password_gen, width=14, bg="#4CAF50", fg="white")
gen_button.grid(column=2, row=3, padx=5)

search_button = Button(window, text="Search", width=14, bg="#2196F3", fg="white",command=find_password)
search_button.grid(column=2, row=1, padx=5)

add_button = Button(window, text="Add", width=36, bg="#FF5722", fg="white", command=save)
add_button.grid(column=1, row=4, columnspan=2, pady=10)

window.mainloop()