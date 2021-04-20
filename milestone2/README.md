# CMPT 459 - COVID-19 Project
### Milestone 2 - Building and Evaluating the Models

**NOTE: The entire notebook takes ~30 minutes to complete. This is mainly because of the accuracy curves created for each model to detect overfitting (each accuracy curve loops through a range of values of a parameter that it trains the model on).**

***1. Please install all these modules to be able to run our program.***
* pandas
* numpy
* pickle
* matplotlib
* sklearn
* lightgbm
* scikit-learn

***2. Please make sure you have the LightGBM API installed on your computer to use the model***
* I installed on MacOS with `brew install lightgbm`
* Please take a look at the installation guide for installing on a different OS.
https://lightgbm.readthedocs.io/en/latest/Installation-Guide.html

***3. Here is the link to download our saved pickle files for the models (since the total submission folder exceeded 30 MB)***
https://drive.google.com/drive/folders/1_MKBGMNY20SFJjTgODMcUwrURxR90CyU?usp=sharing

***4. The src folder includes the main.ipynb which contains our code.***

***5. The models folder includes all the built and saved models***
* `knn_classifier.pkl` 
* `rf_classifier.pkl`
* `lgbm_classifier.pkl`

***6. The plots folder includes the confusion matrices and accuracy curves produced by our models***
* `knn_cm.png` - K-Nearest Neighbours confusion matrices for training and validation
* `rf_cm.png` - Random Forest confusion matrices for training and validation
* `lgbm_cm.png` - LightGBM confusion matrices for training and validation
* `knn_accuracy_curve.png` - K-Nearest Neighbours accuracy curve.
* `rf_accuracy_curve.png` - Random Forest accuracy curve.
* `lgbm_accuracy_curve.png` - LightGBM accuracy curve.