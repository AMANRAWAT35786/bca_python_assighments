"""
Assignment 3 - Hospital Patient Management System
Author: Aman Rawat
Course: Problem Solving with Python
Description:
A complete menu-driven Hospital Patient Management System using:
- OOP (inheritance, dunder methods)
- File handling (JSON)
- Exception handling
- Search, Add, Assign, Discharge operations
- CLI interface
"""

import json
from pathlib import Path

# -------------------------
# Base Person Class
# -------------------------

class Person:
    """Base class for Patient and Doctor"""

    def __init__(self, name, unique_id):
        self.name = name
        self.unique_id = unique_id

    def __str__(self):
        return f"{self.unique_id} - {self.name}"

    def __repr__(self):
        return self.__str__()


# -------------------------
# Patient Class
# -------------------------

class Patient(Person):
    def __init__(self, name, patient_id, age, disease, status="Admitted"):
        super().__init__(name, patient_id)
        self.age = age
        self.disease = disease
        self.status = status
        self.doctor_id = None

    def admit(self):
        self.status = "Admitted"

    def discharge(self):
        self.status = "Discharged"

    def assign_doctor(self, doctor_id):
        self.doctor_id = doctor_id

    def to_dict(self):
        return {
            "name": self.name,
            "patient_id": self.unique_id,
            "age": self.age,
            "disease": self.disease,
            "status": self.status,
            "doctor_id": self.doctor_id
        }


# -------------------------
# Doctor Class
# -------------------------

class Doctor(Person):
    def __init__(self, name, doctor_id, specialization):
        super().__init__(name, doctor_id)
        self.specialization = specialization

    def to_dict(self):
        return {
            "name": self.name,
            "doctor_id": self.unique_id,
            "specialization": self.specialization
        }



# Hospital Management System


class HospitalManagement:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.data_file = Path("hospital_records.json")

    # Add Patient
    def add_patient(self):
        print("\n--- Add Patient ---")
        pid = input("Enter Patient ID: ")
        name = input("Enter Name: ")
        age = input("Enter Age: ")
        disease = input("Enter Disease: ")

        self.patients[pid] = Patient(name, pid, age, disease)
        print("Patient added successfully.")

    # View Patients
    def view_patients(self):
        print("\n--- Patient List ---")
        if not self.patients:
            print("No patient records found.")
            return

        print(f"{'ID':<10}{'Name':<20}{'Age':<10}{'Disease':<20}{'Status':<15}{'Doctor ID'}")
        print("-" * 70)

        for p in self.patients.values():
            print(f"{p.unique_id:<10}{p.name:<20}{p.age:<10}{p.disease:<20}{p.status:<15}{p.doctor_id}")

    # Search Patient
    def search_patient(self):
        keyword = input("Enter patient ID or name: ").lower()
        found = [
            p for p in self.patients.values()
            if keyword in p.unique_id.lower() or keyword in p.name.lower()
        ]

        if found:
            for p in found:
                print(p)
        else:
            print("No matching patient found.")

    # Discharge
    def discharge_patient(self):
        pid = input("Enter Patient ID to discharge: ")
        if pid in self.patients:
            self.patients[pid].discharge()
            print("Patient discharged successfully.")
        else:
            print("Invalid Patient ID.")

    # Add Doctor
    def add_doctor(self):
        print("\n--- Add Doctor ---")
        did = input("Enter Doctor ID: ")
        name = input("Enter Doctor Name: ")
        spec = input("Enter Specialization: ")

        self.doctors[did] = Doctor(name, did, spec)
        print("Doctor added successfully.")

    # View Doctors
    def view_doctors(self):
        print("\n--- Doctor List ---")
        if not self.doctors:
            print("No doctor records available.")
            return

        print(f"{'ID':<10}{'Name':<20}{'Specialization'}")
        print("-" * 50)

        for d in self.doctors.values():
            print(f"{d.unique_id:<10}{d.name:<20}{d.specialization}")

    # Assign Doctor
    def assign_doctor(self):
        pid = input("Enter Patient ID: ")
        did = input("Enter Doctor ID: ")

        if pid not in self.patients:
            print("Patient not found.")
            return

        if did not in self.doctors:
            print("Doctor not found.")
            return

        self.patients[pid].assign_doctor(did)
        print("Doctor assigned successfully.")

    # Save Data
    def save_data(self):
        try:
            data = {
                "patients": {pid: p.to_dict() for pid, p in self.patients.items()},
                "doctors": {did: d.to_dict() for did, d in self.doctors.items()}
            }

            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)

            print("Records saved successfully.")

        except Exception as e:
            print("Error saving file:", e)

    # Load Data
    def load_data(self):
        if not self.data_file.exists():
            print("No saved records found.")
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)

            # restore objects
            self.patients = {
                pid: Patient(
                    info["name"],
                    info["patient_id"],
                    info["age"],
                    info["disease"],
                    info["status"]
                )
                for pid, info in data["patients"].items()
            }

            self.doctors = {
                did: Doctor(
                    info["name"],
                    info["doctor_id"],
                    info["specialization"]
                )
                for did, info in data["doctors"].items()
            }

            print("Records loaded successfully.")

        except Exception as e:
            print("Error loading data:", e)


# Main Menu

def menu():
    HMS = HospitalManagement()

    while True:
        print("\n======= Hospital Management System =======")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Discharge Patient")
        print("5. Add Doctor")
        print("6. View Doctors")
        print("7. Assign Doctor to Patient")
        print("8. Save Records")
        print("9. Load Records")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1": HMS.add_patient()
        elif choice == "2": HMS.view_patients()
        elif choice == "3": HMS.search_patient()
        elif choice == "4": HMS.discharge_patient()
        elif choice == "5": HMS.add_doctor()
        elif choice == "6": HMS.view_doctors()
        elif choice == "7": HMS.assign_doctor()
        elif choice == "8": HMS.save_data()
        elif choice == "9": HMS.load_data()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()

