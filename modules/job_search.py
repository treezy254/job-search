import re
import requests
from bs4 import BeautifulSoup
import logging

PRIORITY_DOMAINS = ['linkedin.com', 'indeed.com', 'glassdoor.com']

def search_jobs(query, location):
    url = f"https://www.google.com/search?q={query}+jobs+in+{location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_listings = []

    for result in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        title = result.get_text()
        link = result.find_parent('a')['href']
        snippet = result.find_next('div', class_='BNeawe s3v9rd AP7Wnd').get_text()
        job_listings.append({'title': title, 'link': link, 'snippet': snippet})

    return job_listings

def is_legitimate_job_site(url):
    legitimate_sites = ['linkedin.com', 'indeed.com', 'glassdoor.com']
    return any(site in url for site in legitimate_sites)

def extract_job_details(snippet):
    salary = "N/A"
    location = "N/A"

    salary_match = re.search(r"\$\d+(?:,\d+)?(?: - \$\d+(?:,\d+)?)?", snippet)
    if salary_match:
        salary = salary_match.group(0)

    location_match = re.search(r"(?:in|at) ([A-Za-z\s]+)", snippet)
    if location_match:
        location = location_match.group(1)

    return salary, location

def is_location_match(job_location, preferred_location):
    return preferred_location.lower() in job_location.lower()
