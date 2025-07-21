import json
import pandas as pd

# df = pd.read_json('Downloads/63963.json')
# print(df.head())

with open('Downloads/63963.json', 'r') as file:
    data = json.load(file)

# Extract all deliveries from the first innings
innings = data['innings']  # This is a list of innings (1 or 2)
records = []

for inning in innings:
    team = inning['team']
    batting={}
    bowling={}
    extras = 0
    for over in inning['overs']:
        for delivery in over['deliveries']:
            if delivery.get("batter") not in batting.keys():
                batting[delivery.get("batter")] ={"run": 0, "ball": 0, "0s": 0, "1s": 0, "2s": 0, "3s": 0, "4s": 0, "6s": 0, "strike_rate": 0, "wicket": "not out"}
                batting[delivery.get("batter")]["run"] = delivery["runs"].get("batter")
                batting[delivery.get("batter")]["ball"] = 1
                if delivery["runs"].get("batter") == 0:
                    batting[delivery.get("batter")]["0s"] = 0
                elif delivery["runs"].get("batter") == 1:
                    batting[delivery.get("batter")]["1s"] = 0
                elif delivery["runs"].get("batter") == 2:
                    batting[delivery.get("batter")]["2s"] = 0
                elif delivery["runs"].get("batter") == 3:
                    batting[delivery.get("batter")]["3s"] = 0
                elif delivery["runs"].get("batter") == 4:
                    batting[delivery.get("batter")]["4s"] = 0
                elif delivery["runs"].get("batter") == 6:
                    batting[delivery.get("batter")]["6s"] = 0
                batting[delivery.get("batter")]["strike_rate"] = (batting[delivery.get("batter")]["run"] / batting[delivery.get("batter")]["ball"]) * 100
            else:
                batting[delivery.get("batter")]["run"] += delivery["runs"].get("batter")
                batting[delivery.get("batter")]["ball"] += 1
                
                if delivery["runs"].get("batter") == 0:
                    batting[delivery.get("batter")]["0s"] += 1
                elif delivery["runs"].get("batter") == 1:
                    batting[delivery.get("batter")]["1s"] += 1
                elif delivery["runs"].get("batter") == 2:
                    batting[delivery.get("batter")]["2s"] += 1
                elif delivery["runs"].get("batter") == 3:
                    batting[delivery.get("batter")]["3s"] += 1
                elif delivery["runs"].get("batter") == 4:
                    batting[delivery.get("batter")]["4s"] += 1
                elif delivery["runs"].get("batter") == 6:
                    batting[delivery.get("batter")]["6s"] += 1
                batting[delivery.get("batter")]["strike_rate"] = round((batting[delivery.get("batter")]["run"] / batting[delivery.get("batter")]["ball"]) * 100,2)
            if delivery.get("wickets"):
                if delivery.get("wickets")[0].get("kind") == "lbw":
                    batting[delivery.get("batter")]["wicket"] = f"lbw b {delivery.get('bowler')}"
                elif delivery.get("wickets")[0].get("kind") == "bowled":
                    batting[delivery.get("batter")]["wicket"] = f"b {delivery.get('bowler')}"
                elif delivery.get("wickets")[0].get("kind") == "caught":
                    batting[delivery.get("batter")]["wicket"] = f"c {delivery.get('wickets')[0].get('fielders')[0].get('name')} b {delivery.get('bowler')}"
                elif delivery.get("wickets")[0].get("kind") == "stumped":
                    batting[delivery.get("batter")]["wicket"] = f"st {delivery.get('wickets')[0].get('fielders')[0].get('name')} b {delivery.get('bowler')}"
                elif delivery.get("wickets")[0].get("kind") == "run out":
                    batting[delivery.get("batter")]["wicket"] = f'''run out {", ".join(f["name"] for f in delivery.get('wickets')[0].get('fielders'))}'''
                elif delivery.get("wickets")[0].get("kind") == "hit wicket":
                    batting[delivery.get("batter")]["wicket"] = f"hw b {delivery.get('bowler')}"
                elif delivery.get("wickets")[0].get("kind") == "obstructing the field":
                    batting[delivery.get("batter")]["wicket"] = f"otf b {delivery.get('bowler')}"
                elif delivery.get("wickets")[0].get("kind") == "handled the ball":
                    batting[delivery.get("batter")]["wicket"] = f"htb b {delivery.get('bowler')}"
                

            # if delivery.get("bowler") not in bowling.keys():
            #     bowling[delivery.get("bowler")] = delivery["runs"].get("batter")
    records.append({"team": team, "batting": batting, "bowling": bowling, "extras": extras})    

print(records)


# for inning in innings:
    # team = inning['team']
    # for over in inning['overs']:
    #     over_num = over['over']
    #     for delivery in over['deliveries']:
    #         delivery_flat = {
    #             "team": team,
    #             "over": over_num,
    #             "batter": delivery.get("batter"),
    #             "bowler": delivery.get("bowler"),
    #             "non_striker": delivery.get("non_striker"),
    #             "runs_batter": delivery["runs"].get("batter", 0),
    #             "runs_extras": delivery["runs"].get("extras", 0),
    #             "runs_total": delivery["runs"].get("total", 0),
    #             "wicket": delivery.get("wickets", None)
    #         }
    #         records.append(delivery_flat)

# Convert to DataFrame
# df = pd.DataFrame(records)

# # Optionally, expand 'wicket' into separate columns
# df['wicket_kind'] = df['wicket'].apply(lambda x: x[0]['kind'] if isinstance(x, list) else None)
# df['player_out'] = df['wicket'].apply(lambda x: x[0]['player_out'] if isinstance(x, list) else None)

# # Drop the original wicket column if not needed
# df.drop(columns=['wicket'], inplace=True)

# print(df)
