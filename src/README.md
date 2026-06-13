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
