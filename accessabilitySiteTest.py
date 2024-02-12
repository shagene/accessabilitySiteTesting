from selenium import webdriver
from axe_selenium_python import Axe
import pprint
import json
import csv
import re

def ensure_protocol(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://' + url
    return url

def process_url(url):
    url = ensure_protocol(url)
    driver = webdriver.Chrome()  # Replace 'Chrome' with your desired browser
    driver.get(url)

    axe = Axe(driver)
    axe.inject()  # Inject axe-core into the browser page

    results = axe.run()
    driver.quit()

    pprint.pprint(results['violations'])

    # Extract domain name for the output file name
    domain_name = re.findall('(?:http[s]*://)?([^/]+)', url)[0]
    domain_name = domain_name.replace("www.", "").split('.')[0]  # Remove 'www.' and get the domain name
    file_name = f"{domain_name}_output.json"
    with open(file_name, 'w') as f:
        json.dump(results['violations'], f, indent=4)
    print(f"Output saved to {file_name}")

def get_input_type():
    while True:
        input_type = input("Do you want to input a single URL or a CSV file? (url/csv): ").lower()
        if input_type in ['url', 'csv']:
            return input_type
        else:
            print("Invalid input. Please type 'url' for a single URL or 'csv' for a CSV file.")

input_type = get_input_type()

if input_type == 'url':
    url = input("Please enter the URL: ")
    process_url(url)
elif input_type == 'csv':
    try:
        with open('urls.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                url = row[0]
                print(f"Processing URL: {url}")
                process_url(url)
    except FileNotFoundError:
        print("The file 'urls.csv' was not found.")
