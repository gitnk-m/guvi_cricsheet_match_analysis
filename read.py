import json
import pandas as pd

# df = pd.read_json('Downloads/63963.json')
# print(df.head())

with open('Downloads/63963.json', 'r') as file:
    data = json.load(file)


# Extract all deliveries from the first innings
innings = data['innings']  # This is a list of innings (1 or 2)
records = []

# Iterate through each inning
for inning in innings:
    team = inning['team']
    total = 0
    batting={}
    bowling={}
    extras = 0
    fall_of_wickets = []
    for over in inning['overs']:
        run_in_over = 0
        ball_count = 0
        for delivery in over['deliveries']:
            ball_count += 1
            # Check for Maiden Over
            if delivery.get("extras") and delivery["extras"].get("wides") or delivery.get("extras") and delivery["extras"].get("noballs"):
                run_in_over += delivery["runs"].get("batter") + delivery.get("extras").get("wides", 0) + delivery.get("extras").get("noballs", 0)
            else:
                run_in_over += delivery["runs"].get("batter")
                
            # Track of Total Runs
            total += delivery["runs"].get("total", 0)

            # Track of Batsman
            # if delivery.get("batter") not in batting.keys():
            batter = data["info"]["registry"]["people"][delivery.get("batter")]
            if batter not in batting.keys():
                batting[batter] ={"run": 0, "ball": 0, "0s": 0, "1s": 0, "2s": 0, "3s": 0, "4s": 0, "6s": 0, "strike_rate": 0, "wicket": "not out"}
                batting[batter]["run"] = delivery["runs"].get("batter")
                batting[batter]["ball"] = 1
                if delivery["runs"].get("batter") == 0:
                    batting[batter]["0s"] = 0
                elif delivery["runs"].get("batter") == 1:
                    batting[batter]["1s"] = 0
                elif delivery["runs"].get("batter") == 2:
                    batting[batter]["2s"] = 0
                elif delivery["runs"].get("batter") == 3:
                    batting[batter]["3s"] = 0
                elif delivery["runs"].get("batter") == 4:
                    batting[batter]["4s"] = 0
                elif delivery["runs"].get("batter") == 6:
                    batting[batter]["6s"] = 0
                batting[batter]["strike_rate"] = (batting[batter]["run"] / batting[batter]["ball"]) * 100
            else:
                batting[batter]["run"] += delivery["runs"].get("batter")
                batting[batter]["ball"] += 1
                
                if delivery["runs"].get("batter") == 0:
                    batting[batter]["0s"] += 1
                elif delivery["runs"].get("batter") == 1:
                    batting[batter]["1s"] += 1
                elif delivery["runs"].get("batter") == 2:
                    batting[batter]["2s"] += 1
                elif delivery["runs"].get("batter") == 3:
                    batting[batter]["3s"] += 1
                elif delivery["runs"].get("batter") == 4:
                    batting[batter]["4s"] += 1
                elif delivery["runs"].get("batter") == 6:
                    batting[batter]["6s"] += 1
                batting[batter]["strike_rate"] = round((batting[batter]["run"] / batting[batter]["ball"]) * 100,2)

            # Track of Bowler
            if delivery.get("bowler") not in bowling.keys():
                bowling[delivery.get("bowler")] = {"ball": 0, "run": 0, "wicket": 0, "economy": 0, "maidens": 0, "no_balls": 0, "wides": 0}
                bowling[delivery.get("bowler")]["ball"] += 1
                bowling[delivery.get("bowler")]["run"] += delivery["runs"].get("batter")
                if delivery.get("extras") and delivery["extras"].get("wides"):
                    bowling[delivery.get("bowler")]["wides"] += delivery["extras"].get("wides")
                    bowling[delivery.get("bowler")]["ball"] -= 1
                    bowling[delivery.get("bowler")]["run"] += 1
                if delivery.get("extras") and delivery["extras"].get("noballs"):
                    bowling[delivery.get("bowler")]["no_balls"] += delivery["extras"].get("noballs")
                    bowling[delivery.get("bowler")]["ball"] -= 1
                    bowling[delivery.get("bowler")]["run"] += 1
                if delivery.get("wickets"):
                    bowling[delivery.get("bowler")]["wicket"] += 1
                bowling[delivery.get("bowler")]["economy"] = round(bowling[delivery.get("bowler")]["run"] / bowling[delivery.get("bowler")]["ball"] * 6, 2)
            else:
                bowling[delivery.get("bowler")]["ball"] += 1
                bowling[delivery.get("bowler")]["run"] += delivery["runs"].get("batter")
                if delivery.get("extras") and delivery["extras"].get("wides"):
                    bowling[delivery.get("bowler")]["wides"] += delivery["extras"].get("wides")
                    bowling[delivery.get("bowler")]["ball"] -= 1
                    bowling[delivery.get("bowler")]["run"] += 1
                if delivery.get("extras") and delivery["extras"].get("noballs"):
                    bowling[delivery.get("bowler")]["no_balls"] += delivery["extras"].get("noballs")
                    bowling[delivery.get("bowler")]["ball"] -= 1
                    bowling[delivery.get("bowler")]["run"] += 1
                if delivery.get("wickets"):
                    bowling[delivery.get("bowler")]["wicket"] += 1
                bowling[delivery.get("bowler")]["economy"] = round(bowling[delivery.get("bowler")]["run"] / bowling[delivery.get("bowler")]["ball"] * 6, 2)

            # Track of Extras
            if delivery.get("extras"):
                extras += delivery["extras"].get("wides", 0) + delivery["extras"].get("noballs", 0) + delivery["extras"].get("byes", 0) + delivery["extras"].get("legbyes", 0)
                if "penalty" in delivery["extras"]:
                    extras += delivery["extras"]["penalty"]
            
            # Track of Wickets  
            if delivery.get('wickets'):
                if isinstance(delivery['wickets'], list):
                    for wicket in delivery['wickets']:
                        wicket["bowler"]=(delivery.get("bowler"))
                        wicket["ball"] = f'''{over.get("over")}.{ball_count}'''
                        wicket["runs"] = batting[batter]["run"]
                        batting[batter]["wicket"] = wicket
                        # Fall of Wickets
                        fall_of_wickets.append(wicket)

                else:
                    batting[batter]["wicket"] = delivery['wickets'].get("kind")
                

        # Check for Maiden Over
        if run_in_over == 0 and ball_count == 6:
            bowling[delivery.get("bowler")]["maidens"] += 1
    records.append({"team": team, "batting": batting, "bowling": bowling, "extras": extras, "total": total, "fall_of_wickets": fall_of_wickets})    

records.insert(0,data.get("info"))

# Save the records to a JSON file
with open('test.json', 'w') as file:
    json.dump(records, file, indent=4)


# Convert to DataFrame
# df = pd.DataFrame(records)


# print(df)
