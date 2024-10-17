import json
import os
import random
from datetime import datetime

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

# Function to create a test from random questions across years
def create_random_test(data, startyear, endyear, output_dir):
    # Ensure startyear and endyear are valid
    if startyear > endyear or str(startyear) not in data or str(endyear) not in data:
        print(f"Invalid year range: {startyear} to {endyear}")
        return

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    htmlOutputFiles = f"AMC_8_Random_Test_{startyear}_{endyear}_{timestamp}.html"

    # Prepare the HTML content for the test
    test_html_content = f"<html><body>\n<h1>AMC 8 Random Test, {htmlOutputFiles}</h1>\n"
    answer_key = []

    # Loop through the 25 questions, and pick a random one for each position
    for i in range(25):
        # Collect all possible questions for this position (i-th question) from each year
        possible_questions = []
        for year in range(startyear, endyear + 1):
            if str(year) in data:
                if i < len(data[str(year)]):
                    possible_questions.append((year, data[str(year)][i]))  # Store the year and the i-th question

        # Randomly select one question from the possible questions
        selected_year, selected_question = random.choice(possible_questions)

        # Add the selected question to the test
        h2 = selected_question['h2']
        paragraphs = ''.join(selected_question['paragraphs'])
        test_html_content += f"<p><h3>Problem {i + 1}</h3></p>{paragraphs}\n"
        test_html_content += f"<p><em>Selected from the year {selected_year}, Problem {i + 1}</em></p>\n<br>\n"

        # Add the answer to the answer key
        answer_key.append(f"Problem {i + 1} (from {selected_year}): {selected_question['answer']}")

    test_html_content += "</body></html>"

    # Save the test as a single HTML file with a timestamp in the filename
    test_file_path = os.path.join(output_dir, htmlOutputFiles)
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_html_content.replace('src="//latex', 'src="https://latex'))

    print(f"Random test generated and saved to {test_file_path}")

    # Save the answer key to a separate file with a timestamp in the filename
    answer_key_content = '\n'.join(answer_key)
    answer_key_file = os.path.join(output_dir, f"AMC_8_Random_Test_Answers_{startyear}_{endyear}_{timestamp}.txt")
    with open(answer_key_file, 'w', encoding='utf-8') as f:
        f.write(answer_key_content)

    print(f"Answer key saved to {answer_key_file}")

# Main function to load JSON and generate the random test
def main():
    json_file = "amc_8_problems_with_answers_1999_2024.json"  # Path to your JSON file
    output_dir = "amc_test_output"  # Directory to save the test and answer files

    # Load the data from the JSON file
    data = load_json(json_file)
    if data:
        # Example: Create a test from 1999 to 2024
        startyear = 1999
        endyear = 2018
        create_random_test(data, startyear, endyear, output_dir)

# Example usage
if __name__ == "__main__":
    main()
