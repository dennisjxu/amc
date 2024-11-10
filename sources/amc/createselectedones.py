import json
import os
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

# Function to generate questions and answers for multiple years and question numbers
def generate_questions_and_answers_for_multiple_years(data, input_data, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare the HTML content for all questions
    questions_html_content = "<html><body>\n<h1>AMC 8 Selected Questions</h1>\n"
    answer_key_content = []

    # Loop through each year and question numbers provided in the input data
    for entry in input_data:
        if len(entry) < 2:
            print(f"Invalid input format for entry {entry}. Must include year and question numbers.")
            continue

        year = entry[0]
        question_numbers = entry[1:]

        # Check if the year exists in the data
        if str(year) not in data:
            print(f"Year {year} is not available in the data.")
            continue

        # Add a heading for the year in the HTML content
        questions_html_content += f"<h2>Questions from {year}</h2>\n"

        # Loop through the question numbers for the given year
        for question_num in question_numbers:
            question_idx = question_num - 1  # Zero-based index

            # Check if the question number is valid for the year
            if question_idx < 0 or question_idx >= len(data[str(year)]):
                print(f"Question number {question_num} for year {year} is out of range.")
                continue

            # Retrieve the question and answer
            selected_question = data[str(year)][question_idx]

            # Add the question to the HTML content
            h2 = selected_question['h2']
            h2 = h2.replace("Problem", f"{year} Problem")
            paragraphs = ''.join(selected_question['paragraphs'])
            questions_html_content += f"{h2}\n{paragraphs}\n"

            # Add the answer to the answer key content
            answer_key_content.append(f"Year {year}, Problem {question_num}: {selected_question['answer']}")

    questions_html_content += "</body></html>"

    # Get the current timestamp for unique file names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    years = f"{input_data[0][0]}-{input_data[-1][0]}"
    # Save the compiled questions as a single HTML file
    html_file_path = os.path.join(output_dir, f"AMC_8_Questions_Multiple_Years_{years}.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(questions_html_content.replace('src="//latex', 'src="https://latex'))

    print(f"Questions saved to {html_file_path}")

    # Save the compiled answer key to a separate text file
    answer_key_file_path = os.path.join(output_dir, f"AMC_8_Answers_Multiple_Years_{years}.txt")
    with open(answer_key_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(answer_key_content))

    print(f"Answers saved to {answer_key_file_path}")

# Main function to load JSON and generate questions for multiple years
def main():
    json_file = "amc_8_problems_with_answers_1999_2024.json"  # Path to your JSON file
    output_dir = "amc_questions_output"  # Directory to save the question and answer files

    # Load the data from the JSON file
    data = load_json(json_file)
    if data:
        # Example input: multiple year-question pairs
        input_data = [
            [2000, 5, 18, 21, 24], 
            [2001, 11, 13, 17, 18],
            [2002, 6, 10, 11, 21, 22, 25],
            [2003, 2, 5, 18, 20, 22, 25],
            [2004, 5, 8, 13, 14, 24, 25],
            [2005, 17, 20, 23],
            [2006, 6, 21],
            [2007, 11, 19, 21, 25],
            [2008, 3, 14, 20, 22, 25],
            [2009, 9, 20, 22, 24, 25],
            [2010, 7, 13, 16, 19, 21, 22],
            [2011, 17, 18, 22, 23, 24],
            [2012, 9, 11, 13, 14, 18, 23],
            [2013, 9, 18, 19, 20, 21, 22, 23, 25],
            [2014, 25],
            [2015, 3, 7, 8, 9, 12, 16, 20, 22, 23, 25],
            [2016, 8, 13, 15, 16, 19, 21, 22],
            [2017, 4, 10, 13, 16, 19, 20, 22, 23],
            [2018, 3, 5, 19, 20, 22, 23, 24, 25],
            [2019, 8, 10, 14, 16, 17, 19, 20, 21, 25],
            [2020, 7, 15, 17, 19, 21, 22, 23, 24, 25]
        ]

        # Generate questions and answers for the input data
        generate_questions_and_answers_for_multiple_years(data, input_data, output_dir)

# Example usage
if __name__ == "__main__":
    main()
