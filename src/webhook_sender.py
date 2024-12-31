import requests
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner_text = "Webhook Sender Tool"
    created_by_text = "Created by: Jigsaww"
    additional_text = "Use this tool to send webhooks easily"
    max_length = max(len(banner_text), len(created_by_text), len(additional_text))
    border = "*" * (max_length + 4)
    
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"* {banner_text.center(max_length)} *")
    print()
    print(Fore.CYAN + f"* {created_by_text.center(max_length)} *")
    print()
    print(Fore.CYAN + f"* {additional_text.center(max_length)} *")
    print(Fore.CYAN + border)
    print()  # Add a space after the banner

def send_webhook():
    print_banner()
    url = input(Fore.YELLOW + "Enter the webhook URL: ")
    payload_str = input(Fore.YELLOW + "Enter the payload (in JSON format): ")
    
    try:
        # Parse the JSON payload
        payload = json.loads(payload_str)
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(Fore.GREEN + "Webhook sent successfully!")
        else:
            print(Fore.RED + f"Failed to send webhook. Status code: {response.status_code}")
            print(Fore.RED + f"Response: {response.text}")
    except json.JSONDecodeError:
        print(Fore.RED + "Invalid JSON format. Please enter a valid JSON payload.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"An error occurred: {e}")

if __name__ == "__main__":
    send_webhook()