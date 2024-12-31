import wifi_lookup
import ip_lookup
import webhook_sender
import password_generator
import wifi_brute_force
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = r"""
+----------------------------------------------------------------------------+
|                                                                            |
|  __  __ _    _ _   _______ _____            _______ ____   ____  _         |
| |  \/  | |  | | | |__   __|_   _|          |__   __/ __ \ / __ \| |        |
| | \  / | |  | | |    | |    | |    ______     | | | |  | | |  | | |        |
| | |\/| | |  | | |    | |    | |   |______|    | | | |  | | |  | | |        |
| | |  | | |__| | |____| |   _| |_              | | | |__| | |__| | |____    |
| |_|  |_|\____/|______|_|  |_____|             |_|  \____/ \____/|______|   |
|                                                                            |
|                            MULTI-TOOL                                      |
|                                                                            |
|                            Created by: Jigsaww                             |
|                                                                            |
+----------------------------------------------------------------------------+
    """
    print(Fore.CYAN + banner)
    print(Style.RESET_ALL)

def main_menu():
    while True:
        print_banner()
        print(Fore.CYAN + "Select an option:")
        print(Fore.CYAN + "1. WiFi Lookup")
        print(Fore.CYAN + "2. IP Lookup")
        print(Fore.CYAN + "3. Webhook Sender")
        print(Fore.CYAN + "4. Password Generator")
        print(Fore.CYAN + "5. WiFi Brute Force")
        print(Fore.CYAN + "6. Exit")

        choice = input(Fore.YELLOW + "Enter your choice (1-6): ")

        if choice == '1':
            wifi_lookup.scan_wifi_networks()
        elif choice == '2':
            ip_lookup.ip_lookup()
        elif choice == '3':
            webhook_sender.send_webhook()
        elif choice == '4':
            password_generator.password_generator()
        elif choice == '5':
            wifi_brute_force.main()
        elif choice == '6':
            print(Fore.RED + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()