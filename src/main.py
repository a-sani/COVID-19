import pandas as pd
import numpy as np
import statistics
import re
import sys
import math
from geopy.geocoders import Nominatim


def replace_missing_values(df):
    '''
    This function replaces missing values in gender, dates, additional information and source
    Input: dataframe
    Output: dataframe
    
    References:
    # https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
    # https://stackoverflow.com/questions/38607381/python-pandas-if-the-data-is-nan-then-change-to-be-0-else-change-to-be-1-in-d
    '''
    df["sex"].fillna("Unknown", inplace = True) 
    df["date_confirmation"].fillna("20.09.2020", inplace = True) 
    df[["additional_information", "source"]] = df[["additional_information", "source"]].notnull().astype(int)

    return df


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

    if result1: #if age is a range value, return the average
        i = int(result1.group(1))
        j = int(result1.group(2))
        return math.ceil((i+j)//2)

    if result2: #if age is float/int, return int
        #if age is in months, consider them 1 years old
        if result3:
            return 1
        else:
            return int(result2.group(1))


def imputing_province(latitude,longitude):
    '''
    Imputing the province and country names according to their latitude and longitude values
    Reference:
    https://www.geeksforgeeks.org/get-the-city-state-and-country-names-from-latitude-and-longitude-using-python/
    '''
    # initialize Nominatim API  
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(latitude) + "," + str(longitude), language = 'en', timeout=None) 
    if location is None:
        return None, None
    address = location.raw['address'] 

    state = address.get('state', '') 
    country = address.get('country', '') 
    return state,country


def key_generation(df, province, country):
    '''
    This function combines province and country names to make a compound key
    
    Input: dataframe, "province name", "country name"
    Output: original dataframe & a new key column
    
    Reference:
    https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
    '''
    return df.assign(key = df[province].str.cat(df[country], sep = ', '))


def convert_time(df, time_column):
    '''
    This function extracts the necessary date components and converts them to date
    
    Input: dataframe, column
    Output: date column
    
    References:
    # https://stackoverflow.com/questions/13682044/remove-unwanted-parts-from-strings-in-a-column
    # https://stackoverflow.com/questions/40841867/how-to-convert-dd-mm-yyyy-into-yyyy-mm-dd-with-pandas-in-python
    '''
    time_extract = df[time_column].map(lambda x: str(x)[:10])
    #train[time_column] = pd.to_datetime(train[time_column].map(lambda x: str(x)[:10]))
    
    df[time_column] = pd.to_datetime(time_extract)
    
    return df


def imputation(data): # Function to clean and imput the dataset
    ### Fixing Age Attribute
    #copy only the age and outcome attributes of original data
    temp = data["age"].dropna() #drop all NaN age values
    data['age'] = temp.apply(fixAge) #fix the ages

    age_mean = round(data["age"].mean())
    data["age"].fillna(float(age_mean), inplace = True)
    print(data)

    ### Replaces missing values in sex, date, source, and additional info
    data = replace_missing_values(data) 


    ### Imputing Missing values in Province and Country attributes
    data = data[data["latitude"].notnull()]


    for index, row in data.iterrows():
        #print(row['province'], row['country'])
        if (pd.isnull(row['province']) or pd.isnull(row['country'])): #checks if province or country is Null
            province, country = imputing_province(row['latitude'],row['longitude']) #does imputation
            if (pd.isnull(row['province'])): #if its province that's null
                if province is None: 
                    data.loc[index,'province'] = "Unknown"
                elif len(province) == 0:
                    data.loc[index,'province'] = "Unknown"
                else:
                    data.loc[index,'province'] = province
            if (pd.isnull(row['country'])): # if country is Null
                if len(country) == 0:
                    data.loc[index,'country'] = "Unknown"
                elif country is None:
                    data.loc[index,'country'] = "Unknown"
                else:
                    data.loc[index,'country'] = country
    print(data.head(26412))


    data = data.replace({'country':{"United States":"US"}})
    data = key_generation(data, "province", "country")
    dataset = convert_time(data, "date_confirmation")

    return dataset


################################################################

def missing_value_by_mean(df, column, key = "key"):
    
    '''
    This function fills in the missing values by group mean using key as the group
    
    Input: dataframe, column to be filled, groupby column name
    Output: column to be filled
    
    Reference:
    # https://stackoverflow.com/questions/19966018/pandas-filling-missing-values-by-mean-in-each-group

    '''
    
    df[column] = df[column].fillna(df.groupby(key)[column].transform("mean"))
    return df[column]

def missing_value_by_country_mean(df, column, key = "Country_Region"):
    
    '''
    This function fills in the missing values by group mean using country as the group
    
    Input: dataframe, column to be filled, groupby column name
    Output: column to be filled
    
    Reference:
    # https://stackoverflow.com/questions/19966018/pandas-filling-missing-values-by-mean-in-each-group

    '''
    
    df[column] = df[column].fillna(df.groupby(key)[column].transform("mean"))
    return df[column]


def aggregate(df):
    
    '''
    This function aggregates groups by sums and means then perform column operations
    
    Input: dataframe
    Output: dataframe
    
    References:
    https://stackoverflow.com/questions/48909110/python-pandas-mean-and-sum-groupby-on-different-columns-at-the-same-time
    # https://stackoverflow.com/questions/20461165/how-to-convert-index-of-a-pandas-dataframe-into-a-column
    '''
    
    # aggregation of sums and means
    col_names = {'Lat':'latitude', 'Long_':'longitude','Confirmed':'confirmed_sum', 'Deaths':'death_sum', 'Recovered':'recovered_sum', 'Incidence_Rate':'incidence_rate_avg'}
    df = df.groupby('key').agg({'Lat':'mean', 'Long_':'mean', 'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum', 'Incidence_Rate':'mean'}).rename(columns = col_names)
    
    # reset key index
    df.reset_index(level = 0, inplace = True)
    
    # column operations
    df["active_sum"] = df["confirmed_sum"] - df["death_sum"] - df["recovered_sum"]
    df["Case-Fatality_Ratio"] = df["death_sum"] / df["confirmed_sum"] * 100
    
    return df


def transform(data):

    del data["Case-Fatality_Ratio"]
    del data["Active"]

    ### Only running the latitude and longitude that are not null
    data = data[data["Lat"].notnull()]

    for index, row in data.iterrows():
        #print(row['province'], row['country'])
        if (pd.isnull(row['Province_State']) or pd.isnull(row['Country_Region'])): #checks if province or country is Null
            province, country = imputing_province(row['Lat'],row['Long_']) #does imputation
            if (pd.isnull(row['Province_State'])): #if its province that's null
                if province is None: # if latitude and longitude is not valid
                    data.loc[index,'Province_State'] = "Unknown"
                elif len(province) == 0: # if province is empty
                    data.loc[index,'Province_State'] = "Unknown"
                else: # if it returns a valid province
                    data.loc[index,'Province_State'] = province
            if (pd.isnull(row['Country_Region'])): # if country is Null
                if len(country) == 0:
                    data.loc[index,'Country_Region'] = "Unknown"
                elif country is None:
                    data.loc[index,'Country_Region'] = "Unknown"
                else:
                    data.loc[index,'Country_Region'] = country
    print(data.head(26412))
                
    df2 = key_generation(data, "Province_State", "Country_Region")
    df2["Incidence_Rate"] = missing_value_by_mean(df2, "Incidence_Rate")
    df2["Incidence_Rate"] = missing_value_by_country_mean(df2, "Incidence_Rate")
    df3 = aggregate(df2)

    return df3




def main():
    # Reading the tree datasets in 
    train = pd.read_csv('../data/cases_train.csv')
    test = pd.read_csv('../data/cases_test.csv')
    location = pd.read_csv('../data/location.csv')

    ###### IMPUTING AND CLEANING "TRAINING" DATA #####
    new_train = imputation(train)
    new_train.to_csv('../results/cases_train_processed_new.csv')

    new_test = imputation(test)
    new_test.to_csv('../results/cases_test_processed.csv')

    new_location = transform(location)
    new_location.to_csv('../results/location_transformed.csv')


if __name__ == "__main__":
    main()