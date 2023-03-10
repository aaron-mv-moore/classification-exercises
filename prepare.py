import pandas as pd
import numpy as np
from acquire import get_telco_data, get_iris_data, get_titanic_data
from sklearn.model_selection import train_test_split

def prep_iris(df):
    '''
    Arguments: Iris Dataframe
    Actions: 
        1. Drops columns[species_id, measurement_id]
        2. Renames species_name to species
        3. Creates dummies for the species columns
    Returns: iris dataframe with all changes
    '''
    
    # drop column names
    df = df.drop(columns=['species_id', 'measurement_id'])
    
    # rename species_name to species
    df = df.rename(columns={'species_name':'species'})
    
    # creates dummies for the species columns and concatenates the dummy variables to original df
    df = pd.concat([df, pd.get_dummies(df['species'], drop_first=True)], axis=1)
    
    return df

def prep_titanic(df):
    '''
    Arguments: Titanic Dataframe
    Actions:
        1. Drops columns['class', 'deck', 'passenger_id']
        2. Fills null values for age with the mean age
        3. Fills null values for embark_town with most common occurinf values
        4. Created dummy variables for columns[embark_town, sex]
        5. Concatenated dummy variables to df
    Returns: one dataframe with changes
    '''
    # droping duplicates/not useful ones
    df = df.drop(columns=['class', 'deck', 'passenger_id'])
    
    # imputing
    df['age'] = df.age.fillna(df.age.mean())
    df['embark_town'] = df.embark_town.fillna('Southampton')
    
    # encoding
    df = pd.concat([df, pd.get_dummies(df[['embark_town', 'sex']], drop_first=True)], axis=1)
    
    return df

def prep_telco(df):
    '''
    Arguments: telco df 
    Actions:
        1. Assigns contents of duplicate columns to new columns with different names
        2. Drops unnecessary columns including duplicate columns and primary/foreign key columns
        3. Change data type of column from object to float
        4. Create a list of columns with object data types
        5. Create dummy variables for all object type data types
        6. Concatenates dummay variabels to original dataframe
    Returns: telco df prepared to be split
    '''
    
    # Handle duplicate columns
    df['total_charges_1'] = df['total_charges'].iloc[:,0]
    df['monthly_charges_1'] = df['monthly_charges'].iloc[:,0]
    df['paperless_billing_1'] = df['paperless_billing'].iloc[:,0]
    
    # Drop unnecessary columns
    df = df.drop(columns=
                 ['total_charges', 'monthly_charges', 'paperless_billing',
                  'contract_type_id', 'payment_type_id', 'internet_service_type_id', 
                  'customer_id'])
    
    # Convert columns data type from object to float
    df['total_charges_1'] = (df['total_charges_1'] + '0').astype(float)
    
    # Create list of object type/categorical columns
    df_objects = []
    for col in df:
        if df[col].dtype == 'O':
            df_objects.append(col)

    # Create dummy variables and add them to the df
    df = pd.concat([df, pd.get_dummies(df[df_objects], drop_first=True)], axis=1)
    
    return df


def split_data(df, target=None):
    '''
    Arguments: prepared dataframe, optional target - must be a string literal
    Actions: 
        1. Splits the dataframe with 80% of the data assigned to tv and 20% assigned to test
        2. Splits the tv dataset with 70% of tv assigned to train and 30% assigned to validate
    Returns: 3 variables, each containing a portion
    Note: Order matters with variable assignment
    '''
    # splitting df 80/20 
    
    if target == None:
        train_validate, test = train_test_split(df, train_size=.8, random_state = 1017,
                stratify = target)
    else:
        train_validate, test = train_test_split(df, train_size=.8, random_state = 1017,
                stratify = df[target])
    
    # splitting train_validate 70/30
    train, validate = train_test_split(train_validate, train_size=.7, random_state = 1738)
    
    return train, validate, test
