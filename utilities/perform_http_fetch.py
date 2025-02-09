import requests

def perform_http_get(ip_address):
    url = f"http://{ip_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    ip_address = input("Enter the IP address: ")
    result = perform_http_get(ip_address)
    print(result)