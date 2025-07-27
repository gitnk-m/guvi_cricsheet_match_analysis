import mysql.connector
# import json 

dbSetup = True # Set to False if you don't want to create the database


class mySQLDB:
    def __init__(self, host='localhost', user='root', password='', database='test', port=4000):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.connection.cursor()
    
    # Create a database if it does not exist
    def create_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.connection.commit()
    
    # Use a specific database    
    def use_database(self, db_name):
        self.cursor.execute(f"USE {db_name}")
        self.connection.commit()

    def create_table(self, table_name, columns, constraints=None):
        columns_with_types = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        constraints_sql = ""
        for constraint, details in constraints.items():
            if constraint == "PRIMARY KEY":
                constraints_sql+=f", CONSTRAINT {details[0]} PRIMARY KEY ({details[1]})"
            elif constraint == "FOREIGN KEY":
                constraints_sql+=f", CONSTRAINT {details[0]} FOREIGN KEY ({details[1]}) REFERENCES {details[2]} ON UPDATE CASCADE ON DELETE RESTRICT"
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types} {constraints_sql})")
        self.connection.commit()
        # print(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types} {constraints_sql})")
    
    def insert_data(self, table_name, data):
        columns = ', '.join(data[0].keys())
        values = ', '.join(['%s'] * len(data[0]))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        values_list = [tuple(item.values()) for item in data]
        self.cursor.executemany(sql, values_list)
        self.connection.commit()
        
    def select_data(self, table_name, columns='*', where=None):
        sql = f"SELECT {columns} FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def drop_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()

    # Close the cursor and connection
    def close(self):
        self.cursor.close()
        self.connection.close()
        


db = mySQLDB(
    host = 'gateway01.us-west-2.prod.aws.tidbcloud.com',
    user = '2giLRMddJvjQq3S.root',
    password = 'RBujztoEPbUH8Mhy',
    port = 4000
    )

if dbSetup:
    try:
        # Create the database if it does not exist
        db.create_database("crickSheet_analysis")

        # Use the created database
        db.use_database("crickSheet_analysis")

    except(mysql.connector.Error, mysql.connector.Warning) as e:
        print(f"An error occurred: {e}")
        db.connection.rollback()
    finally:
        db.close()
        print("Database operations completed.")