# Assignment 3 – Hospital Patient Management System
### Course: Problem Solving with Python  
### Author: Aman Rawat  
### Semester: I (BCA – AI & DS)


## 📌 Project Overview
This project is a **menu-driven Hospital Patient Management System** built using Python.  
It uses **Object-Oriented Programming, JSON file handling, exception handling**, and a clean CLI interface to manage patient and doctor records.

The system allows:
- Adding patients
- Adding doctors
- Assigning doctors to patients
- Searching patient records
- Viewing all patients and doctors
- Discharging patients
- Saving & loading records using JSON

This project follows the exact structure required in Unit 3 Assignment instructions.



## 🧩 Key Features

## ✔ Object-Oriented Design  
Classes implemented:
- `Person` (Base Class)
- `Patient` (Inherits Person)
- `Doctor` (Inherits Person)
- `HospitalManagement` (Manages all operations)

## ✔ File Handling (JSON)
- Records stored in `hospital_records.json`
- Uses `json` and `pathlib.Path`

## ✔ Menu-Driven CLI
A simple text-based menu allows easy navigation:
