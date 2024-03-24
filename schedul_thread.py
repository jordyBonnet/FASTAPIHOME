import threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from pushbullet import Pushbullet
import pushbullet_messages as pbm
import pushbullet_functions as pbf

important_teams = ['France', 'Marseille', 'ParisSG', 'San Antonio', 'Real Madrid', 'FC Barcelone', 'Manchester City', 'Arsenal', 'Liverpool', 'Bayern Munich']

# Flag to check if the function has already run today
has_run_today = False

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
    important_matches = df[(df['CleanTeam1'].isin(important_teams)) | (df['CleanTeam2'].isin(important_teams))]
    important_matches.drop(['CleanTeam1', 'CleanTeam2'], axis=1, inplace=True)
    df_string = important_matches.to_string(index=False, header=False)
    return df_string

def get_GPs(soup):
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

def get_lequipe_informations(date=None):
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
    PB_API_KEY = ''
    pb = Pushbullet(PB_API_KEY)
    pb.push_note("Daily sports events", message)
#endregion PUSHBULLET functions


def my_function():
    """Function to run every day after 8:30 AM and get the data from the website"""
    global has_run_today
        
    # Get the current time
    now = datetime.now()

    # Check if it's past 8:30 AM and the function hasn't run today
    if now.hour >= 8 and now.minute >= 30 and not has_run_today:
        # 0. Get the data from the website as text
        out_string = get_lequipe_informations()

        # 1. Send the data to the user
        send_message_to_user(out_string)

        # Set the flag to True so the function won't run again today
        has_run_today = True

    # At midnight, reset the flag
    if now.hour == 0:
        has_run_today = False


def run_thread():
    threading.Timer(60 * 30, run_thread).start()  # Check every 30 minutes
    my_function()

run_thread()