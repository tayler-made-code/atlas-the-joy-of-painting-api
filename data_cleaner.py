from database import db
import pandas as pd
import ast
import json
import re
from fuzzywuzzy import process, fuzz

from models import Episodes

# Define the functions to extract the data from the sources
def parse_episode_line(line):
    # split line into episode_name and rest
    episode_name, rest = line.split(' (', 1)
    # remove the quotes from the episode
    episode_name = episode_name.strip('"')

    dates_and_notes = rest.split(')')
    date = dates_and_notes[0]

    # remove day from date, only keep month and year
    date = date.split(' ')[0] + ' ' + date.split(' ')[2]

    # extract notes if there are any and then clean them up
    notes = dates_and_notes[1] if len(dates_and_notes) > 1 else None
    if notes:
        # removes leading dashes and spaces
        if notes.startswith(' - '):
            notes = notes[3:]
        # add a closing parenthesis if there is an opening parenthesis but no closing parenthesis
        if '(' in notes and not notes.endswith(')'):
            notes = notes + ')'
            
    return {'episode': episode_name, 'date': date, 'notes': notes}

# Read the episode dates from the text file
def read_episode_dates_to_df(filepath):
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            parsed_data = parse_episode_line(line.strip())
            data.append(parsed_data)
    
    return pd.DataFrame(data)

# Extract the subjects from the row
def extract_subjects(row):
    subjects = [column for column in row.index if row[column] == 1]
    return subjects

# Extract the data from the sources
colors_used = pd.read_csv('data/colors_used.csv')
subject_matter = pd.read_csv('data/subject_matter.csv')
episode_dates = read_episode_dates_to_df('data/episode_dates.txt')
colors_used['colors'] = colors_used['colors'].apply(lambda x: ast.literal_eval(x.replace('\\n', '').replace('\\r', '').replace('\\', '')))
subject_matter['subjects'] = subject_matter.apply(extract_subjects, axis=1)

# Clean up the data
def clean_string(s):
    return re.sub(r'(\\r|\\n|\\r\\n|\r|\n|\\)', '', s)

# Finds the best match for a title in a list of choices
def find_best_match(title, choices, scorer=fuzz.token_sort_ratio):
    best_match = process.extractOne(title, choices, scorer=scorer)
    return best_match[0] if best_match else None

# Load the data into the database
def load_data_into_db():
    colors_titles = colors_used['painting_title'].tolist()
    subject_titles = subject_matter['TITLE'].tolist()

    for index, row in episode_dates.iterrows():
        episode_title = row['episode']
        episode_date = row['date']
        episode_obj = Episodes.query.filter_by(title=episode_title, date=episode_date).first()
        if not episode_obj:
            episode_obj = Episodes(title=episode_title, date=episode_date, description=row['notes'])

            # Prepare and assign colors JSON
            best_match_color_title = find_best_match(episode_title, colors_titles)
            if best_match_color_title:
                episode_colors = colors_used[colors_used['painting_title'] == best_match_color_title]
                cleaned_colors = [clean_string(color) for color in episode_colors['colors'].iloc[0]]
                episode_obj.colors = json.dumps(cleaned_colors)
            else:
                print(f"Error: No colors found for episode {episode_title}")

            # Prepare and assign subjects JSON
            best_match_subject_title = find_best_match(episode_title, subject_titles)
            if best_match_subject_title:
                episode_subjects = subject_matter[subject_matter['TITLE'] == best_match_subject_title]
                cleaned_subjects = [clean_string(subject) for subject in extract_subjects(episode_subjects.iloc[0])]
                episode_obj.subjects = json.dumps(cleaned_subjects)
            else:
                print(f"Error: No subjects found for {episode_title}")

            db.session.add(episode_obj)

    db.session.commit()
