# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def train_test_split(data):
    """
    This function creates a set for cross-validation
    :param data: pd.DataFrame
    :return train, test as 2 DataFrame with the same columns than data
    """

    if any(col not in data.columns for col in ["user_id", "ts_listen"]):
        raise IOError("The DF must contain fields user_id and ts_listen")

    data_by_user = data.groupby("user_id")
    user_ids = np.unique(data.user_id.values)

    idx_train = np.empty((0,), dtype='int64')
    idx_test = np.empty((0,), dtype='int64')

    for user_id in user_ids:
        df_user = data_by_user.get_group(user_id)

        # sort ts_listen values
        user_values = df_user.ts_listen.values
        sort_index = np.argsort(user_values)

        idx = df_user.index[sort_index]

        # eache user has a different train_length
        n_train_samples = int(len(user_values) / 2)

        # TODO: try different strategies when there is not enough samples to
        # put in train and test
        if n_train_samples == 0:
            continue

        idx_train = np.concatenate((idx_train, idx[:n_train_samples]), axis=0)
        idx_test = np.concatenate((idx_test,
                                   np.asarray(n_train_samples).reshape((1,))),
                                  axis=0)

    return data.iloc[idx_train], data.iloc[idx_test]


if __name__ == '__main__':
    df = pd.read_csv('../data/train.csv')
    train, test = train_test_split(df)
