#import modules
import pandas as pd
import numpy as np

#read the processed csv files
train = pd.read_csv('../results/cases_train_processed.csv')
test = pd.read_csv('../results/cases_test_processed.csv')
location = pd.read_csv('../results/location_transformed.csv')


#Using left join

#join the training and location datasets
train_location_joined = pd.merge(train,location, on='key', how = 'left')

#join the test and location datasets
test_location_joined = pd.merge(test,location, on='key', how = "left")



train_location_joined = train_location_joined.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1)
test_location_joined = test_location_joined.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1)

#write csv files
train_location_joined.to_csv('../results/train_location_joined.csv', index=False)
test_location_joined.to_csv('../results/test_location_joined.csv', index=False)