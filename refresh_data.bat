@echo off

echo ========================================
echo DOWNLOADING LATEST KAGGLE DATA
echo ========================================

kaggle datasets download -d eoinamoore/historical-nba-data-and-player-box-scores -p data/raw --unzip --force

echo.
echo ========================================
echo REBUILDING DATA TABLES
echo ========================================

python scripts/02_clean_player_boxscores.py
python scripts/03_clean_team_boxscores.py
python scripts/04_build_dim_players.py
python scripts/05_build_dim_teams.py
python scripts/06_build_dim_games.py
python scripts/07_build_dim_team_seasons.py

echo.
echo ========================================
echo DATA REFRESH COMPLETE
echo ========================================

pause