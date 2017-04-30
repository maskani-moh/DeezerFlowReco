import numpy as np
import pandas as pd
import json

from .History import date_format, History

"""
General features
"""
def get_moment_of_day(ts_listen):
    """
    Gets the moment of the day
    :param ts_listen: int | timestamp of listening
    :return: string | element of MOMENTS.keys()
    """

    # Define the moments of the day
    MOMENTS = {
        "early_morning": (6, 8),
        "morning": (9, 12),
        "day": (12, 17),
        "evening": (17, 22),
        "late_night": (23, 5)
    }

    # Get the hour of listening
    hour = date_format(ts_listen)[1].hour

    # Get the corresponding moment
    moment = [k for (k, v) in MOMENTS.items() if v[0] <= hour <= v[1]][0]

    return moment

def get_season(ts_listen):
    """
    Gets the season corresponding to the timestamp of listening
    :param ts_listen: int | timestamp of listening
    :return: string | element of SEASONS.keys()
    """

    # Define the seasons
    SEASONS = {
        "spring": (3, 5),
        "summer": (6, 8),
        "autumn": (9, 11),
        "winter": (0, 2)
    }

    # Get the month of listening
    month = date_format(ts_listen)[1].month % 12

    # Get the corresponding moment
    season = [k for (k, v) in SEASONS.items() if v[0] <= month <= v[1]][0]

    return season

"""
User features
"""
def get_user_age_bucket(user_age):
    """
    Bucketize the age of the user
    :param user_age: int | age of the user
    :return: string | bucket of age
    """

    # Define age buckets: ages between 18 and 30
    BUCKETS = {
        "[18-21]" : (18, 21),
        "[22-25]" : (22, 25),
        "[26-30]" : (26, 30)
    }

    # Get user bucket
    bucket = [k for (k, v) in BUCKETS.items() if v[0] <= user_age <= v[1]][0]

    return bucket

def get_user_cluster():
    # TODO: implement
    pass

def get_user_lang():
    # TODO: implement
    pass

"""
Track features
"""
def get_track_age_bucket(track_release_date):
    """
    Get the "generation" of a track given its release date
    :param track_release_date: int | format YYYYMMDD : date of release
    :return: string | decade of release of the track
    """

    # Buckets defined thanks to :
    BUCKETS = {
        "50s" : (1950, 1959),
        "60s" : (1960, 1969),
        "70s" : (1970, 1979),
        "80s" : (1980, 1989),
        "90s" : (1990, 1999),
        "00s" : (2000, 2009),
        "10s" : (2010, 2019),
    }

    # Get release year of song: parse YYYYMMDD
    year = track_release_date // 10000

    # Deal with outliers (cf. dates distribution)
    # TODO: remove once the data has been cleaned
    if year == 3000:
        return "00s" # teenage years of most users
    elif year < 1950:
        return "old"
    else:
        # Get bucket
        bucket = [k for (k, v) in BUCKETS.items() if v[0] <= year <= v[1]][0]
        return bucket

def is_new_track(track_release_date, ts_listen):
    """
    Checks if the track was released the year of listening
    :param track_release_date: int | format YYYYMMDD: date of release
    :param ts_listen: int | timestamp of listening
    :return: boolean | whether the track is released the same year or not
    """

    year_release = track_release_date // 10000
    year_listen = date_format(ts_listen).year

    if year_release == year_listen:
        return True

    #TODO: We can add a difference of 1 year to consider it "new"
    return False

def get_track_lang():
    # TODO: to implement
    pass

def get_ranking_bucket(tracks_df, track_id):
    """
    Get the rank bucket of a track
    The higher the rank, the most famous the song is
    :param tracks_df: pd.DataFrame | the dataframe of tracks
    :param track_id: int | track id
    :return: string | bucket describing how famous the track is
    """

    # Levels got by taking a look at the distribution of songs:
    # plt.plot(range(len(tracks['rank'])),np.sort(tracks['rank']))
    # TODO: adjust if necessary
    BUCKET_RANKING = {
        "not_famous" : (0, 280000),
        "normal" : (280001, 330000),
        "quite_famous" : (330001, 530000),
        "really_famous" : (530001, 1000000)
    }

    # Get ranking from tracks dataframe
    rank = tracks_df[tracks_df['id'] == track_id]['rank'].values[0]

    # Get bucket
    bucket = [k for (k, v) in BUCKET_RANKING.items() if v[0] <= rank <= v[1]][0]

    return bucket

def get_track_tempo(tracks_df, track_id):
    """
    Get the tempo of the track as defined by
    https://fr.wikipedia.org/wiki/Battement_par_minute
    :param tracks_df: pd.DataFrame | the dataframe of tracks
    :param track_id: int | track id
    :return: string | tempo of the track
    """

    # TODO: Make sure that the track dataframe does not contain bpm with value 0
    # TODO: adjust to be more specific if needed
    BUCKET_BPM = {
        "very_slow" : (25, 65),
        "slow" : (66, 80),
        "moderate" : (81, 99),
        "fast" : (100, 120),
        "very_fast": (121, 1000)
    }

    # Get bpm from tracks dataframe
    bpm = tracks_df[tracks_df['id'] == track_id]['bpm'].values[0]

    # Get bucket
    bucket = [k for (k, v) in BUCKET_BPM.items() if v[0] <= bpm <= v[1]][0]

    return bucket

def track_was_previously_listened(history, track_id, user_id):
    # Check in history
    pass

def is_top_n_track(history, user_id, track_id):
    # whether artist is in user's top N artists
    pass

def similar_to_previously_listened_track():
    pass

def number_of_similar_tracks_listened_to_in_the_last_hour():
    pass

def track_was_listened_by_cluster():
    # track listened by someone similar to current user
    pass

def get_lower_genre():
    # number of genre-id too big
    # can be too specific
    pass

"""
Artist features
"""

def artist_was_previously_listened():
    # Check in history
    pass

def artist_was_listened_by_cluster():
    # track listened by someone similar to current user
    pass

def is_top_n_artist(history, user_id, artist_id):
    # whether artist is in user's top N artists
    pass

def number_of_times_listened_to_artist_in_last_hour():
    pass
