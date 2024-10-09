import requests

# OPTIONS a specific todo
todo_id = "1"
response = requests.options(f"http://localhost:4567/todos/{todo_id}/categories")


print("Response Data:", response.headers)
print("Status Code:", response.status_code)

