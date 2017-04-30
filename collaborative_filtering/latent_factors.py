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

# Create a mask using 'listen_type'
def create_mask(df, predictions):
    pairs_user_song = predictions.map(lambda r: (r[0][0], r[0][1])).collect()

    mask = []
    for (user, song) in pairs_user_song:
        mask.append(df[(df['user_id'] == user) & (df['media_id'] == song)]['listen_type'].values[0])
    mask = np.array(mask)

    # Convert 0-1 to boolean
    mask = (mask == 1)
    return mask

# ROC AUC metric
def compute_roc_auc(data, predictions, mask):
    """
    ROC AUC with rdd data
    """
    
    # Join the predictions to the original data
    data_pred = data.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    y_true = np.array(data_pred.map(lambda r: (r[1][0])).collect())
    y_pred = np.array(data_pred.map(lambda r: (r[1][1])).collect())
    y_pred = (y_pred - min(y_pred)) / (max(y_pred) - min(y_pred))
    
    roc_auc = roc_auc_score(y_true[mask], y_pred[mask])
    return roc_auc

if __name__ == '__main__':

	full_train = pd.read_csv('../train.csv')
	# Reduced train dataset
	train = full_train[:1000000]

	# Initialise Spark
	conf = SparkConf() \
	      .set("spark.executor.memory", "2g")
	sc = SparkContext(conf=conf)

	rank_grid = [5, 10]
	lmbda_grid = [0.1, 0.2]
	nb_iterations = 10

	# Need to compute the train/test split

	for (rank, lmbda) in itertools.product(rank_grid, lmbda_grid):
	    model = ALS.train(train_rdd, rank=rank, 
	                      iterations=nb_iterations, lambda_=lmbda)
	    
	    # Test data without its last element for predictAll
	    test_1_rdd_ = test_1_rdd.map(lambda r: (r[0], r[1]))
	    predictions = model.predictAll(test_1_rdd_).map(lambda r: ((r[0], r[1]), r[2]))
	    mask = create_mask(test_cv_1, predictions)
	    
	    print('Parameters: rank={0}, lambda={1}:'.format(rank, lmbda))
	    print(compute_roc_auc(test_1_rdd, predictions, mask))