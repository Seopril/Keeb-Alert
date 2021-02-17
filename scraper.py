# Imports
import json
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup
import argparse


# Gets the HTML of the GB and IC Forums
# Returns a list with each entry being an html page
def get_html(thread_type):
    if thread_type == "gb":
        gb_page = requests.get(
            "https://geekhack.org/index.php?board=70.0;all"
        )
        print(f'GB Status Code: {gb_page.status_code}')
        gb_soup = BeautifulSoup(gb_page.content, "html.parser")
        pages = []
        pages.append(gb_soup)
        return pages
    elif thread_type == "ic":
        #Get the initial IC page
        ic_page = requests.get(
                f"https://geekhack.org/index.php?board=132.0"
            )
        #Parse IC Page
        ic_soup = BeautifulSoup(ic_page.content, "html.parser")
        # Get the nav bar with the page numbers (2, 3, 4, ..40)
        results = ic_soup.find_all("div", class_="pagelinks floatleft")

        # Create list to hold the possible page numbers
        page_numbers = []

        # Pull out all of the 'a' tags (ahref) in the divs
        for div in results:
            links = div.find_all('a')
            # Get the text of the link (2, 3, 4, etc) and add it as an integer to the list if it is a number (avoids >> and .. )
            for a in links:
                if a.text.isdigit():
                    page_numbers.append(int(a.text))
        # Finds the last page of the IC section
        max_page = max(page_numbers)
        
        # Creates a list to hold the html pages
        pages = []
        i = 0
        # Iterates over each page, downloads it, parses it, and adds it to the pages list. 
        while i <= max_page:
            page_number = (i - 1) * 50
            ic_page = requests.get(
                f"https://geekhack.org/index.php?board=132.{page_number}"
            )
            print(f'IC Status Code: https://geekhack.org/index.php?board=132.{page_number} --  {ic_page.status_code}')
            ic_soup = BeautifulSoup(ic_page.content, "html.parser")
            pages.append(ic_soup)
            i = i + 1

        return pages
    else:
        print("Thread Type Not Specified")


# Parses the HTML for all thread links.
def parse_html(pages):
    table_dict = {}
    td_tagged = []
    for html in pages:
        windowbg2 = html.find_all("td", class_="subject windowbg2")
        td_tagged.append(windowbg2)
    for item in td_tagged:
        for i in item:
            # Removes the phpsession id that gets added to the thread links.
            # PHPSESSID causes issues comparing the dicitonaries
            table_dict[re.sub('PHPSESSID=.{33}', '', i.a.get('href'))] = (i.a.text)

    print(table_dict)

    return table_dict


# Only tests the dictionary output
def test_dict(dictionary):
    for item, val in dictionary.items():
        print(item, "=>", val)


# Defines the baseline dictionary
def baseline(thread_type):
    table_dict = parse_html(get_html(thread_type))

    with open(f'{thread_type}_baseline.json', 'w') as baseline:
        json.dump(table_dict, baseline)


# Tests the baseline
def test_baseline(thread_type):
    with open(f'{thread_type}_baseline.json', 'r') as baseline:
        table_dict = json.load(baseline)
    for item, val in table_dict.items():
        print(item, "=>", val)


# Detects if a baseline exists
def detect_baseline(thread_type):
    baseline = Path(f'{thread_type}_baseline.json')
    if baseline.is_file():
        print(f'{thread_type} Baseline: True')
        return True
    else:
        print(f'{thread_type} Baseline: False')
        return False


# Compares the dictionaries to the baseline
def compare_dicts(table_dict, thread_type):
    print("=========================Compare=======================")
    with open(f'{thread_type}_baseline.json', 'r') as baseline:
        baseline_dict = json.load(baseline)
    new_items = dict(table_dict.items() - baseline_dict.items())
    print(len(new_items))
    for key, val in new_items.items():
        print(f"{val} ----> {key}")

    return new_items


# Updates the Baseline with new differences
def update_baseline(updates, thread_type):
    # Open the baseline.json file and load it into the baseline variable
    with open(f'{thread_type}_baseline.json') as f:
        baseline = json.load(f)

    # Add the updates dictionary into the baseline dictionary
    baseline.update(updates)

    # Write out the combined dictionary as a new baseline
    with open(f'{thread_type}_baseline.json', 'w') as f:
        json.dump(baseline, f)


def scrape(thread_type):
    # Establish Baseline
    baseline_exists = detect_baseline(thread_type)
    if baseline_exists:
        pass
        print(f'{thread_type} Baseline Exists')
    else:
        baseline(thread_type)
        test_baseline(thread_type)

    # Pull Updates
    thread_dict = get_html(thread_type)
    thread_dict = parse_html(thread_dict)

    # Test the dictionaries to make sure it was populated correctly
    test_dict(thread_dict)

    # Compare Updates to Baseline
    thread_updates = compare_dicts(thread_dict, thread_type)

    # Update Baseline With Changes
    update_baseline(thread_updates, thread_type)

    return thread_updates


def main(gb=None, ic=None):
    if gb:
        gb_updates = scrape('gb')
    if ic:
        ic_updates = scrape('ic')

    return dict(gb_updates), dict(ic_updates)


if __name__ == "__main__":
    main()
