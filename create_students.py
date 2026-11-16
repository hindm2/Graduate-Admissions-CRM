
import pandas as pd
import numpy as np

# Make the fictional data reproducible
rng = np.random.default_rng(42)

# Number of prospective students
n_students = 100

# Create unique student IDs
student_ids = range(1001, 1001 + n_students)

# Fictional names
first_names = [
    "Emma", "Liam", "Olivia", "Noah", "Sophia",
    "James", "Ava", "Lucas", "Mia", "Ethan"
]

last_names = [
    "Smith", "Johnson", "Brown", "Davis", "Wilson",
    "Taylor", "Anderson", "Thomas", "Martin", "Lee"
]

# Create the student database
students = pd.DataFrame({
    "student_id": student_ids,

    "first_name": rng.choice(first_names, n_students),

    "last_name": rng.choice(last_names, n_students),

    "program": rng.choice(
        ["Online MBA", "Management", "Accounting", "Business Analytics"],
        n_students
    ),

    "recruitment_source": rng.choice(
        ["Website", "Webinar", "Social Media", "Referral", "Email Campaign"],
        n_students
    ),

    "application_status": rng.choice(
        ["Inquiry", "Interested", "Applied", "Admitted", "Enrolled"],
        n_students
    )
})

# Generate unique fictional email addresses
students["email"] = students["student_id"].apply(
    lambda student_id: f"student{student_id}@example.com"
)

# Save the dataset
students.to_csv("students.csv", index=False)

print("Student database created successfully!")
print(students.head())
print(f"Total students: {len(students)}")
