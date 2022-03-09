# cs5293sp22-project0
# Text Analytics - Project 0 - Data Import using Python

# **Libraries Used**

**requests** - <https://docs.python-requests.org/en/latest/>

The requests module is utilized to download the file from the URL provided to the program

**PyPDF2** - (PyPDF2 1.26.0) <https://pypi.org/project/PyPDF2/>

The PyPDF2 module is used to read and extract data from the PDF file   

**re (Regex)** - <https://docs.python.org/3/library/re.html>

The re module is used to perform regular expression operations on the extracted data

**csv** - <https://docs.python.org/3/library/csv.html>

The csv module is utilized to read and write data to and from csv files respectively.

**sqlite3** - <https://docs.python.org/3/library/sqlite3.html>

The above module is used for all the database operations required for the project.

**pytest** - <https://docs.pytest.org/en/7.0.x/>

The above module is used to run the test cases written.

**os.path** - <https://docs.python.org/3/library/os.path.html>

The above module is used for accessing files in the project directory during testing.


# **Functions**

## fetchincidents

**_arguments required_** : url <string>

The requests module is used to retrieve the PDF file using the provided URL. The file is then written to the project directory using the built-in write() method, and the file name is returned.

## extractincidents

**_arguments required_** : file_name <string> (Name of the PDF file)

In this function, the text from the PDF file is extracted and written to a csv file. 

This method uses the in built file operation method open() to open the file_name provided. It is assumed that the file is present in the current working directory
A PDF file reader object is created using the PdfFileReader from the PyPDF2 module to read the file.

The file is read using a loop and the data is extracted using the extractText() method. The extracted data is appended to a string. As the data extracted has the new line character as the separator, the string is split on \n to obtain a list containing all the data fields

For setting up the csv file, the header is specified as a row first. The name of the csv file is constant and is opened in write mode to write the header set in the previous step.

The data is now in the form of a list and needs to be converted to a csv file. To achieve this, the list is iterated in a for loop and  regular expressions are used to identify if the value is for the date/time column or the Incident ORI column.
If the value matches the date/time column, it is marked as the start of a record through the flag. The value is then appended to a list and continues adding values to the list till the value matches the Incident ORI column. Each time a value is appended to the list, the count of values is incremented. Once it matches with the Incident ORI column values, the count is checked to see if there are any missing fields. If the count is 2; it implies that only the date time, incident number fields were present for the record before the incident ori value. In such case, two empty values are appended to the list. Else if the count is 4; it is implied that all values are present for the record. 
The values are then written as a row to the csv file. The flag, count and list are reset to continue with the process.

![project0-flow drawio (1)](https://user-images.githubusercontent.com/98193657/157372658-dc7029d7-e663-4e39-a7c0-6a7e242d83ce.png)
  
Once the process is completed, the name of the csv file is returned.

Note: Written code creates a csv file with no empty rows in between when run on jupyter lab where as the csv file has empty rows in between when run on the PyCharm IDE

## createdb

**No arguments are required for this method.**

This method creates and connects to the normanpd database using the sqlite3 module (The database is created if it is not present)
To perform database operations, a cursor object is created using the connection to the database from the previous step.
If the database already exists, the 'incidents' table is dropped using the drop table command and is created once again.
The method then returns the name of the database file,

## populatedb
**_arguments required_** : db <string> (Name of the database file name), incidents <string> (Name of the csv file name)

From the arguments, the csv file is opened and read using the csv module. The query to insert the data into the table is defined and a connection to the database is opened along with a cursor using the first argument.

Now, the data from the csv file is iterated and if the row is not empty, data from the row is inserted into the database using the insert query.
**Note**: This can be done using executemany() without iterating if the csv file doesn't contain any empty records in between

*Refer to below screenshots for difference*
![JupyterLab Gen CSV](https://user-images.githubusercontent.com/98193657/157362700-33bbc8a5-bab1-4d76-817d-2ee6601f6d00.png)
![PyCharm Gen CSV](https://user-images.githubusercontent.com/98193657/157362702-7d666c67-28eb-4066-8666-14a2b57bbea4.png)
  
  
Once all the data is inserted, the changes are then commited using the commit() method.

Note: This function doesn't return any values

## status
**_arguments required_** : db <string> (Name of the database file name)

Using the database name, a connection is opened and a cursor object is created to perform the fetch operation.
The query fetches the nature of all incidents and count of each incident. These records are grouped together based on the nature and the ordered in descending order based on the count. Once fetched, the result is in the form of a list. The list is then iterated and printed.

**Note**: This function returns all the values fetched from the database but is not utilized in main.py. This will be utilized for testing purpose.

# Testing

## Test Cases:

## test_fetchincidents
Runs the fetchincidents function with a url and checks if the PDF file (returned from the method) is created/present in the current directory 

## test_extractincidents
Runs the extractincidents function with the name of a pdf file and checks if a csv file (returned from the method) is created/present in the current directory 

## test_createdb
Runs the createdb function and checks if the database file (returned from the method) is created/present in the current directory

## test_populatedb
Runs the populatedb function using the database and csv file names. The csv file is read and iterated over the data to find the number of rows present. Similarly, a connection to the database is opened and a cursor object is created to extract the count of records present in the database.

The number of rows in the csv file and number of records are asserted. Also, both the values are compared to ensure all available data is populated in the database.

## test_status
Runs the status function with the database name. The returned values from the method are then iterated over to obtain the different number of natures available in the database.

## Steps for local deployment

1] Clone the repository using the below command
git clone https://github.com/SSharath-Kumar/cs5293sp22-project0

2] Install the required dependencies using the command:
pipenv install

## Running the project
pipenv run python main.py --incidents (url)

## Running the test cases
pipenv run python -m pytest
