import requests
from dotenv import load_dotenv
import os
import json
from typing import Dict, Any, Optional

class MetabaseClient:
    def __init__(self, base_url: str = "http://localhost:3000", database_id: int = 1):
        load_dotenv()
        self.base_url = base_url
        self.database_id = database_id
        self.headers = {
            'x-api-key': os.getenv("METABASE_API_KEY"),
            'Content-Type': 'application/json'
        }

    def create_question(
        self,
        name: str,
        query: str,
        display: str = "table",
        visualization_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a native SQL question in Metabase

        Args:
            name: Name of the question
            query: SQL query string
            display: Display type (table, scalar, line, bar, etc.)
            visualization_settings: Optional visualization settings dict

        Returns:
            Response data including question ID and URL
        """
        if visualization_settings is None:
            visualization_settings = {}

        question_data = {
            "name": name,
            "dataset_query": {
                "type": "native",
                "native": {
                    "query": query
                },
                "database": self.database_id
            },
            "display": display,
            "visualization_settings": visualization_settings
        }

        response = requests.post(f"{self.base_url}/api/card", headers=self.headers, json=question_data)

        if response.status_code == 200:
            data = response.json()
            question_id = data.get('id')
            return {
                "success": True,
                "question_id": question_id,
                "question_url": f"{self.base_url}/question/{question_id}",
                "data": data
            }
        else:
            assert False, f"Error: {response.status_code} - {response.text}"