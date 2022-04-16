from matplotlib import pyplot as plt
import matplotlib.dates as mdate
from matplotlib import patheffects
import datetime as dt
import time
import calendar
# noinspection PyUnresolvedReferences
import numpy as np
from myPackages.leaderboard_funcs import check_index


# gets the y ticks from the passed in axis and returns an appropriate replacement list of ticks that only includes ints
def make_yticks_ints(axs, y_num):
    init_yticks_np_arr = axs.get_yticks()

    # this uses numpy, don't remove import
    float_yticks = init_yticks_np_arr.tolist()

    yticks = []
    for i in float_yticks:
        # have to round to two places because np.tolist() adds a very small decimal place
        if round(i, 2).is_integer() and int(i) >= 0:
            yticks.append(int(i))

    if check_index(yticks, 0):
        if y_num == 'y1':
            # pads ytick arrays with few tick counts
            if yticks[0] == 1:
                yticks.insert(0, 2)
                yticks.insert(0, 3)
                yticks.insert(0, 4)
                yticks.insert(0, 5)
                yticks.append(0)
            elif len(yticks) < 4:
                plus_tick_amount = 5-len(yticks)
                for i in range(1, plus_tick_amount):
                    yticks.insert(0, yticks[0] - 1)
                yticks.append(yticks[-1] + 1)
                yticks.append(yticks[-1] + 1)
        elif y_num == 'y2':
            # pads ytick arrays with few tick counts
            if yticks[0] == 1:
                yticks.append(2)
                yticks.append(3)
                yticks.append(4)
                yticks.append(5)
                yticks.insert(0, 0)
            elif len(yticks) < 4:
                plus_tick_amount = 5-len(yticks)
                for i in range(1, plus_tick_amount):
                    yticks.append(yticks[0] + i)
                yticks.insert(0, yticks[0] - 1)
                yticks.insert(0, yticks[0] - 1)

    if check_index(yticks, 1) and yticks[0] == 0 and yticks[1] != 1 and y_num == 'y2':
        yticks[0] = 1

    return yticks


# plots two sets of data that share an x-axis
def plot_2y_axis(champ_name, data1, data2, y1label, y2label, time_len=86400, current_time=calendar.timegm(time.gmtime()), drawstyle='default', marker='', linestyle='solid'):

    start_time = current_time - time_len
    x1 = []
    x2 = []
    y1 = []
    y2 = []

    # adds ranking values to a list of x and y points within the time range
    for entry in data1:
        if entry[0] is not None and entry[1] > start_time:
            datetime = dt.datetime.fromtimestamp(entry[1])
            x1.append(datetime)
            y1.append(int(entry[0]))

    # adds one extra point at the beginning of the time range that's equal to the first point in range
    # makes the graph a lot more clear and helps when there isn't a lot of data
    if len(x1) and len(y1):
        datetime = dt.datetime.fromtimestamp(start_time + 60)
        x1.append(datetime)
        y1.append(y1[-1])

    for entry in data2:
        if entry[0] is not None and entry[1] > start_time:
            datetime = dt.datetime.fromtimestamp(entry[1])
            x2.append(datetime)
            y2.append(int(entry[0]))

    if len(x2) and len(y2):
        datetime = dt.datetime.fromtimestamp(start_time + 60)
        x2.append(datetime)
        y2.append(y2[-1])

    small_size = 10
    medium_size = 10
    bigger_size = 30

    ax1_ycolor = '#EEAF29'
    ax2_ycolor = '#7F8AE8'
    axes_xcolor = '#F8F8FF'

    plt.rc('font', size=small_size)  # controls default text sizes
    plt.rc('axes', titlesize=small_size)  # fontsize of the axes title
    plt.rc('axes', labelsize=medium_size)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=small_size)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=small_size)  # fontsize of the tick labels
    plt.rc('legend', fontsize=small_size)  # legend fontsize

    fig, ax1 = plt.subplots()
    fig.patch.set_facecolor('#40444B')
    ax1.patch.set_facecolor('#40444B')

    # ax1.set_xlabel(xlabel, color='#F2F2ED')
    # ax1.set_ylabel(y1label, color='#EEAF29')
    ax1.plot_date(x1, y1, color=ax1_ycolor, drawstyle=drawstyle, label=y1label, linestyle=linestyle, linewidth=2)

    # adds line glow to the plot
    #ax1.plot_date(x1, y1, color=ax1_ycolor, drawstyle=drawstyle, label=y1label, linestyle=linestyle, linewidth=4, alpha=0.4)
    #ax1.plot_date(x1, y1, color=ax1_ycolor, drawstyle=drawstyle, label=y1label, linestyle=linestyle, linewidth=6, alpha=0.2)

    ax1.tick_params(axis='y', labelcolor=ax1_ycolor)
    ax1.grid(color='#36393F')

    ax2 = ax1.twinx()
    # ax2.set_ylabel(y2label, color='#7F8AE8')
    ax2.plot_date(x2, y2, color=ax2_ycolor, drawstyle=drawstyle, label=y2label, linestyle=linestyle, linewidth=2)
    ax2.tick_params(axis='y', labelcolor=ax2_ycolor)
    ax1.tick_params(axis='x', labelcolor=axes_xcolor)

    for ax, color in zip([ax1, ax2], ['#202225', '#202225']):
        plt.setp(ax.spines.values(), color=color)
        plt.setp([ax.get_xticklines(), ax.get_yticklines()], color=color)

    for bar in ax1.spines:
        ax1.spines[bar].set_linewidth(3)
        # ax1.spines[bar].set_linestyle('dashed')
        # ax1.spines[bar].set_capstyle('butt')

    title = plt.title(champ_name, fontsize=bigger_size, color=axes_xcolor)
    # adds a title outline
    title.set_path_effects([patheffects.withStroke(linewidth=4, foreground='#202225')])

    date_format = mdate.DateFormatter('%I:%M %p, %b %d')

    fig.autofmt_xdate()
    ax2.xaxis.set_major_formatter(date_format)

    ax2.invert_yaxis()

    if not len(y1) or not len(y2):
        props = dict(boxstyle='round', facecolor='ivory', alpha=0.7)
        ax2.text(0.5, 0.5, "Not Enough Data!", transform=ax2.transAxes, fontsize=36,
                 va='center', ha='center', bbox=props)
        ax1.set_yticks([])
        ax1.set_xticks([])
        ax2.set_yticks([])
        fig.legend(bbox_to_anchor=(0.5, 0.70), loc='center')
    else:
        # this chunk makes ylabels that are 0 appear invisible, doing so provides a visual margin between rank one and zero
        new_y2_ticks = make_yticks_ints(ax2, 'y2')
        ax2.set_yticks(new_y2_ticks)
        if check_index(new_y2_ticks, 0) and new_y2_ticks[0] == 0:
            y2_ticks_labels = ax2.get_yticklabels()
            y2_ticks_labels[0].set_alpha(0)

        new_y1_ticks = make_yticks_ints(ax1, 'y1')
        ax1.set_yticks(new_y1_ticks)
        fig.legend(loc='upper left')

    fig.tight_layout()
    plt.show()

