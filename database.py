import mysql.connector
# import json 

dbSetup = False # Set to False if you don't want to create the database


class mySQLDB:
    def __init__(self, host='localhost', user='root', password='', database='test', port=4000):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            # password=password,
            # database=database,
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
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        # values_list = [tuple(data[item]) for item in data]
        values_list = [tuple(data.values()) ]
        self.cursor.executemany(sql, values_list)
        self.connection.commit()
    
    def insert_data_player_stats(self, table_name, data, sum_fields, compare_fields):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sum_updates = ', '.join([f"{field} = {field} + VALUES({field})" for field in sum_fields])
        compare_updates = ', '.join([f"{field} = GREATEST({field}, VALUES({'runs' if field == 'highest_score' else field}))" for field in compare_fields])
        updates = sum_updates+", "+compare_updates
        sql = f'''
            INSERT INTO {table_name} ({columns}) 
            VALUES ({values})
            ON DUPLICATE KEY UPDATE {updates}'''
        # values_list = [tuple(data[item]) for item in data]
        values_list = [tuple(data.values()) ]
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
        


# db = mySQLDB(
#     host = 'gateway01.us-west-2.prod.aws.tidbcloud.com',
#     user = '2giLRMddJvjQq3S.root',
#     password = 'RBujztoEPbUH8Mhy',
#     port = 4000
#     )

db = mySQLDB(
    host = 'localhost',
    user = 'root',
    port = 3306
    )

if dbSetup:
    try:
        # Create the database if it does not exist
        db.create_database("crickSheet_analysis")

        # Use the created database
        db.use_database("crickSheet_analysis")

         # Create the test_match table
        db.create_table("matchs", {
            "match_id": "VARCHAR(20)",
            "city": "VARCHAR(100)",
            "venue": "VARCHAR(300)",
            "date": "JSON",
            "match_type": "VARCHAR(10)",
            "team_type": "VARCHAR(20)",
            "event": "JSON",
            "teams": "JSON",
            "gender": "VARCHAR(10)",
            "officials": "JSON",
            "player_of_the_match": "JSON",
            "players_registry": "JSON",
            "toss": "JSON",
            "outcome": "JSON",
            "innings": "JSON",
        }, {
            "PRIMARY KEY": ["pk_match_id", "match_id"],
            
        })

        # Create the players_test table for palyer statistics in test matches
        db.create_table("players_test", {
            "player_id": "VARCHAR(20)",
            "name": "VARCHAR(100)",
            "country": "VARCHAR(100)",
            "matches": "INT",
            "batted_innings": "INT",
            "balls_faced": "INT",
            "runs": "INT",
            "not_outs": "INT",
            "highest_score": "INT",
            "batting_average": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_faced > 0 AND (batted_innings - not_outs) > 0 THEN ROUND(runs / (batted_innings - not_outs), 2)  ELSE 0 END) STORED",
            "strike_rate": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_faced > 0 AND runs > 0 THEN ROUND((runs / balls_faced) * 100, 2) ELSE 0 END) STORED",
            "hundreds": "INT",
            "fifties": "INT",
            "fours": "INT",
            "sixes": "INT",
            "wicket_by_catches": "INT",
            "wicket_by_stumpings": "INT",
            "catches": "INT",
            "stumpings": "INT",
            "balls_bowled": "INT",
            "run_conceded":"INT",
            "wickets": "INT",
            "bowling_average": "FLOAT GENERATED ALWAYS AS (CASE WHEN wickets > 0 AND run_conceded > 0 THEN ROUND(run_conceded / wickets, 2)  ELSE 0 END) STORED",
            "economy": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_bowled > 0 AND run_conceded > 0 THEN ROUND(run_conceded / balls_bowled / 6, 2)  ELSE 0 END) STORED",
            "bowling_SR": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_bowled > 0 AND wickets > 0 THEN ROUND(balls_bowled / wickets, 2) ELSE 0 END) STORED",
            "five_wickets": "INT",
            "ten_wickets": "INT",
            "maidens": "INT"
            }, {
            "PRIMARY KEY": ["pk_player_id", "player_id"],
            })

        # Create the players_odi table for player statistics in ODI matches
        db.create_table("players_odi", {
            "player_id": "VARCHAR(20)",
            "name": "VARCHAR(100)",
            "country": "VARCHAR(100)",
            "matches": "INT",
            "batted_innings": "INT",
            "balls_faced": "INT",
            "runs": "INT",
            "not_outs": "INT",
            "highest_score": "INT",
            "batting_average": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_faced > 0 AND (batted_innings - not_outs) > 0 THEN ROUND(runs / (batted_innings - not_outs), 2)  ELSE 0 END) STORED",
            "strike_rate": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_faced > 0 AND runs > 0 THEN ROUND((runs / balls_faced) * 100, 2) ELSE 0 END) STORED",
            "hundreds": "INT",
            "fifties": "INT",
            "fours": "INT",
            "sixes": "INT",
            "wicket_by_catches": "INT",
            "wicket_by_stumpings": "INT",
            "catches": "INT",
            "stumpings": "INT",
            "balls_bowled": "INT",
            "run_conceded":"INT",
            "wickets": "INT",
            "bowling_average": "FLOAT GENERATED ALWAYS AS (CASE WHEN wickets > 0 AND run_conceded > 0 THEN ROUND(run_conceded / wickets, 2)  ELSE 0 END) STORED",
            "economy": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_bowled > 0 AND run_conceded > 0 THEN ROUND(run_conceded / balls_bowled / 6, 2)  ELSE 0 END) STORED",
            "bowling_SR": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_bowled > 0 AND wickets > 0 THEN ROUND(balls_bowled / wickets, 2) ELSE 0 END) STORED",
            "five_wickets": "INT",
            "ten_wickets": "INT",
            "maidens": "INT"
            }, {
            "PRIMARY KEY": ["pk_player_id", "player_id"],
            })

        # Create the players_t20 table for player statistics in T20 matches
        db.create_table("players_t20", {
                "player_id": "VARCHAR(20)",
                "name": "VARCHAR(100)",
                "country": "VARCHAR(100)",
                "matches": "INT",
                "batted_innings": "INT",
                "balls_faced": "INT",
                "runs": "INT",
                "not_outs": "INT",
                "highest_score": "INT",
                "batting_average": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_faced > 0 AND (batted_innings - not_outs) > 0 THEN ROUND(runs / (batted_innings - not_outs), 2)  ELSE 0 END) STORED",
                "strike_rate": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_faced > 0 AND runs > 0 THEN ROUND((runs / balls_faced) * 100, 2) ELSE 0 END) STORED",
                "hundreds": "INT",
                "fifties": "INT",
                "fours": "INT",
                "sixes": "INT",
                "wicket_by_catches": "INT",
                "wicket_by_stumpings": "INT",
                "catches": "INT",
                "stumpings": "INT",
                "balls_bowled": "INT",
                "run_conceded":"INT",
                "wickets": "INT",
                "bowling_average": "FLOAT GENERATED ALWAYS AS (CASE WHEN wickets > 0 AND run_conceded > 0 THEN ROUND(run_conceded / wickets, 2)  ELSE 0 END) STORED",
                "economy": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_bowled > 0 AND run_conceded > 0 THEN ROUND(run_conceded / balls_bowled / 6, 2)  ELSE 0 END) STORED",
                "bowling_SR": "FLOAT GENERATED ALWAYS AS (CASE WHEN balls_bowled > 0 AND wickets > 0 THEN ROUND(balls_bowled / wickets, 2) ELSE 0 END) STORED",
                "five_wickets": "INT",
                "ten_wickets": "INT",
                "maidens": "INT"
                }, {
                "PRIMARY KEY": ["pk_player_id", "player_id"],
                })


    except(mysql.connector.Error, mysql.connector.Warning) as e:
        print(f"An error occurred: {e}")
        db.connection.rollback()
    finally:
        db.close()
        print("Database operations completed.")