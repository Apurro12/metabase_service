import requests
from dotenv import load_dotenv
import os


load_dotenv()

# Configuration
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
BASE_URL = "http://localhost:3000"

# Headers
headers = {
    'x-api-key': os.getenv("METABASE_API_KEY"),
}

# Make the GET request
response = requests.get(f"{BASE_URL}/api/permissions/group", headers=headers)

# Handle the response
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")
