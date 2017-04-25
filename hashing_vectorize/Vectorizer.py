import numpy as np
import pandas as pd

class Vectorizer():
    """
    Class to generate cross features
    """

    def __init__(self, transforms):
        """
        Constructor
        :param transforms: list, array | list of 3-tuples with the format
                                         (feature1_name, feature2_name, symbol)
        """
        self.transforms = transforms
        self.data = None

    def fit(self, data):
        """
        Fits the instance to the data
        :param data: pd.DataFrame | dataframe to fit
        :return: None | instanciate self.data
        """
        def _check(data):
            bool_ = True
            all_features = np.ravel(
                list(map(lambda t: (t[0], t[1]), self.transforms)))
            for feat in all_features:
                if feat not in data.columns:
                    raise IOError(
                        "%s must be a column of your dataframe" % feat)
                    bool_ = False
                    break
            return bool_

        if _check(data):
            self.data = data
        else:
            raise UserWarning("Fitting failed")

    def cross_features(self, feature_1, feature_2, symbol='&'):
        """

        :param feature_1: str | name of the first feature in the cross-feature
        :param feature_2: str | name of the second feature in the cross-feature
        :param symbol: str | symbol to join the values of the two features
        """
        feat1_values, feat2_values = self.data[feature_1], self.data[feature_2]
        zipped = list(zip(feat1_values, "&" * self.data.shape[0], feat2_values))
        new_col = list(
            map(lambda t: str(t[0]) + t[1] + str(t[2]), list(zipped)))
        # Update data
        self.data[feature_1 + symbol + feature_2] = new_col

    def transform(self, transforms):
        """
        Makes cross features from the transforms
        :param transforms: list | list of transformations
        :return: None | update self.data
        """
        for transform in transforms:
            self.cross_features(*transform)

    def fit_transform(self, data, transforms):
        """
        :param data: pd.DataFrame | data to fit and transform
        :param transforms: list | list of transform
        :return:
        """
        self.fit(data)
        self.transform(transforms)


if __name__ == "__main__":
    """
    Here is how to use a vectorizer
    """

    # Load data
    data = pd.read_csv("./data/train.csv")
    data = data[:1000]

    # Define a list of cross-features transformations
    # We use symbol "&"
    transforms = [('user_age', 'genre_id', '&'),
                  ('user_gender', 'artist_id', '&'),
                  ('genre_id', 'artist_id', '&')]

    # Instanciate Vectorizer
    vect = Vectorizer(transforms)

    # Fit and Transform
    vect.fit_transform(data=data, transforms=transforms)

    # Check that 3 new columns have been added
    data.columns