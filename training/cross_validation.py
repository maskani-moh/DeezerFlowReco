# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def train_test_split(data, n_splits=2):
    """
    This function creates a set for cross-validation
    :param data: pd.DataFrame
    :return: tuple(pd.DataFrame, pd.DataFrame, list)
    """

    if any(col not in data.columns for col in ["user_id", "ts_listen"]):
        raise IOError("The DF must contain fields user_id and ts_listen")

    data_by_user = data.groupby("user_id")
    user_ids = np.unique(data.user_id.values)

    idx_train = [[] for i in range(n_splits)]
    idx_test = [[] for i in range(n_splits)]

    timestamps = data.ts_listen.values
    timeframes = [[(0,0)] * np.max(user_ids) for i in range(n_splits)]

    for user_id in user_ids:
        df_user = data_by_user.get_group(user_id)

        # sort ts_listen values
        user_values = df_user.ts_listen.values
        sort_index = np.argsort(user_values)

        idx = df_user.index[sort_index]

        # eache user has a different train_length
        n_train_samples = int(np.ceil(len(user_values) / n_splits))
        
        if n_train_samples == 0:
            continue

        idx_chunks = chunks(range(len(user_values)), n_train_samples)
        train_chunks = []
        test_chunks = []
        ts_chunks = []

        for chunk in idx_chunks:
            # last chunk should be shifted to the left
            if chunk[-1] == len(user_values) - 1 and len(chunk) > 1:
                ts_chunks.append([idx[chunk[0]], idx[chunk[-2]]])
                train_chunks.append(idx[chunk[0:-1]])
                test_chunks.append(idx[chunk[-1]])
                
            # not enough samples to create a train and test set
            elif chunk[-1] == len(user_values) - 1:
                continue
            
            else:
                ts_chunks.append([idx[chunk[0]], idx[chunk[-1]]])
                train_chunks.append(idx[chunk])
                test_chunks.append(idx[chunk[-1] + 1])

  
        # users with not enough samples are ignored
        if len(train_chunks) < n_splits:
            continue

        for i in range(n_splits):
            timeframes[i][user_id] = (timestamps[ts_chunks[i][0]],
                                      timestamps[ts_chunks[i][1]])

            idx_train[i].extend(train_chunks[i].tolist())
            idx_test[i].extend([test_chunks[i]])

    for i in range(n_splits):
        idx_train[i] = np.asarray(idx_train[i], dtype='int64')
        idx_test[i] = np.asarray(idx_test[i], dtype='int64')

    return [(data.ix[idx_train[i]], data.ix[idx_test[i]], timeframes[i]) for i in range(n_splits)]


def check_timeframes(timeframes, test):
    """ Tests for the generated sets
    """
    user_ids = test.user_id.values
    ts = test.ts_listen.values
    for i in range(len(user_ids)):
        user_id = user_ids[i]
        ts_listen = ts[i]
        
        ts_begin, ts_end = timeframes[user_id]
        assert ts_begin <= ts_end
        assert ts_end < ts_listen


if __name__ == '__main__':
    df = pd.read_csv('../data/mini-train.csv')
    result = train_test_split(df, n_splits=3)
    
    # Test timeframes and test set
    for train, test, timeframe in result:
        check_timeframes(timeframe, test)
