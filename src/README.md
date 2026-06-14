# Sierra Health Hospital Clinic

A Python‑based GUI application to manage the patient queue, built for clinics and hospitals in Sierra Leone.

## Overview

Sierra Health Hospital Clinic is a desktop application that helps receptionists and doctors work together to manage patient flow more effectively.
Receptionists register new patients with their personal details and complaint, and the system automatically sorts the queue by priority (Emergency, Pregnant, Normal) and arrival time. Doctors can call the next patient, view full patient information, and record prescriptions.

This project was created as part of a software development learning exercise. It demonstrates modular design, clean GUI logic, and real‑world problem solving.

## Features

For Receptionists

- Secure login using a self‑created password
- Register new patients with full name, age, gender, phone number, complaint, arrival time, and priority category
- View the live, priority‑sorted waiting queue with colour‑coded rows
- Search for any patient (waiting or served) by name, ID, or phone number
- View a log of all patients already served
- View a summary of today’s totals: registered, waiting, served, and breakdown by category
- Logout safely to return to the login screen

For Doctors

- Secure login using a self‑created password
- Attend to patients
– View the live waiting queue and call the next patient
- View patient informationc
– Search any patient (waiting or served) by name, ID, or phone number
- Prescribe medication
– Select a served patient and write/save prescription notes
- Logout safely to return to the login screen

General & Technical Features

- Clean, simple GUI using tkinter
– No terminal interaction needed
- In‑memory data storage with Python dictionaries and lists (easy to understand, no external database required)
- Structured programming
– uses functions, loops, decision structures, and modular design
- Real‑world alignment
– built for clinics in Sierra Leone
- Automatic priority queue sorting: Emergency > Pregnant > Normal, then by arrival time
- Each staff role (Doctor / Receptionist) creates and manages its own password on first login


## Screenshot
- Login Page
<img width="1000" height="950" alt="image" src="https://github.com/user-attachments/assets/b0731c2a-da99-4c18-a6de-d4ab1a5e6856" />

- Receptionists Dashboard
<img width="1624" height="980" alt="image" src="https://github.com/user-attachments/assets/168f73f4-84e8-4ef4-9028-1240730bc788" />

- Doctor Dashboard
<img width="1618" height="932" alt="image" src="https://github.com/user-attachments/assets/98aeb6d0-e2c7-4c63-91c4-bad8dcf2fb87" />


 ## How to Run the Project
	1.	Prerequisites
Make sure you have Python 3 installed on your computer. No extra libraries are needed — this project uses only tkinter, which comes built-in with Python.
	2.	Download the code
    https://github.com/mawiyasow-gif/PROG103_SIERRA_HOSPITAL_CLINIC_GROUP4.git
    cd sierra_health_hospital_clinic

    3.	Run the application
 python sierra_health_clinic.py

 ## Authors
	•	Alhaji Mawiya Sow - 905005175
    •	Mohamed Alimu Jalloh - 905005461
    •	Ibrahim JP Kai-Samba - 905005408

 ## Real‑World Impact
	•	Built for Sierra Leone’s healthcare system
	•	Helps clinics manage patient queues fairly, reducing wait‑time confusion and prioritising emergency and pregnant patients
	
 ## Technology Stack
	•	Language: Python 3
	•	GUI: tkinter (built‑in, no third‑party packages required)
	•	Data storage: Python dictionaries & lists (temporary, in‑memory)
	•	License: MIT


