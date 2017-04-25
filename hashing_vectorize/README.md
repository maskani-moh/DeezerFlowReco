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
For example : `('user_gender', 'artist_id', '&')` will give `string` values like `female&123`, `male&456`

**Instanciate a Vectorizer**

```
vect = Vectorizer(transforms)
```

**Fit and transform the training data**

```
vect.fit_transform(data, transforms) # data beig your training dataframe
```

This will update the dataframe `data` by adding the defined **cross-features**.