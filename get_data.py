import sys
sys.path.append("D:\Learn\Guvi\DS\project\Cricksheet Match Analysis")

from database import mySQLDB
import pandas as pd
import matplotlib.pyplot as plt

db = mySQLDB(
    host = 'localhost',
    user = 'root',
    port = 3306
)

db.use_database("crickSheet_analysis")

# Match and player ID
# match_Id = pd.read_sql_query('''SELECT match_id FROM matchs;''', db.connection)
match_Id = pd.read_sql_query('''
                            SELECT 
                                match_id
                            FROM 
                                matchs 
                            WHERE 
                                (team_type = 'international' 
                                OR 
                                JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League')
                            AND
                                gender = 'male';  
                            ''', db.connection)
player_Id = pd.read_sql_query('''
                               SELECT player_id, name FROM players_odi
                               UNION
                               SELECT player_id, name FROM players_t20
                               UNION
                               SELECT player_id, name FROM players_test;
                             ''', db.connection)

# Total Stats
total_stats = pd.read_sql_query('''
                                SELECT 
                                    t.name AS Name, 
                                
                                    t.matches AS Test_Matches,
                                    o.matches AS ODI_Matches,
                                    tt.matches AS T20_Matches,
                                    (o.matches + t.matches + tt.matches) AS Total_Matches,
                                
                                    t.runs AS Test_Runs,
                                    o.runs AS ODI_Runs,
                                    tt.runs AS T20_Runs,
                                    (o.runs + t.runs + tt.runs) AS Total_Runs,
                                
                                    t.wickets AS Test_Wickets,
                                    o.wickets AS ODI_Wickets,
                                    tt.wickets AS T20_Wickets,
                                    (o.wickets + t.wickets + tt.wickets) AS Total_Wickets,
                                
                                    t.batted_innings AS Test_batted_innings,
                                    o.batted_innings AS ODI_batted_innings,
                                    tt.batted_innings AS T20_batted_innings,
                                    (o.batted_innings + t.batted_innings + tt.batted_innings) AS Total_batted_innings,
                                
                                    t.balls_faced AS Test_balls_faced,
                                    o.balls_faced AS ODI_balls_faced,
                                    tt.balls_faced AS T20_balls_faced,
                                
                                    t.not_outs AS Test_not_outs,
                                    o.not_outs AS ODI_not_outs,
                                    tt.not_outs AS T20_not_outs,
                                
                                    t.highest_score AS Test_highest_score,
                                    o.highest_score AS ODI_highest_score,
                                    tt.highest_score AS T20_highest_score,

                                    t.hundreds AS Test_hundreds,
                                    o.hundreds AS ODI_hundreds,
                                    tt.hundreds AS T20_hundreds,
                                    (o.hundreds + t.hundreds + tt.hundreds) AS Total_hundreds,
                                
                                    t.fifties AS Test_fifties,
                                    o.fifties AS ODI_fifties,
                                    tt.fifties AS T20_fifties,
                                    (o.fifties + t.fifties + tt.fifties) AS Total_fifties,
                                
                                    t.fours AS Test_fours,
                                    o.fours AS ODI_fours,
                                    tt.fours AS T20_fours,
                                
                                    t.sixes AS Test_sixes,
                                    o.sixes AS ODI_sixes,
                                    tt.sixes AS T20_sixes,
                                
                                    t.strike_rate AS Test_strike_rate,
                                    o.strike_rate AS ODI_strike_rate,
                                    tt.strike_rate AS T20_strike_rate,
                                
                                    t.batting_average AS Test_batting_average,
                                    o.batting_average AS ODI_batting_average,
                                    tt.batting_average AS T20_batting_average,
                                
                                    t.wicket_by_catches AS Test_wicket_by_catches,
                                    o.wicket_by_catches AS ODI_wicket_by_catches,
                                    tt.wicket_by_catches AS T20_wicket_by_catches,
                                
                                    t.wicket_by_stumpings AS Test_wicket_by_stumpings,
                                    o.wicket_by_stumpings AS ODI_wicket_by_stumpings,
                                    tt.wicket_by_stumpings AS T20_wicket_by_stumpings,
                                
                                    t.catches AS Test_catches,
                                    o.catches AS ODI_catches,
                                    tt.catches AS T20_catches,
                                
                                    t.stumpings AS Test_stumpings,
                                    o.stumpings AS ODI_stumpings,
                                    tt.stumpings AS T20_stumpings,
                                
                                    t.balls_bowled AS Test_balls_bowled,
                                    o.balls_bowled AS ODI_balls_bowled,
                                    tt.balls_bowled AS T20_balls_bowled,
                                    (o.balls_bowled + t.balls_bowled + tt.balls_bowled) AS Total_balls_bowled,
                                
                                    t.run_conceded AS Test_run_conceded,
                                    o.run_conceded AS ODI_run_conceded,
                                    tt.run_conceded AS T20_run_conceded,
                                    (o.run_conceded + t.run_conceded + tt.run_conceded) AS Total_run_conceded,
                                
                                    t.five_wickets AS Test_five_wickets,
                                    o.five_wickets AS ODI_five_wickets,
                                    tt.five_wickets AS T20_five_wickets,
                                
                                    t.ten_wickets AS Test_ten_wickets,
                                    o.ten_wickets AS ODI_ten_wickets,
                                    tt.ten_wickets AS T20_ten_wickets,
                                
                                    t.maidens AS Test_maidens,
                                    o.maidens AS ODI_maidens,
                                    tt.maidens AS T20_maidens,
                                    (o.maidens + t.maidens + tt.maidens) AS Total_Maidens,
                                
                                    t.bowling_SR AS Test_bowling_SR,
                                    o.bowling_SR AS ODI_bowling_SR,
                                    tt.bowling_SR AS T20_bowling_SR,
                                
                                    t.economy AS Test_economy,
                                    o.economy AS ODI_economy,
                                    tt.economy AS T20_economy,
                                
                                    t.bowling_average AS Test_bowling_average,
                                    o.bowling_average AS ODI_bowling_average,
                                    tt.bowling_average AS T20_bowling_average
                                
                                FROM players_test t
                                JOIN players_odi o
                                    ON t.player_id = o.player_id
                                JOIN players_t20 tt
                                    ON tt.player_id = o.player_id
                                
                                ''', db.connection)


player_of_the_match = pd.read_sql_query('''
                                    SELECT
                                        match_id AS Match_id,
                                        JSON_UNQUOTE(JSON_EXTRACT(player_of_the_match, '$[0]')) AS player_of_the_match
                                    FROM
                                        matchs
                                    WHERE 
                                        team_type = 'international' 
                                        OR 
                                        JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League';
                                    ''', db.connection)


teams=pd.read_sql_query('''
                     SELECT 
                        JSON_UNQUOTE(JSON_EXTRACT(teams,'$[0]')) AS teams 
                     FROM matchs
                     WHERE 
                        team_type = 'international' 
                        OR 
                        JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League'
                     UNION
                     SELECT 
                        JSON_UNQUOTE(JSON_EXTRACT(teams,'$[1]')) AS teams 
                     FROM matchs
                     WHERE 
                        team_type = 'international' 
                        OR 
                        JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League';
                     ''', db.connection)

toss=pd.read_sql_query('''
                     SELECT
                        match_id AS Match_Id,
                        JSON_UNQUOTE(JSON_EXTRACT(toss, '$.winner')) AS Toss_Winner,
                        JSON_UNQUOTE(JSON_EXTRACT(toss, '$.decision')) AS Toss_Decision,
                        JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) AS Winner
                     FROM
                        matchs
                     WHERE 
                        (team_type = 'international' 
                        OR 
                        JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League')
                    AND
                        gender = 'male';
                     ''',db.connection)

toss=pd.read_sql_query('''
                        SELECT
                            JSON_UNQUOTE(JSON_EXTRACT(toss, '$.winner')) AS toss_winner,
                            JSON_UNQUOTE(JSON_EXTRACT(toss, '$.decision')) AS toss_decision,
                            JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) AS winner,
                            COUNT(*) AS times_chosen,
                            match_type AS Match_type,
                            SUM(
                                CASE 
                                    WHEN 
                                        JSON_UNQUOTE(JSON_EXTRACT(toss, '$.winner')) = JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) 
                                        THEN 1 
                                    ELSE 0 
                                END
                            ) AS toss_winner_won,
                            SUM(
                                CASE 
                                    WHEN 
                                        JSON_UNQUOTE(JSON_EXTRACT(toss, '$.winner')) != JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) 
                                        THEN 1 
                                    ELSE 0 
                                END
                            ) AS toss_winner_lost,
                            ROUND(
                                100 * SUM(
                                        CASE 
                                            WHEN 
                                                JSON_UNQUOTE(JSON_EXTRACT(toss, '$.winner')) = JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) 
                                            THEN 1 
                                        ELSE 0 
                                    END) / COUNT(*),
                                1
                            ) AS win_percentage
                        FROM 
                            matchs
                        WHERE
                            (team_type = 'international' 
                            OR 
                            JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League')
                        AND
                            gender = 'male'
                        AND
                            JSON_UNQUOTE(JSON_EXTRACT(toss, '$.decision')) IN ('bat', 'field')
                        GROUP BY 
                            toss_winner, toss_decision
                        ORDER BY
                            toss_winner, toss_decision;
                       ''', db.connection)

outcome=pd.read_sql_query('''
                     SELECT
                        match_id AS Match_Id,
                        JSON_UNQUOTE(JSON_EXTRACT(date, '$[0]')) AS date,
                        match_type AS Match_type,
                        JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) AS Winner,
                        JSON_EXTRACT(outcome, '$.by.runs') AS runs,
                        JSON_EXTRACT(outcome, '$.by.wickets') AS wickets,
                        CASE 
                            WHEN JSON_UNQUOTE(JSON_EXTRACT(teams, '$[0]')) = JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner'))
                                THEN JSON_UNQUOTE(JSON_EXTRACT(teams, '$[1]'))
                            ELSE JSON_UNQUOTE(JSON_EXTRACT(teams, '$[0]'))
                        END AS opponent
                     FROM
                        matchs
                     WHERE 
                        (team_type = 'international' 
                        OR 
                        JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League')
                     AND
                        gender = 'male'
                     AND
                        JSON_EXTRACT(outcome, '$.winner') IS NOT NULL;
                     ''',db.connection)

trophy=pd.read_sql_query('''
                     SELECT
                        match_id AS Match_Id,
                        match_type AS Match_type,
                        JSON_EXTRACT(event, '$.name') AS event,
                        JSON_UNQUOTE(JSON_EXTRACT(outcome, '$.winner')) AS Winner
                     FROM
                        matchs
                     WHERE 
                        (team_type = 'international' 
                        OR 
                        JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League')
                     AND
                        gender = 'male'
                     AND
                        JSON_EXTRACT(outcome, '$.winner') IS NOT NULL
                     AND
                        JSON_EXTRACT(event, '$.stage') = 'Final';
                     ''',db.connection)

venue=pd.read_sql_query('''
                     SELECT
                            DISTINCT venue
                        FROM 
                            matchs
                        WHERE
                            (team_type = 'international' 
                            OR 
                            JSON_UNQUOTE(JSON_EXTRACT(event, '$.name')) = 'Indian Premier League')
                        AND
                            gender = 'male'
                     ''',db.connection)
# match_Id.to_csv(f'test.csv', index=False)
# print(player_of_the_match)




# Team Specific decending by date
# df = pd.read_sql_query('''
#                        SELECT 
#                        * 
#                        FROM `matchs` 
#                        WHERE 
#                         JSON_CONTAINS(teams, '"India"') 
#                         AND 
#                         gender = "male" ORDER BY STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(date, '$[0]')), '%Y-%m-%d') DESC 
#                        LIMIT 10;
#                        ''', db.connection)
# print(df)
# df.to_csv(f'test.csv', index=False)

# Player Specific decending by date and by match type
# df = pd.read_sql_query('''
#                         SELECT 
#                         * 
#                         FROM `matchs` 
#                         WHERE 
#                             match_type = "Test"
#                             AND
#                             JSON_SEARCH(innings,'one', 'V Kohli') IS NOT NULL 
#                         ORDER BY STR_TO_DATE(JSON_UNQUOTE(JSON_EXTRACT(date, '$[0]')), '%Y-%m-%d') DESC 
#                        LIMIT 10;
#                        ''', db.connection)
# df.to_csv(f'test.csv', index=False)
# print(df)


# df = pd.read_sql_query('''
#                         SELECT * FROM players_t20
#                        ''', db.connection)
# df.to_csv(f'players_t20.csv', index=False)


# plt.bar(top_test_wickets['Name'],top_test_wickets['Test_Wickets'])
# plt.title('Top Wicket Takers')
# plt.xlabel('Name')
# plt.ylabel('Wickets')
# plt.show()