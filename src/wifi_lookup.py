import subprocess
import re
import platform
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner_text = "WiFi Lookup Tool"
    created_by_text = "Created by: Jigsaww"
    additional_text = "Use this tool to scan and view WiFi network details"
    max_length = max(len(banner_text), len(created_by_text), len(additional_text))
    border = "*" * (max_length + 4)
    
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"* {banner_text.center(max_length)} *")
    print(Fore.CYAN + f"* {created_by_text.center(max_length)} *")
    print(Fore.CYAN + f"* {additional_text.center(max_length)} *")
    print(Fore.CYAN + border)
    print()
    

def scan_wifi_networks():
    print_banner()
    print(Fore.CYAN + "\nScanning for available WiFi networks...")
    networks = []
    
    try:
        os_type = platform.system()
        if os_type == "Linux":
            # For Linux
            result = subprocess.run(["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"], capture_output=True, text=True)
        elif os_type == "Windows":
            # For Windows
            result = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True)
        else:
            print(Fore.RED + "Unsupported operating system.")
            return

        if result.returncode == 0:
            networks = result.stdout.strip().split('\n')
            network_list = []

            if os_type == "Linux":
                # Parse networks on Linux
                for network in networks:
                    ssid, signal = network.split(':')
                    network_list.append({'SSID': ssid, 'Signal': signal})
                    print(Fore.GREEN + f"{len(network_list)}. SSID: {ssid}, Signal Strength: {signal} dBm")
            elif os_type == "Windows":
                # Parse networks on Windows
                count = 1
                for network in networks:
                    if "SSID" in network:
                        ssid = re.search(r": (.+)", network)
                        if ssid:
                            network_list.append({'SSID': ssid.group(1)})
                            print(Fore.GREEN + f"{count}. SSID: {ssid.group(1)}")
                            count += 1

            # Let user select a network by number
            if len(network_list) == 0:
                print(Fore.RED + "No networks found.")
                return

            print(Fore.YELLOW + "\nSelect a network by entering the number (e.g., 1, 2, 3):")
            try:
                selected_index = int(input()) - 1
                if 0 <= selected_index < len(network_list):
                    selected_ssid = network_list[selected_index]['SSID']
                    print(Fore.CYAN + f"\nSelected network: {selected_ssid}")
                    next_action(selected_ssid, network_list)
                else:
                    print(Fore.RED + "Invalid number selected.")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number.")
        else:
            print(Fore.RED + "Failed to scan WiFi networks.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

def next_action(selected_ssid, network_list):
    """Function to handle next actions after network details are shown."""
    while True:
        print(Fore.YELLOW + "\nWhat would you like to do next?")
        print("1. Show network details.")
        print("2. Show connection details.")
        print("3. View details of another network.")
        print("4. Exit.")
        
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            show_network_details(selected_ssid)
        elif choice == "2":
            show_connection_details(selected_ssid)
        elif choice == "3":
            # Let the user choose a different network
            print("\nSelect a network by number:")
            for idx, network in enumerate(network_list, 1):
                print(f"{idx}. {network['SSID']}")
            
            try:
                selected_index = int(input()) - 1
                if 0 <= selected_index < len(network_list):
                    selected_ssid = network_list[selected_index]['SSID']
                    print(Fore.CYAN + f"\nSelected network: {selected_ssid}")
                    next_action(selected_ssid, network_list)
                else:
                    print(Fore.RED + "Invalid number selected.")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number.")
        
        elif choice == "4":
            print(Fore.CYAN + "Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number between 1 and 4.")

def show_network_details(ssid):
    """Show details of the selected WiFi network."""
    try:
        os_type = platform.system()
        if os_type == "Linux":
            # For Linux, get detailed network info using nmcli
            print(Fore.CYAN + f"Fetching details for {ssid}...")
            result = subprocess.run(["nmcli", "-f", "SSID,SECURITY,SSID-BROADCAST", "device", "wifi", "list"], capture_output=True, text=True)
            if result.returncode == 0:
                # Parse the output and show relevant information
                for line in result.stdout.strip().split("\n"):
                    if ssid in line:
                        encryption = re.search(r"SECURITY: (.+)", line)
                        broadcast = re.search(r"SSID-BROADCAST: (.+)", line)
                        encryption_type = encryption.group(1) if encryption else "Unknown"
                        broadcast_status = broadcast.group(1) if broadcast else "Unknown"
                        
                        # Check for vulnerabilities (e.g., weak encryption like WEP or WPA)
                        known_vulnerabilities = "None"
                        if "WEP" in encryption_type:
                            known_vulnerabilities = "WEP (Weak Security)"
                        elif "WPA" in encryption_type and "TKIP" in encryption_type:
                            known_vulnerabilities = "WPA with TKIP (Weak Security)"
                        
                        # Attempt to fetch the password (if possible, with proper permissions)
                        password = "NA"
                        try:
                            result_password = subprocess.run(
                                ["sudo", "nmcli", "-s", "device", "wifi", "show-password", "ifname", "wlan0", "ssid", ssid], 
                                capture_output=True, text=True
                            )
                            if result_password.returncode == 0:
                                password = result_password.stdout.strip()
                            else:
                                password = "NA"
                        except Exception:
                            password = "NA"

                        print(Fore.GREEN + f"Details for {ssid}:")
                        print(f"Encryption: {encryption_type}")
                        print(f"SSID Broadcast: {broadcast_status}")
                        print(f"Known Vulnerabilities: {known_vulnerabilities}")
                        print(f"Password: {password}")

        elif os_type == "Windows":
            # For Windows, use netsh to show network details
            print(Fore.CYAN + f"Fetching details for {ssid}...")
            result = subprocess.run(["netsh", "wlan", "show", "network", "name=" + ssid], capture_output=True, text=True)
            if result.returncode == 0:
                # Check for encryption (WPA, WPA2, etc.)
                encryption = re.search(r"Encryption\s*:\s*(.+)", result.stdout)
                broadcast = re.search(r"SSID\s*:\s*(\S+)", result.stdout)
                
                encryption_type = encryption.group(1) if encryption else "Unknown"
                ssid_broadcast = "Yes" if broadcast else "No"
                
                # Check for vulnerabilities (weak encryption)
                known_vulnerabilities = "None"
                if "WEP" in encryption_type:
                    known_vulnerabilities = "WEP (Weak Security)"
                elif "WPA" in encryption_type and "TKIP" in encryption_type:
                    known_vulnerabilities = "WPA with TKIP (Weak Security)"
                
                # Attempt to fetch the password (if possible, with proper permissions)
                password = "NA"
                try:
                    result_password = subprocess.run(
                        ["netsh", "wlan", "show", "profile", ssid, "key=clear"], capture_output=True, text=True
                    )
                    if result_password.returncode == 0:
                        password_match = re.search(r"Key Content\s*:\s*(.+)", result_password.stdout)
                        if password_match:
                            password = password_match.group(1)
                        else:
                            password = "NA"
                except Exception:
                    password = "NA"
                
                print(Fore.GREEN + f"Details for {ssid}:")
                print(f"Encryption: {encryption_type}")
                print(f"SSID Broadcast: {ssid_broadcast}")
                print(f"Known Vulnerabilities: {known_vulnerabilities}")
                print(f"Password: {password}")

        else:
            print(Fore.RED + "Unsupported operating system for showing network details.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while showing network details: {e}")

def show_connection_details(ssid):
    """Show connection details for the selected network."""
    try:
        os_type = platform.system()
        if os_type == "Linux":
            # For Linux, get connection info using nmcli
            print(Fore.CYAN + f"Fetching connection details for {ssid}...")
            result = subprocess.run(["nmcli", "-t", "-f", "ACTIVE,SSID,IP4.ADDRESS,IP4.GATEWAY,IP4.DNS,SIGNAL", "dev", "wifi"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if ssid in line:
                        active, ssid_result, ip_address, gateway, dns_servers, signal = line.split(":")
                        if active == "yes":
                            status = "Connected"
                        else:
                            status = "Not Connected"
                        
                        # Print connection details
                        print(Fore.GREEN + f"Connection Details for {ssid}:")
                        print(f"Status: {status}")
                        print(f"IP Address: {ip_address}")
                        print(f"Gateway: {gateway}")
                        print(f"DNS Servers: {dns_servers if dns_servers != 'None' else 'Unknown'}")
                        print(f"Signal Strength: {signal} dBm")

        elif os_type == "Windows":
            # For Windows, get connection details using netsh
            print(Fore.CYAN + f"Fetching connection details for {ssid}...")
            result = subprocess.run(["netsh", "interface", "ipv4", "show", "addresses"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                status = "Not Connected"
                ip_address = gateway = dns_servers = "Unknown"
                connection_speed = "Unknown"
                for line in lines:
                    if "IP Address" in line:
                        ip_address_match = re.search(r"IP Address:\s*(\S+)", line)
                        if ip_address_match:
                            ip_address = ip_address_match.group(1)
                    elif "Default Gateway" in line:
                        gateway_match = re.search(r"Default Gateway:\s*(\S+)", line)
                        if gateway_match:
                            gateway = gateway_match.group(1)
                    elif "DNS Servers" in line:
                        dns_servers_match = re.search(r"DNS Servers\s*:\s*(.+)", line)
                        if dns_servers_match:
                            dns_servers = dns_servers_match.group(1)
                
                # Check Wi-Fi connection status (using netsh wlan show interfaces)
                result_status = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
                if result_status.returncode == 0:
                    for line in result_status.stdout.strip().split("\n"):
                        if "State" in line:
                            connection_state_match = re.search(r"State\s*:\s*(\S+)", line)
                            if connection_state_match and connection_state_match.group(1) == "connected":
                                status = "Connected"
                
                # Fetching the connection speed (e.g., using netsh)
                result_speed = subprocess.run(
                    ["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True
                )
                if result_speed.returncode == 0:
                    for line in result_speed.stdout.strip().split("\n"):
                        if "Receive rate" in line:
                            connection_speed_match = re.search(r"Receive rate\s*:\s*(\S+)", line)
                            if connection_speed_match:
                                connection_speed = connection_speed_match.group(1)

                print(Fore.GREEN + f"Connection Details for {ssid}:")
                print(f"Status: {status}")
                print(f"IP Address: {ip_address}")
                print(f"Gateway: {gateway}")
                print(f"DNS Servers: {dns_servers}")
                print(f"Connection Speed: {connection_speed}")

        else:
            print(Fore.RED + "Unsupported operating system for showing connection details.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while showing connection details: {e}")


if __name__ == "__main__":
    scan_wifi_networks()