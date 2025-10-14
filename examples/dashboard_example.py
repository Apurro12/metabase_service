import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metabase_client import MetabaseClient
from src.dashboard_service import DashboardService

# Initialize services
client = MetabaseClient(database_id=1)
dashboard_service = DashboardService()

# Step 1: Create questions
questions = []

# Question 1
result1 = client.create_question(
    name="Accounts by Plan",
    query="""
    select "PLAN", count(*) as "count"
    from "PUBLIC"."ACCOUNTS"
    group by "PLAN"
    """
)
questions.append(result1['question_id'])
print(f"Created question 1: {result1['question_url']}")

# Question 2
result2 = client.create_question(
    name="Total Accounts",
    query='SELECT COUNT(*) FROM "PUBLIC"."ACCOUNTS"',
    display="scalar"
)
questions.append(result2['question_id'])
print(f"Created question 2: {result2['question_url']}")

# Question 3
result3 = client.create_question(
    name="Plan Distribution",
    query="""
    select "PLAN", count(*) as "total"
    from "PUBLIC"."ACCOUNTS"
    group by "PLAN"
    """,
    display="pie",
    visualization_settings={
        "pie.dimension": "PLAN",
        "pie.metric": "total"
    }
)
questions.append(result3['question_id'])
print(f"Created question 3: {result3['question_url']}")

# Step 2: Create dashboard with all questions
dashboard_result = dashboard_service.create_dashboard_with_questions(
    dashboard_name="dash 1",
    question_ids=questions
)

print(f"\nDashboard created successfully!")
print(f"Dashboard URL: {dashboard_result['dashboard_url']}")
print(f"Questions added: {dashboard_result['questions_added']}")