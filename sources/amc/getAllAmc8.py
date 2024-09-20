import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

# Function to fetch the URL content
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors in the response
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Function to extract <h2> and following <p> elements
def extract_elements(html):
    soup = BeautifulSoup(html, 'html.parser')
    h2_elements = soup.find_all('h2')
    
    extracted_data = []
    
    for h2 in h2_elements:
        # Get the <span> inside the <h2> and extract its id
        span = h2.find('span')
        if not span or not span.get('id'):
            continue  # Skip if no <span> with an id is found
        
        h2_id = span.get('id')  # Use the id of the <span>        
        
        print(h2_id)
        p_elements = []
        
        # Find all the following <p> elements after the <h2>
        sibling = h2.find_next_sibling()
        while sibling:
            if sibling.name == 'p':
                p_elements.append(sibling)
            else: 
                break
            sibling = sibling.find_next_sibling()
        
        # Only add if there are any <p> elements
        if p_elements:
            extracted_data.append((h2_id, h2, p_elements))
    
    return extracted_data

# Function to save each <h2> and <p> elements as an HTML file
def save_to_html(elements, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for h2_id, h2, p_elements in elements:
        file_name = f"{h2_id}.html"  # Use the <h2> id as the file name
        file_path = os.path.join(directory, file_name)
        
        # Create HTML content by concatenating h2 and p elements
        html_content = f"<html><body>\n{str(h2)}\n"
        for p in p_elements:
            html_content += f"{str(p)}\n"
        html_content += "</body></html>"
        
        # Perform the string replacement
        html_content = html_content.replace('src="//latex', 'src="https://latex')
        
        # Save the modified HTML content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Saved: {file_name}")

def get_last_part_of_url(url):
    path = urlparse(url).path
    return os.path.basename(path)

# Main script logic
def main(urls):
    for url in urls:
        print(f"Processing URL: {url}")
        html_content = fetch_html(url)
        if html_content:
            directory = get_last_part_of_url(url)  # Extract the last part of the URL for the directory name
            elements = extract_elements(html_content)
            save_to_html(elements, directory)
        else:
            print(f"Failed to retrieve content from {url}")

# Function to generate URLs for AMC 8 Problems from 1999 to 2024
def generate_urls(start_year=1999, end_year=2024):
    base_url = "https://artofproblemsolving.com/wiki/index.php/"
    urls = []
    for year in range(start_year, end_year + 1):
        url = f"{base_url}{year}_AMC_8_Problems"
        urls.append(url)
    return urls


main(generate_urls())
