import time
import calendar
import requests
import re
from bs4 import BeautifulSoup
from myPackages import classes


def create_board_dictionary(url):
    print(f"Requesting {url}L: {time.asctime(time.gmtime())}")
    board_page = requests.get(url, headers={"User-Agent": "42.0.2311.135"})
    print(f"Got {url}: {time.asctime(time.gmtime())}")

    board_soup = BeautifulSoup(board_page.text, 'html.parser')

    board_dict = {}

    board_tr = board_soup.select('tr')
    for i in range(1, 10001):
        board_td = board_tr[i].select('td')

        # gets the specific cell and gets rid of white space to cast to int
        board_rank = int(re.search(r'\d+', board_td[0].get_text()).group())

        champ_name = board_td[1].get_text()

        board_stat = int(re.search(r'\d+', board_td[2].get_text()).group())

        board_dict[champ_name] = (board_stat, board_rank)

    return board_dict

def update_champion_dictionary(champions_dict, skill_dict, wealth_dict, valiant_dict, time_last_updated=calendar.timegm(time.gmtime())):
    for champ in skill_dict.keys():
        if champ in champions_dict.keys():
            # updates the current champion information if they're already in the champion_dict
            champions_dict[champ].most_skillful_rank_hist.insert(0, (skill_dict[champ][1], time_last_updated))
            champions_dict[champ].skill_total_hist.insert(0, (skill_dict[champ][0], time_last_updated))

            # checks to see if the entry data is duplicate
            if champions_dict[champ].most_skillful_rank_hist[0][0] == champions_dict[champ].most_skillful_rank_hist[1][0]:
                champions_dict[champ].most_skillful_rank_hist.pop(1)

            if champions_dict[champ].skill_total_hist[0][0] == champions_dict[champ].skill_total_hist[1][0]:
                champions_dict[champ].skill_total_hist.pop(1)

        else:
            # dynamically creates a champion class if one doesn't exist for the champion and adds it to the champion_dict
            champ_class = classes.Champion(champ, time_last_updated, most_skillful_rank=skill_dict[champ][1],
                                           skill_total=skill_dict[champ][0])
            champions_dict[champ] = champ_class

    for champ in wealth_dict.keys():
        if champ in champions_dict.keys():
            champions_dict[champ].wealthiest_rank_hist.insert(0, (wealth_dict[champ][1], time_last_updated))
            champions_dict[champ].gold_hist.insert(0, (wealth_dict[champ][0], time_last_updated))

            # checks to see if the entry data is duplicate
            if champions_dict[champ].wealthiest_rank_hist[0][0] == champions_dict[champ].wealthiest_rank_hist[1][0]:
                champions_dict[champ].wealthiest_rank_hist.pop(1)

            if champions_dict[champ].gold_hist[0][0] == champions_dict[champ].gold_hist[1][0]:
                champions_dict[champ].gold_hist.pop(1)

        else:
            # dynamically creates a champion class if one doesn't exist for the champion and adds it to the champion_dict
            champ_class = classes.Champion(champ, time_last_updated, wealthiest_rank=wealth_dict[champ][1],
                                           gold=wealth_dict[champ][0])
            champions_dict[champ] = champ_class

    for champ in valiant_dict.keys():
        if champ in champions_dict.keys():
            champions_dict[champ].valiant_rank_hist.insert(0, (valiant_dict[champ][1], time_last_updated))
            champions_dict[champ].enemies_vanquished_hist.insert(0, (valiant_dict[champ][0], time_last_updated))

            # checks to see if the entry data is duplicate
            if champions_dict[champ].valiant_rank_hist[0][0] == champions_dict[champ].valiant_rank_hist[1][0]:
                champions_dict[champ].valiant_rank_hist.pop(1)
            if champions_dict[champ].enemies_vanquished_hist[0][0] == champions_dict[champ].enemies_vanquished_hist[1][0]:
                champions_dict[champ].enemies_vanquished_hist.pop(1)

            # allows us to call champion methods on dynamically named classes
            # classmap = {f'{champ}': classes.Champion}

        else:
            # dynamically creates a champion class if one doesn't exist for the champion and adds it to the champion_dict
            champ_class = classes.Champion(champ, time_last_updated, valiant_rank=valiant_dict[champ][1],
                                           enemies_vanquished=valiant_dict[champ][0])
            champions_dict[champ] = champ_class

    return champions_dict
