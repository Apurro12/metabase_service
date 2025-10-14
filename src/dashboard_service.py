import requests
from dotenv import load_dotenv
import os
from typing import List, Dict, Any

class DashboardService:
    def __init__(self, base_url: str = "http://localhost:3000"):
        load_dotenv()
        self.base_url = base_url
        self.headers = {
            'x-api-key': os.getenv("METABASE_API_KEY"),
            'Content-Type': 'application/json'
        }

    def create_dashboard(self, name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new dashboard in Metabase

        Args:
            name: Dashboard name
            description: Optional dashboard description

        Returns:
            Response data including dashboard ID and URL
        """
        dashboard_data = {
            "name": name,
            "description": description
        }

        response = requests.post(f"{self.base_url}/api/dashboard", headers=self.headers, json=dashboard_data)

        if response.status_code == 200:
            data = response.json()
            dashboard_id = data.get('id')
            return {
                "success": True,
                "dashboard_id": dashboard_id,
                "dashboard_url": f"{self.base_url}/dashboard/{dashboard_id}",
                "data": data
            }
        else:
            assert False, f"Error creating dashboard: {response.status_code} - {response.text}"

    def add_questions_to_dashboard(self, dashboard_id: int, question_ids: List[int]) -> Dict[str, Any]:
        """
        Add questions to a dashboard in a simple grid layout

        Args:
            dashboard_id: ID of the dashboard
            question_ids: List of question IDs to add

        Returns:
            Response data
        """
        cards = []

        # Simple layout: 2 cards per row, each card 12 units wide, 8 units tall
        card_width = 12
        card_height = 8
        cards_per_row = 2

        for i, question_id in enumerate(question_ids):
            row = i // cards_per_row
            col = i % cards_per_row

            card = {
                "id": question_id,
                "card_id": question_id,
                "col": col * card_width,
                "row": row * card_height,
                "size_x": card_width,
                "size_y": card_height
            }
            cards.append(card)

        payload = {"cards": cards}

        response = requests.put(
            f"{self.base_url}/api/dashboard/{dashboard_id}/cards",
            headers=self.headers,
            json=payload
        )

        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Added {len(question_ids)} questions to dashboard",
                "data": response.json()
            }
        else:
            assert False, f"Error adding cards to dashboard: {response.status_code} - {response.text}"

    def create_dashboard_with_questions(self, dashboard_name: str, question_ids: List[int]) -> Dict[str, Any]:
        """
        Create a dashboard and add questions to it in one operation

        Args:
            dashboard_name: Name for the new dashboard
            question_ids: List of question IDs to add to the dashboard

        Returns:
            Complete dashboard info with URL
        """
        # Create dashboard
        dashboard_result = self.create_dashboard(dashboard_name)
        dashboard_id = dashboard_result["dashboard_id"]

        # Add questions to dashboard
        cards_result = self.add_questions_to_dashboard(dashboard_id, question_ids)

        return {
            "success": True,
            "dashboard_id": dashboard_id,
            "dashboard_url": dashboard_result["dashboard_url"],
            "questions_added": len(question_ids),
            "dashboard_data": dashboard_result["data"],
            "cards_data": cards_result["data"]
        }