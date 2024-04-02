from database import db
import pandas as pd
import ast
import json
import re

from models import Episodes

def parse_episode_line(line):
    # split line into episode_name and rest
    episode_name, rest = line.split(' (', 1)
    # remove the quotes from the episode
    episode_name = episode_name.strip('"')

    date_notes_split = rest.split(')')
    date = date_notes_split[0]

    # remove day from date, only keep month and year
    date = date.split(' ')[0] + ' ' + date.split(' ')[2]

    # extract notes if there are any and then clean them up
    notes = date_notes_split[1] if len(date_notes_split) > 1 else None
    if notes:
        if notes.startswith(' - '):
            notes = notes[3:]
        if '(' in notes and not notes.endswith(')'):
            notes = notes + ')'
            
    return {'episode': episode_name, 'date': date, 'notes': notes}

def read_episode_dates_to_df(filepath):
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            parsed_data = parse_episode_line(line.strip())
            data.append(parsed_data)
    
    return pd.DataFrame(data)

def extract_subjects(row):
    subjects = [column for column in row.index if row[column] == 1]
    return subjects
    # print("Processing row:", row)
    # for column in subject_matter.columns[2:]:
    #     print("checking column:", column)
    #     if row[column] == 1:
    #         subjects.append(column)
    # return subjects

# Extract the data from the sources
colors_used = pd.read_csv('data/colors_used.csv')
subject_matter = pd.read_csv('data/subject_matter.csv')
episode_dates = read_episode_dates_to_df('data/episode_dates.txt')


# prints each line from colors_used
colors_used['colors'] = colors_used['colors'].apply(lambda x: ast.literal_eval(x.replace('\\n', '').replace('\\r', '').replace('\\', '')))
# print(colors_used[['painting_index', 'painting_title', 'colors']])


subject_matter['subjects'] = subject_matter.apply(extract_subjects, axis=1)
# print(subject_matter[['EPISODE', 'TITLE', 'subjects']])

# for index, row in episode_dates.iterrows():
#     print(row)
#     print('---')
#     print('')

# these are for printing to test due to the large amount of data
# print(colors_used[['painting_index', 'painting_title', 'colors']])
# print(subject_matter[['EPISODE', 'TITLE', 'subjects']])

def clean_string(s):
    return re.sub(r'(\\r|\\n|\\r\\n|\r|\n|\\)', '', s)

# def load_data_into_db():
#     # Load episode dates, names and notes
#     episode_dates_df = read_episode_dates_to_df('data/episode_dates.txt')
#     for index, row in episode_dates_df.iterrows():
#         episode_obj = Episodes(title=row['episode'], date=row['date'], description=row['notes'])
#         db.session.add(episode_obj)
    
#     # Load colors used
#     colors_used = pd.read_csv('data/colors_used.csv')
#     colors_used['colors'] = colors_used['colors'].apply(lambda x: ast.literal_eval(x))
#     # print(colors_used.columns)

#     for index, row in colors_used.iterrows():
#         cleaned_colors = [clean_string(color) for color in row['colors']]
#         colors_json = json.dumps(cleaned_colors)
#         color = Colors(colors=colors_json, episode_id=row['painting_index'])
#         db.session.add(color)

#     # Load subject matter
#     subject_matter = pd.read_csv('data/subject_matter.csv')
#     subject_matter['subjects'] = subject_matter.apply(extract_subjects, axis=1)

#     for index, row in subject_matter.iterrows():
#         clean_subjects = [clean_string(subject) for subject in row['subjects']]
#         subjects_json = json.dumps(clean_subjects)
#         print(subjects_json)
#         subject = Subjects(painting_index=row['EPISODE'], subjects=subjects_json)
#         db.session.add(subject)

#     db.session.commit()

def load_data_into_db():
    for index, row in episode_dates.iterrows():
        episode_obj = Episodes.query.filter_by(title=row['episode']).first()
        if not episode_obj:
            episode_obj = Episodes(title=row['episode'], date=row['date'], description=row['notes'])

            #prepare and assign colors and subjects JSON
            episode_colors = colors_used[colors_used['painting_index'] == index]
            cleaned_colors = [clean_string(color) for color in ast.literal_eval(episode_colors['colors'].iloc[0])]
            episode_obj.colors = json.dumps(cleaned_colors)

            episode_subjects = subject_matter[subject_matter['EPISODE'] == index]
            cleaned_subjects = [clean_string(subject) for subject in extract_subjects(episode_subjects.iloc[0])]
            episode_obj.subjects = json.dumps(cleaned_subjects)

            db.session.add(episode_obj)

    db.session.commit()