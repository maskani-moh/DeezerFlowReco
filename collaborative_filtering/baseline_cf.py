# -*- coding: utf-8 -*-

class BaselineCF():
    """ A simple model using the aggregated user/song preferences.
    """
    
    def __init__(self):
        self.listen_average = 0
        self.user_dict = None
        self.media_dict = None

    def fit(self, X):
        user_dict = X.groupby('user_id')['is_listened'].mean().to_dict()
        media_dict = X.groupby('media_id')['is_listened'].mean().to_dict()
        
        self.listen_average = X['is_listened'].mean()
        self.user_dict = user_dict
        self.media_dict = media_dict
        
    def predict(self, X):
        user_mean = X['user_id'].map(self.user_dict)
        media_mean = X['media_id'].map(self.media_dict)
        
        # User preference + media popularity - average of is_listened
        y_pred = user_mean + media_mean - self.listen_average
        
        # Normalise to [0, 1]
        y_pred = (y_pred - y_pred.min()) / (y_pred.max() - y_pred.min())
        return y_pred