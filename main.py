from tkinter import *
import random
from tkinter import messagebox
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    new_password = ''
    all = []
    for i in range(0, 5):
        letterz = random.choice(letters)
        all.append(letterz)
    for i in range(0, 5):
        numberz = random.choice(numbers)
        all.append(numberz)
    for i in range(0, 5):
        symbolz = random.choice(symbols)
        all.append(symbolz)
    random.shuffle(all)
    for u in all:
        for i in u:
            new_password += i
    password_input.insert(string=f'{new_password}', index=END)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    password = password_input.get()
    website = website_input.get()
    email = email_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }
    if len(password_input.get()) == 0 or len(website_input.get()) == 0:
        invalid_input = messagebox.askretrycancel(message='Invalid entry, you are missing one or more fields.',
                                                  title='Invalid Entry')
    else:
        try:
            with open('data.json', 'r') as data_file:
                # reading old data
                data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            with open('data.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            # updating data
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                # saving data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


def search():
    searches = website_input.get().lower()
    with open('data.json', 'r') as files_data:
        files = json.load(files_data)
        try:
            item = files[searches]
        except KeyError:
            if len(searches) == 0:
                no_input_box = messagebox.askretrycancel(title='Error',
                                                         message='Invalid search entry, you must input a website name')
            else:
                error_box = messagebox.askretrycancel(title='Error',
                                                      message='The file you are searching for does not exist.')
                if error_box:
                    pass
        else:
            passw = item['password']
            mail = item[f'email']
            info_box = messagebox.showinfo(title=f'{searches.title()}',
                                           message=f'Email: {mail}\nPassword: {passw}')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
# window.minsize(300, 250)
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')

canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website = Label(text='Website:')
website.grid(row=1, column=0)
website_input = Entry(width=21)
website_input.grid(row=1, column=1, sticky='EW')
website_input.focus()

email = Label(text='Email/Username:')
email.grid(row=2, column=0)
email_input = Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2, sticky='EW')
email_input.insert(index=END, string='')

password = Label(text='Password:')
password.grid(row=3, column=0)
password_input = Entry(width=21)
password_input.grid(row=3, column=1, sticky='EW')

generate_password = Button(text='Generate Password', command=password_generator)
generate_password.grid(row=3, column=2, sticky='EW', padx=5)
add_button = Button(text='Add', width=29, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, sticky='EW')
search_button = Button(text='Search', width=20, command=search)
search_button.grid(row=1, column=2, sticky='EW', padx=5)

window.mainloop()
