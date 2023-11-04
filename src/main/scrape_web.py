import os
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re
"""
Make it so it only removes injured players that are considered OUT and not DTD
Use another website to scrape injury reports
https://www.rotowire.com/basketball/injury-report.php

"""
#General Team Stats
heat = "https://www.basketball-reference.com/teams/MIA/2024.html"
bos = "https://www.basketball-reference.com/teams/BOS/2024.html"
lal = "https://www.basketball-reference.com/teams/LAL/2024.html"
lac = "https://www.basketball-reference.com/teams/LAC/2024.html"
cha = "https://www.basketball-reference.com/teams/CHO/2024.html"
atl = "https://www.basketball-reference.com/teams/ATL/2024.html"

orl = "https://www.basketball-reference.com/teams/ORL/2024.html"
mem = "https://www.basketball-reference.com/teams/MEM/2024.html"
nop = "https://www.basketball-reference.com/teams/NOP/2024.html"
was = "https://www.basketball-reference.com/teams/WAS/2024.html"
sas = "https://www.basketball-reference.com/teams/SAS/2024.html"
dal = "https://www.basketball-reference.com/teams/DAL/2024.html"

hou = "https://www.basketball-reference.com/teams/HOU/2024.html"
pho = "https://www.basketball-reference.com/teams/PHO/2024.html"
gsw = "https://www.basketball-reference.com/teams/GSW/2024.html"
sac = "https://www.basketball-reference.com/teams/SAC/2024.html"
por = "https://www.basketball-reference.com/teams/POR/2024.html"
uta = "https://www.basketball-reference.com/teams/UTA/2024.html"

tim = "https://www.basketball-reference.com/teams/MIN/2024.html"
den = "https://www.basketball-reference.com/teams/DEN/2024.html"
okc = "https://www.basketball-reference.com/teams/OKC/2024.html"
nyk = "https://www.basketball-reference.com/teams/NYK/2024.html"
tor = "https://www.basketball-reference.com/teams/TOR/2024.html"
phi = "https://www.basketball-reference.com/teams/PHI/2024.html"

mil = "https://www.basketball-reference.com/teams/MIL/2024.html"
chi = "https://www.basketball-reference.com/teams/CHI/2024.html"
cle = "https://www.basketball-reference.com/teams/CLE/2024.html"
bkn = "https://www.basketball-reference.com/teams/BRK/2024.html"
det = "https://www.basketball-reference.com/teams/DET/2024.html"
ind = "https://www.basketball-reference.com/teams/IND/2024.html"


#Splits Team Stats URLs
heat_splits = "https://www.basketball-reference.com/teams/MIA/2024/splits"
bos_splits = "https://www.basketball-reference.com/teams/BOS/2024/splits"
lal_splits = "https://www.basketball-reference.com/teams/LAL/2024/splits"
lac_splits = "https://www.basketball-reference.com/teams/LAC/2024/splits"
cha_splits = "https://www.basketball-reference.com/teams/CHO/2024/splits"
atl_splits = "https://www.basketball-reference.com/teams/ATL/2024/splits"

orl_splits = "https://www.basketball-reference.com/teams/ORL/2024/splits"
mem_splits = "https://www.basketball-reference.com/teams/MEM/2024/splits"
nop_splits = "https://www.basketball-reference.com/teams/NOP/2024/splits"
was_splits = "https://www.basketball-reference.com/teams/WAS/2024/splits"
sas_splits = "https://www.basketball-reference.com/teams/SAS/2024/splits"
dal_splits = "https://www.basketball-reference.com/teams/DAL/2024/splits"

hou_splits = "https://www.basketball-reference.com/teams/HOU/2024/splits"
pho_splits = "https://www.basketball-reference.com/teams/PHO/2024/splits"
gsw_splits = "https://www.basketball-reference.com/teams/GSW/2024/splits"
sac_splits = "https://www.basketball-reference.com/teams/SAC/2024/splits"
por_splits = "https://www.basketball-reference.com/teams/POR/2024/splits"
uta_splits = "https://www.basketball-reference.com/teams/UTA/2024/splits"

tim_splits = "https://www.basketball-reference.com/teams/MIN/2024/splits"
den_splits = "https://www.basketball-reference.com/teams/DEN/2024/splits"
okc_splits = "https://www.basketball-reference.com/teams/OKC/2024/splits"
nyk_splits = "https://www.basketball-reference.com/teams/NYK/2024/splits"
tor_splits = "https://www.basketball-reference.com/teams/TOR/2024/splits"
phi_splits = "https://www.basketball-reference.com/teams/PHI/2024/splits"

mil_splits = "https://www.basketball-reference.com/teams/MIL/2024/splits"
chi_splits = "https://www.basketball-reference.com/teams/CHI/2024/splits"
cle_splits = "https://www.basketball-reference.com/teams/CLE/2024/splits"
bkn_splits = "https://www.basketball-reference.com/teams/BRK/2024/splits"
det_splits = "https://www.basketball-reference.com/teams/DET/2024/splits"
ind_splits = "https://www.basketball-reference.com/teams/IND/2024/splits"

INJURED = set()    

def injury_scrape(path):
    with open(path, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'lxml')
        players = soup.find_all('span', class_="CellPlayerName--long")
        for player in players:
            player = player.find('a').text
            INJURED.add(player)


def save_page(url, team_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    with open("data/teamWebPages/" + team_name + "Page.html", "w", encoding='utf-8') as file:
        file.write(str(soup))

def save_page_possession_time(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    with open("data/teamWebPages/possessionData.html", "w", encoding='utf-8') as file:
        file.write(str(soup))

def save_page_injury(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    with open("data/injury/injuryData.html", "w", encoding='utf-8') as file:
        file.write(str(soup))

def save_page_teamshooting_splits(url, team_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    time.sleep(random.randint(0, 2))
    with open("data/teamStats/teamSplits/" + team_name + "Splits.html", "w", encoding='utf-8') as file:
        file.write(str(soup))


def save_page_nba_schedule(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    with open("data/schedule/todaySchedule.html", "w", encoding='utf-8') as file:
        file.write(str(soup))


def search_schedule():
    headers = ["Home", "Away"]
    file_name = "todaySchedule.html"
    path = "data/schedule/" + file_name

    schedule_real = []
    with open(path, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')

        schedule = soup.find_all(class_='TeamLogoNameLockup')
        

        for index in range(1, len(schedule), 2):
            game = []
            game.append(schedule[index].text)
            game.append(schedule[index-1].text)
            schedule_real.append(game)
        # for game in schedule:
        
        print(schedule_real)

        sche = pd.DataFrame(schedule_real, columns = headers)
        #create team filename
        file_name = "todaySchedule.csv"
        path = "data/schedule/" + file_name
        sche.to_csv(path, index=False, encoding="utf-8")
        print("Updated Schedule")
        #     print(game.text)
        # print(schedule)

def search_file(team_name):
    roster_set = set()
    stats_data = []
    abbreviation = getAbbreviation(team_name)

    headers = []
    file_name = team_name + "Page.html"
    path = "data/teamWebPages/" + file_name
    # Opens HTML file using utf-8 encoding
    with open(path, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'lxml')
        
        # ROSTER DATA
        # Finds the id of 'div_roster' in the soup of the html file and stores in roster variable
        roster = soup.find(id='div_roster')
        # Then using the roster variable find each 'tr' which is table row and store it in roster_rows which is a list since find_all returns a list
        roster_rows = roster.find_all('tr')
        roster_data_headers = roster.find_all('th')
        roster_headers = []
        roster_col = []
        # Creates 2D List for each player(row) to be stored in roster_col 
        for player in roster_rows:
            roster_col.append(player.find_all('td'))

        for header in range(1, 4, 1):
            text = roster_data_headers[header].text
            if text != "\xa0":
                # Instead of appending to roster_headers and then looping through again to add to headers just add to headers directly
                # roster_headers.append(text)
                headers.append(text)
        
        # print(roster_headers)
        # Iterate through roster_col to add basic player data from the roster table into stats_data
        index = 1
        while(index < len(roster_col)):
            # Makes empty player list to represent each player attributes
            player = []
            name = roster_col[index][0].text
            # Check if the player has a two way contract embedded in name and removes it from name
            if("\xa0\xa0(TW)" in name):
                name_token = name.split("\xa0\xa0(TW)")
                name = name_token[0]
            # Adds name into roster set to filter out what players are on such team
            # Finally adds the players name, position, and height to the player class
            if name not in INJURED:
                roster_set.add(name)
                pos = roster_col[index][1].text
                height = roster_col[index][2].text
                player.append(name)
                player.append(pos)
                player.append(height)
                stats_data.append(player)

            index += 1

        # NORMAL STATS DATA
        norm_stats = []
        normal_stats = soup.find(id='div_per_game')
        normal_rows = normal_stats.find_all('tr')
        normal_data_headers = normal_stats.find_all('th')
        normal_headers = []
        normal_col = []
        for x in normal_rows:
            normal_col.append(x.find_all('td'))
        
        # 27 is number of headers but two of them are empty columns
        for header in range(2, 28, 1):
            text = normal_data_headers[header].text
            if text != "\xa0":
                normal_headers.append(text)
                headers.append(text)

        # print(normal_headers)

        index = 1
        while(index < len(normal_col)):
            player = []
            if(normal_col[index][0].text in roster_set):
                for i in range(len(normal_col[index])):
                    player.append(normal_col[index][i].text)
                norm_stats.append(player)
            index += 1

        while(len(norm_stats) > 10):
            norm_stats.pop(-1)

        # print(norm_stats)

        # Update Roster Set with people in the 10 man roster
        roster_set.clear()
        
        for player in norm_stats:
            name = player[0]
            if("\xa0\xa0(TW)" in name):
                name_token = name.split("\xa0\xa0(TW)")
                name = name_token[0]
                roster_set.add(name)
            else:
                roster_set.add(name)


        # UPDATE THE STATS_DATA LIST TO REMOVE PLAYERS NOT IN ROSTER SET
        # Add indexes to remove into a list
        indexes_to_remove = []
        for index in range(len(stats_data)):
            name = stats_data[index][0]
            if name not in roster_set:
                indexes_to_remove.append(index)
            
        
        # Removes last players until there are 10 left on roster 
        for index in range(len(indexes_to_remove)-1, -1, -1):
            stats_data.pop(indexes_to_remove[index])

        # ADVANCED DATA
        adv_stats = []
        advanced_stats = soup.find(id='div_advanced')
        advanced_data = advanced_stats.find_all('tr')
        advanced_data_headers = advanced_stats.find_all('th')
        adv_headers = []
        adv_col = []
        for x in advanced_data:
            adv_col.append(x.find_all('td'))

        # 27 is number of headers but two of them are empty columns
        for header in range(4, 27, 1):
            text = advanced_data_headers[header].text
            if text != "\xa0":
                adv_headers.append(text)
                headers.append(text)

        # print(adv_headers)
        index = 1
        while(index < len(adv_col)):
            player = []
            if(adv_col[index][0].text in roster_set):
                for i in range(len(adv_col[index])):
                    player.append(adv_col[index][i].text)
                adv_stats.append(player)
            index += 1

        
        
        
        # ONLY USE USAGE RATE FROM ADVANCED STATS

        # SORT THE NORM STATS AND ROSTER LIST BY NAME
        # print(stats_data, "BEFORE SORT")
        stats_data.sort(key=lambda x:x[0], reverse=False)
        norm_stats.sort(key=lambda x:x[0], reverse=False)
        adv_stats.sort(key=lambda x:x[0], reverse=False)
        # print(stats_data, "AFTER SORT")
        # print(norm_stats, "AFTER SORT")
        # print(adv_stats, "AFTER SORT")

        # Adds normal stats into the stats data list
        for player in range(len(stats_data)):
            for index in range(1, len(norm_stats[player]), 1):
                stats_data[player].append(norm_stats[player][index])

        # Adds advanced stats into the stats data list
         
        for player in range(len(stats_data)):
            for index in range(3, len(adv_stats[player]), 1):
                stat = adv_stats[player][index]
                if(stat != ""):
                    stats_data[player].append(stat)
        
        # sort based on minutes played
        stats_data.sort(key=lambda x:x[6], reverse=True)

        # Adjust minutes to equal to 240
        total_minutes = 0;
        # Iterate through the stats_data list and get the total minutes
        for index in range(0, 10, 1):
            total_minutes += float(stats_data[index][6])
        
        surplur_minutes = 0
        minutes_rate = 240.0 / total_minutes 
        # get the rate to change minutes by
        for index in range(0, 10, 1):
            stats_data[index][6] = round(float(stats_data[index][6]) * minutes_rate)
        
        # Adjust minutes to equal to 240
        total_minutes = 0;
        # Iterate through the stats_data list and get the total minutes
        for index in range(0, 10, 1):
            total_minutes += float(stats_data[index][6])
        
        # print(total_minutes, "BEFORE CHANGE")
        if total_minutes > 240:
            index = 9
            while total_minutes > 240 and index > 0:
                stats_data[index][6] = float(stats_data[index][6]) - 1
                total_minutes -= 1
                index -= 1
        elif total_minutes < 240:
            index = 0
            while total_minutes < 240 and index < 10:
                stats_data[index][6] = float(stats_data[index][6]) + 1
                total_minutes += 1
                index += 1


        # Sort by minutes
        # print(stats_data)
        stats_data.sort(key=lambda x:x[6], reverse=True)

        # FIND Division

        # FIND SECONDS PER POSSESSION
        with open("data/teamWebPages/possessionData.html") as file:
            contents = file.read()
            soup = BeautifulSoup(contents, "lxml")
            table = soup.find(class_="iptbl")
            table_rows = table.find_all('tr')
            table_cols = []
            abbrv = []
            # iterate through rows until you hit the correct abbreviation
            for row in table_rows:
                table_cols.append(row.find_all('td'))
            
            for i in range(len(table_cols)):
                if len(table_cols[i]) == 23:
                    abb = table_cols[i][1].text
                    if(abb == abbreviation):
                        abbrv.append(abb)
                        abbrv.append(table_cols[i][4].text)
                        stats_data.append(abbrv)
                        break;
                else:
                    continue
 
        #Find Home and Away Shooting Percentage ABRV, POS_TIME, HOME 2pt%, AWAY 2pt%, HOME 3pt%, AWAY 3pt%
        with open("data/teamStats/teamSplits/" + team_name + "Splits.html", encoding='utf-8') as file:
            contents = file.read()
            soup = BeautifulSoup(contents, "lxml")
            table = soup.find(class_="table_wrapper")
            # print(table)
            table_rows = table.find_all('tr')
            table_cols = []
            team_stats_splits = []
            temp_team_splits = []
            for row in table_rows:
                table_cols.append(row.find_all('td'))


            # Iterate through the table_cols in order to see the specific row we want. We know that the row that we want is
            # Row 4 and 5 (Home and Away/ROAD rows), We then want specific col values of FG, FGA, 3P, 3PA
            for i in range(4, 6, 1):
                # Iterate through array of cols to get specific value for the values we need stated above\
                for k in range(4, 8, 1):
                    temp_team_splits.append(table_cols[i][k].text)
            # temp team splits array is ordered by [FG@Home, FGA@Home, 3P@Home, 3PA@Home, FG@Away, FGA@Away, 3P@Away, 3PA@Away]
            # main array ordered by [2PT% @ Home, 3P% @ Home, 2PT% @ Away, 3PT% @ Away, AVG 2P, AVG 3P]
            FGMadeHome = float(temp_team_splits[0])
            FGAHome = float(temp_team_splits[1])
            threePTsMadeHome = float(temp_team_splits[2])
            threePTAHome = float(temp_team_splits[3])
            FGMadeAway = float(temp_team_splits[4])
            FGAAway = float(temp_team_splits[5])
            threePTsMadeAway = float(temp_team_splits[6]) 
            threePTAAway = float(temp_team_splits[7]) 
            twoPT_attempts_Home = (FGAHome - threePTAHome)
            twoPT_made_Home = (FGMadeHome - threePTsMadeHome)
            twoPT_attempts_Away = (FGAAway - threePTAAway)
            twoPT_made_Away = (FGMadeAway - threePTsMadeAway)

            twoPT_percentage_home = twoPT_made_Home / twoPT_attempts_Home 
            twoPT_percentage_away = twoPT_made_Away / twoPT_attempts_Away 
            threePT_percentage_home = threePTsMadeHome / threePTAHome
            threePT_percentage_away = threePTsMadeAway / threePTAAway
            avg_two_pt = (twoPT_percentage_home + twoPT_percentage_away) / 2.0
            avg_three_pt = (threePT_percentage_home + threePT_percentage_away) / 2.0

            twoPT_percentage_margin_home = twoPT_percentage_home - avg_two_pt
            threePT_percentage_margin_home = threePT_percentage_home - avg_three_pt
            twoPT_percentage_margin_away = twoPT_percentage_away - avg_two_pt
            threePT_percentage_margin_away = threePT_percentage_away - avg_three_pt

            team_stats_splits.append(twoPT_percentage_margin_home)
            team_stats_splits.append(threePT_percentage_margin_home)
            team_stats_splits.append(twoPT_percentage_margin_away)
            team_stats_splits.append(threePT_percentage_margin_away)

            splits_headers = ["2PT% Margin Home", "3PT% Margin Home", "2PT% Margin Away", "3PT% Margin Away"]
            stats_data.append(splits_headers)
            stats_data.append(team_stats_splits)

        # # Adjust minutes to equal to 240
        # total_minutes = 0;
        # # Iterate through the stats_data list and get the total minutes
        # for index in range(0, 10, 1):
        #     total_minutes += float(stats_data[index][6])
        
        # surplur_minutes = 0
        # minutes_rate = 240.0 / total_minutes 
        # # get the rate to change minutes by
        # for index in range(0, 10, 1):
        #     stats_data[index][6] = round(float(stats_data[index][6]) * minutes_rate)
        
        # # Adjust minutes to equal to 240
        # total_minutes = 0;
        # # Iterate through the stats_data list and get the total minutes
        # for index in range(0, 10, 1):
        #     total_minutes += float(stats_data[index][6])
        
        # # print(total_minutes, "BEFORE CHANGE")
        # if total_minutes > 240:
        #     index = 9
        #     while total_minutes > 240 and index > 0:
        #         stats_data[index][6] = float(stats_data[index][6]) - 1
        #         total_minutes -= 1
        #         index -= 1
        # elif total_minutes < 240:
        #     index = 0
        #     while total_minutes < 240 and index < 10:
        #         stats_data[index][6] = float(stats_data[index][6]) + 1
        #         total_minutes += 1
        #         index += 1


        # # Sort by minutes
        # print(stats_data)
        # stats_data.sort(key=lambda x:x[6], reverse=True)

        # Fill in 0.0 when empty string is in CSV
        for index in range(10):
            # print(len(stats_data[index]))
            for player_stat_index in range(50):
                # print(stats_data[index][0], stats_data[index][len(stats_data[index]) - 1])
                if len(stats_data[index]) < 50:
                    stats_data[index].append(0.0)
                    continue
                if stats_data[index][player_stat_index] == "":
                    stats_data[index][player_stat_index] = 0.0


        team_stats = pd.DataFrame(stats_data, columns = headers)
        #create team filename
        file_name = team_name.lower() + ".csv"
        path = "data/teamStats/" + file_name
        team_stats.to_csv(path, index=False, encoding="utf-8")
        print("Updated", team_name)



def getAbbreviation(team_name):
    if team_name == "kings":
        return "SAC"
    elif team_name == "76ers":
        return "PHI"
    elif team_name == "knicks":
        return "NYK"
    elif team_name == "celtics":
        return "BOS"
    elif team_name == "nuggets":
        return "DEN"
    elif team_name == "mavericks":
        return "DAL"
    elif team_name == "hawks":
        return "ATL"
    elif team_name == "cavaliers":
        return "CLE"
    elif team_name == "warriors":
        return "GSW"
    elif team_name == "jazz":
        return "UTA"
    elif team_name == "nets":
        return "BKN"
    elif team_name == "grizzlies":
        return "MEM"
    elif team_name == "raptors":
        return "TOR"
    elif team_name == "suns":
        return "PHX"
    elif team_name == "bucks":
        return "MIL"
    elif team_name == "thunder":
        return "OKC"
    elif team_name == "clippers":
        return "LAC"
    elif team_name == "lakers":
        return "LAL"
    elif team_name == "wizards":
        return "WAS"
    elif team_name == "trailblazers":
        return "POR"
    elif team_name == "pelicans":
        return "NOP"
    elif team_name == "pacers":
        return "IND"
    elif team_name == "timberwolves":
        return "MIN"
    elif team_name == "bulls":
        return "CHI"
    elif team_name == "heat":
        return "MIA"
    elif team_name == "magic":
        return "ORL"
    elif team_name == "rockets":
        return "HOU"
    elif team_name == "pistons":
        return "DET"
    elif team_name == "spurs":
        return "SAS"
    elif team_name == "hornets":
        return "CHA"
    
isConnectingToSite = False
isConnectingInjury = False
isConnectingSplits = False
isConnectingToSchedule = False
isSearchingFile = True

if isConnectingInjury:
    save_page_injury("https://www.cbssports.com/nba/injuries/daily/")

if isConnectingToSite:
    save_page(phi, "76ers")   
    save_page(mil, "bucks") 
    save_page(chi, "bulls")  
    save_page(cle, "cavaliers")    
    save_page(bos, "celtics")   
    save_page(lac, "clippers") 
    save_page(mem, "grizzlies")
    save_page(atl, "hawks")  
    save_page(heat, "heat")  
    save_page(cha, "hornets")       
    save_page(uta, "jazz")   
    save_page(sac, "kings")   
    save_page(nyk, "knicks") 
    save_page(lal, "lakers")  
    save_page(dal, "mavericks")  
    save_page(orl, "magic")   
    save_page(bkn, "nets") 
    save_page(den, "nuggets")  
    save_page(ind, "pacers") 
    save_page(nop, "pelicans") 
    save_page(det, "pistons") 
    save_page(tor, "raptors")   
    save_page(hou, "rockets")    
    save_page(sas, "spurs")  
    save_page(pho, "suns")   
    save_page(tim, "timberwolves") 
    save_page(okc, "thunder")    
    save_page(por, "trailblazers")  
    save_page(gsw, "warriors")  
    save_page(was, "wizards")  


if isConnectingSplits:
    save_page_teamshooting_splits(phi_splits, "76ers")   
    save_page_teamshooting_splits(mil_splits, "bucks") 
    save_page_teamshooting_splits(chi_splits, "bulls")  
    save_page_teamshooting_splits(cle_splits, "cavaliers")    
    save_page_teamshooting_splits(bos_splits, "celtics")   
    save_page_teamshooting_splits(lac_splits, "clippers") 
    save_page_teamshooting_splits(mem_splits, "grizzlies")
    save_page_teamshooting_splits(atl_splits, "hawks")  
    save_page_teamshooting_splits(heat_splits, "heat")  
    save_page_teamshooting_splits(cha_splits, "hornets")       
    save_page_teamshooting_splits(uta_splits, "jazz")   
    save_page_teamshooting_splits(sac_splits, "kings")   
    save_page_teamshooting_splits(nyk_splits, "knicks") 
    save_page_teamshooting_splits(lal_splits, "lakers")  
    save_page_teamshooting_splits(dal_splits, "mavericks")  
    save_page_teamshooting_splits(orl_splits, "magic")   
    save_page_teamshooting_splits(bkn_splits, "nets") 
    save_page_teamshooting_splits(den_splits, "nuggets")  
    save_page_teamshooting_splits(ind_splits, "pacers") 
    save_page_teamshooting_splits(nop_splits, "pelicans") 
    save_page_teamshooting_splits(det_splits, "pistons") 
    save_page_teamshooting_splits(tor_splits, "raptors")   
    save_page_teamshooting_splits(hou_splits, "rockets")    
    save_page_teamshooting_splits(sas_splits, "spurs")  
    save_page_teamshooting_splits(pho_splits, "suns")   
    save_page_teamshooting_splits(tim_splits, "timberwolves") 
    save_page_teamshooting_splits(okc_splits, "thunder")    
    save_page_teamshooting_splits(por_splits, "trailblazers")  
    save_page_teamshooting_splits(gsw_splits, "warriors")  
    save_page_teamshooting_splits(was_splits, "wizards")  
save_page_possession_time("http://stats.inpredictable.com/nba/ssnTeamPoss.php")

if isConnectingToSchedule:
    save_page_nba_schedule("https://www.cbssports.com/nba/schedule/");
    search_schedule()

if isSearchingFile:
    injury_scrape("data/injury/injuryData.html")
    # search_file("76ers")   
    # search_file("bucks") 
    # search_file("bulls")  #more than 5 injuries
    # search_file("cavaliers")    
    # search_file("celtics")   
    # search_file("clippers") 
    # search_file("grizzlies")
    # search_file("hawks")  
    # search_file("heat")  
    # search_file("hornets")       
    # search_file("jazz")   
    # search_file("kings")   
    # search_file("knicks") 
    # search_file("lakers")  #lakers had 5 injuries when only 14 players on roster so only 9 players available when 10 needed
    search_file("mavericks")  
    search_file("magic")   
    search_file("nets") 
    search_file("nuggets")  
    search_file("pacers") 
    search_file("pelicans") 
    search_file("pistons") 
    search_file("raptors")   
    search_file("rockets")    
    search_file("spurs")  
    search_file("suns")   
    search_file("timberwolves") 
    search_file("thunder")    
    search_file("trailblazers")  
    search_file("warriors")  
    search_file("wizards")  

  