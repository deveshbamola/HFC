import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from psycopg2 import OperationalError

# Initialize Faker
fake = Faker()
load_dotenv()

def get_connection():
    dbname   = os.getenv("DB_NAME")
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host     = os.getenv("DB_HOST", "localhost")
    port     = os.getenv("DB_PORT", 5432)

    # debug print
    # print(f"→ Connecting to Postgres with host={host!r}, port={port!r}, dbname={dbname!r}, user={user!r}")

    try:
        return psycopg2.connect(
            dbname=dbname, user=user, password=password,
            host=host, port=port
        )
    except OperationalError as e:
        print("❌ OperationalError:", e)
        raise

connection = get_connection()
cursor = connection.cursor()

# Function to insert users into the user_management.users table
def insert_users(n):
    user_ids = []
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        phone_number = fake.phone_number()
        registration_date = fake.date_this_decade()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
        gender = random.choice(['M', 'F', 'O'])  # Shorten to single-character representation
        activity_status = random.choice([True, False])

        cursor.execute(
            """
            INSERT INTO user_management.user
            (first_name, last_name, email, phone_number, registration_date, date_of_birth, gender, activity_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id
            """, (first_name, last_name, email, phone_number, registration_date, date_of_birth, gender, activity_status)
        )
        user_id = cursor.fetchone()[0]
        user_ids.append(user_id)

    connection.commit()
    return user_ids

# Function to insert programs into the program_management.program table
def insert_programs(n):
    program_ids = []
    for _ in range(n):
        program_title = fake.unique.catch_phrase()
        program_description = fake.unique.text(max_nb_chars=200)
        price = random.randint(100, 1000)
        discount = random.randint(0, 30)
        total_time_required = random.randint(10, 50)
        creation_date = fake.date_this_decade()

        cursor.execute(
            """
            INSERT INTO program_management.program
            (program_title, program_description, price, discount, total_time_required, creation_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING program_id
            """, (program_title, program_description, price, discount, total_time_required, creation_date)
        )
        program_id = cursor.fetchone()[0]
        program_ids.append(program_id)

    connection.commit()
    return program_ids

# Function to insert statuses into the program_management.status table
def insert_statuses():
    statuses = [("In-Progress", "#00FF00"), ("To-Do", "#FFFF00"), ('Done', "#FF0000")]
    status_ids = []
    for label, status in statuses:
        cursor.execute(
            """
            INSERT INTO program_management.status
            (label, status)
            VALUES (%s, %s)
            RETURNING status_id
            """, (label, status)
        )
        status_id = cursor.fetchone()[0]
        status_ids.append(status_id)

    connection.commit()
    return status_ids

# Function to insert enrollments into the user_management.enrollments table
def insert_enrollments(user_ids, program_ids, n):
    for _ in range(n):
        user_id = random.choice(user_ids)
        program_id = random.choice(program_ids)
        enrollment_date = fake.date_this_year()

        cursor.execute(
            """
            INSERT INTO user_management.enrollment
            (user_id, program_id, enrollment_date)
            VALUES (%s, %s, %s)
            """, (user_id, program_id, enrollment_date)
        )

    connection.commit()

# Function to insert tasks into the program_management.tasks table
def insert_tasks(program_ids, n):
    task_ids = []
    for _ in range(n):
        program_id = random.choice(program_ids)
        task_title = fake.unique.catch_phrase()
        task_description = fake.unique.text(max_nb_chars=200)
        total_time_required = random.randint(5, 20)

        cursor.execute(
            """
            INSERT INTO program_management.task
            (program_id, task_title, task_description, total_time_required)
            VALUES (%s, %s, %s, %s)
            RETURNING task_id
            """, (program_id, task_title, task_description, total_time_required)
        )
        task_id = cursor.fetchone()[0]
        task_ids.append(task_id)

    connection.commit()
    return task_ids

# Function to insert task tracker data into the program_management.tasks_tracker table
def insert_tasks_tracker(user_ids, program_ids, task_ids, status_ids, n):
    for _ in range(n):
        user_id = random.choice(user_ids)
        program_id = random.choice(program_ids)
        task_id = random.choice(task_ids)
        status_id = random.choice(status_ids)
        start_time = fake.date_time_this_year()
        end_time = start_time + timedelta(hours=random.randint(1, 3))
        score = random.randint(50, 100)

        cursor.execute(
            """
            INSERT INTO program_management.tasks_tracker
            (user_id, program_id, task_id, status_id, start_time, end_time, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, program_id, task_id, status_id, start_time, end_time, score)
        )

    connection.commit()

# Insert data into expert_management.experts table
def insert_experts(n):
    expert_ids = []
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        bio = fake.text(max_nb_chars=200)
        email = fake.unique.email()
        phone_number = fake.phone_number()
        hire_date = fake.date_this_decade()
        date_of_birth = fake.date_of_birth(minimum_age=25, maximum_age=70)
        gender = random.choice(['M', 'F', 'O'])  # Shorten to single-character representation
        activity_status = random.choice([True, False])

        cursor.execute(
            """
            INSERT INTO expert_management.expert
            (first_name, last_name, bio, email, phone_number, hire_date, date_of_birth, gender, activity_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING expert_id
            """, (first_name, last_name, bio, email, phone_number, hire_date, date_of_birth, gender, activity_status)
        )
        expert_id = cursor.fetchone()[0]
        expert_ids.append(expert_id)

    connection.commit()
    return expert_ids

# Insert data into expert_management.authorship table
def insert_authorship(expert_ids, program_ids):
    for _ in range(len(program_ids)):
        expert_id = random.choice(expert_ids)
        program_id = random.choice(program_ids)

        cursor.execute(
            """
            INSERT INTO expert_management.authorship
            (expert_id, program_id)
            VALUES (%s, %s)
            """, (expert_id, program_id)
        )

    connection.commit()

# Function to insert specialities into the program_management.speciality table
def insert_specialities():
    specialities = [
        ("Data Science", "Advanced analytics and machine learning techniques"),
        ("Web Development", "Full-stack web application development"),
        ("Mobile Development", "iOS and Android application development"),
        ("Cloud Computing", "AWS, Azure, and GCP cloud infrastructure"),
        ("Cybersecurity", "Information security and ethical hacking"),
        ("DevOps", "Continuous integration and deployment practices"),
        ("AI/ML", "Artificial intelligence and machine learning"),
        ("Database Management", "SQL and NoSQL database administration"),
        ("UI/UX Design", "User interface and user experience design"),
        ("Project Management", "Agile and traditional project management"),
        ("Digital Marketing", "SEO, SEM, and social media marketing"),
        ("Business Analytics", "Data-driven business decision making"),
        ("Software Testing", "Quality assurance and automated testing"),
        ("Network Engineering", "Network design and administration"),
        ("Blockchain", "Cryptocurrency and distributed ledger technology")
    ]

    speciality_ids = []
    for name, description in specialities:
        cursor.execute(
            """
            INSERT INTO program_management.speciality
            (speciality_name, speciality_description)
            VALUES (%s, %s)
            RETURNING speciality_id
            """, (name, description)
        )
        speciality_id = cursor.fetchone()[0]
        speciality_ids.append(speciality_id)

    connection.commit()
    return speciality_ids

# Function to insert SME (Subject Matter Expert) relationships
def insert_sme(expert_ids, speciality_ids, n):
    """
    Creates relationships between experts and their specialities.
    Each expert can have multiple specialities.
    """
    inserted_pairs = set()  # To avoid duplicate expert-speciality pairs

    for _ in range(n):
        expert_id = random.choice(expert_ids)
        speciality_id = random.choice(speciality_ids)

        # Avoid duplicate combinations
        pair = (expert_id, speciality_id)
        if pair in inserted_pairs:
            continue

        cursor.execute(
            """
            INSERT INTO program_management.sme
            (expert_id, speciality_id)
            VALUES (%s, %s)
            """, (expert_id, speciality_id)
        )
        inserted_pairs.add(pair)

    connection.commit()

# Main function to insert fake data into all tables
def populate_data():
    # Insert users
    user_ids = insert_users(50)

    # Insert programs
    program_ids = insert_programs(20)

    # Insert statuses
    status_ids = insert_statuses()

    # Insert enrollments
    insert_enrollments(user_ids, program_ids, 30)

    # Insert tasks
    task_ids = insert_tasks(program_ids, 50)

    # Insert task tracker data
    insert_tasks_tracker(user_ids, program_ids, task_ids, status_ids, 50)

    # Insert experts
    expert_ids = insert_experts(10)

    # Insert authorship
    insert_authorship(expert_ids, program_ids)

    speciality_ids = insert_specialities()

    # NEW: Insert SME relationships
    insert_sme(expert_ids, speciality_ids, 25)  # Create 25 expert-speciality relationships

# Run the script to populate the database
populate_data()

# Close the cursor and connection
cursor.close()
connection.close()
