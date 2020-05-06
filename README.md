# CSCI 8876 Project

## Installing MySQL:
For macOS: 
https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/osx-installation-pkg.html

Installing MySQL Workbench:
https://dev.mysql.com/downloads/workbench/5.2.html

Creating table to the DB:
```bash
mysql -u username -p database_name < file.sql
```

Access MySQL:
```bash
/usr/local/mysql/bin/mysql -u username -p
Enter password:
```

## Application:

### Before run the application:

Inserting all data from the 'data' folder:
```bash
python3 insertData2DB.py
```

Note: changing the information of your DB in the insert.py before do this step

### Requestment:
Python 3.6 or above

### Prerequisites:

#### Run this in terminal or command prompt
```bash
python3 -m spacy download en
```

#### install those python library if you don't have them
gensim

spacy

mysql

nltk

numpy

pandas

### Start Running the application
#### At the application directory run it:
```bash
python3 main.py
```

Follow the interface to use it