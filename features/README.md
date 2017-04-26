This folder contains the implementations of some classes used to generate the
features for the training part.

## Listening History

The class `History` allows to get the listening history of some users and filter
 the latter between two dates (important for the Cross Validation) and get some
 patterns on the user listening (ex: `get_top_artists`, `get_top_tracks`, ...)

 **Note** : Fitting a `History` instance to the whole data (around 8 million lines) may take a few seconds.
 **Don't use** `fit_multiproc` as it still contains some bugs linked to `max_depth recursion`.
 However we **favour** loading it from an already existing
 `.json` file (supposes that the fitting has already been done once of course).

Take a look at the *main* in History class to know how to use it.

