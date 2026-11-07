import sys
import requests
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

PER_PAGE = 100   # WordPress REST API maximum per request
MAX_PAGES = 50   # Safety limit: up to 5,000 users per site


def fetch_usernames(domain):
    base = domain.rstrip('/')
    if not base.startswith(('http://', 'https://')):
        base = f"https://{base}"
    api_url = f"{base}/wp-json/wp/v2/users"

    slugs = []
    page = 1
    try:
        while page <= MAX_PAGES:
            response = requests.get(
                api_url, params={'per_page': PER_PAGE, 'page': page}, timeout=10
            )
            if response.status_code != 200:
                break
            try:
                users = response.json()
            except ValueError:
                break  # Ignore invalid JSON response
            if not isinstance(users, list) or not users:
                break

            slugs.extend(user['slug'] for user in users if isinstance(user, dict) and user.get('slug'))

            total_pages = response.headers.get('X-WP-TotalPages')
            if len(users) < PER_PAGE or (total_pages and total_pages.isdigit() and page >= int(total_pages)):
                break
            page += 1
    except requests.exceptions.RequestException:
        pass  # Ignore API request errors; keep whatever pages were fetched

    if slugs:
        domain_result = f"Domain: {domain}\n"
        usernames = [f"Username: {slug}\n" for slug in slugs]
        return domain_result + ''.join(usernames), len(slugs)

    return None, 0

def find_wordpress_usernames(file_path, max_workers):
    with open(file_path, 'r') as file:
        domain_list = [line.strip() for line in file if line.strip()]

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
    print(Fore.GREEN + f"Found: {total_user_count} user(s) on {found_counter} site(s)" + Style.RESET_ALL)


if __name__ == '__main__':
    # Initialize colorama
    init()

    # Print the header
    print_header()

    # Check if the file path and max_workers arguments are provided
    if len(sys.argv) != 4 or sys.argv[1] != '-f':
        print('Usage: python3 wpuser.py -f <file_path> <threads>')
        sys.exit(1)

    file_path = sys.argv[2]
    try:
        max_workers = int(sys.argv[3])
        if max_workers < 1:
            raise ValueError
    except ValueError:
        print('Error: <threads> must be a positive whole number, e.g. 20')
        sys.exit(1)

    find_wordpress_usernames(file_path, max_workers)
