import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
import sys

# Function to get the correct base directory in both development and packaged executable environments
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
DATA_FILE = os.path.join(BASE_DIR, "Individuals' Data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_valid_phone_number(phone):
    """
    Check if the phone number is valid (in the format XXX-XXX-XXXX).
    """
    return re.match(r"^\d{3}-\d{3}-\d{4}$", phone) is not None

def is_valid_input(text, allow_commas=False, allow_apostrophe=False):
    """
    Check if the text contains only valid characters:
    - No special characters
    - Allow spaces, hyphens, and apostrophes (only for name and race).
    """
    if allow_commas and allow_apostrophe:
        return re.match(r"^[A-Za-z0-9 \-,']+$", text) is not None  
    elif allow_commas:
        return re.match(r"^[A-Za-z0-9 \-,]+$", text) is not None  # Allow commas, no apostrophes
    elif allow_apostrophe:
        return re.match(r"^[A-Za-z0-9 \-']+$", text) is not None  # Allow apostrophes and hyphens
    else:
        # Default case: no special characters at all
        return re.match(r"^[A-Za-z0-9 \-]+$", text) is not None  # Only letters, numbers, spaces, hyphens


def auto_format_ssn(ssn):
    """
    Automatically format a 9-digit SSN into XXX-XX-XXXX format.
    """
    ssn_clean = ssn.replace(" ", "").replace("-", "")
    if len(ssn_clean) == 9 and ssn_clean.isdigit():
        return f"{ssn_clean[:3]}-{ssn_clean[3:5]}-{ssn_clean[5:]}"
    return ssn

def is_valid_ssn(ssn):
    return re.match(r"^[0-9 -]+$", ssn) is not None


# Tooltip function
def create_tooltip(widget, text, app):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)

    # Change tooltip background and text color based on the current theme
    if app.is_dark_mode:
        bg_color = '#333333'  
        fg_color = '#ffffff'  
    else:
        bg_color = '#ffffe0'  
        fg_color = '#000000' 

    tooltip_label = ttk.Label(tooltip, text=text, background=bg_color, foreground=fg_color, relief='solid', borderwidth=1, padding=5)
    tooltip_label.pack()

    def on_enter(e):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def on_leave(e):
        tooltip.withdraw()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# Hover effect for buttons
def create_button_styles(style):
    """Define hover and normal styles for buttons."""
    style.configure('TButton', background='#f0f0f5', foreground='black')
    
    style.map('TButton', 
              background=[('active', '#3498db')],
              foreground=[('active', 'white')])

class IdentityManagerApp:
    def __init__(self, root):
        """
        Initialize the Identity Manager application, setting up the main menu and theme.
        """
        self.root = root
        self.root.title("Identity Manager")
        self.root.geometry("700x500")
        self.light_bg = '#f0f0f5' 
        self.dark_bg = '#2e2e2e' 
        self.light_fg = 'black'
        self.dark_fg = 'white'

        self.style = ttk.Style()
        self.style.theme_use('clam')

        create_button_styles(self.style)

        self.root.configure(bg=self.light_bg)  
        self.is_dark_mode = False  
        self.data = load_data()
        self.style = ttk.Style()
        self.style.theme_use('clam')  
        self.style.configure('TFrame', background=self.light_bg)
        self.style.configure('TButton', font=('Helvetica', 10), padding=10)
        self.style.configure('TLabel', background=self.light_bg, font=('Helvetica', 12))
        self.style.configure('Treeview', font=('Helvetica', 10))
        self.current_frame = None
        self.main_menu()  

    def toggle_theme(self):
        """Switch between dark and light mode."""
        if self.is_dark_mode:
            self.root.configure(bg=self.light_bg)
            self.style.configure('TFrame', background=self.light_bg)
            self.style.configure('TLabel', background=self.light_bg, foreground=self.light_fg)
            self.is_dark_mode = False
        else:
            self.root.configure(bg=self.dark_bg)
            self.style.configure('TFrame', background=self.dark_bg)
            self.style.configure('TLabel', background=self.dark_bg, foreground=self.dark_fg)
            self.is_dark_mode = True

    def create_toggle_button(self):
        """Create the dark mode toggle button at the bottom-right corner."""
        self.toggle_button = ttk.Button(self.root, text="🌙", command=self.toggle_theme)
        self.toggle_button.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20, width=40, height=40)

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def main_menu(self):
        """
        Display the main menu with options to add, remove, find, and list people.
        """
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(self.current_frame, text="Identity Manager", font=("Helvetica", 20, "bold"))
        title.pack(pady=20)

        btn_add = ttk.Button(self.current_frame, text="Add a Person", command=self.add_person, width=30)
        btn_add.pack(pady=10)

        btn_remove = ttk.Button(self.current_frame, text="Remove a Person", command=self.remove_person, width=30)
        btn_remove.pack(pady=10)

        btn_find = ttk.Button(self.current_frame, text="Find a Person", command=self.find_person, width=30)
        btn_find.pack(pady=10)

        btn_show_all = ttk.Button(self.current_frame, text="Show All People", command=self.show_all_people, width=30)
        btn_show_all.pack(pady=10)

        self.create_toggle_button()  

    def go_back(self):
        self.main_menu()

    def add_person(self):
        """
        Show the form to add a new person, including all relevant fields (Name, SSN, etc.).
        """
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        # Improved layout with grid system
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        title = ttk.Label(frame, text="Add a Person", font=("Helvetica", 18, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)

        # Fields for form input
        fields = {
            "Name": "Full name, e.g., John Doe",
            "SSN": "Social Security Number in XXX-XX-XXXX format",
            "Phone Number": "Phone number in XXX-XXX-XXXX format",
            "Address": "Full address, e.g., 123 Main St, City, State",
            "DOB": "Date of Birth in YYYY-MM-DD format",
            "Height": "Height in X'Y\" format (e.g., 5'11)",
            "Race": "Race (e.g., Asian, Caucasian)"
        }

        self.entries = {}
        for idx, (field, tooltip_text) in enumerate(fields.items(), start=1):
            label = ttk.Label(frame, text=field + ":", font=('Helvetica', 12))
            label.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.E)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=idx, column=2, padx=10, pady=5, sticky=tk.W)
            self.entries[field.lower().replace(" ", "_")] = entry
            create_tooltip(entry, tooltip_text, self)

        btn_submit = ttk.Button(frame, text="Add Person", command=self.submit_person)
        btn_submit.grid(row=len(fields) + 1, column=1, columnspan=2, pady=20)

        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.grid(row=len(fields) + 2, column=1, columnspan=2, pady=10)


    def submit_person(self):
        """
        Validate the data and add the person to the system if all checks pass.
        """
        new_person = {
            "name": self.entries["name"].get().strip(),
            "ssn": self.entries["ssn"].get().strip(),
            "phone_number": self.entries["phone_number"].get().strip(),
            "address": self.entries["address"].get().strip(),
            "dob": self.entries["dob"].get().strip(),
            "height": self.entries["height"].get().strip(),
            "race": self.entries["race"].get().strip()
        }

        # Validate all fields
        if not all(new_person.values()):
            messagebox.showerror("Error", "All fields are required.")
            return
        
        if not is_valid_ssn(new_person["ssn"]):
            messagebox.showerror("Error", "Invalid SSN. Only digits, spaces, and dashes are allowed.")
            return

        # Validate SSN: ensure only digits, spaces, and dashes
        new_person["ssn"] = auto_format_ssn(new_person["ssn"])
        if len(new_person["ssn"]) != 11:
            messagebox.showerror("Error", "Invalid SSN format. Use XXX-XX-XXXX or provide 9 digits.")
            return

        # Validate Phone Number
        new_person["phone_number"] = new_person["phone_number"].replace(" ", "").replace("-", "")
        if len(new_person["phone_number"]) == 10 and new_person["phone_number"].isdigit():
            new_person["phone_number"] = f"{new_person['phone_number'][:3]}-{new_person['phone_number'][3:6]}-{new_person['phone_number'][6:]}"
        else:
            messagebox.showerror("Error", "Invalid Phone Number format. Use XXX-XXX-XXXX or provide 10 digits.")
            return

        # Validate Date of Birth format (YYYY-MM-DD)
        dob_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(dob_pattern, new_person["dob"]):
            messagebox.showerror("Error", "Invalid Date of Birth format. Use YYYY-MM-DD.")
            return

        # Validate Height format (X'Y")
        height_pattern = r"^\d{1,2}'\d{1,2}$"
        if not re.match(height_pattern, new_person["height"]):
            messagebox.showerror("Error", "Invalid Height format. Use X'Y\" (e.g., 5'11).")
            return

        # Check Address for special characters
        if not is_valid_input(new_person["address"], allow_commas=True):
            messagebox.showerror("Error", "Invalid characters in Address.")
            return
        
        # Name validation (no special characters)
        if not is_valid_input(new_person["name"]):
            messagebox.showerror("Error", "Invalid characters in Name. No special characters allowed.")
            return

        # Race validation (no special characters)
        if not is_valid_input(new_person["race"]):
            messagebox.showerror("Error", "Invalid characters in Race. No special characters allowed.")
            return

        # Validate the height apostrophe character
        if not is_valid_input(new_person["height"], allow_apostrophe=True):
            messagebox.showerror("Error", "Invalid characters in Height.")
            return

        # Check for duplicate SSN
        if any(person["ssn"] == new_person["ssn"] for person in self.data):
            messagebox.showerror("Error", "SSN already exists.")
            return

        # Add to data and save
        self.data.append(new_person)
        save_data(self.data)
        self.refresh_data()
        messagebox.showinfo("Success", "Person added successfully.")
        self.go_back()

    def remove_person(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        title = ttk.Label(frame, text="Remove a Person", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)

        label_ssn = ttk.Label(frame, text="Enter SSN to Remove:", font=('Helvetica', 12))
        label_ssn.grid(row=1, column=1, padx=10, pady=5, sticky=tk.E)
        self.entry_ssn_remove = ttk.Entry(frame, width=40)
        self.entry_ssn_remove.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        btn_remove = ttk.Button(frame, text="Remove", command=self.remove_person_by_ssn)
        btn_remove.grid(row=2, column=1, columnspan=2, pady=20)

        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.grid(row=3, column=1, columnspan=2, pady=10)

    def remove_person_by_ssn(self):
        """
        Remove a person from the system based on their SSN.
        """
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
        """
        Show the form to find a person based on multiple criteria.
        """
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        title = ttk.Label(frame, text="Find a Person", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)

        fields = ["Name", "SSN", "Phone Number", "Address", "DOB", "Height", "Race"]
        self.entries_find = {}
        for idx, field in enumerate(fields, start=1):
            label = ttk.Label(frame, text=f"{field}:", font=('Helvetica', 12))
            label.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.E)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=idx, column=2, padx=10, pady=5, sticky=tk.W)
            self.entries_find[field.lower().replace(" ", "_")] = entry

        btn_find = ttk.Button(frame, text="Find", command=self.search_person)
        btn_find.grid(row=len(fields) + 1, column=1, columnspan=2, pady=20)

        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.grid(row=len(fields) + 2, column=1, columnspan=2, pady=10)

    def search_person(self):
        """
        Search the system for people matching the entered criteria.
        """
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
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        title = ttk.Label(frame, text="Search Results", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        columns = ("Name", "SSN", "Phone Number", "Address", "DOB", "Height", "Race")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)

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

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.pack(pady=5)


    def show_all_people(self):
        """
        Show all people currently in the system.
        """
        self.clear_frame()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        title = ttk.Label(frame, text="All People", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        columns = ("Name", "SSN", "Phone Number", "Address", "DOB", "Height", "Race")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)

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

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_back = ttk.Button(frame, text="Go Back", command=self.go_back)
        btn_back.pack(pady=5)


    def refresh_data(self):
        self.data = load_data()

def main():
    root = tk.Tk()
    app = IdentityManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
