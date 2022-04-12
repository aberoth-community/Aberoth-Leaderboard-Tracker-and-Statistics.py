import calendar
import _pickle
import time
from myPackages import multi_process_leaderboard_funcs as multi
import concurrent.futures
from pathlib import Path
from configparser import ConfigParser

def parse_config(path: str):
    config = ConfigParser()
    config.read(path)
    return config


def main():
    config = parse_config('config.cfg')
    champions_data = Path.joinpath(Path.home(), config['general']['path'])
    start = time.perf_counter()

    f = open(champions_data, 'rb')
    champions_dict = _pickle.load(f)
    f.close()

    # remove comment and run to reset champion data
    # champions_dict = {}

    print(calendar.timegm(time.gmtime()))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        f10 = executor.submit(multi.create_board_dictionary, 'https://aberoth.com/highscore/Most_Skillful.html')
        f20 = executor.submit(multi.create_board_dictionary, 'https://aberoth.com/highscore/Wealthiest.html')
        f30 = executor.submit(multi.create_board_dictionary, 'https://aberoth.com/highscore/Most_Valiant.html')

        champions_dict = multi.update_champion_dictionary(
            champions_dict, f10.result(), f20.result(), f30.result())

    print(calendar.timegm(time.gmtime()))

    # enabling allows searching a specific user's stats
    if True:
        search_name = input("insert the champion you wish to search for:\n")
        search_name = search_name.lower().capitalize()
        print(search_name)

        if search_name in champions_dict:
            print(
                f"{champions_dict[f'{search_name}'].champion_name}"
                f"\n\tSkill Rank Hist:\t\t {champions_dict[f'{search_name}'].most_skillful_rank_hist}"
                f"\n\tSkill Hist:\t\t\t\t {champions_dict[f'{search_name}'].skill_total_hist}\n\t"
                f"Wealth Rank Hist:\t\t {champions_dict[f'{search_name}'].wealthiest_rank_hist}"
                f"\n\tGold Hist:\t\t\t\t {champions_dict[f'{search_name}'].gold_hist}"
                f"\n\tValiant Rank Hist:\t\t {champions_dict[f'{search_name}'].valiant_rank_hist}"
                f"\n\tEnemies slain Hist:\t\t {champions_dict[f'{search_name}'].enemies_vanquished_hist}\n")
        else:
            print("Champion not found in top 10000")

    # creates a pickle in a file
    f = open(champions_data, 'wb')
    _pickle.dump(champions_dict, f)
    f.close()

    # gets time since epoch with a precision of 1 second
    print(calendar.timegm(time.gmtime()))

    finish = time.perf_counter()

    print(f"Execution time: {round(finish-start, 3)} seconds")


if __name__ == "__main__":
    main()

