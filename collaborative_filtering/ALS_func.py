# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pyspark.mllib.recommendation import Rating
from pyspark.sql import SQLContext

def convert_rdd(df, sc):
    """ Convert dataframe to rdd using SQLContext

    Parameters
    ----------
    df: Pandas dataframe
    sc: SparkContext
    
    Output
    ------
    df_rdd: RDD of df
    """
    sqlContext = SQLContext(sc)
    df_rdd = sqlContext.createDataFrame(df[['user_id', 'media_id', 'is_listened']]).rdd
    df_rdd = df_rdd.map(lambda r: Rating(int(r[0]), int(r[1]), float(r[2])))
    return df_rdd

def compute_y_pred(test_f, predictions, user_dict):
    """ Link the predictions to test_f and fill NA with user_dict 

    Parameters
    ----------
    
    Output
    ------

    """

    ALS_pred = np.array(predictions.map(lambda r: [r[0][0], r[0][1], r[1]]).collect())

    ALS_pred_df = pd.DataFrame({'user_id': ALS_pred[:, 0],
                                'media_id': ALS_pred[:, 1],
                                'is_listened_pred': ALS_pred[:, 2]})
    ALS_pred_df['user_id'] = ALS_pred_df['user_id'].astype(int)
    ALS_pred_df['media_id'] = ALS_pred_df['media_id'].astype(int)

    test_f_merged = test_f.merge(ALS_pred_df, how='left', on=['user_id', 'media_id'])
    
    # Compute missing values with user avg
    test_f_merged.loc[np.isnan(test_f_merged['is_listened_pred']), 'is_listened_pred'] = \
        test_f_merged.loc[np.isnan(test_f_merged['is_listened_pred']), 'user_id'].map(user_dict)
    
    # Join the predictions to the original data. Delete instances in data that 
    # does not match the ones in predictions
    #data_pred = data.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    #y_true = np.array(data_pred.map(lambda r: (r[1][0])).collect())
    #y_pred = np.array(data_pred.map(lambda r: (r[1][1])).collect())
    y_pred = test_f_merged['is_listened_pred'].values
    test_f_merged['is_listened_pred'] = (y_pred - min(y_pred)) / (max(y_pred) - min(y_pred))

    return test_f_merged[['user_id', 'media_id', 'is_listened', 'is_listened_pred']]