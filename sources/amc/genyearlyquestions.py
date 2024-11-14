import json
import os

# Function to load the saved JSON file
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        return None

# Function to generate a single HTML file for a given year
def generate_html_for_year(data, year, output_dir):
    # Check if the year exists in the data
    if str(year) not in data:
        print(f"No data available for year {year}")
        return

    # Create the output directory if it doesn't exist
    year_dir = os.path.join(output_dir, str(year))
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    # Get the questions for the given year
    questions = data[str(year)]
    answer_key = []
    
    # Prepare the HTML content
    html_content = "<html><body>\n"
    
    # Loop through the questions and accumulate HTML content
    for i, question in enumerate(questions):
        question_id = question['id']
        h2 = question['h2']
        paragraphs = ''.join(question['paragraphs'])  # Concatenate the <p> elements
        answer = question['answer']
        answer_key.append(f"Problem {i + 1}: {answer}")

        # Add the question to the HTML content
        html_content += f"{h2}\n{paragraphs}\n<br>\n"

    html_content += "</body></html>"

    # Save all questions as a single HTML file
    html_file_path = os.path.join(year_dir, f"{year}_AMC_8_Problems.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content.replace('src="//latex', 'src="https://latex'))
    
    print(f"All questions for year {year} saved to {html_file_path}")

    # Save the answer key to a separate file
    answer_key_content = '\n'.join(answer_key)
    answer_key_file = os.path.join(year_dir, "answer_key.txt")
    with open(answer_key_file, 'w', encoding='utf-8') as f:
        f.write(answer_key_content)
    
    print(f"Answer key saved to {answer_key_file}")

# Main function to load JSON and generate HTML files for a given year
def main():
    json_file = "amc_8_problems_with_answers_1999_2024.json"  # Path to your JSON file
    output_dir = "amc_html_output"  # Directory to save the HTML files

    # Load the data from the JSON file
    data = load_json(json_file)
    if data:
        # Specify the year for which you want to generate the HTML file
        year = 2020  # Change this to any year you want to process
        generate_html_for_year(data, year, output_dir)

# Example usage
if __name__ == "__main__":
    main()
