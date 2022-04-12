import calendar
import _pickle
import time
from myPackages import leaderboard_funcs as board_funcs
from myPackages import stats_funcs
import concurrent.futures
from pathlib import Path
from configparser import ConfigParser


def parse_config(path: str):
    config = ConfigParser()
    config.read(path)
    return config


def main():
    start = time.perf_counter()

    config = parse_config('config.cfg')
    champions_data = Path.joinpath(Path.home(), config['general']['path'])
    start = time.perf_counter()

    with open(champions_data, 'rb') as f:
        champions_dict = _pickle.load(f)

    # remove comment and run to reset champion data
    # champions_dict = {}

    print(calendar.timegm(time.gmtime()))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        f10 = executor.submit(board_funcs.create_board_dictionary, 'https://aberoth.com/highscore/Most_Skillful.html')
        f20 = executor.submit(board_funcs.create_board_dictionary, 'https://aberoth.com/highscore/Wealthiest.html')
        f30 = executor.submit(board_funcs.create_board_dictionary, 'https://aberoth.com/highscore/Most_Valiant.html')

        champions_dict = board_funcs.update_champion_dictionary(
            champions_dict, f10.result(), f20.result(), f30.result())

    print(calendar.timegm(time.gmtime()))

    # creates a pickle in a file
    with open(champions_data, 'wb') as f:
        _pickle.dump(champions_dict, f)

    # gets time since epoch with a precision of 1 second
    print(calendar.timegm(time.gmtime()))

    finish = time.perf_counter()

    # enabling allows searching a specific user's stats
    if True:
        search_name = input("Insert the champion you wish to search for:\n")
        search_name = search_name.lower().capitalize()

        stats_funcs.print_champ_stats(search_name, champions_dict)
        print()
        board_funcs.print_champ_board_changes(search_name, champions_dict)

    print(f"Calculations execution time: {round(finish-start, 3)} seconds")


if __name__ == "__main__":
    main()

