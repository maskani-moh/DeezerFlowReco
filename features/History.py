import json
import pandas as pd
from collections import Counter
from datetime import datetime
from multiprocess import Pool
import calendar

#########################
# Some useful functions #
#########################

def date_format(input_date):
    """
    Returns a tuple of datetime, string and timestamp equivalents from any of these 3 inputs
    At the second precision
    :param input_date: str, datetime.datetime or int, long | date as string, datetime or timestamp
    :return: tuple(str, datetime.datetime, int) all 3 versions of date_formats
    """
    if isinstance(input_date, str):
        dt = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
        ts = int(calendar.timegm(dt.utctimetuple()))
        st = input_date
    elif isinstance(input_date, datetime):
        dt = input_date
        ts = int(calendar.timegm(dt.utctimetuple()))
        st = str(dt)
    elif isinstance(input_date, (int, float)):
        input_date = int(round(input_date))
        dt = datetime.utcfromtimestamp(input_date)
        ts = input_date
        st = str(dt)
    else:
        raise(TypeError, "the input to date_formats should be of type basestring, datetime.datetime or int/long")
    return ts, dt, st

def agg(id, data):
    """
    Intermediary function used for multiprocessing
    """
    df_by_user = data.groupby("user_id").get_group(id).drop("user_id",axis=1)
    df_by_user.sort(columns=['ts_listen'], ascending=False,
                    inplace=True)
    return id, df_by_user

#########################
#     History Class     #
#########################

class History(object):
    def __init__(self, users=None, path=None):
        """
        Constructor of the class
        :param users: list, array | collection of users to get the history from
        :param path: string | path to the .json file containing the history.
                              Favour this case when you've already fitted and
                              saved an history instance on all the users.
        """
        self.path = path
        if path is None:
            self.users = list(set(users))
            self.history = dict()
        else:
            with open(path, "r") as f:
                self.history = json.load(f)
            self.users = [k for k in self.history]

    # The fields kept for the history, add any if needed
    COL_NAMES = ["user_id", "ts_listen", "media_id", "artist_id", "is_listened"]

    def dump(self, path):
        with open(path, "w") as f:
            json.dump(self.history, f)

    def fit_multiproc(self, data, cores=4):
        """
            Computes the listening history for all the users in self.users
        using multiple cores
        /!\ Make sure to install multiprocess 'pip install multiprocess'
        :param data: pd.Dataframe | data form which to get the history
        :param cores: int | number of cores to use
        :return: in place, modifies self.history
        """
        if any(col not in data.columns for col in self.COL_NAMES):
            raise IOError(
                "The dataframe must contain the fields: " + self.COL_NAMES)

        data = data[self.COL_NAMES]

        # Multithreaded computing
        p = Pool(cores)  # swith to max_cores
        tmp = p.map(lambda x: agg(x, data), self.users)
        p.close()

        # Update attribute
        for id, df in tmp:
            self.history[id] = df

    def fit(self, data):
        """
        Fit the instance to the data
        /!\ Can take a lot of time to fit depending on the training data

        :param data: pd.Dataframe | data to get the history from
        :return: inplace | modifies self.history
        """

        if any(col not in data.columns for col in self.COL_NAMES):
            raise IOError(
                "The dataframe must contain the fields: " + self.COL_NAMES)

        data = data[self.COL_NAMES]

        # Update attribute
        for id in self.users:
            df_by_user = data.groupby("user_id").get_group(id).drop("user_id",
                                                                    axis=1)
            df_by_user.sort(columns=['ts_listen'], ascending=False,
                            inplace=True)
            self.history[id] = df_by_user

    def get_current_history(self, id, start_date, end_date):
        """
        Get the history between two given dates
        :param id: int | id of the user
        :param start_date: int, float | start of the history
        :param end_date: int, float | end of the history
        :return: pd.DataFrame | history of the given user between the two dates
        """
        user_history = self.history[id]
        start, end = date_format(start_date)[0], date_format(end_date)[0]
        user_history = user_history[(user_history["ts_listen"] <= end) & (
        user_history["ts_listen"] >= start)]
        return user_history

    def get_top_tracks(self, id, n=10, start_date=None, end_date=None):
        """
        Get the most listened tracks from the user (between two dates if needed)
        :param id: int | id of the user
        :param n: int | top elements of the list
        :param start_date: int, float | start of the history
        :param end_date: int, float | end of the history
        :return: list | list of the n top tracks listened by th user
        """
        user_history = self.history[id]
        if start_date is not None and end_date is not None:
            user_history = self.get_current_history(id, start_date, end_date)
        ranking = Counter(user_history[id]["media_id"].values).most_common(n)
        return [t[0] for t in ranking]

    def get_top_artists(self, id, n=10, start_date=None, end_date=None):
        """
        Get the most listened artists from the user (between two dates if needed)
        :param id: int | id of the user
        :param n: int | top elements of the list
        :param start_date: int, float | start of the history
        :param end_date: int, float | end of the history
        :return: list | list of the n top artists listened by th user
        """
        user_history = self.history[id]
        if start_date is not None and end_date is not None:
            user_history = self.get_current_history(id, start_date, end_date)
        ranking = Counter(user_history["artist_id"].values).most_common(n)
        return [t[0] for t in ranking]


if __name__ == "__main__":
    """
    Here is how to generate the History of all the users from the raw data
    we've been given for the challenge
    """

    train = pd.read_csv("Users/mohamed/Documents/GitHub/data/train.csv")
    nb_users = 100
    hist = History(users=train.user_id.unique()[:nb_users])
    hist.fit(train)

    # Save the instance
    hist.dump("Users/mohamed/Documents/GitHub/data/history_100_users.json")

    # Multiprocessing
    #hist.fit_multiproc(train, cores=4)

    # Get the top-N artists and tracks
    user_id = 42
    N = 10
    top_artists = hist.get_top_artists(user_id, N)
    top_tracks = hist.get_top_tracks(user_id, N)
