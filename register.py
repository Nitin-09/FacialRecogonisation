import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import csv
import shutil
import os

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.photos = {} # Initialize PhotoImage object
        
        # Registration section
        self.register_frame = tk.Frame(root)
        self.register_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.register_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.register_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.register_frame, text="Enrollment Number:").grid(row=1, column=0)
        self.enrollment_entry = tk.Entry(self.register_frame)
        self.enrollment_entry.grid(row=1, column=1)

        tk.Label(self.register_frame, text="Profile Image:").grid(row=2, column=0)
        self.profile_image_entry = tk.Entry(self.register_frame)
        self.profile_image_entry.grid(row=2, column=1)
        browse_button = tk.Button(self.register_frame, text="Browse", command=self.browse_image)
        browse_button.grid(row=2, column=2)

        register_button = tk.Button(self.register_frame, text="Register", command=self.register)
        register_button.grid(row=3, column=0, columnspan=2)

        # Student list section
        self.student_list_frame = tk.Frame(root)
        self.student_list_frame.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(self.student_list_frame, text="Registered Students:").grid(row=0, column=0)
        self.student_listbox = tk.Listbox(self.student_list_frame, width=40, height=10)
        self.student_listbox.grid(row=1, column=0)
        self.student_listbox.bind('<<ListboxSelect>>', self.on_student_select)

        # Update and Delete section
        update_button = tk.Button(self.student_list_frame, text="Update Student", command=self.update_student)
        update_button.grid(row=2, column=0, pady=5)

        delete_button = tk.Button(self.student_list_frame, text="Delete Student", command=self.delete_student)
        delete_button.grid(row=3, column=0, pady=5)

        # Image display
        self.image_label = tk.Label(root)
        self.image_label.grid(row=0, column=1, rowspan=4, padx=10, pady=10)

        # Load students into the listbox at startup
        self.load_students()

    def browse_image(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")))
        if filename:
            self.profile_image_entry.delete(0, tk.END)
            self.profile_image_entry.insert(0, filename)

    def register(self):
        name = self.name_entry.get()
        enrollment_number = self.enrollment_entry.get()
        profile_image_path = self.profile_image_entry.get()

        if not name or not enrollment_number or not profile_image_path:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Save image
        os.makedirs('student_images', exist_ok=True)
        shutil.copy(profile_image_path, f'student_images/{enrollment_number}.png')

        # Write data to CSV
        with open('database.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, enrollment_number])

        messagebox.showinfo("Success", "Registration successful!")
        self.load_students()

    def load_students(self):
        self.student_listbox.delete(0, tk.END)
        if os.path.exists('database.csv'):
            with open('database.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.student_listbox.insert(tk.END, f"{row[0]} ({row[1]})")

    def on_student_select(self, event):
        try:
            selected_student = self.student_listbox.get(self.student_listbox.curselection())
            name, enrollment_number = selected_student.split(' (')
            enrollment_number = enrollment_number[:-1]  # Remove the closing parenthesis

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)

            self.enrollment_entry.delete(0, tk.END)
            self.enrollment_entry.insert(0, enrollment_number)
            self.profile_image_entry.delete(0, tk.END)
            self.show_student_image(enrollment_number)
        except Exception as e:
            print(f"Error in on_student_select: {e}")


    def show_student_image(self, enrollment_number):
        image_path = os.path.join('student_images', f'{enrollment_number}.png')
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Resizing the image to 300x300
            self.photos[enrollment_number] = ImageTk.PhotoImage(image)  # Store PhotoImage object in the dictionary
            self.image_label.config(image=self.photos[enrollment_number])
            print(f"Image loaded for {enrollment_number}")
        else:
            self.image_label.config(image='')
            print(f"No image found for {enrollment_number}")



    def update_student(self):
        name = self.name_entry.get()
        enrollment_number = self.enrollment_entry.get()
        profile_image_path = self.profile_image_entry.get()

        if not name or not enrollment_number:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Update image if a new one is provided
        if profile_image_path:
            shutil.copy(profile_image_path, f'student_images/{enrollment_number}.png')

        # Read all data from the CSV file
        students = []
        with open('database.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == enrollment_number:
                    students.append([name, enrollment_number])
                else:
                    students.append(row)

        # Write updated data back to the CSV file
        with open('database.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(students)

        messagebox.showinfo("Success", "Student details updated successfully!")
        self.load_students()

    def delete_student(self):
        try:
            selected_student = self.student_listbox.get(self.student_listbox.curselection())
            _, enrollment_number = selected_student.split(' (')
            enrollment_number = enrollment_number[:-1]  # Remove the closing parenthesis

            # Remove student image
            image_path = os.path.join('student_images', f'{enrollment_number}.png')
            if os.path.exists(image_path):
                os.remove(image_path)

            # Remove student data from CSV
            students = []
            with open('database.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] != enrollment_number:
                        students.append(row)

            with open('database.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(students)

            messagebox.showinfo("Success", "Student entry deleted successfully!")
            self.load_students()

            # Clear the entry fields and image display
            self.name_entry.delete(0, tk.END)
            self.enrollment_entry.delete(0, tk.END)
            self.profile_image_entry.delete(0, tk.END)
            self.image_label.config(image='')
        except Exception as e:
            messagebox.showerror("Error", f"Please select a student to delete. Error: {e}")

def display_registration_page():
    root = tk.Tk()
    root.title("Student Management System")
    register_app = RegisterApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    display_registration_page()

