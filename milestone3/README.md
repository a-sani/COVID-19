# CMPT 459 - COVID-19 Project
### Milestone 3 - Hyperparameters Tuning & Predictions

***1. Please install all these modules to be able to run our program.***
* pandas
* numpy
* matplotlib
* sklearn (scikit-learn)
* lightgbm
* imbalanced-learn
* lightgbm
* os

***2. Please make sure you have the LightGBM API installed on your computer to use the model***
* I installed on MacOS with `brew install lightgbm`
* Please take a look at the installation guide for installing on a different OS.
https://lightgbm.readthedocs.io/en/latest/Installation-Guide.html

***3. The src folder includes the main.ipynb which contains our code.***

***4. The results of hyperparameter tuning of the models and the final predictions file in the results folder***
* `knn_params.csv` 
* `rf_params.csv`
* `lgbm_params.csv`
*  `predictions.txt`

***5. The plots folder includes the confusion matrices and the pie chart of the predicted outcomes***
* `knn_matrix.png` - K-Nearest Neighbours confusion matrices for training and validation
* `rf_matrix.png` - Random Forest confusion matrices for training and validation
* `lgbm_matrix.png` - LightGBM confusion matrices for training and validation
* `pie_outcomes.png` - Final predictions of outcome labels on the test data