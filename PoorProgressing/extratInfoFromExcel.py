import pandas as pd
import numpy as np
import csv

def get_dataSet():

    # load dataset
    df = pd.read_csv('poorStudents.csv', encoding = "ISO-8859-8")

    # convert df[['ת.ז','מקצוע']] to string 
    df= df[['ת.ז','שם']].astype(str)


    return df

df = get_dataSet()

print(len(df))