import os.path
import project0
import csv
import sqlite3


def test_fetchincidents():
    file_name = project0.fetchincidents(
        'https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf')
    assert os.path.exists('./' + file_name)


def test_extractincidents():
    csv_file = project0.extractincidents('incident_file.pdf')
    assert os.path.exists('./' + csv_file)


def test_createdb():
    db = project0.createdb()
    assert os.path.exists('./' + db)


def test_populatedb():
    # Required variables for method
    db_name = 'normanpd.db'
    # db = sqlite3.connect('normanpd.db')
    csv_file = 'inc_data.csv'
    # Method call
    project0.populatedb(db_name, csv_file)
    connection = sqlite3.connect(db_name)
    # Read CSV and get number of rows
    row_count = 0
    with open(csv_file) as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) !=0:
                row_count += 1


    # Creating a cursor object using the cursor() method
    cursor = connection.cursor()

    # Execute the command to see the status of the incidents
    db_status = cursor.execute("SELECT COUNT(*) FROM incidents;")
    status = db_status.fetchall()
    db_count = status[0][0]
    print(status[0][0])

    assert row_count > 0
    assert db_count > 0
    assert db_count == row_count



def test_status():
    db = 'normanpd.db'
    status = project0.status(db)
    groups = 0
    for category in status:
        groups += 1
    assert groups > 0