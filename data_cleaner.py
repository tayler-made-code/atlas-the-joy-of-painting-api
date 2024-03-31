import pandas as pd
import ast

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
    subjects = []
    for column in subject_matter.columns[2:]:
        if row[column] == 1:
            subjects.append(column)
    return subjects

# Extract the data from the sources
colors_used = pd.read_csv('data/colors_used.csv')
subject_matter = pd.read_csv('data/subject_matter.csv')
episode_dates = read_episode_dates_to_df('data/episode_dates.txt')


# prints each line from colors_used
colors_used['colors'] = colors_used['colors'].apply(lambda x: ast.literal_eval(x.replace('\r\n', '')))
print(colors_used[['painting_index', 'painting_title', 'colors']])


subject_matter['subjects'] = subject_matter.apply(extract_subjects, axis=1)
print(subject_matter[['EPISODE', 'TITLE', 'subjects']])

for index, row in episode_dates.iterrows():
    print(row)
    print('---')
    print('')

# these are for printing to test due to the large amount of data
# print(colors_used[['painting_index', 'painting_title', 'colors']])
# print(subject_matter[['EPISODE', 'TITLE', 'subjects']])