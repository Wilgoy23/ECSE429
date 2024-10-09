import requests

# GET a specific todo
response = requests.get(f"http://localhost:4567/todos")

print("Status Code:", response.status_code)
print("Response Data:", response.json())