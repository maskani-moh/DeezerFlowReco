# -*- coding: utf-8 -*-
import pandas as pd

class BaselineCF():
    """ A simple model using the aggregated user/song preferences.
    """
    
    def __init__(self):
        self.global_baseline = 0
        self.user_dict = None
        self.media_dict = None

    def fit(self, X):
        user_dict = X.groupby('user_id')['is_listened'].mean().to_dict()
        media_dict = X.groupby('media_id')['is_listened'].mean().to_dict()
        
        self.global_baseline = X['is_listened'].mean()
        self.user_dict = user_dict
        self.media_dict = media_dict
        
    def predict(self, X):
        user_mean = X['user_id'].map(self.user_dict).fillna(self.global_baseline) # Fillna should not be necessary
        # Fill missing media_mean with 0
        media_mean = X['media_id'].map(self.media_dict).fillna(self.global_baseline)
        
        # Better way to treat missing media_id would be to
        # match with existing albums, genres etc.
        # unmatched_2 = test_cv_2[~test_cv_2['media_id'].isin(train_cv['media_id'])]
        # Album id then genre_id
        # unmatched_2['genre_id'].isin(train_cv['genre_id']).mean()
        # np.isnan(test_cv_2['media_mean']).mean()

        # User preference + media popularity - average of is_listened
        y_pred = user_mean + media_mean - self.global_baseline
        
        #####
        # To do: find better normalisation
        #####
        
        # Normalise to [0, 1] doesn't change a lot with logit function
        y_pred = (y_pred - y_pred.min()) / (y_pred.max() - y_pred.min())
        #y_pred = 1 / (1 + np.exp(-y_pred))
        return y_pred