from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import requests
import os



load_dotenv()

API_KEY = os.getenv('API_KEY')
# DB_URI = os.getenv('DB_URI')

BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3'
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
}

# League IDs
LEAGUE_IDS = {
    'La Liga': 140,
    'Premier League': 39,
    'Bundesliga': 78,
    'Serie A': 135
}

def format_birth_date(birth_date):
    if birth_date:
        return datetime.strptime(birth_date, '%Y-%m-%d').date()
    else:
        return None



def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


def extract_teams(league_id, season):
    endpoint = f'/teams?league={league_id}&season={season}'
    # print(BASE_URL+endpoint)
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    if response.status_code == 200:
        teams_data = response.json().get('response', [])
        teams = []
        for entry in teams_data:
            team = entry['team']
            team_id = team['id']
            # coach_name = fetch_coach_name(team_id)
            teams.append({
                'team_id': team_id,
                'name': team['name'],
                'league': get_key_by_value(LEAGUE_IDS, league_id),
                'coach': ""
            })
        return teams
    else:
        print(f"Failed to fetch data for league {league_id}, season {season}: {response.text}")
        return []
    
    
def fetch_coach_name(team_id):
    coach_endpoint = f'/coachs?team={team_id}'
    coach_response = requests.get(BASE_URL + coach_endpoint, headers=HEADERS)
    if coach_response.status_code == 200:
        coach_data = coach_response.json().get('response', [])
        if coach_data:
            return coach_data[0]['name']
    return None






# Function to fetch players for a given team ID and season
def fetch_players_for_team(team_id, season):
    url = f"/players?team={team_id}&season={season}"
    response = requests.get(BASE_URL+ url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['response']
    else:
        print(f"Failed to fetch players for team {team_id}, season {season}")
        return []

# Function to extract player information for the latest season
def get_latest_season_player_info(team_ids, latest_season):
    player_info = []
    for team_id in tqdm(team_ids, desc="Teams"):
        players = fetch_players_for_team(team_id, latest_season)
        for player_data in players:
            player = player_data['player']
            player_id = player['id']
            player_info.append({
                'player_id': player_id,
                'name': player['name'],
                'team_id': team_id,
                'position': player_data['statistics'][0]['games']['position'],
                'birth_date': player['birth']['date'],
                'nationality': player['nationality']
            })
    return player_info

