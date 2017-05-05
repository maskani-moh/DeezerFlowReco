# -*- coding: utf-8 -*-
import pandas as pd
import json
import datetime

def preprocess_media_ids(df):
    """ Clean the duplicate media_ids
    
    About 20,000 media_ids contain duplicates -
    same song, album and artist name but different media_id.
    
    Parameters
    ----------
    df: Pandas dataframe containing a column media_id
    """

    with open('./preprocessing/unique_media_id.json') as f:
        unique_media_list = json.load(f).values()
    
    # Dictionary with key=duplicate media_ids, value=original media_id
    unique_media_dict = dict()
    for elt in unique_media_list:
        for duplicate in elt[1:]:
            unique_media_dict[duplicate] = elt[0]
            
    # Duplicate elements without the original media_ids
    unique_media_unravel = []
    for elt in unique_media_list:
        unique_media_unravel.extend(elt[1:])

    mask_duplicates = df['media_id'].isin(unique_media_unravel)
    df.loc[mask_duplicates, 'media_id'] = df.loc[mask_duplicates, 'media_id'].map(unique_media_dict)

def convert_ts(ts):
    """ Convert a timestamp to a date %Y-%m-%d %H:%M:%S
    
    Parameters
    ----------
    ts: Timestamp
    
    Output
    ------
    formatted_date: datetime %Y-%m-%d %H:%M:%S
    """
    
    formatted_date = datetime.datetime.fromtimestamp(
        ts).strftime('%Y-%m-%d %H:%M:%S')
    return(formatted_date)

def parse_ts(df):
    """ Create year/month/day/hour columns from ts_listen
    
    Parameters
    ----------
    df: Pandas dataframe containing a column ts_listen
    """
    
    df['ts_listen_fmt'] = df['ts_listen'].map(convert_ts)

    # Parse year/month/day/hour
    df['year_listen'] = pd.DatetimeIndex(df['ts_listen_fmt']).year
    df['month_listen'] = pd.DatetimeIndex(df['ts_listen_fmt']).month
    df['day_listen'] = pd.DatetimeIndex(df['ts_listen_fmt']).day
    df['hour_listen'] = pd.DatetimeIndex(df['ts_listen_fmt']).hour


def categorise_media_duration(df):
    """ Create very short/short/medium/long categories with media_duration
    
    Parameters
    ----------
    df: Pandas dataframe containing a column media_duration
    """

    # Very short song
    df['media_duration_categ'] = 0
    
    # Short song
    df.loc[df['media_duration'] > 150, 'media_duration_categ'] = 1
    # Medium song
    df.loc[df['media_duration'] > 210, 'media_duration_categ'] = 2
    # Long song
    df.loc[df['media_duration'] > 300, 'media_duration_categ'] = 3

def full_preprocessing(df):
    """ Full preprocessing as specified above
    
    Parameters
    ----------
    df: Pandas dataframe
    """
    preprocess_media_ids(df)
    parse_ts(df)
    categorise_media_duration(df)
