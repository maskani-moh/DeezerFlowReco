# -*- coding: utf-8 -*-
import pandas as pd

def train_split_2(train, nb_songs):
    """ Split training data in train/test:

    Parameters
    ----------
    train: Pandas dataframe, training set
    nb_songs: Number of songs for each user in the test set
    
    Output
    ------
    train_f: Pandas dataframe, the new training fold
    test_f: Pandas dataframe, the test fold
    """

    train_sorted = train.sort_values(by='ts_listen')
    train_sorted['index'] = train_sorted.index
    
    train_index = set(train_sorted['index'].values)
    test_index = set()
    for k in range(nb_songs):
        current_test_index = train_sorted[train_sorted['listen_type'] == 1].groupby('user_id')['index'].nth(-(k+1)).values
        
        # Remove elements in test set from the train set
        train_index = train_index.difference(set(current_test_index))
        test_index = test_index.union(set(current_test_index))
    
    train_f = train_sorted.loc[train_index]
    test_f_temp = train_sorted.loc[test_index]
    # Make sure that every user in the test set are in the train set
    test_f = test_f_temp[test_f_temp['user_id'].isin(train_f['user_id'].unique())]

    return train_f, test_f

def train_split(train, nb_folds=1):
    """ Split training data in several folds of train/test:
    
    Parameters
    ----------
    train: Pandas dataframe, training set
    nb_folds: Number of folds wanted

    Output
    ------
    train_folds: list of the train folds indices
    test_folds: list of the test folds indices
    """

    train_sorted = train.sort_values(by='ts_listen')
    train_sorted['index'] = train_sorted.index
    
    train_folds = []
    test_folds_temp = []
    test_folds = []
    
    for k in range(nb_folds):
        train_index = set(train_sorted['index'].values)
        
        # Each test sets contain 1 song with Flow
        test_index = train_sorted[train_sorted['listen_type'] == 1].groupby('user_id')['index'].nth(-(k+1)).values
        
        # Remove elements in test set from the train set
        train_index = train_index.difference(set(test_index))
        train_folds.append(train_index)
        test_folds_temp.append(train_sorted.loc[test_index])
    
    for (k, test_f) in enumerate(test_folds_temp):
        # Make sure that each user_id in the test set is
        # the train set
        train_f = train_sorted.loc[train_folds[k]]
        new_test_f_index = set(test_f[test_f['user_id'].isin(train_f['user_id'].unique())]['index'].values)
        test_folds.append(new_test_f_index)

    return train_folds, test_folds