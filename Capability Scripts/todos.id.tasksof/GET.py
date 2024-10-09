import requests

# GET a specific todo
todo_id = "1"  # Example ID
data = {
    "id": "1"
    }
response = requests.get(f"http://localhost:4567/todos/{todo_id}/tasksof")

print("Status Code:", response.status_code)
print("Response Data:", response.json())