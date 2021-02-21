#import modules
import pandas as pd
import numpy as np

#read csv files
train = pd.read_csv('../data/cases_train_processed.csv')
test = pd.read_csv('../data/cases_test_processed.csv')
location = pd.read_csv('../data/location_transformed.csv')

#join the training and location datasets
train_location_joined = pd.merge(train,location, on='name')

#join the test and location datasets
test_location_joined = pd.merge(test,location, on='name')

#write csv files
train_location_joined.to_csv('train_location_joined.csv')
test_location_joined.to_csv('test_location_joined.csv')