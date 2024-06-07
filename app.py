import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime

class ImageDatasetManager:
    def __init__(self):
        self.dataset = []

    def add_entry(self, id, roll_no, name):
        entry = {'id': id, 'roll_no': roll_no, 'name': name}
        self.dataset.append(entry)
        self.save_to_csv()

    def update_entry(self, index, id, roll_no, name):
        self.dataset[index] = {'id': id, 'roll_no': roll_no, 'name': name}
        self.save_to_csv()

    def delete_entry(self, index):
        del self.dataset[index]
        self.save_to_csv()

    def save_to_csv(self):
        with open('dataset.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'roll_no', 'name'])
            writer.writeheader()
            writer.writerows(self.dataset)

    def load_from_csv(self):
        try:
            with open('dataset.csv', 'r') as file:
                reader = csv.DictReader(file)
                self.dataset = list(reader)
        except FileNotFoundError:
            pass


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Dataset Manager")

        self.dataset_manager = ImageDatasetManager()
        self.dataset_manager.load_from_csv()

        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for Image id
        tk.Label(self.master, text="id:").grid(row=0, column=0)
        self.id_entry = tk.Entry(self.master, width=30)
        self.id_entry.grid(row=0, column=1)

        # Label and Entry for Roll Number
        tk.Label(self.master, text="Roll Number:").grid(row=1, column=0)
        self.roll_no_entry = tk.Entry(self.master)
        self.roll_no_entry.grid(row=1, column=1)

        # Label and Entry for Name
        tk.Label(self.master, text="Name:").grid(row=2, column=0)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(self.master, text="Add", command=self.add_entry).grid(row=3, column=0, sticky="w")
        tk.Button(self.master, text="Update", command=self.update_entry).grid(row=3, column=1)
        tk.Button(self.master, text="Delete", command=self.delete_entry).grid(row=3, column=1, sticky="e")

        # Listbox to display dataset
        self.listbox = tk.Listbox(self.master, height=10, width=50)
        self.listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Load dataset into the listbox
        self.load_dataset()

    def add_entry(self):
        id = self.id_entry.get()
        roll_no = self.roll_no_entry.get()
        name = self.name_entry.get()

        if id and roll_no and name:
            self.dataset_manager.add_entry(id, roll_no, name)
            self.load_dataset()
            self.clear_entries()

    def update_entry(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            id = self.id_entry.get()
            roll_no = self.roll_no_entry.get()
            name = self.name_entry.get()

            if id and roll_no and name:
                self.dataset_manager.update_entry(selected_index[0], id, roll_no, name)
                self.load_dataset()
                self.clear_entries()

    def delete_entry(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.dataset_manager.delete_entry(selected_index[0])
            self.load_dataset()
            self.clear_entries()

    def load_dataset(self):
        self.listbox.delete(0, tk.END)
        for entry in self.dataset_manager.dataset:
            self.listbox.insert(tk.END, f"{entry['roll_no']} - {entry['name']}")

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.roll_no_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
