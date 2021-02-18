import pandas as pd
import numpy as pandas
import re
import sys
import math

#read csv file from command line
data = pd.read_csv(sys.argv[1])

#fixing the various age formats
def fixAge(age):
    #pattern to match if age is between a range
    range_pat = "(\d+)-(\d+)"
    #pattern to match if range is float or int
    single_pat = "(\d+)"
    #create regex patterns
    pat1 = re.compile(range_pat)
    pat2 = re.compile(single_pat)
    #match the age format to the regex pattern
    result1 = pat1.match(age)
    result2 = pat2.match(age)
    #if age is a range value, return the average
    if result1:
        i = int(result1.group(1))
        j = int(result1.group(2))
        return math.ceil((i+j)//2)
    #if age is float/int, return int
    if result2:
        return int(result2.group(1))





