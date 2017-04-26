# Vectorizer and Hasher

## Vectorizer

Instances of this class will allow you to generate **cross features** from already
existing features.

**Define a list of transformations** following the format `(feature_name_1, feature_name_2, symbol)`:
```
transforms = [('user_age', 'genre_id', '&'),
              ('user_gender', 'artist_id', '&'),
              ('genre_id', 'artist_id', '&')]
```
These transforms will take the value from each feature and join it with the symbol used.
For example : `('user_gender', 'artist_id', '&')` will give `string` values like `female&123` and `male&456`

**Instanciate a Vectorizer**

```
vect = Vectorizer(transforms)
```

**Fit and transform the training data**

```
vect.fit_transform(data, transforms) # data being your training dataframe
```

This will update the dataframe `data` by adding the defined **cross-features**.

## Hasher

This class was implemented in order to transform a dataframe into a sparse matrix.

The `Hasher` instance must be applied to your **final dataframe** (*i.e.* processed + cross-features).

The sparse matrix obtained must be used as the **input of your model** (Logistic Regression, ...).

Here is ahow to make use of it:

```
my_hash = Hasher(size=100000) # size being the size of your sparse vectors
                              # make sure to take a big number to avoid collisions

X_sparse = my_hash.fit_transform(data) # obtain sparse matrix (does not contain labels Y)
```

**VERY IMPORTANT**: **DO NOT APPLY** `.toarray()` **ON YOUR SPARSE MATRIX**. **HIGH RISK OF MEMORY ISSUE**.
