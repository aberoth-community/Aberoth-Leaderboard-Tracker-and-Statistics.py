import time
import calendar
from myPackages import classes


def calc_num_change(rank_hist, time_len, current_time=calendar.timegm(time.gmtime())):
    current_rank = rank_hist[0][0]
    first_rank_in_range = None
    first_time = current_time - time_len
    for entry in rank_hist:
        # stops incrementing through previous entries for first rank if outside time range or None rank
        if (entry[1] < first_time) or (entry[0] is None):
            break
        first_rank_in_range = entry[0]

    rank_change = current_rank - first_rank_in_range

    return rank_change


def calc_percent_change(value_hist, time_len, current_time=calendar.timegm(time.gmtime())):
    current_value = value_hist[0][0]
    first_value_in_range = None
    first_time = current_time - time_len
    for entry in value_hist:
        # stops incrementing through previous entries for first rank if outside time range or None rank
        if (entry[1] < first_time) or (entry[0] is None):
            break
        first_value_in_range = entry[0]

    percent_change = ((current_value - first_value_in_range) / first_value_in_range) * 100

    return percent_change


# takes a champion class and creates a StatsContainer class containing statistics about the champion
def gen_stats(champ):
    # expresses each time length in terms of seconds
    one_day = 86400
    times_lens = {
        'one_day': one_day,
        'one_week': one_day * 7,
        'thirty_days': one_day * 30,
        'half_a_year': one_day * 182.5,
        'one_year': one_day * 365}

    stats_class = classes.StatContainer(champ.champion_name)

    for entry in times_lens:
        # rank change calculation
        stats_class.skill_rank_stats[entry] = (calc_num_change(champ.most_skillful_rank_hist, times_lens[entry]))
        stats_class.wealth_rank_stats[entry] = (calc_num_change(champ.wealthiest_rank_hist, times_lens[entry]))
        stats_class.valiant_rank_stats[entry] = (calc_num_change(champ.valiant_rank_hist, times_lens[entry]))

        # ranking value change calculation
        stats_class.skill_total_stats[entry] = (calc_num_change(champ.skill_total_hist, times_lens[entry]))
        stats_class.gold_stats[entry]['quantity change'] = (calc_num_change(champ.gold_hist, times_lens[entry]))
        stats_class.enemies_vanquished_stats[entry]['quantity change'] = (calc_num_change(champ.enemies_vanquished_hist, times_lens[entry]))

        # value percent change calculation
        stats_class.gold_stats[entry]['percent change'] = (
            calc_percent_change(champ.gold_hist, times_lens[entry]))
        stats_class.enemies_vanquished_stats[entry]['percent change'] = (
            calc_percent_change(champ.enemies_vanquished_hist, times_lens[entry]))

    return stats_class


def gen_stats_dict(champions_dict):
    stats_dict = {}
    for champ in champions_dict:
        stats_dict[champ] = gen_stats(champ)

    return stats_dict


def print_champ_stats(search_name, champions_dict, decimals=3):
    if search_name in champions_dict:

        champ_stat_class = gen_stats(champions_dict[search_name])

        print(f"Champion: {champ_stat_class.champion_name}\n")

        print("Skill Rank Placement Stats:")
        for entry in champ_stat_class.skill_rank_stats:
            print(f"\t{entry} {champ_stat_class.skill_rank_stats[entry]}")

        print("Skill Total Stats:")
        for entry in champ_stat_class.skill_total_stats:
            print(f"\t{entry} {champ_stat_class.skill_total_stats[entry]}")

        print("Wealth Rank Placement Stats:")
        for entry in champ_stat_class.wealth_rank_stats:
            print(f"\t{entry} {champ_stat_class.wealth_rank_stats[entry]}")

        print("Gold Stats:")
        for entry in champ_stat_class.gold_stats:
            print(f"\t{entry} {champ_stat_class.gold_stats[entry]['quantity change']} "
                  f"({round(champ_stat_class.gold_stats[entry]['percent change'], decimals)}% change)")

        print("Valiant Rank Placement Stats:")
        for entry in champ_stat_class.valiant_rank_stats:
            print(f"\t{entry} {champ_stat_class.valiant_rank_stats[entry]}")

        print("Enemies Vanquished Stats:")
        for entry in champ_stat_class.enemies_vanquished_stats:
            print(f"\t{entry} {champ_stat_class.enemies_vanquished_stats[entry]['quantity change']} "
                  f"({round(champ_stat_class.enemies_vanquished_stats[entry]['percent change'], decimals)}% change)")

    else:
        print("Champion not found in indexed range!")