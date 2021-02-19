import pandas as pd
import numpy as pandas
import re
import sys
import math

#read csv file from command line
data = pd.read_csv(sys.argv[1])
data = data.drop(columns=['additional_information', 'source'])

#fixing the various age formats
def fixAge(age):
    #pattern to match if age is between a range
    range_pat = "(\d+)-(\d+)"
    #pattern to match if range is float or int
    single_pat = "(\d+)"
    #pattern to match months
    month_pat = "(\d+) month"
    #create regex patterns
    pat1 = re.compile(range_pat)
    pat2 = re.compile(single_pat)
    pat3 = re.compile(month_pat)

    #match the age format to the regex pattern
    result1 = pat1.match(age)
    result2 = pat2.match(age)
    result3 = pat3.match(age)
    #if age is a range value, return the average
    if result1:
        i = int(result1.group(1))
        j = int(result1.group(2))
        return math.ceil((i+j)//2)
    #if age is float/int, return int
    if result2:
        #if age is in months, consider them 1 years old
        if result3:
            return 1
        else:
            return int(result2.group(1))

#copy only the age and outcome attributes of original data
temp = data.filter(['age','outcome'])
#drop all NaN age values
temp = temp.dropna()
#fix the ages
temp['age'] = temp['age'].apply(fixAge)
#group by outcome and calculate the average age for each outcome
temp = temp.groupby(['outcome']).mean()
#use celing function to make age a whole number
temp['age'] = temp['age'].apply(math.ceil)
#get age averages and store them in list
categoryAges = temp['age'].tolist()




