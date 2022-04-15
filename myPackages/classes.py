import time


# stores the level board history for a champion
class Champion:
    def __init__(self, champion_name, time_last_updated=time.gmtime(), most_skillful_rank=None, skill_total=None,
                 wealthiest_rank=None, gold=None, valiant_rank=None, enemies_vanquished=None):

        self.champion_name = champion_name

        self.most_skillful_rank_hist = [(most_skillful_rank, time_last_updated)]
        self.skill_total_hist = [(skill_total, time_last_updated)]

        self.wealthiest_rank_hist = [(wealthiest_rank, time_last_updated)]
        self.gold_hist = [(gold, time_last_updated)]

        self.valiant_rank_hist = [(valiant_rank, time_last_updated)]
        self.enemies_vanquished_hist = [(enemies_vanquished, time_last_updated)]

        self.time_last_updated = time_last_updated


# stores the statistics associated with the board history for a champion
class StatContainer:
    def __init__(self, champion_name, time_last_updated=time.gmtime()):

        self.champion_name = champion_name
        self.time_last_updated = time_last_updated

        self.skill_rank_stats = {'one_day': None, 'one_week': None, 'thirty_days': None, 'half_a_year': None, 'one_year': None}
        self.skill_total_stats = {'one_day': None, 'one_week': None, 'thirty_days': None, 'half_a_year': None, 'one_year': None}

        self.wealth_rank_stats = {'one_day': None, 'one_week': None, 'thirty_days': None, 'half_a_year': None, 'one_year': None}
        self.gold_stats = {'one_day': {'quantity change': None, 'percent change': None},
                           'one_week': {'quantity change': None, 'percent change': None},
                           'thirty_days': {'quantity change': None, 'percent change': None},
                           'half_a_year': {'quantity change': None, 'percent change': None},
                           'one_year': {'quantity change': None, 'percent change': None}}

        self.valiant_rank_stats = {'one_day': None, 'one_week': None, 'thirty_days': None, 'half_a_year': None, 'one_year': None}
        self.enemies_vanquished_stats = {'one_day': {'quantity change': None, 'percent change': None},
                                         'one_week': {'quantity change': None, 'percent change': None},
                                         'thirty_days': {'quantity change': None, 'percent change': None},
                                         'half_a_year': {'quantity change': None, 'percent change': None},
                                         'one_year': {'quantity change': None, 'percent change': None}}
