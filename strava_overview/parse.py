# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_parse.ipynb (unless otherwise specified).

__all__ = ['interpolate', 'moving_average', 'training_impulse', 'parse_tss']

# Cell
from .to_csv import *
import pandas as pd
import numpy as np

# Cell
def interpolate(df):
    df.index = df['time']
    df2 = df.reindex(np.arange(df.index[-1]))
    df2 = df2.interpolate()
    return df2

# Cell
def moving_average(time_series, window_len):
    """Calculates the moving average of an unevenly spaced time series.

    This moving average implementation weights each value by the time it remained
    unchanged, which conceptually matches smart recording on GPS devices: a sample
    is taken when some value changes sufficiently, so before a new sample is taken
    the previous one is assumed to be more or less constant.

    The term "area" below means a sum of time-weighted values.

    This implementation follows the SMA_last algorithm proposed
    in (Eckner, 2017) (see README for citation).

    Args:
    time_series: A pandas.Series of the values to average,
                 indexed with timestamps.
    window_len: The size of the moving average window, in seconds.

    Returns:
    A numpy array of length len(time_series) containing the
    moving average values
    """
    # Re-index the time series with duration in seconds from the first value
#     time_series.index = (
#       (time_series.index
#        - time_series.index[0]) / np.timedelta64(1, 's')).astype('int')

    window_area = time_series.iloc[0] * window_len

    # It may not always be possible to construct a window of length exactly equal
    # to window_len using timestamps present in the data. To handle this, the left
    # side of the window is allowed to fall between timestamps (the right side is
    # always fixed to a timestamp in the data). Therefore we need to separately
    # compute the area of the inter-timestamp region on the left side of the
    # window so that it can be added to the window area. left_area is that value.
    left_area = window_area

    out = np.zeros(len(time_series))
    out[0] = time_series.iloc[0]

    # i is the left side of the window and j is the right
    i = 0
    for j in range(1, len(time_series)):
        # Remove the last iteration's left_area as a new right window bound may
        # change the left_area required in this iteration
        window_area -= left_area

        # Expand window to the right
        window_area += time_series.iloc[j-1] * (time_series.index[j]
                                                - time_series.index[j-1])

        # Shrink window from the left if expanding to the right has created too
        # large a window. new_left_time may fall between timestamps present in the
        # data, which is fine, since that's handled by left_area.
        new_left_time = time_series.index[j] - window_len
        while time_series.index[i] < new_left_time:
            window_area -= time_series.iloc[i] * (time_series.index[i+1]
                                                - time_series.index[i])
            i += 1

        # Add left side inter-timestamp area to window
        left_area = time_series.iloc[max(0, i - 1)] * (time_series.index[i]
                                                       - new_left_time)
        window_area += left_area

        out[j] = window_area / window_len

    return out

# Cell
def training_impulse(norm_p, total_time, ftp):
    intesity = norm_p/float(ftp)
    return (total_time*norm_p * intesity)/(float(ftp)*3600.) *100


# Cell
def parse_tss(df, threshold = 179, ftp = 339):
    df.index = df['time']
    df.reindex(np.arange(df.index[-1]))
    if 'watts' in list(df.columns):
        df['ftp'] = df['watts']
        print('watts')
    elif 'heartrate' in list(df.columns):
        df['ftp'] = (df['heartrate'])/ (threshold)
    else:
        print(df.columns)
    return df
