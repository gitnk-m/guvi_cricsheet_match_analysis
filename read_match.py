import json
import os
import zipfile
from database import mySQLDB

db = mySQLDB(
    host = 'localhost',
    user = 'root',
    port = 3306
)

class Match:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load_data()
        self.records = {}
        self.inning_count = 0

# Load the JSON data from the file
    # def load_data(self):
    #     with open(f'Downloads/{self.file_name}.json', 'r') as file:
    #         print(self.file_name)
    #         return json.load(file)

    def load_data(self):
        with zipfile.ZipFile('Downloads/all_json.zip', 'r') as zip_ref:
            if f'{self.file_name}.json' in zip_ref.namelist():
                with zip_ref.open(f'{self.file_name}.json') as file:
                    data = json.load(file)
                    if data.get("info").get("match_type") in ["Test", "ODI", "T20", "IT20"]:
                        return data
                    else :
                        return False
            else:
                raise FileNotFoundError(f"{self.file_name}.json not found in the zip file.")
    
# is valid match (test, ODI, T20)
    def is_valid_match(self):
        match_type = self.data.get("info", {}).get("match_type", "")
        return match_type in ["Test", "ODI", "T20", "IT20"]
    
# Extract all deliveries from the innings
    def extract_innings(self):
        # self.records = {}
        innings = self.data['innings']

        formatted_innings = {}
        # Iterate through each inning
        for inning in innings:
            self.inning_count += 1
            # set up initial variables of the inning
            team = inning['team']
            total = 0
            batting = {}
            bowling = {}
            extras = 0
            fall_of_wickets = []

            # Iterate through each over in the inning
            if "overs" in inning and inning["overs"]:
                for over in inning['overs']:
                    # set up variables for the over
                    run_in_over = 0
                    ball_count = 0
                    # Iterate through each delivery in the over
                    for delivery in over['deliveries']:
                        ball_count += 1
                        # bowler_id = self.data["info"]["registry"]["people"][delivery.get("bowler")]
                        # batter_id = self.data["info"]["registry"]["people"][delivery.get("batter")]

                        bowler_id = delivery.get("bowler")
                        batter_id = delivery.get("batter")

                        # Check for Maiden Over
                        if delivery.get("extras") and (delivery["extras"].get("wides") or delivery["extras"].get("noballs")):
                            run_in_over += delivery["runs"].get("batter", 0) + delivery.get("extras", {}).get("wides", 0) + delivery.get("extras", {}).get("noballs", 0)
                        else:
                            run_in_over += delivery["runs"].get("batter", 0)

                        # Track of Total Runs
                        total += delivery["runs"].get("total", 0)

                        # Track of Batsman
                        if batter_id not in batting.keys():
                            batting[batter_id] = {
                                "run": delivery["runs"].get("batter", 0),
                                "ball": 1,
                                "0s": 0, "1s": 0, "2s": 0, "3s": 0, "4s": 0, "6s": 0,
                                "strike_rate": 0,
                                "wicket": "not out"
                            }
                            # Update runs and balls for the batsman
                            if delivery["runs"].get("batter", 0) == 0:
                                batting[batter_id]["0s"] = 1
                            elif delivery["runs"].get("batter", 0) == 1:
                                batting[batter_id]["1s"] = 1
                            elif delivery["runs"].get("batter", 0) == 2:
                                batting[batter_id]["2s"] = 1
                            elif delivery["runs"].get("batter", 0) == 3:
                                batting[batter_id]["3s"] = 1
                            elif delivery["runs"].get("batter", 0) == 4:
                                batting[batter_id]["4s"] = 1
                            elif delivery["runs"].get("batter", 0) == 6:
                                batting[batter_id]["6s"] = 1
                            batting[batter_id]["strike_rate"] = (batting[batter_id]["run"] / batting[batter_id]["ball"]) * 100

                        else:
                            batting[batter_id]["run"] += delivery["runs"].get("batter", 0)
                            batting[batter_id]["ball"] += 1
                            
                            # Update runs and balls for the batsman
                            if delivery["runs"].get("batter", 0) == 0:
                                batting[batter_id]["0s"] += 1
                            elif delivery["runs"].get("batter", 0) == 1:
                                batting[batter_id]["1s"] += 1
                            elif delivery["runs"].get("batter", 0) == 2:
                                batting[batter_id]["2s"] += 1
                            elif delivery["runs"].get("batter", 0) == 3:
                                batting[batter_id]["3s"] += 1
                            elif delivery["runs"].get("batter", 0) == 4:
                                batting[batter_id]["4s"] += 1
                            elif delivery["runs"].get("batter", 0) == 6:
                                batting[batter_id]["6s"] += 1
                            batting[batter_id]["strike_rate"] = round((batting[batter_id]["run"] / batting[batter_id]["ball"]) * 100, 2)

                        # Track of Bowler
                        if bowler_id not in bowling.keys():
                            bowling[bowler_id] = {
                                "ball": 1,
                                "run": delivery["runs"].get("batter", 0),
                                "wicket": 0,
                                "economy": 0,
                                "maidens": 0,
                                "no_balls": 0,
                                "wides": 0
                            }
                            if delivery.get("extras") and delivery["extras"].get("wides"):
                                bowling[bowler_id]["wides"] += delivery["extras"].get("wides", 0)
                                bowling[bowler_id]["ball"] -= 1
                                bowling[bowler_id]["run"] += 1
                            if delivery.get("extras") and delivery["extras"].get("noballs"):
                                bowling[bowler_id]["no_balls"] += delivery["extras"].get("noballs", 0)
                                bowling[bowler_id]["ball"] -= 1
                                bowling[bowler_id]["run"] += 1
                            if delivery.get("wickets"):
                                bowling[bowler_id]["wicket"] += 1
                            
                            bowling[bowler_id]["economy"] = round(bowling[bowler_id]["run"] / (bowling[bowler_id]["ball"]+1) * 6, 2)
                        else:
                            bowling[bowler_id]["ball"] += 1
                            bowling[bowler_id]["run"] += delivery["runs"].get("batter", 0)
                            if delivery.get("extras") and delivery["extras"].get("wides"):
                                bowling[bowler_id]["wides"] += delivery["extras"].get("wides", 0)
                                bowling[bowler_id]["ball"] -= 1
                                bowling[bowler_id]["run"] += 1
                            if delivery.get("extras") and delivery["extras"].get("noballs"):
                                bowling[bowler_id]["no_balls"] += delivery["extras"].get("noballs", 0)
                                bowling[bowler_id]["ball"] -= 1
                                bowling[bowler_id]["run"] += 1
                            if delivery.get("wickets"):
                                bowling[bowler_id]["wicket"] += 1
                            bowling[bowler_id]["economy"] = round(bowling[bowler_id]["run"] / (bowling[bowler_id]["ball"]+1) * 6, 2)
                        
                        # Track of Extras
                        if delivery.get("extras"):
                            extras += delivery["extras"].get("wides", 0) + delivery["extras"].get("noballs", 0) + delivery["extras"].get("byes", 0) + delivery["extras"].get("legbyes", 0)
                            if "penalty" in delivery["extras"]:
                                extras += delivery["extras"]["penalty"]

                        # Track of Fall of Wickets
                        if delivery.get("wickets"):
                            if isinstance(delivery['wickets'], list):
                                for wicket in delivery['wickets']:
                                    wicket["bowler"] = bowler_id
                                    wicket["ball"] = f'''{over.get("over")}.{ball_count}'''
                                    wicket["runs"] = batting[batter_id]["run"]
                                    batting[batter_id]["wicket"] = wicket
                                    # Fall of Wickets
                                    fall_of_wickets.append(wicket)
                            else:
                                batting[batter_id]["wicket"] = delivery['wickets'].get("kind", "not out")

                # Check for Maiden Over
                if run_in_over == 0 and ball_count == 6:
                    bowling[bowler_id]["maidens"] += 1

                # Store the inning record
                # self.records[f'innings_{self.inning_count}'] = {
                #     "team": team,
                #     "total": total,
                #     "batting": batting,
                #     "bowling": bowling,
                #     "extras": extras,
                #     "fall_of_wickets": fall_of_wickets
                #     }
                formatted_innings[f'innings_{self.inning_count}'] = {
                    "team": team,
                    "total": total,
                    "batting": batting,
                    "bowling": bowling,
                    "extras": extras,
                    "fall_of_wickets": fall_of_wickets
                }
            else:
                # self.records[f'spl_innings'] = inning
                formatted_innings["spl_innings"]= inning
        # Store the formatted innings in records
        self.records["innings"] = formatted_innings

#  Trial to add match info using method calling
    def add_record(self, key, value):
        self.records[key] = value

# Insert match info at the beginning of records
    def match_info(self):
        players_list = {}

        # Iterate through each team and player
        for country, players in self.data.get("info")["players"].items():
            for player_name in players:
                player_id = self.data.get("info")["registry"]["people"].get(player_name)
                if player_id:
                    players_list[player_id]= {
                            "name": player_name,
                            "country": country
                        }
                    
        self.add_record ("match_id", self.file_name)
        # self.records["match_id"] =self.file_name
        self.records ["city"]= self.data.get("info").get("city", "Unknown")
        self.records ["venue"]= self.data.get("info").get("venue", "Unknown")
        self.records ["date"]= self.data.get("info").get("dates", [])
        self.records ["match_type"]= self.data.get("info").get("match_type", "Unknown")
        self.records ["team_type"]= self.data.get("info").get("team_type", "Unknown")
        self.records ["event"]= self.data.get("info").get("event", [])
        self.records ["teams"]=self.data.get("info").get("teams", [])
        self.records ["gender"]=self.data.get("info").get("gender", "Unknown")
        self.records ["officials"]= self.data.get("info").get("officials", [])
        self.records ["player_of_the_match"]= self.data.get("info").get("player_of_match", [])
        self.records ["players_registry"] =players_list
        # self.records ["playres"]= self.data.get("info").get("players", [])
        self.records ["toss"] = self.data.get("info").get("toss", [])
        self.records ["outcome"]= self.data.get("info").get("outcome", [])

    def match_info_2(self):
        self.records["info"] = self.data.get("info", {})
        self.records["info"]["match_id"] = self.file_name

# Save the records to a JSON file
    def save_records(self, output_file):
        with open(output_file, 'w') as file:
            json.dump(self.records, file, indent=4)
        print(f"Records saved to {output_file}")

    def save_file(self, output_file):
        with open(output_file, 'a') as file:
            file.write(f"{self.file_name}\n")

    def reject_match(self, output_file):
        with open(output_file, 'a') as file:
            file.write(f"{self.file_name}\n")

# Generate a DataFrame from the records and save it to a CSV file
    def df_generate(self):
        import pandas as pd
        df = pd.DataFrame(self.records)
        df.to_csv(f'{self.file_name}.csv', index=False)
        print(f"DataFrame saved to {self.file_name}.csv")

# Save the match data to the database
    def save_match(self):
        # Assuming db is an instance of a database connection class
        formatted = {}
        for key, value in self.records.items():
            if isinstance(value, dict):
                formatted[key] = json.dumps(value)
            elif isinstance(value, list):
                formatted[key] = json.dumps(value)
            else:
                formatted[key] = value
        # Use the created database
        db.use_database("crickSheet_analysis")
        # insert data into the test_match table
        db.insert_data("matchs", formatted)
        print(f"Records for match {self.file_name} saved to database.")

    def get_palyer_stats(self):
        # Getting player statistics from the records
        player_stats = {}
        for id, player in self.records["players_registry"].items():
            player_stats[id] = {
                "name": player["name"],
                "country": player["country"],
                "match":1,
                "batted_innings": 0,
                "balls_faced": 0,
                "runs": 0,
                "not_outs": 0,
                "fours": 0,
                "sixes": 0,
                "fifties":0,
                "hundreds":0,
                "highest_score":0,
                "wicket_by_catches": 0,
                "wicket_by_stumpings": 0,
                "wicket_by_bowled": 0,
                "balls_bowled": 0,
                "run_conceded":0,
                "wickets": 0,
                "best_bowling": "0/0",
                "five_wickets": 0,
                "ten_wickets": 0,
                "maidens": 0,
                "catches": 0,
                "stumpings": 0,
                }
        # Iterate through each inning and update player statistics
        for inning in self.records["innings"].values():
            if "batting" in inning and inning["batting"]:
                for player, stats in inning["batting"].items():
                    player_id = next(
                        (playerID for playerID in player_stats if player_stats[playerID]["name"] == player),
                        None  # Default if not found
                    )
                    if player_id:
                        player_stats[player_id]["batted_innings"] += 1
                        player_stats[player_id]["balls_faced"] += stats["ball"]
                        player_stats[player_id]["runs"] += stats["run"]
                        player_stats[player_id]["highest_score"] += stats["run"]
                        if stats["wicket"] == "not out":
                            player_stats[player_id]["not_outs"] += 1
                        player_stats[player_id]["fours"] += stats["4s"]
                        player_stats[player_id]["sixes"] += stats["6s"]
                        # check for century and fifties
                        if stats["run"]>100:
                            player_stats[player_id]["hundreds"] += 1
                        elif stats["run"]>50 and stats["run"]<100:
                            player_stats[player_id]["fifties"] += 1
                        if isinstance(stats["wicket"], dict):
                            if stats["wicket"]["kind"] == "caught":
                                player_stats[player_id]["wicket_by_catches"] += 1
                            elif stats["wicket"]["kind"] == "stumped":
                                player_stats[player_id]["wicket_by_stumpings"] += 1
                            elif stats["wicket"]["kind"] == "bowled":
                                player_stats[player_id]["wicket_by_bowled"] += 1

            if "bowling" in inning and inning["bowling"]:
                for player, stats in inning["bowling"].items():
                    player_id = next(
                        (playerID for playerID in player_stats if player_stats[playerID]["name"] == player),
                        None  # Default if not found
                    )
                    if player_id:
                        player_stats[player_id]["balls_bowled"] += stats["ball"]
                        player_stats[player_id]["run_conceded"] += stats["run"]
                        player_stats[player_id]["wickets"] += stats["wicket"]
                        if stats["maidens"] > 0:
                            player_stats[player_id]["maidens"] += stats["maidens"]
                        if stats["wicket"] > 0:
                            player_stats[player_id]["best_bowling"] = f"{stats['run']}/{stats['wicket']}"
                        if stats["wicket"] >= 5:
                            player_stats[player_id]["five_wickets"] += 1
                        if stats["wicket"] >= 10:
                            player_stats[player_id]["ten_wickets"] += 1
            
            if "fall_of_wickets" in inning and inning["fall_of_wickets"]:
                for wicket in inning["fall_of_wickets"]:
                    if wicket.get("kind") in ["caught", "stumped"]:
                        for player in wicket.get("fielders"):
                            player_id = next(
                                (playerID for playerID in player_stats if player_stats[playerID]["name"] == player.get("name")),
                                None  # Default if not found
                            )
                            if player_id and wicket.get("kind") == "caught":
                                player_stats[player_id]["wicket_by_catches"] += 1
                            elif player_id and wicket.get("kind") == "stumped":
                                player_stats[player_id]["wicket_by_stumpings"] += 1
                        
        # store the player statistics in database
        for player_id, stats in player_stats.items():
            match.save_player_stats({
                "player_id": player_id,
                "name": stats["name"],
                "country": stats["country"],
                "matches": stats["match"],
                "batted_innings": stats["batted_innings"],
                "balls_faced": stats["balls_faced"],
                "runs": stats["runs"],
                "highest_score":stats["highest_score"],
                "not_outs": stats["not_outs"],
                "fours": stats["fours"],
                "sixes": stats["sixes"],
                "hundreds": stats["hundreds"],
                "fifties": stats["fifties"],
                "wicket_by_catches": stats["wicket_by_catches"],
                "wicket_by_stumpings": stats["wicket_by_stumpings"],
                "balls_bowled": stats["balls_bowled"],
                "wickets": stats["wickets"],
                "run_conceded": stats["run_conceded"],
                "five_wickets": stats["five_wickets"],
                "ten_wickets": stats["ten_wickets"],
                "maidens": stats["maidens"],
                "catches": stats["catches"],
                "stumpings": stats["stumpings"]
            }, [
                "matches",
                "batted_innings",
                "balls_faced",
                "runs",
                "not_outs",
                "hundreds",
                "fifties",
                "fours",
                "sixes",
                "wicket_by_catches",
                "wicket_by_stumpings",
                "catches",
                "stumpings",
                "balls_bowled",
                "run_conceded",
                "wickets",
                "maidens",
                "five_wickets",
                "ten_wickets"
            ], 
            [
                "highest_score",
            ])

    def save_player_stats(self, player_stats, sum_fields, compare_fields):
        # Assuming db is an instance of a database connection class
        formatted = {}
        for key, value in player_stats.items():
            if isinstance(value, dict):
                formatted[key] = json.dumps(value)
            elif isinstance(value, list):
                formatted[key] = json.dumps(value)
            else:
                formatted[key] = value
        if self.records["match_type"] == "Test":
            # Use the created database
            db.use_database("crickSheet_analysis")
            # insert data into the players_test table
            db.insert_data_player_stats("players_test", formatted, sum_fields, compare_fields)
        elif self.records["match_type"] == "ODI":
            # Use the created database
            db.use_database("crickSheet_analysis")
            # insert data into the players_odi table
            db.insert_data_player_stats("players_odi", formatted, sum_fields, compare_fields)
        elif self.records["match_type"] == "T20":
            # Use the created database
            db.use_database("crickSheet_analysis")
            # insert data into the players_t20 table
            db.insert_data_player_stats("players_t20", formatted, sum_fields, compare_fields)        
        print(f"Player stats for match {self.file_name} saved to database.")

# read match data from JSON file
# if __name__ == "__main__":
#     match = Match('63963')
#     # match.match_info_2()
#     if match.data:
#         match.match_info()
    # match.extract_innings()
    # match.save_match()
    # match.get_palyer_stats()
    # match.metaData()
    # match.save_records('test_oops_1.json')
    # match.df_generate()


# loop through all JSON files in the Downloads folder
# if __name__ == "__main__":
#     folder = 'Downloads'
#     for file in os.listdir(folder):
#         if file.endswith('.json'):
#             match_id = file.split('.')[0]
#             match = Match(match_id)
#             match.match_info()
#             match.extract_innings()
#             match.save_match()
#             match.get_palyer_stats()
#             # match.save_file(f'test_all.txt')


# loop through all JSON files in zip file
if __name__ == "__main__":
    zip_file = 'Downloads/all_json.zip'
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.json'):
                match_id = file.split('.')[0]
                match = Match(match_id)
                if match.data:
                    match.match_info()
                    match.extract_innings()
                    match.save_match()
                    match.get_palyer_stats()
                    match.save_file(f'test_all.txt')
                else:
                    match.reject_match(f'other_match.txt')

print("All match records processed and saved to test_all.txt")





# db = mySQLDB(
#     host = 'gateway01.us-west-2.prod.aws.tidbcloud.com',
#     user = '2giLRMddJvjQq3S.root',
#     password = 'RBujztoEPbUH8Mhy',
#     port = 4000
#     )