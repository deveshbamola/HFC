import subprocess
import sys
import time

def install_requirements(requirements_file='initialize-dependencies/requirements.txt'):
    try:
        # Run pip install command to install dependencies from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print(f"Dependencies from {requirements_file} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies. Error: {e}")

def initialize_datbase():
    try:
        result = subprocess.run(['docker-compose', 'build', '--no-cache'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        
        # Take down existing containers and volumes
        result = subprocess.run(['docker-compose', 'down', '-v'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        
        # Start the containers in detached mode
        result = subprocess.run(['docker-compose', 'up', '-d'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)

        print("Database HFC is ready to connect.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies. Error: {e}")
    
    
def load_db():
    time.sleep(5)
    try:
        result = subprocess.run(['py', 'initialize-dependencies/load_fake_data.py'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print(f"Dummy Data injected.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies. Error: {e}")


# Call the function to install dependencies
install_requirements()
initialize_datbase()
load_db()
