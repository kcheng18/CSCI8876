# CSCI 8876 Project
## Entity Relationship Diagram
![Image of ERD](https://github.com/kcheng18/CSCI8876/ERD.jpeg)

## Requestment:

### Python Version
* Python 3.6 or above

#### Install those python library if you don't have them

* gensim
* spacy
* mysql
* nltk
* numpy
* pandas

#### Run this in terminal or command prompt
```bash
python3 -m spacy download en
```

## Installing MySQL:
### For macOS: 
https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/osx-installation-pkg.html

### Installing MySQL Workbench:
https://dev.mysql.com/downloads/workbench/5.2.html

### Creating table to the DB:
Go to database directory and run it:
```bash
mysql -u [username] -p [database_name] < table.sql
```

### If you want to drop all the tables:
```bash
mysql -u [username] -p [database_name] < droptable.sql
```

### Access MySQL:
```bash
/usr/local/mysql/bin/mysql -u username -p
Enter password:
```

## Application:

### Before run the application:
Inserting all data from the 'data' folder into the DB:

Note: changing the information of your DB at the head of the workspace/database/insert.py before do this step

```bash
python3 insertData2DB.py
```

### Start Running the application
Go to the workspace/application directory run it:

Note: changing the information of your DB at the head of the workspace/application/selectDB.py before do this step

```bash
python3 main.py
```
Follow the interface to use it