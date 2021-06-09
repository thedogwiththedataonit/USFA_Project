#webscaping for the USFA results
#backend 

"========================================================"
"========================================================"

from pandas.core.indexes.base import Index
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np

from flask import Flask, request, render_template, session, redirect

#FULL RESULTS SCRAPE 
#https://www.usfencingresults.org/results/

#Junior nacs
comp_list = [["confirm","confirm"], #DB THIS
            ["October NAC 2017", "https://www.usfencingresults.org/results/2017-2018/2017.11-NOV-NAC/FTEvent_2017Nov10_U20ME.htm"],
            ["November NAC 2018", "https://www.usfencingresults.org/results/2018-2019/2018.11-NOV-NAC/FTEvent_2018Nov09_U20ME.htm"],
            ["January NAC 2018", "https://www.usfencingresults.org/results/2018-2019/2019.01-JAN-NAC/FTEvent_2019Jan04_U20ME.htm"],
            ["July NAC 2018", "https://www.usfencingresults.org/results/2017-2018/2018.06-JUN-SN/FTEvent_2018Jun28_U19ME.htm"],
            ["November NAC 2018", "https://www.usfencingresults.org/results/2018-2019/2018.11-NOV-NAC/FTEvent_2018Nov09_U20ME.htm"],
            ["January NAC 2019", "https://www.usfencingresults.org/results/2018-2019/2019.01-JAN-NAC/FTEvent_2019Jan04_U20ME.htm"],
            ["February NAC 2019", "https://www.usfencingresults.org/results/2018-2019/2019.02-FEB-JO/FTEvent_2019Feb15_U20ME.htm"],
            ["July NAC 2019", "https://www.usfencingresults.org/results/2018-2019/2019.06-JUN-SN/FTEvent_2019Jun28_U19ME.htm"],
            ["November NAC 2019", "https://www.usfencingresults.org/results/2019-2020/2019.11-NOV-NAC/FTEvent_2019Nov08_U20ME.htm"],
            ["February NAC 2020", "https://www.usfencingresults.org/results/2019-2020/2020.02-FEB-JO/FTEvent_2020Feb14_U20ME.htm"]
            ]           
#On webpage, have the month and year be drop down choices, so the reference name for the links is clear




def comp_manage(comp_name, comp_url, comp_list):

    comp_linked = []
    comp_linked.append(comp_name)
    comp_linked.append(comp_url)

    if (comp_linked in comp_list) == True:
        return (comp_list)
        
    else:
        comp_list.append(comp_linked)
        return (comp_list)

list_of_competitions = comp_manage("confirm", "confirm", comp_list)
"========================================================"

def competition_pool(url):

    req = requests.get(url)
    soup_url = BeautifulSoup(req.text, "html.parser")

    fencer_pools = soup_url.find_all("td", class_="poolNameCol")
    name_list = []
    club_list_pre = []

    for fencer in range(len(fencer_pools)): #Iterates through peoples names
        name = str(fencer_pools[fencer])

        for i in range(len(name)):
            if (name[i] == "<") and (name[i+1] == "b"):
                fencer_name = name[24:i]
                name_list.append(fencer_name)
            if (name[i]=="i") and (name[i+1]=="l") and (name[i+3]==">"):
                fencer_club =name[(i+4):-1] #SOMEHOW SLICE PRE OR POST LIST
                for j in range(len(fencer_club)):
                    if (fencer_club[j] == "/"):
                        club_list_pre.append(fencer_club[0:(j-1)])
                        break
                    else:
                        pass
                
            else:
                pass

    "================================================================================"

    oddrows = soup_url.find_all("tr", class_="poolOddRow")
    evenrows = soup_url.find_all("tr", class_="poolEvenRow")
    pool_fencer_num = soup_url.find_all("td", class_="poolPosCol")

    number_fencers_in_pool_list = []
    for num in range(len(pool_fencer_num)):
        counter = str(pool_fencer_num[num])
        fencer_count = counter[23]

        number_fencers_in_pool_list.append(fencer_count)

    "================================================================================"

    oddrows_list = []
    for scores in range(len(oddrows)):
        name_match = str(oddrows[scores])
        oddscores_list = []
        for value in range(len(name_match)):
            if (name_match[value]=="e") and (name_match[value-1]=="r") and (name_match[value+1]=="C"):
                bout_score = str(name_match[value+6]) + str(name_match[value+7])
                oddscores_list.append(bout_score)
                
            else:
                pass
        oddrows_list.append(oddscores_list)


    evenrows_list = []
    for scores in range(len(evenrows)):
        name_match = str(evenrows[scores])
        evenscores_list = []
        for value in range(len(name_match)):
            if (name_match[value]=="e") and (name_match[value-1]=="r") and (name_match[value+1]=="C") and (name_match[value+5]==">"):
                bout_score = str(name_match[value+6]) + str(name_match[value+7])
                evenscores_list.append(bout_score)
                
            else:
                pass
        evenrows_list.append(evenscores_list)

    "================================================================================"

    final_pools_list = []
    for g in range(len(number_fencers_in_pool_list)):
        if (int(number_fencers_in_pool_list[g]) % 2) == 0: #Check if even pool number
            final_pools_list.append(evenrows_list[0])
            del evenrows_list[0]
        else:
            final_pools_list.append(oddrows_list[0])
            del oddrows_list[0]

    index_num = list(range(1, len(name_list)+1))
    title_scrape = str(soup_url.select(".tournDetails"))
    division = title_scrape[28:45]
    date = title_scrape[58:76]

    title = "USFA NAC " +division + " " + date

    title_list = []
    for lol in range(len(name_list)):
        title_list.append(title)

    data = {"Title": title_list,
            "Name": name_list,
            "Club": club_list_pre,
            "Pool#": number_fencers_in_pool_list,
            "Pool_Results": final_pools_list

            }
    

    df = pd.DataFrame(data, index=index_num)

    return df

"========================================================"

competition_df1 = (competition_pool("https://www.usfencingresults.org/results/2017-2018/2017.11-NOV-NAC/FTEvent_2017Nov10_U20ME.htm"))
test_name = "Park, Thomas Junseo"

"========================================================"

def name_winloss(name, competition_df):
    for b in range(1,(len(competition_df["Name"])+1)): #iterating through index 
        #print(competition_df.at[b,"Name"])
        #print(b)
        if (competition_df.at[b,"Name"] == name):
            pool_bout = (competition_df.at[b,"Pool_Results"])
            #print(competition_df.at[b+1, "Pool_Results"][1]) #INDEXES SPECIFICALLY HOLY SHIT
            win_count = 0
            loss_count = -1

            bouts = []
            wins = []
            losses = []

            if (pool_bout[0] == "</"):
                for p in range(1,len(pool_bout)):
                    name_score = str(pool_bout[p]) + str(competition_df.at[b+p,"Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p, "Pool_Results"][0])
                    win_loss = name_score[:1]

                    if win_loss == "V":
                        wins.append(name_score[2:len(name_score)])
                    
                    if win_loss == "D":
                        losses.append(name_score[2:len(name_score)])

                    else:
                        pass
            
            if (pool_bout[1] == "</"):
                for p in range(0,len(pool_bout)):
                    if p == 1:
                        continue
                    else:
                        name_score = str(pool_bout[p]) + str(competition_df.at[b+p-1, "Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p-1, "Pool_Results"][1])
                        win_loss = name_score[:1]

                        if win_loss == "V":
                            wins.append(name_score[2:len(name_score)])
                    
                        if win_loss == "D":
                            losses.append(name_score[2:len(name_score)])

                        else:
                            pass

            if (pool_bout[2] == "</"):
                for p in range(0, len(pool_bout)):
                    if p == 2:
                        continue
                    else:
                        name_score = str(pool_bout[p]) + str(competition_df.at[b+p-2, "Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p-2, "Pool_Results"][2])
                        win_loss = name_score[:1]

                        if win_loss == "V":
                            wins.append(name_score[2:len(name_score)])
                    
                        if win_loss == "D":
                            losses.append(name_score[2:len(name_score)])

                        else:
                            pass
            
            if (pool_bout[3] == "</"):
                for p in range(0, len(pool_bout)):
                    if p == 3:
                        continue
                    else:
                        name_score = str(pool_bout[p]) + str(competition_df.at[b+p-3, "Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p-3, "Pool_Results"][3])
                        win_loss = name_score[:1]

                        if win_loss == "V":
                            wins.append(name_score[2:len(name_score)])
                    
                        if win_loss == "D":
                            losses.append(name_score[2:len(name_score)])

                        else:
                            pass

            if (pool_bout[4] == "</"):
                for p in range(0, len(pool_bout)):
                    if p == 4:
                        continue
                    else:
                        name_score = str(pool_bout[p]) + str(competition_df.at[b+p-4, "Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p-4, "Pool_Results"][4])
                        win_loss = name_score[:1]

                        if win_loss == "V":
                            wins.append(name_score[2:len(name_score)])
                    
                        if win_loss == "D":
                            losses.append(name_score[2:len(name_score)])

                        else:
                            pass

            if (pool_bout[5] == "</"):
                for p in range(0, len(pool_bout)):
                    if p == 5:
                        continue
                    else:
                        name_score = str(pool_bout[p]) + str(competition_df.at[b+p-5, "Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p-5, "Pool_Results"][5])
                        win_loss = name_score[:1]

                        if win_loss == "V":
                            wins.append(name_score[2:len(name_score)])
                    
                        if win_loss == "D":
                            losses.append(name_score[2:len(name_score)])

                        else:
                            pass

            if (len(pool_bout) == 7) and (pool_bout[6] == "</"):
                for p in range(0, len(pool_bout)):
                    if p == 6:
                        continue
                    else:
                        name_score = str(pool_bout[p]) + str(competition_df.at[b+p-6, "Name"]) + " | " + str(pool_bout[p]) + "-" + str(competition_df.at[b+p-6, "Pool_Results"][6])
                        win_loss = name_score[:1]

                        if win_loss == "V":
                            wins.append(name_score[2:len(name_score)])
                    
                        if win_loss == "D":
                            losses.append(name_score[2:len(name_score)])

                        else:
                            pass

            for g in range(len(pool_bout)):
                victory = pool_bout[g]
                if victory[0] == "V":
                    win_count = win_count + 1

                else:
                    loss_count = loss_count + 1
        
        else:
            continue #doesnt work when name is not present in the competition since wins is not defined before
    

    
    if (len(wins) < len(losses)):
        count = len(losses) - len(wins)
        match = 0
        while match < count:
            wins.append("NA")
            match = match + 1

    if (len(wins) > len(losses)):
        count = len(wins) - len(losses)
        match = 0
        while match < count:
            losses.append("NA")
            match = match + 1
    else:
        pass
    
    index_count = list(range(1,len(wins)+1))

    fencer_bouts = {"Won_Against: ": wins,
                    "Lost_Against: ": losses,
                    }

    fencer_df = pd.DataFrame(fencer_bouts, index=index_count)
    
    return(fencer_df)

"========================================================"

def driver(list_of_competitions, name): #loops through list of competitions, telling you which ones fencer was present then results of that individual
    for comp in range(1,len(list_of_competitions)):
        
        competition_df = competition_pool(list_of_competitions[comp][1])
        present = name_present(name, competition_df)
        if (present == True):
            print(list_of_competitions[comp][0])
            print(name +" Pool Results: ")
            print(name_winloss(name, competition_df))
            print(" ")
            print(" ")

        else:
            print(" ")
            print(name + " was not present at " + list_of_competitions[comp][0]) #ditcionary the htm. url with the title of the competition

        
"========================================================"

#Creating the Search algorithm
def name_present(name, competition_df):
    list = (competition_df["Name"].tolist())
    if (test_name in list) == True:
        return True

    else:
        return False

"========================================================"


#DRIVER
print(driver(list_of_competitions,test_name))
#print(driver(list_of_competitions, test_name))

#addressing specific parts of won and loss against datatable
#print(won_loss_df.at[1, "Won_Against: "])






#print(competition_pool("https://www.usfencingresults.org/results/2017-2018/2018.06-JUN-SN/FTEvent_2018Jun28_U19ME.htm"))

#create database that stores values, checks if the competitionurl.htm is exisiting or not in the database
#if not present in the database, call the fucntions to add to database

#check if name is present within the selected competition

"========================================================"
"========================================================"


#UI front end
#Lally
#json endpoints rather than react.js



