# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import itertools
from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS, Rating
from pyspark.sql import SQLContext

from sklearn.metrics import roc_auc_score


# Convert dataframe to rdd using SQLContext
def convert_rdd(df, sc):
    sqlContext = SQLContext(sc)
    df_rdd = sqlContext.createDataFrame(df[['user_id', 'media_id', 'is_listened']]).rdd
    df_rdd = df_rdd.map(lambda r: Rating(int(r[0]), int(r[1]), float(r[2])))
    return df_rdd


def compute_y_pred(test_f, predictions, user_dict):
    """
    ROC AUC with rdd data
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
    y_true = test_f_merged['is_listened']
    y_pred = test_f_merged['is_listened_pred']
    y_pred = (y_pred - min(y_pred)) / (max(y_pred) - min(y_pred))

    return (y_true, y_pred)

if __name__ == '__main__':

	rank = 8
	lmbda = 0.1
	iterations = 10

	sc = SparkContext(conf=conf)

	# Need a column 'is_listened' in convert_rdd
	test['is_listened'] = 0
	train_rdd = convert_rdd(train, sc)
	test_rdd = convert_rdd(test, sc)

	model = ALS.train(train_rdd, rank=rank, 
	                  iterations=iterations, lambda_=lmbda,
	                  seed=random_seed)

	# Test data without its last element for predictAll
	test_rdd_X = test_rdd.map(lambda r: (r[0], r[1]))
	predictions = model.predictAll(test_rdd_X).map(lambda r: ((r[0], r[1]), r[2]))
	user_dict = train.groupby('user_id')['is_listened'].mean().to_dict()
	        
	# Prediction
	y_true, y_pred = compute_y_pred(test, predictions, user_dict)
	test['is_listened'] = y_pred

	test[['sample_id', 'is_listened']].to_csv('ALS_rank_8_lambda_01.csv',
                                          index=False)