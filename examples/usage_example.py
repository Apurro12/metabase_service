import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metabase_client import MetabaseClient

# Initialize client
client = MetabaseClient(database_id=1)  # Adjust database_id as needed

# Example 1: Simple table query
result1 = client.create_question(
    name="All Accounts Sample",
    query="""
select "PLAN", count(*)
from "PUBLIC"."ACCOUNTS"
group by "PLAN"
"""
)
print(f"Created question: {result1['question_url']}")

# Example 2: Scalar/metric query
result2 = client.create_question(
    name="Total Accounts Count",
    query="""
select "PLAN", count(*)
from "PUBLIC"."ACCOUNTS"
group by "PLAN"
""",
    display="scalar"
)
print(f"Created metric: {result2['question_url']}")

# Example 3: Chart with custom visualization settings
result3 = client.create_question(
    name="apuquery",
    query="""
select "PLAN", count(*) "total"
from "PUBLIC"."ACCOUNTS"
group by "PLAN"
""",
    display="pie",
    visualization_settings={
        "pie.dimension": "PLAN",
        "pie.metric": "total"
    }
)
print(f"Created chart: {result3['question_url']}")