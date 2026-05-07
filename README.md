# DBS-Group10-TheaterHelper
UWM CS557 Group 10 semester project. A webapp solution for an individual movie theater to keep track of movie/attendee data &amp; statistics.

### Database + App Setup
1. Download MySQL server and Workbench at
[mysql.com](https://dev.mysql.com/downloads/installer/)

2. Create a schema named `theater`

3. Open MySQL Workbench and connect to your local MySQL server.
Open the table script (`TheaterHelperDB TABLES.sql`).
Execute the script to generate the `theater` database and its tables.
Run the TheaterHelperDB MOCKDATA.sql(OR TheaterHelperDB.sql) script to populate the tables with sample data.


### Streamlit Configuration
Install python packages:

```
python -m pip install -r requirements.txt
```

Streamlit requires a local secrets file to connect to the database.

Create a folder named `.streamlit` in the root of the project.
Inside that folder, create a file named `secrets.toml`.
should look like this:
```toml
[connections.mysql]
dialect = "mysql"
host = "localhost"
port = 3306
database = "theater"
username = "root" 
password = "<WHAT_YOUR_SQL_WORKBENCH_PASSWORD_IS>"
query = { charset = "utf8mb4" }
```

When the database is running and configured, start the app with the following command:

```
python -m streamlit run database_debug.py
```
