from tkinter import *
from tkinter import messagebox
from db import Database

db = Database('store.db')

def populate_list():
    part_list.delete(0, END)
    for row in db.fetch():
        part_list.insert(END, row)

def add_item():
    if part_text.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required fields', 'Please include all fields')
        return
    db.insert(part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
    part_list.delete(0, END)
    part_list.insert(END, (part_text.get(), customer_text.get(), retailer_text.get(), price_text.get()))
    delete_item()
    populate_list()

def select_item(event):
    try:
        global selected_item # global variable to be used for remove_item
        index = part_list.curselection()[0] 
        selected_item = part_list.get(index)
        # print(selected_item)

        # to show the selected items into the field boxes present
        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass

def remove_item():
    db.remove(selected_item[0])
    delete_item()
    populate_list()

def update_item():
    db.update(selected_item[0], part_text.get(), customer_text.get(), retailer_text.get(), price_text.get())
    populate_list()

def delete_item():
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)

# window object
app = Tk()
app.title("Part Manager")
app.geometry('700x350')

# part
part_text = StringVar()
part_label = Label(app, text="Part Name", font=('bold',14), pady=20)
part_label.grid(row=0, column=0, sticky=W)
part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=1)

# customer
customer_text = StringVar()
customer_label = Label(app, text="Customer", font=('bold',14))
customer_label.grid(row=0, column=2, sticky=W)
customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)

# retailer
retailer_text = StringVar()
retailer_label = Label(app, text="Retailer", font=('bold',14))
retailer_label.grid(row=1, column=0, sticky=W)
retailer_entry = Entry(app, textvariable=retailer_text)
retailer_entry.grid(row=1, column=1)

# price
price_text = StringVar()
price_label = Label(app, text="Price", font=('bold',14))
price_label.grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)

# parts list
part_list = Listbox(app, height=8, width=50, border=0)
part_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# scroll bar
scroll_bar = Scrollbar(app)
scroll_bar.grid(row=3, column=3)

# set scroll to listbox
part_list.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=part_list.yview)

# bind select
part_list.bind('<<ListboxSelect>>', select_item)

# button
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Part', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Input', width=12, command=delete_item)
clear_btn.grid(row=2, column=3)

# populate data
populate_list()
# populate_list()

# start program
app.mainloop()

#  to create an executable, install pyinstaller and run
# pyinstaller part_manager.py --onefile --windowed
# dist folder contains the executable