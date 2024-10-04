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

# Function to check if any keyword exists in paragraphs
def contains_keywords(paragraphs, keywords):
    for paragraph in paragraphs:
        for keyword in keywords:
            if keyword.lower() in paragraph.lower():  # Case-insensitive check
                return True
    return False

# Function to generate problems and answers based on keywords in the paragraphs
def generate_problems_by_keywords(data, keywords, fileNamePrefix, toYear, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare the HTML content for matching questions
    questions_html_content = "<html><body>\n<h1>AMC 8 Problems Containing Keywords</h1>\n"
    answer_key_content = []

    # Loop through all years and all problems
    for year, problems in data.items():
        if int(year) > toYear: 
            continue
        for idx, problem in enumerate(problems):
            # Check if any paragraph contains any of the keywords
            if contains_keywords(problem['paragraphs'], keywords):
                question_num = idx + 1
                selected_question = problem

                # Add the question to the HTML content
                h2 = selected_question['h2']
                paragraphs = ''.join(selected_question['paragraphs'])
                questions_html_content += f"<h2>Year {year}, Problem {question_num}</h2>\n{h2}\n{paragraphs}\n"

                # Add the answer to the answer key content
                answer_key_content.append(f"Year {year}, Problem {question_num}: {selected_question['answer']}")

    questions_html_content += "</body></html>"

    # Get the current timestamp for unique file names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the compiled questions as a single HTML file
    html_file_path = os.path.join(output_dir, f"{fileNamePrefix}_{timestamp}.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(questions_html_content.replace('src="//latex', 'src="https://latex'))

    print(f"Questions saved to {html_file_path}")

    # Save the compiled answer key to a separate text file
    answer_key_file_path = os.path.join(output_dir, f"{fileNamePrefix}_{timestamp}.txt")
    with open(answer_key_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(answer_key_content))

    print(f"Answers saved to {answer_key_file_path}")

# Main function to load JSON and generate problems based on keywords
def main():
    json_file = "amc_8_problems_with_answers_1999_2024.json"  # Path to your JSON file
    output_dir = "amc_questions_by_keywords_output"  # Directory to save the question and answer files

    # Load the data from the JSON file
    data = load_json(json_file)
    if data:
        # keywords = ["year", "month", "week", "day", "hour", "minute", "secord", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]  # Example keywords
        # generate_problems_by_keywords(data, keywords, "TimeRelated", 2018, output_dir)
        keywords = ["Circle", "Square", "Triangle", "Rectangle", "Oval", "Hexagon", "Pentagon", "Octagon", "Star", "Diamond", "Point", "Line", "Angle", "Ray", "Plane", "Polygon", "Perimeter", "Area", "Volume", "Circumference", "Radius", "Diameter", 
        "Chord", "Arc", "Tangent", "Secant", "Vertex", "Edge", "Face", "Axis", "Parallel", "Perpendicular", "Symmetry", "Centroid", "Slope", "Intersection", "Coordinate", "Axis", "Dimension", 
        "Meter", "Centimeter", "Millimeter", "Kilometer", "Inch", "Foot", "Yard", "Mile", "Square Meter", "Square Kilometer", "Square Foot", "Square Inch", "Cubic Meter", "Cubic Centimeter", "Cubic Inch", "Degree", "Radian", "degree" ]
        generate_problems_by_keywords(data, keywords, "GeometryRelated", 2018, output_dir)
# Example usage
if __name__ == "__main__":
    main()
