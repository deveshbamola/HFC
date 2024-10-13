# HFC
HFC aka hunt for career

# PRE-Requisites
Install python 
Download docker and docker-compose

# Setup
run 'initialize.py' -> command "py initialize.py"

# Steps to connect to database
1. connect to db 
    docker exec -it postgres-db  psql -U postgres -d HFC

2. list all schemas
    \dn

3. list all tables
    \dt *.*

3. navigate through db using sql commands
    select * from program_management.tasks_tracker;



