from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import random

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '@', '-', '_']

def password_gen():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(LETTERS) for _ in range(nr_letters)]
    password_symbols = [random.choice(SYMBOLS) for _ in range(nr_symbols)]
    password_numbers = [random.choice(NUMBERS) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip().lower()
    user = user_entry.get().strip()
    password = password_entry.get().strip()

    if len(website) == 0 or len(user) == 0 or len(password) == 0:
        messagebox.showerror(title="Uyarı / Warning", message="Lütfen tüm alanları doldurunuz! / Please fill in all fields.")
        return

    account = {
        website: {
            "mail": user,
            "password": password
        }
    }

    is_ok = messagebox.askokcancel(
        title=website,
        message=f"Hesap Bilgileri / Account Details:\n\nWeb Sitesi: {website}\nKullanıcı: {user}\nŞifre: {password}\n\nKaydetmek istiyor musunuz?"
    )

    if is_ok:
        try:
            with open("data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data.update(account)

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        website_entry.delete(0, END)
        password_entry.delete(0, END)
        messagebox.showinfo(title="Başarılı / Success", message="Şifre güvenle kaydedildi! / Password saved successfully.")

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    searched_web = website_entry.get().strip().lower()
    if not searched_web:
        messagebox.showwarning(title="Uyarı", message="Lütfen aramak istediğiniz web sitesini girin.")
        return

    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        if searched_web in data:
            searched_email = data[searched_web]["mail"]
            searched_password = data[searched_web]["password"]
            pyperclip.copy(searched_password)
            messagebox.showinfo(
                title=searched_web.capitalize(),
                message=f"Web Sitesi: {searched_web}\nE-posta / Kullanıcı: {searched_email}\nŞifre: {searched_password}\n\n(Şifre panoya kopyalandı!)"
            )
        else:
            messagebox.showinfo(title="Bulunamadı", message=f"'{searched_web}' için kayıtlı bir hesap bulunamadı.")
    except FileNotFoundError:
        messagebox.showerror(title="Hata", message="Henüz kayıtlı bir şifre veritabanı (data.json) bulunamadı.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Modern Desktop Password Manager")
window.config(padx=40, pady=40, bg="#0f172a")

# Logo
canvas = Canvas(window, width=200, height=200, bg="#0f172a", highlightthickness=0)
try:
    logo_image = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_image)
except Exception:
    pass
canvas.grid(column=1, row=0, pady=(0, 20))

# Labels
website_label = Label(window, text="Web Sitesi / Domain:", font=("Helvetica", 10, "bold"), fg="#94a3b8", bg="#0f172a")
website_label.grid(column=0, row=1, pady=6, sticky=E)

user_label = Label(window, text="E-Posta / Kullanıcı Adı:", font=("Helvetica", 10, "bold"), fg="#94a3b8", bg="#0f172a")
user_label.grid(column=0, row=2, pady=6, sticky=E)

password_label = Label(window, text="Şifre:", font=("Helvetica", 10, "bold"), fg="#94a3b8", bg="#0f172a")
password_label.grid(column=0, row=3, pady=6, sticky=E)

# Entries
website_entry = Entry(window, width=22, font=("Helvetica", 11), bg="#1e293b", fg="#f8fafc", insertbackground="white", relief=FLAT)
website_entry.grid(column=1, row=1, sticky=W, padx=(0, 8), ipady=4)
website_entry.focus()

user_entry = Entry(window, width=36, font=("Helvetica", 11), bg="#1e293b", fg="#f8fafc", insertbackground="white", relief=FLAT)
user_entry.grid(column=1, row=2, columnspan=2, sticky=W, ipady=4)

password_entry = Entry(window, width=22, font=("Helvetica", 11), bg="#1e293b", fg="#f8fafc", insertbackground="white", relief=FLAT)
password_entry.grid(column=1, row=3, sticky=W, padx=(0, 8), ipady=4)

# Buttons
search_button = Button(
    window,
    text="Ara / Search",
    width=13,
    bg="#0284c7",
    fg="white",
    font=("Helvetica", 9, "bold"),
    relief=FLAT,
    cursor="hand2",
    command=find_password
)
search_button.grid(column=2, row=1)

gen_button = Button(
    window,
    text="Şifre Üret",
    width=13,
    bg="#10b981",
    fg="white",
    font=("Helvetica", 9, "bold"),
    relief=FLAT,
    cursor="hand2",
    command=password_gen
)
gen_button.grid(column=2, row=3)

add_button = Button(
    window,
    text="Hesabı Kaydet",
    width=38,
    bg="#6366f1",
    fg="white",
    font=("Helvetica", 10, "bold"),
    relief=FLAT,
    cursor="hand2",
    command=save
)
add_button.grid(column=1, row=4, columnspan=2, pady=16, ipady=4)

window.mainloop()
