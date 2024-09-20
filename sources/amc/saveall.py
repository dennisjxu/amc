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

# Function to generate a single HTML file for all years and a separate answer key file
def generate_html_for_all_years(data, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare the HTML content
    html_content = "<html><body>\n"
    answer_key = []

    # Loop through each year from 1999 to 2024
    for year in range(1999, 2025):
        if str(year) in data:
            questions = data[str(year)]
            html_content += f"<h1>{year} AMC 8 Problems</h1>\n"

            # Loop through the questions for each year
            for i, question in enumerate(questions):
                question_id = question['id']
                h2 = question['h2']
                paragraphs = ''.join(question['paragraphs'])  # Concatenate the <p> elements
                answer = question['answer']
                answer_key.append(f"{year} Problem {i + 1}: {answer}")

                # Add the question to the HTML content
                html_content += f"{h2}\n{paragraphs}\n<br>\n"

            # Add a page break after each year's questions
            html_content += "<hr style='page-break-after: always;'>\n"

    html_content += "</body></html>"

    # Save all questions as a single HTML file
    html_file_path = os.path.join(output_dir, "AMC_8_Problems_1999_2024.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content.replace('src="//latex', 'src="https://latex'))

    print(f"All questions from 1999 to 2024 saved to {html_file_path}")

    # Save the answer keys to a separate file
    answer_key_content = '\n'.join(answer_key)
    answer_key_file = os.path.join(output_dir, "answer_key_1999_2024.txt")
    with open(answer_key_file, 'w', encoding='utf-8') as f:
        f.write(answer_key_content)

    print(f"Answer keys saved to {answer_key_file}")

# Main function to load JSON and generate HTML files for all years
def main():
    json_file = "amc_8_problems_with_answers_1999_2024.json"  # Path to your JSON file
    output_dir = "amc_html_output"  # Directory to save the HTML files

    # Load the data from the JSON file
    data = load_json(json_file)
    if data:
        generate_html_for_all_years(data, output_dir)

# Example usage
if __name__ == "__main__":
    main()
