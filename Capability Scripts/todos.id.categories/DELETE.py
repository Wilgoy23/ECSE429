import requests

# Undocumented
data = {
    "id": 1
    }
todo_id = "1"
response = requests.delete(f"http://localhost:4567/todos/{todo_id}/categories", json=data)

if response.status_code == 201:
    print("Response Data:", response.json())
print("Status Code:", response.status_code)

