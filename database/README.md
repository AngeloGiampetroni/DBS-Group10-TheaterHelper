### Database Setup

Open MySQL Workbench and connect to your local MySQL server.
Open the table script (`TheaterHelperDB TABLES.sql`).
Execute the script to generate the `theater` database and its tables.
Run the TheaterHelperDB MOCKDATA.sql script to populate the tables with sample data.

 ```pip install -r requirements.txt```

Streamlit Configuration

Streamlit requires a local secrets file to connect to the database.

Create a folder named `.streamlit` in the root of the project.
Inside that folder, create a file named `secrets.toml`.
should look like this:
```
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
streamlit run database_debug.py
```