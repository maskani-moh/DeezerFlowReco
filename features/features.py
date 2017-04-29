import numpy as np
import pandas as pd
import json

from .History import history

"""
General features
"""
def get_moment_of_day():
    pass

def get_season():
    pass

"""
User features
"""
def get_user_age_bucket():
    pass

def get_user_cluster():
    pass

def get_user_lang():
    pass

"""
Track features
"""
def get_track_age_bucket():
    pass

def get_track_lang():
    pass

def get_ranking():
    # bucketize ? top 10% on Deezer ?
    pass

def get_track_bpm():
    pass

def track_was_previously_listened():
    # Check in history
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

def is_top_n_track():
    # whether artist is in user's top N artists
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

def is_top_n_artist():
    # whether artist is in user's top N artists
    pass

def number_of_times_listened_to_artist_in_last_hour():
    pass
