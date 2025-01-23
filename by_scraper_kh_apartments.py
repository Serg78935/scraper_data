
#import os
#os.system(" pip install selenium")

#  ! Code with SSL

import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import date
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from contextlib import closing
import ssl   
import re

def initialize_database():                   # Initializes the database and creates the table apartments if it does not exist 
    conn = sqlite3.connect("apartments.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS apartments(
        id INTEGER PRIMARY KEY,
        location TEXT,
        link_dom_ria_com TEXT,
        rooms INTEGER,
        area_general_living_kitch TEXT,
        floor TEXT,
        price_usd TEXT,
        post_date TEXT,
        scrape_date1 TEXT,
        views1 INTEGER
    )''')  
    conn.commit()
    return conn, cursor

# Initialize database
conn, cursor = initialize_database()

# Function to scrape a single page
def scrape_page(url, driver):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    apartments = []

    for listing in soup.select('a.realty-link'):  # Adjust this selector based on website analysis     
        try:
            
            # Getting the link from the href attribute of the listing element
            link = listing.get('href')
            if link:
                  full_link = f"https://dom.ria.com{link}"  #  Add a domain if you need to form a full URL   
            else:
                  full_link = None
                  print("Error: listing is missing href attribute") 
            link = full_link
            link_dom_ria_com = link.split('kvartira')[1]
            # Get additional details with Selenium
            driver.get(link)
            sleep(2)  # Allow the page to load completely  
            id_ = int(driver.find_element(By.CLASS_NAME, 'realty-info li:nth-of-type(2)').text.split(' ')[1])  # Adjust selector
            location = ' '.join(driver.find_element(By.CLASS_NAME, 'm0').text.split(' ')[7:11])  # Adjust selector
            rooms = int(driver.find_element(By.CLASS_NAME, 'inspected-box li:nth-of-type(2)').text.split(' ')[0])  # Adjust selector: inspected-box li:nth-of-type(2)  or size18 span:nth-of-type(1) 
            area1 = driver.find_element(By.CLASS_NAME, 'inspected-box li:nth-of-type(1)').text ## Adjust selector: inspected-box li:nth-of-type(1)  or main-list li:nth-of-type(2) 
            area2 = driver.find_element(By.CLASS_NAME, 'mt-20 .size18 span').text  
            area = area1 +' '+ area2 
            area_general_living_kitch = ' м²\ '.join(re.findall(r"(\d+(?:\.\d+)?) м²",  area)) + ' м²'    # or replace: r'\d{1,3}.\d+\sм²'  
            floor ='th of'.join(driver.find_element(By.CLASS_NAME, 'inspected-box li:nth-of-type(3)').text.split(' поверх з')[:])  # Adjust selector: inspected-box li:nth-of-type(3)  or  size18 span:nth-of-type(2)
            price_usd = ' '.join(driver.find_element(By.CLASS_NAME, 'size30').text.split(' ')[:2])  # Adjust selector
            views = int(driver.find_element(By.CLASS_NAME, 'realty-info li:nth-of-type(3)').text.split(' ')[1])  # Adjust selector            
            post_date0 = driver.find_element(By.CLASS_NAME,'realty-info li:nth-of-type(1)').text.split(' ')  # Adjust selector
            post_date = date(2024, ["січ.","лют.","бер.","кві.","тра.","чер.","лип.","сер.","вер.","жов.","лис.","гру."].index(post_date0[3])+1, int(post_date0[2]))  #.strftime('%Y-%m-%d')
            scrape_date = date.today()  
            apartments.append((id_, location, link_dom_ria_com, rooms, area_general_living_kitch, floor, price_usd, post_date, scrape_date, views  ))  #  , link 

        except Exception as e:
            print(f"Error processing listing: {e}")

    return apartments

# Initialize Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

try:
    with closing(webdriver.Chrome(options=options)) as driver:
        # Scrape pages
        all_apartments = []
        base_url = "https://dom.ria.com/uk/prodazha-kvartir/kharkov/?page={}"  
        for page in range(1, 51):  # Pages 1 to n
            url = base_url.format(page)
            print(f"Scraping {url}...")
            apartments = scrape_page(url, driver)
            all_apartments.extend(apartments)
            
        # Save to database
        cursor.executemany('''INSERT OR REPLACE INTO apartments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', all_apartments)  # , ?
        conn.commit()

except Exception as e:
    print(f"An error occurred with the Selenium driver: {e}")


# Close database connection
conn.close()

print("Scraping completed and data saved to apartments.db.")


#  Code for displaying the table

import sqlite3
import pandas as pd
import csv

def display_table(db_path, table_name):     # Displays the content of a SQLite table as a DataFrame
        
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    # Read the table into a DataFrame
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn) 
    # df.to_csv("apartments.csv", index=False)  # Send database in format: .csv  # Obviously: df.to_csv("C:/Users/phili/Python/apartments.csv", index=False)     
    # df.to_csv(r'D:\apartments.csv', index=False)

    # Close the connection
    conn.close()
    
    # Display the DataFrame
    print(df)
    return df 

# Specify database path and table name

database_path = "apartments.db"
table_name = "apartments"

# Display the table
dataframe = display_table(database_path, table_name)


#  Rename Table
"""
import sqlite3
# Connecting to a database (or creating one if there is no database)
conn = sqlite3.connect('apartments.db')
cursor = conn.cursor()

# SQL query to rename a table
old_table_name = "apartments"
new_table_name = "apartments1"

try:
    cursor.execute(f"ALTER TABLE {old_table_name} RENAME TO {new_table_name}")
    conn.commit()
    print(f"Table '{old_table_name}' successfully renamed to '{new_table_name}'.")
except sqlite3.Error as e:
    print(f"Error renaming table: {e}")
finally:
    # Closing the connection
    conn.close()
"""

#  DELETE from db  

"""
import sqlite3
# Connecting to a database (or creating one if there is no database)
conn = sqlite3.connect('apartments.db')
cursor = conn.cursor()

# SQL query to delete a table
old_table_name = "apartments"

try:
    cursor.execute(f"drop table if exists {old_table_name} ")  # DELETE from table (it's only date of table); # DROP (this is all a table with a name)
    conn.commit()
    print(f"Table '{old_table_name}' successfully deleted.")
except sqlite3.Error as e:
    print(f"Error deleting table: {e}")
finally:
    # Closing the connection
    conn.close()
"""

# List of tables that are stored
"""
import sqlite3

def list_tables(db_path):
    # Connecting to a database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to get a list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Closing the connection
    conn.close()
    
    return [table[0] for table in tables]

database_path = "apartments.db"
print("List of tables:", list_tables(database_path))
"""

# Checking saved  data of all stored tables
""" 
import sqlite3
import pandas as pd
conn = sqlite3.connect("apartments.db")
table_names = [ 'apartments1']  # Table names found in the database # 'apartments3', "apartments_decision"
for table_name in table_names:
    print(f"Table contents: {table_name}")
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)  # LIMIT 5
    print(df)
conn.close()
"""


# Merging tab1 and tab2 using FULL OUTER JOIN

"""
import sqlite3
import pandas as pd

def display_table(db_path, table_name1, table_name2, output_table):     
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    try:
        # Read the first table into a DataFrame
        query1 = f"SELECT * FROM {table_name1}"
        df1 = pd.read_sql_query(query1, conn)

        # Read the second table into a DataFrame
        query2 = f"SELECT * FROM {table_name2}"
        df2 = pd.read_sql_query(query2, conn)

        # Merge the two DataFrames
        merged_df = pd.merge(
            df1, df2, 
            on=['id', 'location', 'link_dom_ria_com', 'rooms', 'area_general_living_kitch', 'floor', 'price_usd', 'post_date'], 
            how="outer"
        )

        # Ensure the output table exists
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {output_table} (
                id INTEGER,
                location TEXT,
                link_dom_ria_com TEXT,
                rooms INTEGER,
                area_general_living_kitch REAL,
                floor INTEGER,
                price_usd REAL,
                post_date TEXT
            )
        ''')

        # Insert data into the output table
        merged_df.to_sql(output_table, conn, if_exists='replace', index=False)

        # Read back the table to display it
        result_df = pd.read_sql_query(f"SELECT * FROM {output_table}", conn)
        print(result_df)

    finally:
        # Close the connection
        conn.close()

    return result_df

# Specify database path and table names
database_path = "tab.db"
table_name1 = "apartments1"
table_name2 = "apartments2"
output_table = "apartments3"

# Display the merged table
dataframe = display_table(database_path, table_name1, table_name2, output_table)
"""

#  Adds new columns with calculates:

"""
import pandas as pd
import numpy as np
import sqlite3

def display_table(db_path, table_name, output_table):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    if df.empty:
        print(f"Table '{table_name}' contains no data.")
        conn.close()
        return

    # Date conversion
    df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
    df["scrape_date"] = pd.to_datetime(df["scrape_date"], errors="coerce")
    df["scrape_date2"] = pd.to_datetime(df["scrape_date2"], errors="coerce")

    # Calculation scrape_date_cal and scrape_date_cal1
    df["scrape_date_cal"] = (df["scrape_date"] - df["post_date"]).dt.days.fillna(0)   # if you need to 'int':   .astype(int)
    df["scrape_date_cal1"] = (df["scrape_date2"] - df["post_date"]).dt.days.fillna(0)
    df.loc[df["scrape_date_cal"] >= 365 , "scrape_date_cal"] = df["scrape_date_cal"] - 366
    df.loc[df["scrape_date_cal1"] >= 365 , "scrape_date_cal1"] = df["scrape_date_cal1"] - 366 
    
    k = 0.18  # from 0.05  to  0.18

    # Iterative function
    def calculate_views0(row, views_av, k):
        scrape_date_cal = row["scrape_date_cal"]
        if scrape_date_cal == 0:
            return 0, scrape_date_cal
        views_0 = row["views"] * k / (1 - np.exp(-k * scrape_date_cal))
        if np.isnan(views_av):
            return views_0, scrape_date_cal
        """ """
        while not (views_av * 0.5 < views_0 < 2.0 * views_av):
            scrape_date_cal += 30.417  # it's 365 / 12
            views_0 = row["views"] * k / (1 - np.exp(-k * scrape_date_cal))
            if scrape_date_cal > 365 :
                break
        """ """
        return views_0, scrape_date_cal

    # Calculating the average value views_av    
    df["views_0"] = round(df.apply(                                                         # _in
        lambda row: row["views"] * k / (1 - np.exp(-k * row["scrape_date_cal"]))
        if row["scrape_date_cal"] > 0 else 0,
        axis=1), 2)
        
    views_av = round(df.loc[(df["views_0"] > 0) & (df["views_0"] < 700), "views_0"].mean(), 2)   # _in
    print(repr(views_av))
    if np.isnan(views_av):
        views_av = 100

    # Calculation views_0
    """ """
    df[["views_0", "scrape_date_cor"]] = round(df.apply(
        lambda row: pd.Series(calculate_views0(row, views_av, k)), axis=1), 2)
    """ """
    # Calculation views_decision_%
    df["views_decision_%"] = round(((df["views_0"] - views_av) / views_av) * 100 , 2)
    df.loc[(df["views_0"] == 0), "views_decision_%" ] = 0
    # Calculation views_dec1
    df["views_dec1"] = round((
        (
            df["views2"] - df["views"]
            * (1 - np.exp(-k * df["scrape_date_cal1"]))
            / (1 - np.exp(-k * df["scrape_date_cal"]))
        )
        / (
            df["views"]
            * (1 - np.exp(-k * df["scrape_date_cal1"]))
            / (1 - np.exp(-k * df["scrape_date_cal"]))
        )
    ) * 100 , 2)
    df.loc[np.isnan(df["views_dec1"]), "views_dec1" ] = 0
    df = df.sort_values(by=['views_decision_%', 'views_dec1'], ascending=[False, False])
    df.loc[(df["views_decision_%"] > 200.00), "views_decision_%" ] = 'Unreal'
    df.loc[(df["views_decision_%"] == 0), "views_decision_%" ] = 'NaN'
    df.loc[(df["views_dec1"] == 0), "views_dec1" ] = 'NaN' 

    # Ensure the output table exists
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {output_table} (
            id INTEGER,
            location TEXT,
            rooms INTEGER,
            area_sq_m_gen_liv_kitch REAL,
            floor INTEGER,
            price_usd REAL,
            post_date TEXT
        )
    ''')

    # Insert data into the output table
    df.to_sql(output_table, conn, if_exists='replace', index=False)

    # Read back the table to display it
    result_df = pd.read_sql_query(f"SELECT * FROM {output_table}", conn)
    print(result_df)

    # Close the connection
    conn.close()

    return result_df    

database_path = "apartments.db"
table_name = "apartments3"
output_table = "apartments_decision"
dataframe = display_table(database_path, table_name, output_table)
"""

# Calculate k :
"""
import pandas as pd
import numpy as np
import sqlite3
import math
m1 = [108,122,85,134]                      # views in one day
m2 = [199,223,157,244]                     # views in two days
m3 = [j/i - 1 for i,j in list(zip(m1, m2))] 
#print(m3)
m = np.average(m3)
print(m)
k = round(( - math.log(m, math.e)), 5)
print(k)
"""