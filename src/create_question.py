import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Configuration
BASE_URL = "http://localhost:3000"
DATABASE_ID = 1  # Adjust this to your H2 sample database ID

# Headers
headers = {
    'x-api-key': os.getenv("METABASE_API_KEY"),
    'Content-Type': 'application/json'
}

# Question payload
question_data = {
    "name": "sample query 1",
    "dataset_query": {
        "type": "native",
        "native": {
            "query": "SELECT *\nFROM \"PUBLIC\".\"ACCOUNTS\"\nLIMIT 1"
        },
        "database": DATABASE_ID
    },
    "display": "table",
    "visualization_settings": {}
}

# Create the question
response = requests.post(f"{BASE_URL}/api/card", headers=headers, json=question_data)

# Handle the response
if response.status_code == 200:
    data = response.json()
    question_id = data.get('id')
    print(f"Question created successfully!")
    print(f"Question ID: {question_id}")
    print(f"Question URL: {BASE_URL}/question/{question_id}")
else:
    assert False, f"Error: {response.status_code} - {response.text}"