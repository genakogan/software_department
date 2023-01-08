# Genady Kogan
# TODO - change path for table2.csv
# In[1]:
import pandas as pd
import numpy as np
import csv
# In[2]:
def get_dataSet():

    # load dataset
    df = pd.read_csv('table2.csv', encoding = "ISO-8859-8")
    
    # convert df[['ת.ז','מקצוע']] to string 
    df= df[['ת.ז','מקצוע']].astype(str)

    # convert 'מקצוע' to key and marge the 'ת.ז'
    df = df.groupby(by = 'מקצוע').agg(','.join)

    # string to list students id
    df['ת.ז']= df['ת.ז'].str.split(',')
    df.reset_index(inplace=True)
    return df

# In[3]:
def merge_func(df, res_df):

    # true if contain same elem else false
    same_elem = lambda a,b: True if a & b else False 
    set_i = set(df.iloc[0]['ת.ז'])
    subject_i = df.iloc[0]['מקצוע']
    for ind2 in range(1,len(df)):
            set_j = set(df.iloc[ind2]['ת.ז'])

            # If the elements in the two lists are different
            if(False == same_elem(set_i,set_j)):
                subject_i = subject_i +','+df.iloc[ind2]['מקצוע']
                set_i = set_i.union(set_j)

    # Add the row to a res_df (the row contains subjects that can be tested on the same day)
    #res_df = res_df.append({'id': list(set_i), 'subject': subject_i}, ignore_index=True)
    res_df = pd.concat([res_df, pd.DataFrame.from_records([{'id': list(set_i), 'subject': subject_i}])])
    # Download rows from a df that contain values that are in the res_df
    x = res_df['subject'].iloc[len(res_df)-1].split(',')
    df = df[~df['מקצוע'].isin(x)]
    return df, res_df

# In[4]:
def merge_courses(df):

    # Replaces lines randomly for random result
    df =df.sample(frac=1) 
    
     # Create a data frame
    res_df = pd.DataFrame(columns=['id', 'subject']) 
 
    for _ in range(len(df)):
        df, res_df = merge_func(df, res_df)
        # If the data frame is empty
        if df.empty:
            break
   
    return res_df

# In[5]:
df = get_dataSet()


# In[6]:
res_df = merge_courses(df)

# In[7]:
res_df= res_df.drop(['id'], axis=1)

# In[8]:

res_list  = res_df.values.tolist()
with open('readme.txt', 'w') as f:
    wr = csv.writer(f)
    wr.writerows(res_list)
    
