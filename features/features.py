import numpy as np
import pandas as pd
import json

from .History import date_format

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
    """
    Checks whether a track has already been listened by a user
    :param history: History instance | history of all users between two dates
    :param track_id: int | id of track
    :param user_id: int | user id
    :return: boolean | True if track already listened, else False
    """

    user_history = history.history[user_id]
    tracks_list = user_history[user_history.is_listened == 1]['media_id'].values

    return track_id in tracks_list

def is_top_n_track(history, user_id, track_id, n=10):
    """
    Checks whether a track is in user's favorite tracks
    :param history: History instance | history of all users between two dates
    :param user_id: int | user id
    :param track_id: int | id of track
    :param n: int | number of top tracks
    :return: boolean | True if track in user's top N tracks, else False
    """

    top_n_tracks = history.get_top_tracks(user_id, n)
    return track_id in top_n_tracks

def similar_to_previously_listened_track():
    # TODO: to implement
    pass

def number_of_similar_tracks_listened_to_in_the_last_hour():
    # TODO: to implement
    pass

def track_was_listened_by_cluster():
    # track listened by someone similar to current user
    # TODO: to implement
    pass

def get_genre(album_genres_df, album_id):
    """
    Get the genre of album (by extension that of the song)
    Up to 45 genres
    :param album_genres_df: pd.DataFrame | dataframe mapping each album to a genre
    :param album_id: int | album id
    :return:
    """
    return album_genres_df[album_genres_df.album_id == album_id].new_genre_name.values[0]


def categorise_media_duration(df):
    """
    Create very short/short/medium/long categories with media_duration

    Parameters
    ----------
    df: pd.DataFrame | contains a column media_duration
    """

    # Very short song
    df['media_duration_categ'] = 0

    # Short song
    df.loc[df['media_duration'] > 150, 'media_duration_categ'] = 1
    # Medium song
    df.loc[df['media_duration'] > 210, 'media_duration_categ'] = 2
    # Long song
    df.loc[df['media_duration'] > 300, 'media_duration_categ'] = 3

"""
Artist features
"""

def artist_was_previously_listened(history, user_id, artist_id):
    """
    Checks whether an artist has already been listened by a user
    :param history: History instance | history of all users between two dates
    :param artist_id: int | id of artist
    :param user_id: int | user id
    :return: boolean | True if track already listened, else False
    """

    user_history = history.history[user_id]
    artists = user_history[user_history.is_listened == 1]['artist_id'].values

    return artist_id in artists

def artist_was_listened_by_cluster():
    # track listened by someone similar to current user
    # TODO: to implement
    pass

def is_top_n_artist(history, user_id, artist_id, n=10):
    """
    Checks whether an artist is in user's favorite artists
    :param history: History instance | history of all users between two dates
    :param user_id: int | user id
    :param artist_id: int | id of artist
    :param n: int | number of top tracks
    :return: boolean | True if artist in user's top N artists, else False
    """

    top_n_artists = history.get_top_artists(user_id, n)
    return artist_id in top_n_artists

def number_of_times_listened_to_artist_in_last_hour():
    # TODO: to implement
    pass
