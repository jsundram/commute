import pandas as pd
import csv
import cStringIO
import json
import numpy as np
import seaborn as sns
import time

sns.set(style="darkgrid")


def to_minutes(s):
    """ Parse input that looks something like:
            "1 hour 0 mins"
            "46 mins"
            "1 hour 1 min"
    """
    try:
        end = -5 if s.endswith('mins') else -4  # min
        fields = map(int, s[:end].split(' hour '))
        return sum(f*60**i for (i, f) in enumerate(reversed(fields)))
    except ValueError: 
        return ''  # 0?

def round_ts(s, minutes=5):
    # TODO: resample is probably better:
    # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#up-and-downsampling
    # s looks like "2014-01-15 04:18 PM"
    fmt = "%Y-%m-%d %I:%M %p"
    time_struct = time.strptime(s, fmt)
    time_seconds = time.mktime(time_struct)

    seconds = minutes * 60
    rounded = time.localtime((time_seconds // seconds) * seconds)
    return time.strftime(fmt, rounded)

def to_csv(filename):
    out = cStringIO.StringIO()
    fieldnames = 'ts, home, work'.split(', ')
    w = csv.DictWriter(out, fieldnames)
    w.writeheader()
    with open(filename) as f:
        #{"home": "1 hour 0 mins", "time": "2014-01-15 04:18 PM", "work": "46 mins"}
        for line in f:
            d = json.loads(line)
            e = {
                'home': to_minutes(d.get('home', '')),
                'work': to_minutes(d.get('work', '')),
                'ts': round_ts(d['time'])
            }
            w.writerow(e)
    out.seek(0)
    if False:
        with open('data.csv', 'w') as f:
            f.write(out.getvalue())
    return out

def to_df(csv_buffer):
    df = pd.read_csv(csv_buffer, parse_dates=True, dayfirst=False, index_col='ts')
    df['time'] = df.index.time
    return df

def parse(filename='data.txt'):
    csv_buffer = to_csv(filename)
    return to_df(csv_buffer)

def plot(df):
    """
    plt = df.groupby('time').aggregate(np.mean)['home'].plot()
    plt.set_title('To Home')
    plt.set_ylabel('Minutes')
    plt.set_ybound(lower=0)

    # mean commute time under 40 minutes after 9:30am
    plt = df.groupby('time').aggregate(np.mean)['work'].plot()
    plt.set_title('To Work')
    plt.set_ylabel('Minutes')
    plt.set_ybound(lower=0)
    """

    # Convert it to "long-form" or "tidy" representation
    lf = pd.melt(df, id_vars=["time"], var_name="condition")

    # Plot the average value by condition and date
    palette = sns.color_palette('BrBG', 2)
    with palette:
        ax = lf.groupby(["condition", "time"]).mean().unstack("condition").plot(
                xticks=np.arange(0, 24*3600, 60*60*2),
                legend=False,
        )
    ax.set_xticklabels([time.strftime('%H:%M', time.gmtime(s)) for s in ax.get_xticks()])
        

    # Get a reference to the x-points corresponding to the dates and the the colors
    # x = np.arange(len(lf.time.unique()))
    secs = 300
    start, end = ax.get_xbound()
    x = np.arange(start, end + secs, secs)

    # Calculate the 25th and 75th percentiles of the data
    # and plot a translucent band between them
    for cond, cond_df in lf.groupby("condition"):
        low = cond_df.groupby("time").value.apply(np.percentile, 25)
        high = cond_df.groupby("time").value.apply(np.percentile, 75)
        ax.fill_between(x, low, high, alpha=.2, color=palette.pop(0))

    ax.set_ybound(lower=0)
    ax.set_ylabel('Minutes')
    ax.set_xlabel('Time of Day')
    ax.set_title('Commute Time')
    ax.legend(('Home', 'Work'))

    # rotate date to avoid overlap...
    # ax.figure.autofmt_xdate()

    return ax


def main():
    df = parse()

    plot(df)

    
if __name__ == '__main__':
    main()
