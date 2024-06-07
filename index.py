import face_recognition
import numpy as np
import sqlite3
import threading
from datetime import datetime
import time

# Connect to SQLite database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Create table for student data if not exists
c.execute('''CREATE TABLE IF NOT EXISTS students 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT, name TEXT, face_encoding BLOB)''')
conn.commit()

def insert_student_data(roll_no, name, face_encoding):
    c.execute("INSERT INTO students (roll_no, name, face_encoding) VALUES (?, ?, ?)",
              (roll_no, name, face_encoding))
    conn.commit()

def mark_attendance(name):
    now = datetime.now()
    time = now.strftime('%I:%M:%S:%p')
    date = now.strftime('%d-%B-%Y')
    print(f"Marking attendance for {name} at {time}, {date}")
    # You can further process attendance data here

def recognize_faces(frame, encoded_faces, known_face_encodings, known_face_names):
    for encoded_face in encoded_faces:
        matches = face_recognition.compare_faces(known_face_encodings, encoded_face)
        face_distances = face_recognition.face_distance(known_face_encodings, encoded_face)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            name = known_face_names[match_index]
            mark_attendance(name)
            print(f"Recognized: {name}")
            # Draw rectangle and name on the face in the image if needed

def process_video_feed(cap, known_face_encodings, known_face_names):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from the camera.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        recognize_faces(frame, face_encodings, known_face_encodings, known_face_names)
        cv2.imshow('Video Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_names = []

    # Fetch student data from the database
    c.execute("SELECT name, face_encoding FROM students")
    rows = c.fetchall()
    for row in rows:
        known_face_names.append(row[0])
        known_face_encodings.append(np.frombuffer(row[1]))

    threading.Thread(target=process_video_feed, args=(cap, known_face_encodings, known_face_names)).start()

    # Run face recognition and attendance marking at regular time intervals
    while True:
        time.sleep(10)  # Time interval for attendance marking in seconds
        # Code for face recognition and attendance marking goes here

    cap.release()

if __name__ == "__main__":
    main()
