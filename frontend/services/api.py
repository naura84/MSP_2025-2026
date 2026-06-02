import requests
BASE_URL = "http://127.0.0.1:8000"

def login_request(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            params={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            return data["access_token"]
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None 
    
def history_request(token):
    try:
        if not token:
            print("No token provided for history request")
            return None

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/history", headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("history")
        else:
            print(f"Failed to retrieve history: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def scan_request(token, host):

    try:
        if not host:
            print("No host provided for scan request")
            return None

        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(f"{BASE_URL}/scan", headers=headers, params={"host": host})

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to perform scan: {response.status_code} - {response.text}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def pdf_request(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/report", headers=headers)

        if response.status_code == 200:
            with open("report.pdf", "wb") as f:
                f.write(response.content)
            print("PDF report downloaded successfully.")
        else:
            print(f"Failed to download PDF report: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")