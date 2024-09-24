# Download all quetions and answers to local and save into a json file "amc_8_problems_with_answers_1999_2024.json"
getAllAmc8.py

# To generate quetions/answers for given year
python genyearlyquestions.py

# To genearte all questions/answers in single file
python saveall.py

# To generate a random test. modify the to and from year in the script
python createRandomTest.py
powershell (1..25) | %{python .\createRandomTest.py;Start-Sleep -Seconds 1}

# To generate the interested tests (wronged ones)
python createselectedones.py
