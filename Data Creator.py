import json
import random
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# List of races to choose from
races = ['White', 'Black or African American', 'Asian', 'Native American', 'Pacific Islander', 'Other']

# Function to generate a formatted phone number
def generate_phone_number():
    # Generate a random phone number in XXX-XXX-XXXX format
    area_code = random.randint(100, 999)
    first_part = random.randint(100, 999)
    second_part = random.randint(1000, 9999)
    return f"{area_code}-{first_part}-{second_part}"

# Function to generate a random height in feet and inches
def generate_height():
    feet = random.randint(4, 6)  # Height in feet between 4 and 6 feet
    inches = random.randint(0, 11)  # Height in inches
    return f"{feet}'{inches}"

# Create a list to hold the user data
individuals = []

# Generate 100 individuals with formatted SSNs, consistent phone numbers, and additional fields
for _ in range(1000):
    individual = {
        "name": fake.name(),
        "ssn": fake.ssn(),
        "phone_number": generate_phone_number(),  # Ensure consistent phone number format
        "address": fake.address().replace("\n", ", "),  # Clean up newlines in addresses
        "dob": str(fake.date_of_birth(minimum_age=18, maximum_age=90)),  # Date of birth for adults
        "height": generate_height(),  # Random height
        "race": fake.random_element(races)  # Random race from the list
    }
    individuals.append(individual)

# Convert the list to JSON
individuals_json = json.dumps(individuals, indent=4)

# Print the JSON data
print(individuals_json)

# Optionally, write the JSON data to a file
with open("Individuals' Data.json", "w") as f:
    f.write(individuals_json)