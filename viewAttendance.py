import tkinter as tk
import csv
import os
from collections import defaultdict
from datetime import datetime
from tkinter import messagebox

def load_attendance():
    subject = subject_entry.get()
    attendance_listbox.delete(0, tk.END)
    if os.path.exists('attendance.csv'):
        with open('attendance.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if subject in row:
                    attendance_listbox.insert(tk.END, row)

def display_unique_entry_times():
    subject = subject_entry.get()
    attendance_listbox.delete(0, tk.END)
    entry_times = defaultdict(list)
    names = defaultdict(set)
    if os.path.exists('attendance.csv'):
        with open('attendance.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if subject in row:
                    enrollment_number = row[0]
                    name = row[1]
                    timestamp = row[3] + ' ' + row[4]
                    time_format = '%d-%B-%Y %I:%M:%S %p'
                    current_time = datetime.strptime(timestamp, time_format).time()
                    entry_times[enrollment_number].append(current_time)
                    names[enrollment_number].add(name)

    for enrollment_number, times in entry_times.items():
        unique_times = set(times)
        min_time = min(unique_times).strftime('%I:%M:%S %p')
        max_time = max(unique_times).strftime('%I:%M:%S %p')
        total_distinct_entries = len(unique_times)
        unique_names = ', '.join(names[enrollment_number])
        attendance_listbox.insert(tk.END, f"Enrollment: {enrollment_number}, Names: {unique_names}, First Entry: {min_time}, Last Entry: {max_time}, Total Distinct Entries: {total_distinct_entries}")

def save_unique_entry_times():
    subject = subject_entry.get()
    filename = f"{subject}_unique_entry_times.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Enrollment", "Names", "First Entry", "Last Entry", "Total Distinct Entries"])
        entry_times = defaultdict(list)
        names = defaultdict(set)
        if os.path.exists('attendance.csv'):
            with open('attendance.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if subject in row:
                        enrollment_number = row[0]
                        name = row[1]
                        timestamp = row[3] + ' ' + row[4]
                        time_format = '%d-%B-%Y %I:%M:%S %p'
                        current_time = datetime.strptime(timestamp, time_format).time()
                        entry_times[enrollment_number].append(current_time)
                        names[enrollment_number].add(name)
            for enrollment_number, times in entry_times.items():
                unique_times = set(times)
                min_time = min(unique_times).strftime('%I:%M:%S %p')
                max_time = max(unique_times).strftime('%I:%M:%S %p')
                total_distinct_entries = len(unique_times)
                unique_names = ', '.join(names[enrollment_number])
                writer.writerow([enrollment_number, unique_names, min_time, max_time, total_distinct_entries])
    messagebox.showinfo("Save", f"Unique entry times saved to {filename}")

def display_attendance_records():
    root = tk.Tk()
    root.title("Attendance Records")
    root.geometry("700x600")  # Set the width and height of the window

    # Subject entry section
    subject_frame = tk.Frame(root, width=800)  # Adjusting width
    subject_frame.pack(pady=10)

    tk.Label(subject_frame, text="Subject:").pack(side=tk.LEFT)
    global subject_entry
    subject_entry = tk.Entry(subject_frame)
    subject_entry.pack(side=tk.LEFT)
    load_button = tk.Button(subject_frame, text="Load Attendance", command=load_attendance)
    load_button.pack(side=tk.LEFT, padx=10)

    # Unique Entry Times Button
    unique_entry_button = tk.Button(subject_frame, text="Unique Entry Times", command=display_unique_entry_times)
    unique_entry_button.pack(side=tk.LEFT, padx=10)

    # Save Unique Entry Times Button
    save_button = tk.Button(subject_frame, text="Save Unique Entry Times", command=save_unique_entry_times)
    save_button.pack(side=tk.LEFT, padx=10)

    # Attendance section
    attendance_frame = tk.Frame(root, width=00)  # Adjusting width
    attendance_frame.pack(pady=10)

    # Attendance list section
    attendance_list_frame = tk.Frame(attendance_frame, width=600)  # Adjusting width
    attendance_list_frame.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Label(attendance_list_frame, text="Attendance Records:").pack()
    global attendance_listbox
    attendance_listbox = tk.Listbox(attendance_list_frame, width=900, height=200)  # Adjusting width
    attendance_listbox.pack()

    # Image display
    image_label = tk.Label(attendance_frame, width=200)  # Adjusting width
    image_label.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    display_attendance_records()
