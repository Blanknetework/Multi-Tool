import wifi_lookup
import ip_lookup
import webhook_sender
import password_generator
import wifi_brute_force
import shutil
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    terminal_width = shutil.get_terminal_size().columns
    banner_text = [
        r" __  __ _    _ _   _______ _____            _______ ____   ____  _      ",
        r"|  \/  | |  | | | |__   __|_   _|          |__   __/ __ \ / __ \| |     ",
        r"| \  / | |  | | |    | |    | |    ______     | | | |  | | |  | | |     ",
        r"| |\/| | |  | | |    | |    | |   |______|    | | | |  | | |  | | |     ",
        r"| |  | | |__| | |____| |   _| |_              | | | |__| | |__| | |____ ",
        r"|_|  |_|\____/|______|_|  |_____|             |_|  \____/ \____/|______|",
    ]
    created_by_text = "Created by: Jigsaww"
    
    # Ensure banner width is between 40 and terminal width
    banner_width = max(40, min(terminal_width - 4, 120))
    border = "+" + "-" * (banner_width - 2) + "+"
    
    
   # Center the text within the banner
    banner_lines = [border]
    for line in banner_text:
        if len(line) > banner_width - 2:
            # Truncate the line if it's too long
            line = line[:banner_width - 2]
        banner_lines.append("|" + line.center(banner_width - 2) + "|")
    banner_lines.append("|" + " " * (banner_width - 2) + "|")
    banner_lines.append("|" + created_by_text.center(banner_width - 2) + "|")
    banner_lines.append("|" + " " * (banner_width - 2) + "|")
    banner_lines.append(border)
    
    
    # Print the banner
    for line in banner_lines:
        print(Fore.CYAN + line)
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