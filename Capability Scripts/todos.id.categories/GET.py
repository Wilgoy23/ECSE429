import requests

# GET a specific todo
todo_id = "1"  # Example ID
data = {
    "id": "1"
    }
response = requests.get(f"http://localhost:4567/todos/{todo_id}/categories")

print("Status Code:", response.status_code)
print("Response Data:", response.json())