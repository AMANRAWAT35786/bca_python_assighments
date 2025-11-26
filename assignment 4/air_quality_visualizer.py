"""
Assignment 4 - Air Quality Data Visualizer (robust loader)
Author: Aman Rawat
Description:
Same simple CLI visualizer but load_data now tries multiple paths:
 - path as entered (relative or absolute)
 - script folder + entered name
It prints attempted paths so you can see where it looked.
"""

import csv
import matplotlib.pyplot as plt
from pathlib import Path
import sys

class AirQualityVisualizer:
    def __init__(self):
        self.data = []

    # -------------------------
    # Resolve file path robustly
    # -------------------------
    def _resolve_csv_path(self, file_name: str) -> Path:
        """Return a Path object if the file exists, otherwise None.
        Tries:
          1) Path(file_name) as given (absolute or relative to cwd)
          2) Path(script_folder) / file_name
        """
        attempts = []

        p1 = Path(file_name)
        attempts.append(p1.resolve())
        if p1.exists():
            return p1

        # try script directory
        script_dir = Path(__file__).parent.resolve()
        p2 = script_dir / file_name
        attempts.append(p2)
        if p2.exists():
            return p2

        # also try replacing spaces in folder name if user copied weird path
        # (not necessary usually, but harmless)
        # final attempt: absolute version of p1
        attempts.append(p1.resolve())

        # print debug info of what we tried
        print("Tried these paths (in order):")
        for a in attempts:
            print(" -", a)
        return None

    # -------------------------
    # Load CSV File
    # -------------------------
    def load_data(self, file_name):
        try:
            resolved = self._resolve_csv_path(file_name)
            if not resolved:
                print("Error: File not found.")
                return

            with open(resolved, "r", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
            print("Data loaded successfully from:", resolved)
        except FileNotFoundError:
            print("Error: File not found (FileNotFoundError).")
        except Exception as e:
            print("Unexpected error while loading:", e)

    # -------------------------
    # Preview Data
    # -------------------------
    def preview(self, count=5):
        if not self.data:
            print("Load data first.")
            return

        print(f"\nShowing first {count} records:")
        for row in self.data[:count]:
            print(row)

    # -------------------------
    # Filter by City
    # -------------------------
    def filter_by_city(self, city):
        if not self.data:
            print("Load data first.")
            return

        result = [
            row for row in self.data
            if "City" in row and row["City"].lower() == city.lower()
        ]

        if result:
            print(f"\nRecords for {city}:")
            for r in result[:10]:
                print(r)
        else:
            print("City not found.")

    # -------------------------
    # AQI Summary
    # -------------------------
    def show_summary(self):
        if not self.data:
            print("Load data first.")
            return

        try:
            aqis = [int(row["AQI"]) for row in self.data if row.get("AQI") not in (None, "")]
            if not aqis:
                print("No AQI numeric values found in data.")
                return
            print("\nAQI Summary:")
            print("Max AQI:", max(aqis))
            print("Min AQI:", min(aqis))
            print("Avg AQI:", sum(aqis) / len(aqis))
        except Exception as e:
            print("Error calculating summary:", e)

    # -------------------------
    # Plot AQI Trend
    # -------------------------
    def plot_city(self, city):
        if not self.data:
            print("Load data first.")
            return

        filtered = [
            row for row in self.data
            if "City" in row and row["City"].lower() == city.lower()
        ]

        if not filtered:
            print("City not found.")
            return

        days = [row.get("Date","") for row in filtered]
        try:
            values = [int(row["AQI"]) for row in filtered]
        except Exception as e:
            print("Error: AQI values could not be converted to int:", e)
            return

        plt.figure()
        plt.plot(days, values, marker="o")
        plt.title(f"AQI Trend for {city}")
        plt.xlabel("Date")
        plt.ylabel("AQI")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# -------------------------
# Menu
# -------------------------

def menu():
    tool = AirQualityVisualizer()

    while True:
        print("\n==== Air Quality Data Visualizer ====")
        print("1. Load CSV File")
        print("2. Preview Data")
        print("3. Filter by City")
        print("4. AQI Summary")
        print("5. Plot AQI Trend")
        print("0. Exit")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            fn = input("Enter CSV file name (or full path): ").strip()
            tool.load_data(fn)
        elif ch == "2":
            tool.preview()
        elif ch == "3":
            tool.filter_by_city(input("Enter city: ").strip())
        elif ch == "4":
            tool.show_summary()
        elif ch == "5":
            tool.plot_city(input("Enter city: ").strip())
        elif ch == "0":
            print("Program terminated.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
