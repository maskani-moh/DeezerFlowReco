This folder contains the implementations of some classes used to generate the
features for the training part.

## Listening History

The class `History` allows to get the listening history of some users and filter
 the latter between two dates (important for the Cross Validation) and get some
 patterns on the user listening (ex: `get_top_artists`, `get_top_tracks`, ...)

 **Important** : Fitting a `History` instance to the data may take a lot of time
 if computed in a multithreaded fashion. **Favour** loading it from an already existing
 `.json` file (supposes that the fitting has already been done once of course).

