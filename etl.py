from cgitb import reset
from curses import keyname
#import configparser
import psycopg2
import sql_queries as sql
import credentials
import pandas as pd
import test_queries as tc

# Drop table before do somethings
def drop_tables(cur, conn):
    """
    Drop tables if exsiting in redshift

        Parameters:
                cur (obj): Create SQL execute
                conn (obj): Create DB connection

        Returns: N/A
    """
    for query in sql.drop_table_queries:
        cur.execute(query)
        conn.commit()

# Create new tables in redshift
def create_tables(cur, conn):
    """
    Create new tables in redshift

        Parameters:
                cur (obj): Create SQL execute
                conn (obj): Create DB connection

        Returns: N/A
    """
    for query in sql.create_table_queries:
        cur.execute(query)
        conn.commit()

# Create staging table
def copy_staging_tables(cur, conn):
    """
    Copy local CSV file to staging tables in redshift

        Parameters:
                cur (obj): Create SQL execute
                conn (obj): Create DB connection

        Returns: N/A
    """
    for query in sql.copy_table_queries:
        cur.execute(query)
        conn.commit()

# Insert fact and dimension tables
def insert_tables(cur, conn):
    """
    Insert record to fact and dimension tables in redshift

        Parameters:
                cur (obj): Create SQL execute
                conn (obj): Create DB connection

        Returns: N/A
    """
    for query in sql.insert_table_queries:
        cur.execute(query)
        conn.commit()

# Test table is inserted
def check_greater_than_zero(cur, table):
    """
    Test table is inserted data

        Parameters:
                cur (obj): Create SQL execute

        Returns: N/A
    """
    query = ("""SELECT COUNT(*) FROM {};""").format(table)
    cur.execute(query)
    result = cur.fetchall()
    if result:
        print(f"{table} have {result} records. Pass test")
    else: raise ValueError(f"Data quality check failed. {table} return no results")
   

def check_field_len(cur):
    """
    Test length of state_code

        Parameters:
                cur (obj): Create SQL execute

        Returns: N/A
    """
    for len in tc.check_field_len_queries:
        cur.execute(len)
        records = cur.fetchall()
        if records != []:
             raise ValueError(f"Data quality check failed.  is abnormal")  
        else: print("state_code lenght Pass test")

def main():
    """
    Run this function if run etl.py

        Parameters: None

        Returns: None
    """
    #config = configparser.ConfigParser()
    #config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(credentials.HOST, credentials.DB_NAME, credentials.DB_USER, credentials.DB_PASSWORD, credentials.DB_PORT))
    cur = conn.cursor()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)
    
    # Load table
    copy_staging_tables(cur, conn)

    # Data quality check
    check_greater_than_zero(cur, "stg_demographic")
    check_greater_than_zero(cur, "stg_covid_us")

    # Insert table
    insert_tables(cur, conn)

    # Data quality check
    check_greater_than_zero(cur, "agg_covid_state")
    check_greater_than_zero(cur, "dim_states")
    
    # Length data field check
    check_field_len(cur)

    conn.close()


if __name__ == "__main__":
    main()