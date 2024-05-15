import requests

JAWCE_URL = "http://localhost:8080/webhook"


def get_data_from_session(user: str, data_key: str = None):
    response = requests.get(JAWCE_URL + "/session/" + user + "/" + data_key)

    if response.status_code == 200:
        return response.json().get("data")

    raise Exception("Failed to get session data")


def save_session_data(user: str, data_key: str, data):
    requests.post(JAWCE_URL + "/session/", data={"user": user, "key": data_key, "data": data})
