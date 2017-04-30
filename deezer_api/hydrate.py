# -*- coding: utf-8 -*-
"""
Hydrate (get extra infos from deezer api)
Require package deezer-python
"""

import deezer
import pandas as pd
import numpy as np


def hydrate_tracks(tracks):
    client = deezer.Client()
    result = []

    for track_id in tracks:
        track = client.get_track(track_id)

        try:
            row = [track.id, track.rank, track.bpm, track.explicit_lyrics]
            result.append(row)
        except AttributeError:
            continue

    return result


def hydrate_albums(albums):
    client = deezer.Client()
    result = []

    for album_id in albums:
        album = client.get_album(album_id)

        try:
            row = [album.id, album.fans, album.rating]
            result.append(row)
        except AttributeError:
            continue

    return result


def hydrate_artists(artists):
    client = deezer.Client()
    result = []

    for artist_id in artists:
        artist = client.get_artist(artist_id)

        try:
            row = [artist.id, artist.name, artist.nb_album, artist.nb_fan]
            result.append(row)
        except AttributeError:
            continue

    return result


if __name__ == '__main__':
    train = pd.read_csv('../data/train.csv')
    test = pd.read_csv('../data/test.csv')

    # Tracks
    tracks = train.media_id.values
    tracks = np.concatenate((tracks, test.media_id.values))
    tracks = np.unique(tracks)
    track_data = hydrate_tracks(tracks)

    df = pd.DataFrame(track_data)
    df.columns = ['id', 'rank', 'bpm', 'is_explicit']
    df.to_csv('tracks.csv', index=False)

    # Artists
    artists = train.train_id.values
    artists = np.concatenate((artists, test.artist_id.values))
    artists = np.unique(artists)
    artist_data = hydrate_artists(artists)

    df = pd.DataFrame(artist_data)
    df.columns = ['id', 'nb_album', 'nb_fan']
    df.to_csv('artists.csv', index=False)

    # Albums
    albums = train.album_id.values
    albums = np.concatenate((albums, test.album_id.values))
    albums = np.unique(albums)
    album_data = hydrate_albums(albums)

    df = pd.DataFrame(album_data)
    df.columns = ['id', 'fans']
    df.to_csv('albums.csv', index=False)
