import requests

# PUT a specific todo
data = {
    "title": "hello",
    "doneStatus": False,
    "description": "no"
    }
response = requests.put(f"http://localhost:4567/todos", json=data)

if response.status_code == 201:
    print("Response Data:", response.json())
print("Status Code:", response.status_code)
