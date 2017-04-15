This directory aims to contain all the submissions done.
Try to be as specific as possible in order to avoid ambiguity in the names of the files.

### Naming conventions:
Each submission must contain the name of the **model** used, its **parameters** and their **values** as well as the **score** (at a *5 floating points precision*) obtained in cross validation.

For example:
* `randomForests_maxDepth_8_numEstimators_100_score_75328.csv` : for a Random Forest used with `max_depth=8` and `num_estimators=100` and which led to a score of `0.75328xxx`.
* `logisticReg_penalty_l2_regParam_1e-4_score_74873.csv` : for a Logistic Regression used with an `L2` penalty and a regularization parameter of `C=.0001`. Led to a score of `0.74873xxx`.

Naming the files like this will help us parse them and get the models and their parameters easily and **rank the submissions** when the directory will contain a lot of them.