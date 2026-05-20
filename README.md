# NBA Playoff History Dashboard

Interactive Power BI dashboard exploring the complete history of the NBA playoffs using custom metrics, historical team modeling, and dynamic player/team analysis.

---

## Project Overview

This project analyzes the full history of the NBA playoffs through an interactive Power BI dashboard built on top of a custom Python ETL pipeline. The dashboard combines player-level and team-level playoff data with historical franchise tracking, custom playoff scoring systems, and dynamic filtering tools to create a highly exploratory basketball analytics experience.

The project was designed to go beyond basic sports dashboards by emphasizing:

- Historical playoff storytelling
- Dynamic player and team exploration
- Custom playoff importance metrics
- Proper historical franchise modeling
- Interactive drilldown analysis
- Reproducible ETL and refresh workflows

The final dashboard currently includes:

- Home Page
- Player Spotlight Page
- Team Dynasties Page

---

## Dashboard Features

### Home Page
High-level overview of NBA playoff history featuring:
- Total playoff games
- Total playoff points
- Franchise playoff wins
- Historical playoff leaders
- Interactive filtering and navigation

### Player Spotlight
Deep-dive analysis of individual playoff careers featuring:
- Dynamic KPI cards (PPG, RPG, APG, Stocks/Game, etc.)
- Multi-metric playoff trend analysis
- Interactive metric selection using Power BI field parameters
- Best playoff performances table using a custom playoff game score metric
- Historical team-aware filtering

### Team Spotlight
Franchise-level playoff exploration featuring:
- Historical team playoff trends
- Team playoff game score metric
- Elimination-game weighting
- Round importance weighting
- Historical franchise continuity across relocations and name changes
- Team playoff performance analysis across eras

---

## Data Source

Dataset sourced from Kaggle:

Historical NBA Data and Player Box Scores

https://www.kaggle.com/datasets/eoinamoore/historical-nba-data-and-player-box-scores

The project uses historical playoff player and team box score data spanning the full history of the NBA playoffs.

---

## Tech Stack

### Python
Used for:
- ETL workflows
- Data cleaning
- Historical franchise modeling
- Building dimension tables
- Automated refresh pipeline generation

Libraries used include:
- pandas
- pathlib

### Power BI
Used for:
- Data modeling
- DAX calculations
- Dashboard development
- Drilldown hierarchies
- Field parameters
- Interactive filtering
- Custom playoff metrics

### Git / GitHub
Used for:
- Version control
- Portfolio hosting
- Project documentation

---

## Project Structure

```
nba-playoff-history-dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── 02_clean_player_boxscores.py
│   ├── 03_clean_team_boxscores.py
│   ├── 04_build_dim_players.py
│   ├── 05_build_dim_teams.py
│   ├── 06_build_dim_games.py
│   └── 07_build_dim_team_seasons.py
│
├── refresh_data.bat
│
├── powerbi/
│
└── README.md
```

---

## Historical Franchise Modeling

One of the main technical challenges in this project involved correctly modeling historical NBA franchises across relocations and name changes.

Examples include:
- St. Louis Hawks → Atlanta Hawks
- Minneapolis Lakers → Los Angeles Lakers
- Seattle SuperSonics → Oklahoma City Thunder

To solve this, a custom historical bridge table (`dim_team_seasons`) was created to map:

team_id + season_year

to the historically correct franchise identity for that season.

This allowed:
- historically accurate filtering
- proper playoff trend analysis
- franchise continuity across eras
- cleaner Power BI relationships

---

## Custom Metrics

### Playoff Game Score
Custom player-level metric designed to identify the greatest playoff performances using:
- points
- rebounds
- assists
- steals
- blocks
- turnovers

### Team Playoff Game Score
Custom team-level metric incorporating:
- team box score performance
- margin of victory
- playoff round importance
- elimination-game pressure
- win/loss context

This metric was designed to prioritize historically meaningful playoff wins over raw statistical accumulation alone.

---

## Dynamic Interactivity

The dashboard uses several advanced Power BI features, including:

- Field parameters for dynamic metric selection
- Context-aware filtering
- Historical franchise relationships
- Dynamic KPI cards
- Cross-page interactive slicers

Users can dynamically explore:
- playoff careers
- franchise histories
- playoff runs
- elimination games
- playoff scoring trends
- historical playoff eras

---

## Automated Refresh Workflow

The project includes a reusable refresh pipeline.

Running:

refresh_data.bat

will:
1. Download the latest Kaggle dataset
2. Rebuild processed tables
3. Recreate dimension tables
4. Prepare the Power BI model for refresh

This allows the dashboard to remain reproducible and maintainable.

---

## Future Improvements

Potential future additions include:
- Era comparison page
- Playoff upset analysis
- Shot profile visualizations
- Advanced efficiency metrics

---

## Author

Jacob Bowling

Statistics (B.S.) and Sociology (B.A.)
Baylor University

GitHub:
https://github.com/Jabrwocky
