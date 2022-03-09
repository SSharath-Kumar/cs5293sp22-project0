# To handle csv read/write
import csv
# To handle PDF file read
from PyPDF2 import PdfFileReader
# To handle file download from url
import requests
# Regex library for regular expressions
import re
# To handle sqlite3 database
import sqlite3

def fetchincidents(url):
    # get file from URL
    file = requests.get(url)
    # save PDF file on local drive
    with open('incident_file.pdf', 'wb') as fp:
        fp.write(file.content)

    return 'incident_file.pdf'

def extractincidents(file_name):
    # create a file Object
    fileObj = open(file_name, 'rb')

    # create a new reader object for the pdf file
    fileReader = PdfFileReader(fileObj)

    # initialize string to hold extracted data
    text_data = ''

    # Loop through all pages of the file and add the text to the string
    for i in range(fileReader.numPages):
        text_data += fileReader.getPage(i).extractText()

    # Split data on new line to get into array format
    text_data = text_data.split("\n")
    # print(text_data)

    # Setting the header for the CSV File
    fields = ['Date/Time', 'Incident Number', 'Location', 'Nature', 'Incident ORI']
    # Set the file name
    csv_file_name = 'inc_data.csv'
    # Open the file & write the header to the file
    with open(csv_file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

    flag = False
    row = []
    count = 0
    csv_count = 0

    # have the file open while data is processed
    with open(csv_file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for value in text_data:
            if flag:
                # Flag == TRUE
                if re.match(r"(EMSSTAT|OK[0-9]{7}|[0-9]{5}$)", value) is not None:
                    # Value is INC-ORI
                    if count == 2:
                        row.append('')
                        row.append('')
                    row.append(value)

                    # display row before insertion
                    # print(row)

                    # edge case - if record has multiple lines of address
                    if len(row) == 6:
                        row[2] += row.pop(3)

                    # write to csv file
                    csvwriter.writerow(row)
                    csv_count += 1
                    # Reset row and count
                    row.clear()
                    count = 0

                    # Reset flag
                    flag = False
                else:
                    # for values of other columns
                    row.append(value)
                    count += 1
            else:
                # Flag == FALSE
                if re.match(r"\d/\d/\d{4} \d\d?:\d{2}", value) is not None:
                    flag = True
                    row.append(value)
                    count += 1
                else:
                    continue
    fileObj.close()
    return csv_file_name

def createdb():
    # setting the database file name
    database = 'normanpd.db'
    try:
        # connect to the database
        conn = sqlite3.connect(database)
        # print("DB CREATED!")
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Doping incidents table if already exists.
        cursor.execute("DROP TABLE IF EXISTS incidents")
        # Setting up the table using the create table command
        createTable = '''
        CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        );
        '''
        cursor.execute(createTable)

    except sqlite3.Error as e:
        print(e)
    return  database

def populatedb(db, incidents):
    # open the csv file
    csvFile = open(incidents)
    # read the csv file
    data = csv.reader(csvFile)

    insert_records = '''INSERT INTO incidents 
        (incident_time,
         incident_number,
         incident_location,
         nature,
         incident_ori)
        VALUES(?,?,?,?,?)'''

    conn = sqlite3.connect(db)
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Insert all the records from the csv file to the database
    for row in data:
        if len(row) == 0:
            continue
        cursor.execute(insert_records, row)

    # cursor.executemany(insert_records, data)
    # commit all the changes done to the database
    conn.commit()

def status(db):
    conn = sqlite3.connect(db)
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    inc_details = cursor.execute("select nature, count(nature) from incidents group by nature order by count(nature) desc;").fetchall()
    for record in inc_details:
        print(record[0],'|',record[1])
    return inc_details
