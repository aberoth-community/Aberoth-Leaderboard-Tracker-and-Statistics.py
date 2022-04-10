import time


class Champion:
    def __init__(self, champion_name, time_last_updated=time.gmtime(), most_skillful_rank=None, skill_total=None,
                 wealthiest_rank=None, gold=None, valiant_rank=None, enemies_vanquished=None):

        self.champion_name = champion_name

        self.most_skillful_rank_hist = [(most_skillful_rank, time_last_updated)]
        self.skill_total_hist = [(skill_total, time_last_updated)]

        self.wealthiest_rank_hist = [(wealthiest_rank, time_last_updated)]
        self.gold_hist = [(gold, time_last_updated)]
        self.gold_PC_change_1_day = None
        self.gold_PC_change_1_week = None
        self.gold_PC_change_1_month = None

        self.valiant_rank_hist = [(valiant_rank, time_last_updated)]
        self.enemies_vanquished_hist = [(enemies_vanquished, time_last_updated)]

        self.time_last_updated = time_last_updated
