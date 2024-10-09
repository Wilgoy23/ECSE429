import requests

# HEAD a specific todo
todo_id = "1"
categories_id = "1"
response = requests.head(f"http://localhost:4567/todos/{todo_id}/categories/{categories_id}")

status = response.status_code

print("Response Data:", response.headers)
print("Status Code:", response.status_code)

