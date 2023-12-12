import os
import pandas as pd
from pathlib import Path

def create_folders_for_teams(team_names, base_path):
    """
    Create folders for each team in the specified path.
    """
    for team_name in team_names:
        team_path = Path(base_path) / team_name
        try:
            team_path.mkdir(parents=True, exist_ok=True)
            print(f"Directory '{team_path}' was created successfully.")
        except OSError as error:
            print(f"Creation of the directory '{team_path}' failed due to: {error}")

def create_year_week_folders(team_names, base_path, start_year, end_year):
    """
    Create year and week folders within each team's directory.
    """
    for team_name in team_names:
        team_path = Path(base_path) / team_name
        if team_path.is_dir():
            for year in range(start_year, end_year):
                year_folder = team_path / str(year)
                year_folder.mkdir(exist_ok=True)

                # Define weeks based on the year
                weeks = range(1, 19) if year > 2020 else range(1, 18)
                for week in weeks:
                    week_folder = year_folder / f'week{week}'
                    week_folder.mkdir(exist_ok=True)
        else:
            print(f"Folder '{team_name}' does not exist in the specified directory.")

def create_additional_folders(root_path, start_year, end_year):
    """
    Create additional folders for madden and betting odds.
    """
    madden_dir = root_path / 'madden'
    betting_odds_folder = root_path / 'betting odds'
    madden_dir.mkdir(exist_ok=True)
    betting_odds_folder.mkdir(exist_ok=True)

    for year in range(start_year, end_year):
        year_folder = madden_dir / str(year)
        year_folder.mkdir(exist_ok=True)

def get_teams_from_file(file_path):
    """
    Read team names from the provided Excel file.
    """
    team_names_table = pd.read_excel(file_path, engine='openpyxl')
    return team_names_table['team name']

def create_the_folders(file_path,teams_file_path,start_year,end_year):
    """
    Main function to execute the folder creation process.
    """

    root_dir = Path(file_path)
    team_names = get_teams_from_file(teams_file_path)
    team_base_path = root_dir / "teams"

    create_folders_for_teams(team_names, team_base_path)
    create_year_week_folders(team_names, team_base_path, start_year, end_year)
    create_additional_folders(root_dir, start_year, end_year)
    print("Folder structure setup complete.")

