create schema user_management;

create schema program_management;

create schema expert_management;

create table
    user_management.users (
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone_number VARCHAR UNIQUE,
        registration_date DATE NOT NULL,
        date_of_birth DATE NOT NULL,
        Gender VARCHAR(100) NOT NULL,
        activity_status BOOLEAN DEFAULT TRUE
    );

create table
    program_management.program (
        program_id SERIAL PRIMARY KEY,
        program_title VARCHAR UNIQUE NOT NULL,
        program_description VARCHAR UNIQUE NOT NULL,
        price INTEGER,
        discount INTEGER DEFAULT 0,
        total_time_required INTEGER,
        creation_date DATE NOT NULL
    );

create table
    program_management.status (
        status_id SERIAL PRIMARY KEY,
        label VARCHAR NOT NULL,
        hexcode VARCHAR
    );

create table
    user_management.enrollments (
        enrollment_id SERIAL PRIMARY KEY,
        user_id INTEGER,
        program_id INTEGER,
        enrollment_date DATE NOT NULL,
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user_management.users (user_id),
        CONSTRAINT fk_program FOREIGN KEY (program_id) REFERENCES program_management.program (program_id)
    );

create table
    program_management.tasks (
        task_id SERIAL PRIMARY KEY,
        program_id INTEGER NOT NULL,
        task_title VARCHAR UNIQUE NOT NULL,
        task_description VARCHAR UNIQUE NOT NULL,
        total_time_required INTEGER,
        CONSTRAINT fk_program FOREIGN KEY (program_id) REFERENCES program_management.program (program_id)
    );

create table
    program_management.tasks_tracker (
        program_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        start_time timestamp NOT NULL,
        end_time timestamp NOT NULL,
        score INTEGER,
        PRIMARY KEY (user_id, program_id, task_id),
        CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES program_management.status (status_id),
        CONSTRAINT fk_program FOREIGN KEY (program_id) REFERENCES program_management.program (program_id),
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user_management.users (user_id),
        CONSTRAINT fk_task FOREIGN KEY (task_id) REFERENCES program_management.tasks (task_id)
    );

create table
    expert_management.experts (
        expert_id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        bio VARCHAR NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone_number VARCHAR UNIQUE,
        hire_date DATE NOT NULL,
        date_of_birth DATE NOT NULL,
        Gender VARCHAR(100) NOT NULL,
        activity_status BOOLEAN DEFAULT TRUE
    );

create table
    expert_management.authorship (
        authorship_id SERIAL PRIMARY KEY,
        expert_id INTEGER NOT NULL,
        program_id INTEGER NOT NULL,
        CONSTRAINT fk_expert FOREIGN KEY (expert_id) REFERENCES expert_management.experts (expert_id),
        CONSTRAINT fk_program FOREIGN KEY (program_id) REFERENCES program_management.program (program_id)
    );

create table
    program_management.speciality (
        speciality_id SERIAL PRIMARY KEY,
        speciality_name VARCHAR(50) NOT NULL,
        speciality_description VARCHAR NOT NULL
    );

create table
    program_management.sme (
        sme_id SERIAL PRIMARY KEY,
        expert_id INTEGER NOT NULL,
        speciality_id INTEGER NOT NULL,
        CONSTRAINT fk_expert FOREIGN KEY (expert_id) REFERENCES expert_management.experts (expert_id),
        CONSTRAINT fk_speciality FOREIGN KEY (speciality_id) REFERENCES program_management.speciality (speciality_id)
    );