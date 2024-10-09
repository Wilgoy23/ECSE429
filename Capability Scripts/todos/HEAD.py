import requests

# HEAD a specific todo
response = requests.head(f"http://localhost:4567/todos")

status = response.status_code

print("Response Data:", response.headers)
print("Status Code:", response.status_code)

