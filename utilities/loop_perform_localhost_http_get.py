import requests, time

def perform_http_get(ip_address):
    url = f"http://{ip_address}"
    print(f"Sending GET request to {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        pass
        return f"An error occurred: {e}"

if __name__ == "__main__":

    ip_address = "localhost:8000"

    while True:
        result = perform_http_get(ip_address)
        print(result)
        time.sleep(5)  # Wait for 1 second before sending another request