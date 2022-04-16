import _pickle
import time
from myPackages import leaderboard_funcs as board_funcs
from myPackages import stats_funcs, time_limited_input, plot_stats
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

    running = True
    updating_data = False
    clear_data = False

    while running:
        if clear_data:
            champions_dict = {}
        else:
            with open(champions_data, 'rb') as f:
                champions_dict = _pickle.load(f)

        if updating_data:
            with concurrent.futures.ProcessPoolExecutor() as e:

                f10 = e.submit(board_funcs.create_board_dictionary, 'https://aberoth.com/highscore/Most_Skillful_More.html')
                f20 = e.submit(board_funcs.create_board_dictionary, 'https://aberoth.com/highscore/Wealthiest_More.html')
                f30 = e.submit(board_funcs.create_board_dictionary, 'https://aberoth.com/highscore/Most_Valiant_More.html')

                champions_dict = board_funcs.update_champion_dictionary(
                    champions_dict, f10.result(), f20.result(), f30.result())

            # disable to prevent accidentally deleting data when the pickle file is being updated from multiple places
            # setting to false won't update the pickle file
            if updating_data:
                # writes over the pickle file that the data was read in from with the new pickle
                with open(champions_data, 'wb') as f:
                    _pickle.dump(champions_dict, f)

        # gets time since epoch with a precision of 1 second

        finish = time.perf_counter()

        # enabling allows searching a specific user's stats
        if True:
            search_name = input("Insert the champion you wish to search for:\n")
            search_name = search_name.lower().capitalize()

            board_funcs.print_champ_board_changes(search_name, champions_dict)
            print()
            # stats_funcs.print_champ_stats(search_name, champions_dict)
            if search_name in champions_dict:
                champ = champions_dict[search_name]

                plot_stats.plot_2y_axis(search_name, champ.skill_total_hist, champ.most_skillful_rank_hist,
                                        "Skill Total", "Most Skillful Rank", marker='o')
                plot_stats.plot_2y_axis(search_name, champ.gold_hist, champ.wealthiest_rank_hist,
                                        "Banked Gold", "Wealthiest Rank", marker='o')
                plot_stats.plot_2y_axis(search_name, champ.enemies_vanquished_hist, champ.valiant_rank_hist,
                                        "Enemies Vanquishes", "Most Valiant Rank", marker='o')

        if False:
            stats_dict = stats_funcs.gen_stats_dict(champions_dict)
            for champ in stats_dict:
                board_funcs.print_champ_board_changes(champ, champions_dict)
                print()
                stats_funcs.print_champ_stats(champ, champions_dict)

        print(f"\nCalculations execution time: {round(finish-start, 3)} seconds")

        if False:
            time_out_in_ms = 5400 * 1000
            time_limited_input.W_Input('Type anything to exit program', timeout=time_out_in_ms)
            user_input = time_limited_input.W_Input.data
            user_input = user_input.lower()

            if user_input:
                print("\nSafely exiting program")
                quit()
        if updating_data:
            time.sleep(5400)

if __name__ == "__main__":
    main()
