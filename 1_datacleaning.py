""" Intended to clean and preprocess the data, pulling from i_landing_layer and putting out into ii_raw_layer """

# Constants
MATCH_URL_FORMAT = "https://www.wheeloratings.com/afl_match_stats.html?id="


# Imports
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from playwright.sync_api import sync_playwright

# Preliminary File Access
print("(*) Identifying files:")
for f in Path("i_landing_layer/player_match_stats").iterdir():
    if f.is_file():
        print("> " + f.name)
    with open(f, "r", encoding="utf-8") as p:
        try:
            writ = p.read()
        except: 
            print("(!) File Access Error occurred")

# Collects a list of all teams and builds a dictionary
all_teams = []
team_dict = {}
num_games = 0
for game in Path("i_landing_layer/player_match_stats").iterdir():
    if f.is_file():
        print("(*) Extracting from", game.name)
        match_df = pd.read_csv(game)
        teams = list(set(match_df["Team"]))
        if len(teams) != 2:
            raise ValueError("File contains more than two teams, this is likely incorrect")
        all_teams = list(set(all_teams + teams))
        num_games = num_games + 1
all_teams.sort()
n = len(all_teams)
for i in range(n):
    team_dict[all_teams[i]] = i
print(team_dict)


# Iterates through each game-data file to extract 
for game in Path("i_landing_layer/player_match_stats").iterdir():
    if f.is_file():

        # Extracts dataframe
        print("(*) Extracting from", game.name)
        match_df = pd.read_csv(game)
        match_id = match_df["MatchId"][0]
        teams = sorted(list(set(match_df["Team"])))
        t1 = team_dict[teams[0]]
        t2 = team_dict[teams[1]]  
        print(teams)

        # Here, cleans the data appropriately

        # Saves the cleaned player-wise data
        Path("ii_raw_layer/match_stats/").mkdir(parents=True, exist_ok=True)
        print("(*)", game.name, "processed successfully. Writing to 'ii_raw_layer/player_match_stats/" + str(match_id) + "-match-TM" + str(t1) + "-TM" + str(t2) + ".csv")
        match_df.to_csv("ii_raw_layer/match_stats/" + str(match_id) + "-match-TM" + str(t1) + "-TM" + str(t2) + ".csv", index=False)

        # Scrapes relevant website data and reduces it to 
        url = MATCH_URL_FORMAT + str(match_id)
        with sync_playwright() as p:

            # Opens relevant page for data scraping
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            # Determines the organisation of the data column
            match_title = page.locator("#match-banner").inner_text().strip()
            mt = match_title.split()
            if mt[0] == teams[0]:
                pass
            else:
                teams.sort(reverse=True)

            # Extracts team statistics themselves
            stats = {}
            rows = page.locator(".row.hover-row").all()
            for row in rows:
                stat_name = row.locator(".col-5").inner_text().strip()
                stat_values = [v.strip() for v in row.locator(".stat").all_inner_texts()]
                if len(stat_values) == 2:
                    stats[stat_name] = {
                        teams[0]: stat_values[0],
                        teams[1]: stat_values[1]
                    }
            for k,v in stats.items():
                print(k,v)

            # Determines winner
            t1_score = int(((stats["Score"][teams[0]]).split())[1].strip("()"))
            t2_score = int(((stats["Score"][teams[1]]).split())[1].strip("()"))
            winning = max({t1_score, t2_score})

            # Returns individual team responses and saves
            for team in teams:
                match_df = {}



            browser.close()


            
