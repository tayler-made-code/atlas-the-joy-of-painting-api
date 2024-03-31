import pandas as pd
import sqlalchemy

def parse_episode_line(line):
    # split line into episode_name and rest
    episode_name, rest = line.split(' (', 1)
    # remove the quotes from the episode
    episode_name = episode_name.strip('"')

    date_notes_split = rest.split(')')
    date = date_notes_split[0]

    # remove day from date, only keep month and year
    date = date.split(' ')[0] + ' ' + date.split(' ')[2]

    notes = date_notes_split[1] if len(date_notes_split) > 1 else None

    #clean notes
    if notes:
        if notes.startswith(' - '):
            notes = notes[3:]
        # if notes contains a '(' then add a closing ')'
        if '(' in notes and not notes.endswith(')'):
            notes = notes + ')'
        # if not notes.endswith(')'):
        #     notes = notes + ')'
            
    
    return {'episode': episode_name, 'date': date, 'notes': notes}

def read_episode_dates_to_df(filepath):
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            parsed_data = parse_episode_line(line.strip())
            data.append(parsed_data)
    
    return pd.DataFrame(data)


# Extract the data from the sources
colors_used = pd.read_csv('data/colors_used.csv')
subject_matter = pd.read_csv('data/subject_matter.csv')
# extract data from the episode dates plain text file
episode_dates = read_episode_dates_to_df('data/episode_dates.txt')


# print each line from colors_used
# for index, row in colors_used.iterrows():
#     print(row)
#     print('---')
#     print('')

for index, row in episode_dates.iterrows():
    print(row)
    print('---')
    print('')