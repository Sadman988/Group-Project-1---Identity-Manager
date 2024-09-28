import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
import sys

# Function to get the correct base directory in both development and packaged executable environments
def get_base_dir():
    if getattr(sys, 'frozen', False):
        # If the application is frozen 
        return os.path.dirname(sys.executable)
    else:
        # If the script is being run normally 
        return os.path.dirname(os.path.abspath(__file__))

# Get the correct base directory
BASE_DIR = get_base_dir()

# Define the path to the JSON file relative to the script location
DATA_FILE = os.path.join(BASE_DIR, "Individuals' Data.json")

# Utility functions
def load_data():
    """Load individual data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    """Save individual data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_valid_phone_number(phone):
    """Validate phone number format (XXX-XXX-XXXX)."""
    return re.match(r"^\d{3}-\d{3}-\d{4}$", phone) is not None

def is_valid_input(text, allow_commas=False, allow_apostrophe=False):
    """Check if the text contains only valid characters (no special characters).
    Commas are allowed for address fields."""
    if allow_commas and allow_apostrophe:
        return re.match(r"^[A-Za-z0-9 \-,']+$", text) is not None
    elif allow_commas:
        return re.match(r"^[A-Za-z0-9 \-,]+$", text) is not None
    elif allow_apostrophe:
        return re.match(r"^[A-Za-z0-9 \-']+$", text) is not None
    return re.match(r"^[A-Za-z0-9 \-]+$", text) is not None

def auto_format_ssn(ssn):
    """Automatically format a 9-digit SSN into XXX-XX-XXXX format."""
    ssn_clean = ssn.replace(" ", "").replace("-", "")
    if len(ssn_clean) == 9 and ssn_clean.isdigit():
        return f"{ssn_clean[:3]}-{ssn_clean[3:5]}-{ssn_clean[5:]}"
    return ssn

class IdentityManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Identity Manager")
        self.root.geometry("700x500")  # Adjusted size for better visibility
        self.data = load_data()
        self.current_frame = None
        self.main_menu()

    def clear_frame(self):
        """Clear the current frame before switching views."""
        if self.current_frame is not None:
            self.current_frame.destroy()

    def main_menu(self):
        """Display the main menu with options."""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        title = ttk.Label(self.current_frame, text="Identity Manager", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        # Buttons
        btn_add = ttk.Button(self.current_frame, text="Add a Person", command=self.add_person, width=30)
        btn_add.pack(pady=5)

        btn_remove = ttk.Button(self.current_frame, text="Remove a Person", command=self.remove_person, width=30)
        btn_remove.pack(pady=5)

        btn_find = ttk.Button(self.current_frame, text="Find a Person", command=self.find_person, width=30)
        btn_find.pack(pady=5)

        btn_show_all = ttk.Button(self.current_frame, text="Show All People", command=self.show_all_people, width=30)
        btn_show_all.pack(pady=5)

    def go_back(self):
        """Go back to the main menu."""
        self.main_menu()

    def add_person(self):
        """Display the Add Person form within the same window."""
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        # Create empty columns on either side to center content
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        # Title
        title = ttk.Label(frame, text="Add a Person", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)

        # Fields with placeholder examples
        fields = {
            "Name": "John Doe",
            "SSN": "123-45-6789",
            "Phone Number": "123-456-7890",
            "Address": "123 Main St, City, State",
            "DOB": "YYYY-MM-DD",
            "Height": "5'11",
            "Race": "Asian"
        }

        self.entries = {}
        for idx, (field, placeholder) in enumerate(fields.items(), start=1):
            label = ttk.Label(frame, text=field + ":")
            label.grid(row=idx, column=1, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(frame, width=50)
            entry.insert(0, placeholder)  # Show example format in each box
            entry.grid(row=idx, column=2, padx=5, pady=5, sticky=tk.W)
            self.entries[field.lower().replace(" ", "_")] = entry

        # Submit Button
        btn_submit = ttk.Button(frame, text="Add Person", command=self.submit_person)
        btn_submit.grid(row=len(fields) + 1, column=1, columnspan=2, pady=10)

        # Go Back Button
        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.grid(row=len(fields) + 2, column=1, columnspan=2, pady=5)

    def submit_person(self):
        """Process submission and add the person."""
        new_person = {
            "name": self.entries["name"].get().strip(),
            "ssn": self.entries["ssn"].get().strip(),
            "phone_number": self.entries["phone_number"].get().strip(),
            "address": self.entries["address"].get().strip(),
            "dob": self.entries["dob"].get().strip(),
            "height": self.entries["height"].get().strip(),
            "race": self.entries["race"].get().strip()
        }

        # Validation
        if not all(new_person.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        # SSN auto-formatting and validation
        new_person["ssn"] = auto_format_ssn(new_person["ssn"])
        if len(new_person["ssn"]) != 11:  # XXX-XX-XXXX format length
            messagebox.showerror("Error", "Invalid SSN format. Use XXX-XX-XXXX.")
            return

        # Phone number validation
        new_person["phone_number"] = new_person["phone_number"].replace(" ", "").replace("-", "")
        if len(new_person["phone_number"]) == 10 and new_person["phone_number"].isdigit():
            new_person["phone_number"] = f"{new_person['phone_number'][:3]}-{new_person['phone_number'][3:6]}-{new_person['phone_number'][6:]}"
        else:
            messagebox.showerror("Error", "Invalid Phone Number format. Use XXX-XXX-XXXX or provide 10 digits.")
            return

        # Date of Birth validation
        dob_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(dob_pattern, new_person["dob"]):
            messagebox.showerror("Error", "Invalid Date of Birth format. Use YYYY-MM-DD.")
            return

        # Height validation
        height_pattern = r"^\d{1,2}'\d{1,2}$"
        if not re.match(height_pattern, new_person["height"]):
            messagebox.showerror("Error", "Invalid Height format. Use X'Y (e.g., 5'11).")
            return

        # Validate input fields for special characters (allowing commas and apostrophes where appropriate)
        for field, value in new_person.items():
            if field == "address":
                if not is_valid_input(value, allow_commas=True):
                    messagebox.showerror("Error", f"Invalid characters in {field.capitalize()}.")
                    return
            elif field == "height":
                if not is_valid_input(value, allow_apostrophe=True):
                    messagebox.showerror("Error", f"Invalid characters in {field.capitalize()}. Only digits and apostrophe allowed.")
                    return
            elif field != "ssn" and not is_valid_input(value):
                messagebox.showerror("Error", f"Invalid characters in {field.capitalize()}. No special characters allowed.")
                return

        # Check for duplicate SSN
        if any(person["ssn"] == new_person["ssn"] for person in self.data):
            messagebox.showerror("Error", "SSN already exists.")
            return

        # Add to data and refresh
        self.data.append(new_person)
        save_data(self.data)
        self.refresh_data()
        messagebox.showinfo("Success", "Person added successfully.")
        self.go_back()

    def remove_person(self):
        """Display the Remove Person form within the same window."""
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        # Create empty columns on either side to center content
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        # Title
        title = ttk.Label(frame, text="Remove a Person", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)

        # SSN Entry
        label_ssn = ttk.Label(frame, text="Enter SSN to Remove:")
        label_ssn.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        self.entry_ssn_remove = ttk.Entry(frame, width=40)
        self.entry_ssn_remove.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        # Remove Button
        btn_remove = ttk.Button(frame, text="Remove", command=self.remove_person_by_ssn)
        btn_remove.grid(row=2, column=1, columnspan=2, pady=10)

        # Go Back Button
        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.grid(row=3, column=1, columnspan=2, pady=5)

    def remove_person_by_ssn(self):
        """Remove a person based on the provided SSN."""
        ssn_input = self.entry_ssn_remove.get().strip()
        ssn_formatted = auto_format_ssn(ssn_input)

        if len(ssn_formatted) != 11:
            messagebox.showerror("Error", "Invalid SSN format. Use XXX-XX-XXXX.")
            return

        for person in self.data:
            if person["ssn"] == ssn_formatted:
                confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {person['name']}?")
                if confirm:
                    self.data.remove(person)
                    save_data(self.data)
                    self.refresh_data()
                    messagebox.showinfo("Success", "Person removed successfully.")
                    self.go_back()
                return

        messagebox.showerror("Error", "Person with the given SSN not found.")

    def find_person(self):
        """Display the Find Person form within the same window."""
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        # Create empty columns on either side to center content
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        # Title
        title = ttk.Label(frame, text="Find a Person", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)

        # Fields for search criteria
        fields = ["Name", "SSN", "Phone Number", "Address", "DOB", "Height", "Race"]
        self.entries_find = {}
        for idx, field in enumerate(fields, start=1):
            label = ttk.Label(frame, text=f"{field}:")
            label.grid(row=idx, column=1, padx=5, pady=5, sticky=tk.E)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=idx, column=2, padx=5, pady=5, sticky=tk.W)
            self.entries_find[field.lower().replace(" ", "_")] = entry

        # Find Button
        btn_find = ttk.Button(frame, text="Find", command=self.search_person)
        btn_find.grid(row=len(fields) + 1, column=1, columnspan=2, pady=10)

        # Go Back Button
        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.grid(row=len(fields) + 2, column=1, columnspan=2, pady=5)


    def search_person(self):
        """Search for persons based on provided criteria."""
        criteria = {field: entry.get().strip() for field, entry in self.entries_find.items()}

        if not any(criteria.values()):
            messagebox.showerror("Error", "At least one search criterion is required.")
            return

        results = []
        for person in self.data:
            match = True
            for key, value in criteria.items():
                if value:
                    person_value = person.get(key, "").lower()
                    search_value = value.lower()
                    if key == "ssn":
                        person_value = person_value.replace("-", "")
                        search_value = search_value.replace("-", "")
                    if search_value not in person_value:
                        match = False
                        break
            if match:
                results.append(person)

        if not results:
            messagebox.showinfo("No Results", "No matching records found.")
            return

        self.show_search_results(results)

    def show_search_results(self, results):
        """Display search results within the same window."""
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        # Title
        title = ttk.Label(frame, text="Search Results", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        # Treeview for displaying results
        columns = ("Name", "SSN", "Phone Number", "Address", "DOB", "Height", "Race")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)

        # Insert Data
        for person in results:
            tree.insert("", tk.END, values=(
                person.get("name", ""),
                person.get("ssn", ""),
                person.get("phone_number", ""),
                person.get("address", ""),
                person.get("dob", ""),
                person.get("height", ""),
                person.get("race", "")
            ))

        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Go Back Button
        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.pack(pady=5)

    def show_all_people(self):
        """Display all people within the same window."""
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        # Title
        title = ttk.Label(frame, text="All People", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        # Treeview for displaying all people
        columns = ("Name", "SSN", "Phone Number", "Address", "DOB", "Height", "Race")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)

        # Insert Data
        for person in self.data:
            tree.insert("", tk.END, values=(
                person.get("name", ""),
                person.get("ssn", ""),
                person.get("phone_number", ""),
                person.get("address", ""),
                person.get("dob", ""),
                person.get("height", ""),
                person.get("race", "")
            ))

        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Go Back Button
        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.pack(pady=5)

    def refresh_data(self):
        """Refresh the data from the JSON file."""
        self.data = load_data()

def main():
    root = tk.Tk()
    app = IdentityManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
