This folder contains the functions used for cross-validation.

## Train test split

The main function is `train_test_split` which creates train and test sets temporally coherent.
Parameters are the DataFrame containing the data and the number `n_splits` of train/test sets you want.

Output is a list of tuples (train, test, timeframes) Train and test are pd.DataFrame with the same columns than input data. TimeFrames is a list giving the start date and end date of training data for each user.

Test set is built with **only one** sample for each user.

```python
data = pd.read_csv('data/train_csv')

sets = train_test_split(data, n_splits=3)
# sets is a list of size 3

for train, test, timeframes in sets:
  # first thing is to create X and y vectors
  y_train = train.is_listened
  X_train = train.drop('is_listened', axis=1)
  
  y_test = test.is_listened
  X_test = test.drop('is_listened', axis=1)
  
  # train your model
  clf.fit(X_train, y_train)
  # ...
```


