import json
import zipfile
from database import mySQLDB

db = mySQLDB(
    host = 'gateway01.us-west-2.prod.aws.tidbcloud.com',
    user = '2giLRMddJvjQq3S.root',
    password = 'RBujztoEPbUH8Mhy',
    port = 4000
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
                    return json.load(file)
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
                self.records[f'innings_{self.inning_count}'] = {
                    "team": team,
                    "total": total,
                    "batting": batting,
                    "bowling": bowling,
                    "extras": extras,
                    "fall_of_wickets": fall_of_wickets
                    }
            else:
                self.records[f'spl_innings'] = inning

#  Trial to add match info using method calling
    def add_record(self, key, value):
        self.records[key] = value

# Insert match info at the beginning of records
    def match_info(self):
        self.add_record ("match_id", self.file_name)
        # self.records["match_id"] =self.file_name
        self.records ["city"]= self.data.get("info").get("city", "Unknown")
        self.records ["venue"]= self.data.get("info").get("venue", "Unknown")
        self.records ["date"]= self.data.get("info").get("dates", "Unknown")
        self.records ["match_type"]= self.data.get("info").get("match_type", "Unknown")
        self.records ["team_type"]= self.data.get("info").get("team_type", "Unknown")
        self.records ["event"]= self.data.get("info").get("event", "Unknown")
        self.records ["teams"]=self.data.get("info").get("teams", [])
        self.records ["gender"]=self.data.get("info").get("gender", "Unknown")
        self.records ["officials"]= self.data.get("info").get("officials", "Unknown")
        self.records ["player_of_the_match"]= self.data.get("info").get("player_of_match", "Unknown")
        self.records ["players_registry"] =self.data.get("info").get("registry", {}).get("people", {})
        self.records ["toss"] = self.data.get("info").get("toss", "Unknown")
        self.records ["outcome"]= self.data.get("info").get("outcome", "Unknown")

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
            # json.dump(self.file_name, file, indent=4)
            file.write(f"{self.file_name}\n")
        # print(f"Data saved to {output_file}")

    def metaData(self):
        metadata = {
            "match_id": self.file_name,
            "match_type": self.data.get("info", {}).get("match_type", "Unknown"),
            "team_type": self.data.get("info", {}).get("team_type", "Unknown"),
            "teams": " vs ".join(self.data.get("info", {}).get("teams", [])),
            "season": self.data.get("info", {}).get("season", "Unknown"),
            "event": self.data.get("info", {}).get("event", "Unknown"),
            "gender": self.data.get("info", {}).get("gender", "Unknown")
        }
        self.records["metadata"] = metadata
    
    def df_generate(self):
        import pandas as pd
        df = pd.DataFrame(self.records)
        df.to_csv(f'{self.file_name}.csv', index=False)
        print(f"DataFrame saved to {self.file_name}.csv")

    def save_to_db(self):
        # Assuming db is an instance of a database connection class
        formatted = {}
        for key, value in self.records.items():
            if isinstance(value, dict):
                formatted[key] = json.dumps(value)
            elif isinstance(value, list):
                formatted[key] = json.dumps(value)
            else:
                formatted[key] = value
        if self.records["match_type"] == "Test":
            # Use the created database
            db.use_database("crickSheet_analysis")
            # insert data into the test_match table
            db.insert_data("test_match", formatted)
        print(f"Records for match {self.file_name} saved to database.")

# read match data from JSON file
if __name__ == "__main__":
    match = Match('63963')
    # match.match_info_2()
    match.match_info()
    match.extract_innings()
    match.save_to_db()
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
#             # if not match.is_valid_match():
#             #         print(f"Skipping invalid match: {match_id}")
#             #         continue
#             match.extract_innings()
#             match.match_info()
#             match.save_file(f'test_all.txt')

# loop through all JSON files in zip file
# if __name__ == "__main__":
#     zip_file = 'Downloads/all_json.zip'
#     with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#         for file in zip_ref.namelist():
#             if file.endswith('.json'):
#                 match_id = file.split('.')[0]
#                 match = Match(match_id)
#                 match.extract_innings()
#                 match.match_info()
#                 match.save_file(f'test_all.txt')

print("All match records processed and saved to test_all.txt")





# db = mySQLDB(
#     host = 'gateway01.us-west-2.prod.aws.tidbcloud.com',
#     user = '2giLRMddJvjQq3S.root',
#     password = 'RBujztoEPbUH8Mhy',
#     port = 4000
#     )