from pymongo import MongoClient
import pandas as pd

# Step 1: Connect to MongoDB
client = MongoClient("localhost", 27017) # Replace with your MongoDB URI if necessary
db = client["job_forecast"]  # Replace with your database name
collection = db["hh_ru_jobs"]  # Replace with your collection name

# Step 2: Fetch the required fields from MongoDB
# Use projection to fetch only the necessary fields
data = list(collection.find( {},{
    "name": 1,
    "area.name": 1,
    "salary.from": 1,
    "salary.to": 1,
    "url": 1,
    "employer.name": 1,
    "schedule.id": 1,
    "working_days.id": 1,
    "working_time_intervals.id": 1,
    "working_time_modes.id": 1,
    "professional_roles.name": 1,
    "experience.id": 1,
    "employment.id": 1,
    "entry_date": 1,
    "area_name": 1
}))

processed_data = []
for doc in data:
    processed_doc = {
        "name": doc.get("name"),
        "city": doc.get("area", {}).get("name"),
        "area_name": doc.get("area_name"),
        "salary_from": doc.get("salary", {}).get("from"),
        "salary_to": doc.get("salary", {}).get("to"),
        "url": doc.get("url"),
        "employer_name": doc.get("employer", {}).get("name"),
        "schedule_id": doc.get("schedule", {}).get("id"),
        "working_days_id": doc.get("working_days", [{}])[0].get("id") if doc.get("working_days") else None,
        "working_time_intervals_id": doc.get("working_time_intervals", [{}])[0].get("id") if doc.get("working_time_intervals") else None,
        "working_time_modes_id": doc.get("working_time_modes", [{}])[0].get("id") if doc.get("working_time_modes") else None,
        "professional_roles_name": doc.get("professional_roles", [{}])[0].get("name") if doc.get("professional_roles") else None,
        "experience_id": doc.get("experience", {}).get("id"),
        "employment_id": doc.get("employment", {}).get("id"),
        "entry_date": doc.get("entry_date")
    }
    processed_data.append(processed_doc)

# Step 4: Convert to pandas DataFrame
df = pd.DataFrame(processed_data)
df.to_csv('all_jobs.csv')




