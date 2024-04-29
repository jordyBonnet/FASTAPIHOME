"""
Get all interesting sports events from the website lequipe.fr send it to the user via pushbullet
"""
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from pushbullet import Pushbullet
import pushbullet_messages as pbm
import warnings
warnings.filterwarnings('ignore')

IMPORTANT_TEAMS = [
    'France', 'Marseille', 'ParisSG', 'San Antonio',\
    'Real Madrid', 'FC Barcelone', 'Manchester City',\
    'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United',\
    'Bayern Munich'\
]

                
                
#region LEQUIPE scrap functions
def scrape_lequipe(date=None):
    if date is not None:
        url = f"https://www.lequipe.fr/Directs/{date}"
    else:
        url = "https://www.lequipe.fr/Directs"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Process the soup object as needed
    else:
        print("Error: Failed to retrieve data from the URL")
    return soup

def get_all_matchs(soup):
    # get all matches
    matches = soup.find_all(class_='MatchSchedule__item')
    data = []
    team1 = None
    team2 = None
    time = None
    for match in matches:
        team_name = match.find(class_='MatchSchedule__teamName')
        match_time = match.find(class_='MatchSchedule__scheduled')
        
        if team_name:
            team_name_txt = re.sub(r'[^\w\(\) ]|_', '', team_name.text.strip().replace('\n', ''))
            sport = team_name.find_previous('h2', class_='Lives__title')
            competition = team_name.find_previous('h3', class_='Lives__title')
            if not team1:
                team1 = team_name_txt
            else:
                team2 = team_name_txt
        if match_time:
            time = match_time.text.strip()

        if team1 and team2 and time:
            data.append([team1, time, team2, sport.text, competition.text])
            team1 = None
            team2 = None
            time = None

    df = pd.DataFrame(data, columns=['Team1', 'Hour', 'Team2', 'Sport', 'Competition'])
    # Remove numbers and parentheses from team names
    df['CleanTeam1'] = df['Team1'].apply(lambda x: re.sub(r'\(\d+\)', '', x).strip())
    df['CleanTeam2'] = df['Team2'].apply(lambda x: re.sub(r'\(\d+\)', '', x).strip())
    # print(df.head)

    df['Team1'] = df['Team1'].apply(lambda x: re.sub(r' ', '', x))
    df['Team2'] = df['Team2'].apply(lambda x: re.sub(r' ', '', x))

    # Check if important teams are in the new columns
    important_matches = df[(df['CleanTeam1'].isin(IMPORTANT_TEAMS)) | (df['CleanTeam2'].isin(IMPORTANT_TEAMS))]
    # Split the condition into two parts
    football_matches = important_matches[(important_matches['Sport'] == 'Football')]
    basketball_matches = important_matches[(important_matches['Sport'] == 'Basket') & (important_matches['Competition'].str.contains('NBA'))]

    # Concatenate the results
    important_matches = pd.concat([football_matches, basketball_matches])

    important_matches.drop(['CleanTeam1', 'CleanTeam2', 'Sport'], axis=1, inplace=True)
    df_string = important_matches.to_string(index=False, header=False)
    return df_string

def get_GPs(soup):
    # get F1, cyclisms , MotoGP races
    sports = soup.find_all('h2', class_='Lives__title')
    sports_txt = [sport.text for sport in sports]
    GPs_txt = ''

    for i, sport in enumerate(sports_txt):
        if sport == 'Formule 1' or sport == 'Moto' or sport == 'Cyclisme':
            competition = sports[i].find_next('h3', class_='Lives__title')
            # race finished
            race_finished = sports[i].find_next('div', class_='liveScore__linkLabel')
            if race_finished != None:
                pass
            else:
                course_type = sports[i].find_next('span', class_='Lives__competNiveau')
                course_hour = sports[i].find_next('div', class_='liveScore__schedule')
                # print(sport, ' - ', competition.text, course_type.text, course_hour.text)
                GPs_txt += f"{sport} - {competition.text} {course_type.text} {course_hour.text}\n"
    return GPs_txt

def get_lequipe_sports_events(date=None):
    total_txt = ''
    soup = scrape_lequipe(date)
    matchs_txt = get_all_matchs(soup)
    if 'Empty DataFrame' in matchs_txt:
        total_txt += "Pas de match aujourd'hui" + '\n'
    else:
        total_txt += matchs_txt + '\n'

    Gps_txt = get_GPs(soup)
    total_txt += Gps_txt

    return total_txt
#endregion LEQUIPE scrap functions

#region PUSHBULLET functions
def send_message_to_user(message):
    pb = Pushbullet(pbm.API_KEY)
    pb.push_note("Daily sports events", message)
#endregion PUSHBULLET functions
    
def main():
    # 0. Get the data from the website as text
    out_string = get_lequipe_sports_events()
    # 1. Send the data to the user
    send_message_to_user(out_string)