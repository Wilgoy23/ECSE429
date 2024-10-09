import requests

# OPTIONS a specific todo

response = requests.options(f"http://localhost:4567/todos")


print("Response Data:", response.headers)
print("Status Code:", response.status_code)

