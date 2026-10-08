import tkinter as tk
from tkinter import messagebox

from database import create_database, add_note, get_notes


def save_note():
    text = note_entry.get().strip()

    if text == "":
        messagebox.showwarning("Warning", "Please enter a note.")
        return

    add_note(text)
    note_entry.delete(0, tk.END)
    display_notes()


def display_notes():
    notes_list.delete(0, tk.END)

    for note_id, text in get_notes():
        notes_list.insert(tk.END, f"{note_id}: {text}")


create_database()

app = tk.Tk()
app.title("Offline Notes App")
app.geometry("500x400")

title_label = tk.Label(app, text="My Offline Notes", font=("Arial", 18))
title_label.pack(pady=15)

note_entry = tk.Entry(app, width=50)
note_entry.pack(pady=10)

save_button = tk.Button(app, text="Save Note", command=save_note)
save_button.pack(pady=5)

notes_list = tk.Listbox(app, width=60, height=12)
notes_list.pack(pady=15)

display_notes()

app.mainloop()