import sys
import requests
import json
import concurrent.futures
from colorama import init, Fore, Style

def print_header():
    header = r"""
                                                                
                                                                
$$\  $$\  $$\  $$$$$$\  $$\   $$\  $$$$$$$\  $$$$$$\   $$$$$$\  
$$ | $$ | $$ |$$  __$$\ $$ |  $$ |$$  _____|$$  __$$\ $$  __$$\ 
$$ | $$ | $$ |$$ /  $$ |$$ |  $$ |\$$$$$$\  $$$$$$$$ |$$ |  \__|
$$ | $$ | $$ |$$ |  $$ |$$ |  $$ | \____$$\ $$   ____|$$ |      
\$$$$$\$$$$  |$$$$$$$  |\$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      
 \_____\____/ $$  ____/  \______/ \_______/  \_______|\__|      
              $$ |                                              
              $$ |                                              
              \__|                                              
    """
    print(header)

def fetch_usernames(domain):
    api_url = f"{domain.rstrip('/')}/wp-json/wp/v2/users"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            try:
                users = response.json()
                if users:
                    domain_result = f"Domain: {domain}\n"
                    usernames = [f"Username: {user['slug']}\n" for user in users]
                    result = domain_result + ''.join(usernames)
                    return result, len(users)
            except json.JSONDecodeError:
                pass  # Ignore invalid JSON response
    except requests.exceptions.RequestException as e:
        pass  # Ignore API request errors

    return None, 0

def find_wordpress_usernames(file_path, max_workers):
    with open(file_path, 'r') as file:
        domain_list = file.read().splitlines()

    results = []
    found_counter = 0
    total_user_count = 0

    print("Running...")  # Display the "Running" notice

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {executor.submit(fetch_usernames, domain): domain for domain in domain_list}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            result, user_count = future.result()
            if result:
                found_counter += 1
                results.append(result)
                total_user_count += user_count

    with open('found-users.txt', 'w') as output_file:
        output_file.write('\n'.join(results))

    # Print the "Found" count in green color
    print(Fore.GREEN + f"Found: {total_user_count}" + Style.RESET_ALL)

# Initialize colorama
init()

# Print the header
print_header()

# Check if the file path and max_workers arguments are provided
if len(sys.argv) != 4 or sys.argv[1] != '-f':
    print('Usage: python script.py -f <file_path> <max_workers>')
else:
    file_path = sys.argv[2]
    max_workers = int(sys.argv[3])
    find_wordpress_usernames(file_path, max_workers)
