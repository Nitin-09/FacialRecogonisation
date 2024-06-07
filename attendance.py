import tkinter as tk
from tkinter import messagebox
import csv
import cv2
import face_recognition
import numpy as np
import threading
from datetime import datetime

def mark_attendance(roll_no, name, subject):
    now = datetime.now()
    enter_time = now.strftime('%I:%M:%S %p')
    date = now.strftime('%d-%B-%Y')
    print(f"Marking attendance for {name} (Roll No: {roll_no}) in subject {subject} at {enter_time}, {date}")
    # Write to CSV file
    with open('attendance.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([roll_no, name, subject, date, enter_time])

def recognize_faces(frame, encoded_faces, known_face_encodings, known_face_roll_numbers, known_face_names, subject):
    for encoded_face in encoded_faces:
        matches = face_recognition.compare_faces(known_face_encodings, encoded_face)
        face_distances = face_recognition.face_distance(known_face_encodings, encoded_face)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            roll_no = known_face_roll_numbers[match_index]
            name = known_face_names[match_index]
            mark_attendance(roll_no, name, subject)
            print(f"Recognized: {name} (Roll No: {roll_no})")

def process_video_feed(cap, known_face_encodings, known_face_roll_numbers, known_face_names, stop_event, subject):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from the camera.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        recognize_faces(frame, face_encodings, known_face_encodings, known_face_roll_numbers, known_face_names, subject)
        cv2.imshow('Video Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_camera():
    cap = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_roll_numbers = []
    known_face_names = []

    # Fetch student data from the CSV
    with open('database.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name, roll_no = row
            known_face_names.append(name)
            known_face_roll_numbers.append(roll_no)
            image_path = f'student_images/{roll_no}.png'
            student_image = face_recognition.load_image_file(image_path)
            student_encoding = face_recognition.face_encodings(student_image)[0]
            known_face_encodings.append(student_encoding)

    subject = subject_entry.get()  # Get subject from the entry field
    if not subject:
        messagebox.showerror("Error", "Please enter a subject.")
        return

    global stop_event
    stop_event = threading.Event()
    threading.Thread(target=process_video_feed, args=(cap, known_face_encodings, known_face_roll_numbers, known_face_names, stop_event, subject)).start()

def stop_camera():
    global stop_event
    stop_event.set()

def start_attendance_system():
    root = tk.Tk()
    root.title("Student Attendance System")

    subject_label = tk.Label(root, text="Subject:")
    subject_label.grid(row=0, column=0)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.grid(row=0, column=1)

    start_button = tk.Button(root, text="Start Camera", command=start_camera)
    start_button.grid(row=1, column=0, pady=10)

    stop_button = tk.Button(root, text="Stop Camera", command=stop_camera)
    stop_button.grid(row=1, column=1, pady=10)

    root.mainloop()
