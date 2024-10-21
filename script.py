import os
import requests
import csv
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {TOKEN}'}

def get_users():
    url = 'https://api.github.com/search/users?q=location:Tokyo+followers:>200&per_page=100'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  
    return response.json()['items']

def get_user_details(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_user_repositories(username):
    url = f'https://api.github.com/users/{username}/repos?per_page=500'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Write users.csv
def write_users_csv(users):
    with open('users.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        for user in users:
            writer.writerow([
                user['login'],
                user.get('name', ''),
                user['company'].strip().lstrip('@').upper() if user.get('company') else '',
                user.get('location', ''),
                user.get('email', ''),
                user.get('hireable', False),  
                user.get('bio', ''),
                user['public_repos'],
                user['followers'],
                user['following'],
                user['created_at']
            ])

def write_repositories_csv(repositories):
    with open('repositories.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
        for repo in repositories:
            writer.writerow([
                repo['owner']['login'],
                repo['full_name'],
                repo['created_at'],
                repo['stargazers_count'],
                repo['watchers_count'],
                repo.get('language', ''),  
                repo.get('has_projects', False),  
                repo.get('has_wiki', False), 
                repo['license']['key'] if repo.get('license') else ''  
            ])

def main():
    try:
        users = get_users()
        
        detailed_users = [get_user_details(user['login']) for user in users]
        
        repositories = [repo for user in detailed_users for repo in get_user_repositories(user['login'])]
        
        write_users_csv(detailed_users)
        write_repositories_csv(repositories)
        
        print("Data scraped successfully and written to users.csv and repositories.csv")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
