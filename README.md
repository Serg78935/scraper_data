# 📌 "Monitoring the real estate market in a specific location."

"""
Build status :

 https://img.shields.io/github/actions/workflow/status/Serg78935/scraper_data/blank.yml?branch=main        
![MIT](https://img.shields.io/github/license/Serg78935/scraper_data) 
                   
## 📖 Description 

   This project has developed some tools for monitoring the real estate market.
A data table has been built for a certain period of time,
which makes it possible to analyze real estate objects put up for sale.
The goal of the work is to find the most attractive (valuable) options 
when investing in real estate. The project is complete. But it can be improved,
for example, by entering data about the location of the object and 
conducting an analysis against the area assessment index.
As an example, the final result is given in "apartments_decision.csv".

## 🚀 Functionality

- 🔹 Data scraping
- 🔹 Joining two or more tables
- 🔹 Creating a result table by adding calculated columns
- 🔹 Definition of a first-order function describing 
      a potential buyer's interest in an object over time
- 🔹 Defining the function and calculating the coefficient of interest decay


### Requirements
- Python 3.8+

### Instruction
```bash
# Cloning a repository
git clone https://github.com/Serg78935/scraper_data.git
cd yourrepo

# Installing dependencies
pip install requests
pip install selenium
pip install beautifulsoup4
pip install chromedriver
pip install datetime
pip install pandas

## 💡 Using

  The first (basic) script for collecting data from the "dom ria" site.
The result is a table of 8 indicators that characterize the real estate object,
2 of which will change over time: views, scraper_date. You can specify 
the number of pages for collecting data (string 104).
   Next, you can rename the table using the "rename table" script and 
thus use the main script to build multiple tables with the corresponding 
values: views_n, scraper_data_n.
  If something goes wrong you can delete any table by "delete table".
  You can see the list of tables by "List of tables that are stored".
  You can check the contents of the tables by "Checking saved  data of all stored tables"
  You can join two or more tables by " Merging tab1 and tab2 using FULL OUTER JOIN".
  And finally, you can create a result table that will help you choose 
the most valuable options for real estate investment 
by "Interest in real estate is displayed in a pivot table".
  If you need to store result in .csv format please launch miniscript (string from 124 to 154).


## 📌 Development plan
- 📌 Defining district assessment criteria
- 📌 Defining a function to describe the district rating
- 📌 Documentation improvements

## 📝 License

This project is licensed under the [MIT](LICENSE) license.

## 🤝 Contacts

If you have any questions, please contact me at [serg.20.10.1963@gmail.com] or create an Issue in the repository.
"""
