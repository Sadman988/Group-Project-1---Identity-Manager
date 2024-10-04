import json
import random
from faker import Faker

# Initialize the Faker generator
fake = Faker()

races = ['White', 'Black or African American', 'Asian', 'Native American', 'Pacific Islander', 'Other']

# Function to generate a formatted phone number
def generate_phone_number():
    '''
    Generate a random phone number in XXX-XXX-XXXX format
    '''
    area_code = random.randint(100, 999)
    first_part = random.randint(100, 999)
    second_part = random.randint(1000, 9999)
    return f"{area_code}-{first_part}-{second_part}"

# Function to generate a random height in feet and inches
def generate_height():
    feet = random.randint(4, 6)
    inches = random.randint(0, 11) 
    return f"{feet}'{inches}"

individuals = []

for _ in range(1000):
    '''
    Generate 100 individuals with formatted SSNs, consistent phone numbers, and additional fields
    '''
    individual = {
        "name": fake.name(),
        "ssn": fake.ssn(),
        "phone_number": generate_phone_number(), 
        "address": fake.address().replace("\n", ", "), 
        "dob": str(fake.date_of_birth(minimum_age=18, maximum_age=90)),
        "height": generate_height(),
        "race": fake.random_element(races) 
    }
    individuals.append(individual)

# Convert the list to JSON
individuals_json = json.dumps(individuals, indent=4)

with open("Individuals' Data.json", "w") as f:
    f.write(individuals_json)