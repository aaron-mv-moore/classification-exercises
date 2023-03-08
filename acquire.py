import env
import os

def get_titanic_data():
    '''
    This function returns the passengers table from the titanic db. 
    This funcction requires the user to have an env.py file with a 
    function to create a MySQL url without user input from this module.
    '''
    filename = "titanic.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else: 
        db = ('titanic_db')
        query = 'SELECT * FROM passengers;'
        url = env.get_db_url(db)
        return pd.read_sql(query, url)
    

def get_iris_data():
    '''
    This function returns the species table from the iris_db. 
    No arguments are needed for it run
    '''
    filename = 'iris.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else: 
        db = ('iris_db')
        query = 'SELECT * FROM species;'
        url = env.get_db_url(db)
        return pd.read_sql(query, url)

def get_telco_data():
    '''
    This function a dataframe containing all the contract, payment, and internet service options for each customer.
    '''
    filename = 'telco.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        db = 'telco_churn'
        url = env.get_db_url(db)
        query = '''SELECT *
            FROM customers c
            JOIN customer_contracts cc ON c.customer_id = cc.customer_id
            JOIN contract_types ct ON cc.contract_type_id = ct.contract_type_id
            JOIN internet_service_types ist ON c.internet_service_type_id = ist.internet_service_type_id
            JOIN customer_payments cp ON c.customer_id = cp.customer_id
            JOIN payment_types pt ON cp.payment_type_id = pt.payment_type_id;'''
        return pd.read_sql(query, url)
    