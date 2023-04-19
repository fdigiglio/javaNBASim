import os
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
heat = "https://www.basketball-reference.com/teams/MIA/2023.html"
bos = "https://www.basketball-reference.com/teams/BOS/2023.html"
lal = "https://www.basketball-reference.com/teams/LAL/2023.html"
lac = "https://www.basketball-reference.com/teams/LAC/2023.html"
cha = "https://www.basketball-reference.com/teams/CHO/2023.html"
atl = "https://www.basketball-reference.com/teams/ATL/2023.html"

orl = "https://www.basketball-reference.com/teams/ORL/2023.html"
mem = "https://www.basketball-reference.com/teams/MEM/2023.html"
nop = "https://www.basketball-reference.com/teams/NOP/2023.html"
was = "https://www.basketball-reference.com/teams/WAS/2023.html"
sas = "https://www.basketball-reference.com/teams/SAS/2023.html"
dal = "https://www.basketball-reference.com/teams/DAL/2023.html"

hou = "https://www.basketball-reference.com/teams/HOU/2023.html"
pho = "https://www.basketball-reference.com/teams/PHO/2023.html"
gsw = "https://www.basketball-reference.com/teams/GSW/2023.html"
sac = "https://www.basketball-reference.com/teams/SAC/2023.html"
por = "https://www.basketball-reference.com/teams/POR/2023.html"
uta = "https://www.basketball-reference.com/teams/UTA/2023.html"

tim = "https://www.basketball-reference.com/teams/MIN/2023.html"
den = "https://www.basketball-reference.com/teams/DEN/2023.html"
okc = "https://www.basketball-reference.com/teams/OKC/2023.html"
nyk = "https://www.basketball-reference.com/teams/NYK/2023.html"
tor = "https://www.basketball-reference.com/teams/TOR/2023.html"
phi = "https://www.basketball-reference.com/teams/PHI/2023.html"

mil = "https://www.basketball-reference.com/teams/MIL/2023.html"
chi = "https://www.basketball-reference.com/teams/CHI/2023.html"
cle = "https://www.basketball-reference.com/teams/CLE/2023.html"
bkn = "https://www.basketball-reference.com/teams/BRK/2023.html"
det = "https://www.basketball-reference.com/teams/DET/2023.html"
ind = "https://www.basketball-reference.com/teams/IND/2023.html"

INJURED = set()    

def injury_scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
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
    


# injury_scrape("https://www.cbssports.com/nba/injuries/daily/")

# save_page(phi, "76ers")   
# save_page(mil, "bucks") 
# save_page(chi, "bulls")  
# save_page(cle, "cavaliers")    
# save_page(bos, "celtics")   
# save_page(lac, "clippers") 
# save_page(mem, "grizzlies")
# save_page(atl, "hawks")  
# save_page(heat, "heat")  
# save_page(cha, "hornets")       
# save_page(uta, "jazz")   
# save_page(sac, "kings")   
# save_page(nyk, "knicks") 
# save_page(lal, "lakers")  
# save_page(dal, "mavericks")  
# save_page(orl, "magic")   
# save_page(bkn, "nets") 
# save_page(den, "nuggets")  
# save_page(ind, "pacers") 
# save_page(nop, "pelicans") 
# save_page(det, "pistons") 
# save_page(tor, "raptors")   
# save_page(hou, "rockets")    
# save_page(sas, "spurs")  
# save_page(pho, "suns")   
# save_page(tim, "timberwolves") 
# save_page(okc, "thunder")    
# save_page(por, "trailblazers")  
# save_page(gsw, "warriors")  
# save_page(was, "wizards")  

# save_page_possession_time("http://stats.inpredictable.com/nba/ssnTeamPoss.php")

search_file("76ers")   
search_file("bucks") 
search_file("bulls")  
search_file("cavaliers")    
search_file("celtics")   
search_file("clippers") 
search_file("grizzlies")
search_file("hawks")  
search_file("heat")  
search_file("hornets")       
search_file("jazz")   
search_file("kings")   
search_file("knicks") 
search_file("lakers")  
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

  