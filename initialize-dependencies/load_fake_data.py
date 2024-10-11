



import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to the PostgreSQL database
# Establish a connection to your Postgres database
connection = psycopg2.connect(database = "HFC", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "mysecretpassword",
                        port = 5432)
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
            INSERT INTO user_management.users
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
    for label, hexcode in statuses:
        cursor.execute(
            """
            INSERT INTO program_management.status
            (label, hexcode)
            VALUES (%s, %s)
            RETURNING status_id
            """, (label, hexcode)
        )
        status_id = cursor.fetchone()[0]
        status_ids.append(status_id)

    connection.commit()
    return status_ids

# Function to insert enrollments into the user_management.enrollments table
def insert_enrollments(user_ids, program_ids, status_ids, n):
    for _ in range(n):
        user_id = random.choice(user_ids)
        program_id = random.choice(program_ids)
        start_date = fake.date_this_year()
        end_date = fake.date_between(start_date=start_date, end_date='+30d')
        status_id = random.choice(status_ids)

        cursor.execute(
            """
            INSERT INTO user_management.enrollments
            (user_id, program_id, start_date, end_date, status_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (user_id, program_id, start_date, end_date, status_id)
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
        price = random.uniform(50, 200)
        discount = random.randint(0, 20)
        creation_date = fake.date_this_decade()

        cursor.execute(
            """
            INSERT INTO program_management.tasks
            (program_id, task_title, task_description, total_time_required, price, discount, creation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING task_id
            """, (program_id, task_title, task_description, total_time_required, price, discount, creation_date)
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
            INSERT INTO expert_management.experts
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

# Main function to insert fake data into all tables
def populate_data():
    # Insert users
    user_ids = insert_users(50)

    # Insert programs
    program_ids = insert_programs(20)

    # Insert statuses
    status_ids = insert_statuses()

    # Insert enrollments
    insert_enrollments(user_ids, program_ids, status_ids, 30)

    # Insert tasks
    task_ids = insert_tasks(program_ids, 50)

    # Insert task tracker data
    insert_tasks_tracker(user_ids, program_ids, task_ids, status_ids, 50)

    # Insert experts
    expert_ids = insert_experts(10)

    # Insert authorship
    insert_authorship(expert_ids, program_ids)

# Run the script to populate the database
populate_data()

# Close the cursor and connection
cursor.close()
connection.close()
