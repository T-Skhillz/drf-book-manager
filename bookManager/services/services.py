import requests

base_url = 'http://127.0.0.1:8000'
protected_path = '/api/books/'
auth_path = '/auth/token/login/'

login_details = {
    "username" : "bolu",
    "password" : "435",
}

context = {
    "title" : "The Client",
    "author" : "John Grisham",
    "completed" : False,
}

CONNECT_TIMEOUT = 4
READ_TIMEOUT = 5

try:
    response_post = requests.post(f"{base_url}{auth_path}", timeout=(CONNECT_TIMEOUT, READ_TIMEOUT), json=login_details)
    response_post.raise_for_status()
    data = response_post.json()
    auth_token = data.get("auth_token")
    print(f"Token: {auth_token}")
except requests.exceptions.ConnectTimeout:
    print("Connection Timeout")
except requests.exceptions.ReadTimeout:
    print("Read Timeout")
except requests.exceptions.JSONDecodeError:
    print("JOSN data could not be decoded.")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")

try:
    auth_header = {
        "Authorization" : f"Token {auth_token}"
    }
    response_get = requests.get(f"{base_url}{protected_path}", timeout=(CONNECT_TIMEOUT, READ_TIMEOUT), headers=auth_header)
    response_get.raise_for_status()
    data = response_get.json()
    print(data)

    deleted_data = {"id" : 7}
    response_delete = requests.post(f"{base_url}{protected_path}", timeout=(CONNECT_TIMEOUT, READ_TIMEOUT), headers=auth_header, data=context)
    new_data = response_delete.json()
    print(f"New Data: {new_data}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.ConnectTimeout:
    print("Connection Timeout")
except requests.exceptions.ReadTimeout:
    print("Read Timeout")
except requests.exceptions.JSONDecodeError:
    print("JOSN data could not be decoded.")
    
