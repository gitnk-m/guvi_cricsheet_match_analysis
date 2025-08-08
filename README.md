# guvi_cricsheet_match_analysis
Data Science project with web scrapping using selenium and visualizing using power BI.

Power BI based analysis of cricket data scraped from online using selenium and processed in python and structured using pandas.

** Stacks used
    - Python
        - Selenium
        - Pandas
        - mysql.connector
    - MySQL
        - Xampp
    - Power BI
         

** Scraping

    - Cricket data from https://cricsheet.org/matches/ is scrabed using selenium and by accessing the download option in the website using X.PATH selector of selenium.

    - Selenium by default will close before download is complete, to overcome sleep time is dynamically increased by checking the download folder for file with extension  .crdownload.

** Data Processing

    - Scrapped Cricket data have ball by ball data of match and each match is stored in seperate JSON file.
    
    - Using Zipfile library each json file inside the zip file is itrated and data was readed in python as dict.

    - Ball by ball data in the json is processed and stored as player, innings and match basis data.

    - Store the processed data in Database in matches, players_odi, players_t20 and players_test tables

** Analysis
    -   Power BI
        - Page - Players
            - Slicer 
                # Player 
            - Card
                # Total Matches
                # Total Runs
                # Total Wickets
                # No. of Player of Matchs
            - Column Chart
                # Top 10 Run Scrores (sum of all Format)
                # Top 10 Wicket Takers (sum of all Format)
            - Pie Chart
                # Number of Matches each players Played in each format


        - Page - Batting
            - Slicer
                # Player 
            - Card
                # No. of innings Batted
                # Runs
                # Fifties
                # Hundreds
            - Multi Row Cards
                # Players Stats in each format


        - Page - Bowling
            - Slicer
                # Player 
            - Card
                # No. of Balls Bowled
                # Runs Conceded
                # Wickets
                # Madiens
            - Multi Row Cards
                # Players Stats in each format

        - Page - Team
            - Slicer
                # Team 
                # Match Type
            - Card
                # Matches
                # Teams
                # Trophies
                # Draw
            - Line Chart
                # Matches won by chase win in 2025
                # Matches won by win by defending in 2025
            - Table 
                # Matches won by chase win in 2025
                # Matches won by win by defending in 2025
                # Tropies won by teams
            - Bar Chart
                # Percentage of Team winning after toss win, based on decision to bat or field first