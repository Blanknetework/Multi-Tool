import requests
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner_text = "IP Lookup Tool"
    created_by_text = "Created by: Jigsaww"
    additional_text = "Use this tool to look up IP addresses"
    max_length = max(len(banner_text), len(created_by_text), len(additional_text))
    border = "*" * (max_length + 4)
    
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"* {banner_text.center(max_length)} *")
    print(Fore.CYAN + f"* {created_by_text.center(max_length)} *")
    print(Fore.CYAN + f"* {additional_text.center(max_length)} *")
    print(Fore.CYAN + border)
    print()  

def ip_lookup():
    while True:
        print_banner()
        print(Fore.CYAN + "\nIP Lookup Tool")
        ip = input(Fore.YELLOW + "Enter the IP address (or type 'my' for your IP): ")
        if ip.lower() == "my":
            ip = requests.get("https://api64.ipify.org").text  # Get your public IP
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                data = response.json()
                print(Fore.GREEN + f"\nIP Address: {data['query']}")
                print(Fore.GREEN + f"City: {data['city']}")
                print(Fore.GREEN + f"Region: {data['regionName']}")
                print(Fore.GREEN + f"Country: {data['country']}")
                print(Fore.GREEN + f"ISP: {data['isp']}")
                print(Fore.GREEN + f"Latitude: {data['lat']}")
                print(Fore.GREEN + f"Longitude: {data['lon']}")
            else:
                print(Fore.RED + "Failed to retrieve data. Please try again.")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"An error occurred: {e}")

        # Ask the user if they want to try again
        choice = input(Fore.YELLOW + "\nDo you want to look up another IP address? (y/n): ").strip().lower()
        if choice != 'y':
            print(Fore.CYAN + "Exiting the IP Lookup Tool.")
            break

if __name__ == "__main__":
    ip_lookup()