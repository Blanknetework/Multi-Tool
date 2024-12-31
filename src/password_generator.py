import random
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner_text = "Password Generator Tool"
    created_by_text = "Created by: Jigsaww"
    additional_text = "Use this tool to generate secure passwords"
    max_length = max(len(banner_text), len(created_by_text), len(additional_text))
    border = "*" * (max_length + 4)
    
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"* {banner_text.center(max_length)} *")
    print(Fore.CYAN + f"* {created_by_text.center(max_length)} *")
    print(Fore.CYAN + f"* {additional_text.center(max_length)} *")
    print(Fore.CYAN + border)
    print()  

def password_generator():
    print_banner()
    print(Fore.CYAN + "\nPassword Generator Tool")
    length = int(input(Fore.YELLOW + "Enter the length of the password: "))
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
    password = ''.join(random.choice(chars) for _ in range(length))
    print(Fore.GREEN + f"Generated Password: {password}")
    
    while True:
        try_again = input(Fore.CYAN + "Do you want to generate another password? (Yes/No): ")
        if try_again.lower() == "yes":
            password = ''.join(random.choice(chars) for _ in range(length))
            print(Fore.GREEN + f"Generated Password: {password}")
            
        else:
            print(Fore.RED + "Exiting...")
            break
    

if __name__ == "__main__":
    password_generator()