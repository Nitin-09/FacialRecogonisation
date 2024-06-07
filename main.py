import tkinter as tk
import register
import attendance  # Import the attendance module
import viewAttendance

# Function to handle the registration of a new student
def register_student():
    register.display_registration_page()

# Function to handle taking attendance
def take_attendance():
    # Call the start_attendance_system function from the attendance module
    attendance.start_attendance_system()

# Function to handle viewing attendance
def view_attendance():
    viewAttendance.display_attendance_records()

# GUI
root = tk.Tk()
root.title("Face Recognition Based Attendance System")
root.configure(padx=20, pady=20)

# Function to load images
def load_image(image_name, size=None):
    image = tk.PhotoImage(file=f"UI_Image/{image_name}.png")
    if size:
        image = image.subsample(size)
    return image

# Load title image
title_image = load_image("0002", size=4)

# Title label
title_label = tk.Label(root, text="Face Recognition Based Attendance System", font=("Arial", 18, "bold"), image=title_image, compound=tk.TOP)
title_label.pack(pady=10)

# Main buttons with images
register_image = load_image("register")
attendance_image = load_image("attendance")
verify_image = load_image("verifyy")

register_button = tk.Button(root, text="Register New Student", image=register_image, command=register_student, compound=tk.TOP)
register_button.pack(side=tk.LEFT, padx=10)

attendance_button = tk.Button(root, text="Take Attendance", image=attendance_image, command=take_attendance, compound=tk.TOP)
attendance_button.pack(side=tk.LEFT, padx=10)

view_button = tk.Button(root, text="View Attendance", image=verify_image, command=view_attendance, compound=tk.TOP)
view_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
