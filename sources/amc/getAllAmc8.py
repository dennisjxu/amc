import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import json

# Example answer key object (replace with your actual amc_answer_keys object)
def extract_ordered_list(url):
    # Fetch the HTML content from the given URL
    response = requests.get(url)
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first ordered list (<ol>)
    ordered_list = soup.find('ol')

    # Check if an ordered list exists
    if ordered_list:
        # Extract the list items (<li>) from the ordered list
        items = ordered_list.find_all('li')
        return [item.text for item in items]
    else:
        return []

def get_amc_answer_keys(start_year=1999, end_year=2024):
    amc_keys = {}
    
    for year in range(start_year, end_year + 1):
        # Generate the URL
        url = f'https://artofproblemsolving.com/wiki/index.php/{year}_AMC_8_Answer_Key'
        print(f"Fetching data for {year}...")

        # Extract the answer key
        answers = extract_ordered_list(url)
        
        # If answers were found, add them to the dictionary
        if answers:
            amc_keys[year] = answers
        else:
            amc_keys[year] = "No data available"
    
    return amc_keys

# Fetch the answer keys from 1999 to 2024
amc_answer_keys = get_amc_answer_keys()

# Function to fetch the URL content
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors in the response
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Function to extract <h2> and all following <p> elements
def extract_elements(html, year):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the main content div with class "mw-parser-output"
    main_content = soup.find("div", class_="mw-parser-output")
    if not main_content:
        print(f"Could not find content in {url}")
        return []
    
    questions = []
    
    question_number = 1  # Initialize question number
    for h2 in main_content.find_all(['h2', 'h3']):
        # Get the <span> inside the <h2> and extract its id
        span = h2.find('span')
        if not span or not span.get('id'):
            continue  # Skip if no <span> with an id is found
        
        span_id = span.get('id')  # Use the id of the <span>
        if "Problem_".lower() not in span_id.lower(): 
            print(f"unrecognized problem {span_id}")
            continue
        
        p_elements = []
        
        # Find all the following <p> elements after the <h2>
        sibling = h2.find_next_sibling()
        while sibling:
            if not sibling.name.startswith('h') : 
                p_elements.append(str(sibling).replace('src="//latex', 'src="https://latex'))  # Save p elements as strings
            else: 
                break
            sibling = sibling.find_next_sibling()
        
        # Only add if there are any <p> elements
        if p_elements:
            answer_key = amc_answer_keys.get(year, [])[question_number - 1] if year in amc_answer_keys else None
            question = {
                "id": span_id,
                "h2": str(h2),  # Save h2 as string
                "paragraphs": p_elements,
                "answer": answer_key  # Add the corresponding answer key
            }
            questions.append(question)
        
        question_number += 1  # Increment question number
        if question_number > 25: 
            break
    
    if question_number != 26: 
        print(f"Error found during extract. found {question_number} problems")

    return questions

# Function to generate URLs for AMC 8 Problems from 1999 to 2024
def generate_urls(start_year=1999, end_year=2024):
    base_url = "https://artofproblemsolving.com/wiki/index.php/"
    urls = {}
    for year in range(start_year, end_year + 1):
        url = f"{base_url}{year}_AMC_8_Problems"
        urls[year] = url
    return urls

# Main script logic to process all URLs and save as JSON
def main():
    # Generate URLs from 1999 to 2024
    urls = generate_urls(1999, 2024)
    
    # Dictionary to store all years and their questions
    data = {}
    
    # Loop through each year and URL
    for year, url in urls.items():
        print(f"Processing {year} AMC 8 Problems from URL: {url}")
        html_content = fetch_html(url)
        if html_content:
            questions = extract_elements(html_content, year)
            if questions:
                data[year] = questions  # Store questions by year
        else:
            print(f"Failed to retrieve content from {url}")
    
    # Save all data to a JSON file
    output_file = "amc_8_problems_with_answers_1999_2024.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {output_file}")

main()
