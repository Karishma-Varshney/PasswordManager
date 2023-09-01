from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ----------------------------SEARCH PASSWORD ----------------------------------#
def search():
    w = web_input.get()
    try:
        with open('data.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No data file found')
    else:
        if w in data:
            e = data[w]['email']
            p = data[w]['password']
            messagebox.showinfo(title=w, message=f'Email: {e}\nPassword: {p}')

        else:
            messagebox.showerror(title='Opps!!!', message=f"No details for {w} exists.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', ')', '(', '+', '*']


def generate():
    nr_letters = random.randint(3, 5)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(1, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    password_num = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letter + password_symbol + password_num

    random.shuffle(password_list)

    # joining the list element
    password = "".join(password_list)
    pwd_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    w = web_input.get()
    e = email_input.get()
    p = pwd_input.get()
    new_dict = {
        w: {
            'email': e,
            'password': p,
        }
    }

    if len(w) == 0 or len(p) == 0:
        messagebox.showerror(title='Opps!!!', message="Please don't leave any field empty")

    else:
        is_ok = messagebox.askokcancel(title=w, message=f"These are the details entered: \nEmail: {e}\nPassword: {p} "
                                                        f"\nIs it ok to save?")
        if is_ok:
            try:
                with open('data.json', 'r') as f:
                    # reading old data
                    data = json.load(f)
            except FileNotFoundError:
                # creating a json file if not exists
                with open('data.json', 'w') as f:
                    json.dump(new_dict, f, indent=4)
            else:
                # updating new data
                data.update(new_dict)
                with open('data.json', 'w') as f:
                    # saving updated data
                    json.dump(data, f, indent=4)
            finally:
                web_input.delete(0, END)
                pwd_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text='Website:')
website_label.grid(column=0, row=1)

email_label = Label(text='Email/Username:')
email_label.grid(column=0, row=2)

password_label = Label(text='Password:')
password_label.grid(column=0, row=3)

# entries
web_input = Entry(width=25)
web_input.grid(column=1, row=1, padx=2, pady=10, sticky=E)
web_input.focus()

email_input = Entry(width=35)
email_input.grid(column=1, row=2, columnspan=2, padx=10, pady=10)
email_input.insert(0, string='xyz@gmail.com')

pwd_input = Entry(width=25)
pwd_input.grid(column=1, row=3, pady=10, padx=2, sticky=E)

# buttons
generate_button = Button(text='Generate Password', command=generate)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', width=30, command=save)
add_button.grid(column=1, row=4, columnspan=2, padx=10, pady=10)

search_button = Button(text='Search', command=search, width=10)
search_button.grid(column=2, row=1)

window.mainloop()
