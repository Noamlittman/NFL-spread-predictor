
from Collect_game_stats_and_personnel import *
from Collect_Madden_Stats import *
from Collect_Betting_Odds import *
from Constants import *
from Update_Players_Roster_Spot import *
from Find_Starting_QB import *
from Madden_Stars_Data import *


def collect_the_data():
    team_ovr_df_years, player_team_stats_madden_years = take_madden_stats(start, end, file_path)
    teams_standing_df, coaches_df, merged_df_all_games, full_teams_roster_df = find_team_rosters(start, end,
                                                                                                      teams_file_path,
                                                                                                      file_path,
                                                                                                      current_week,
                                                                                                      current_year)
    betting_odds_df = get_betting_odds(start, end, file_path, current_year, current_week)
    full_teams_roster_df = update_players_on_teams(full_teams_roster_df)
    starting_qb = find_starting_qb(full_teams_roster_df, player_team_stats_madden_years)
    star_player_df, superstar_player_df = madden_stars_data(full_teams_roster_df,
                                                            player_team_stats_madden_years)

    return (team_ovr_df_years, player_team_stats_madden_years, teams_standing_df, coaches_df,
            merged_df_all_games, full_teams_roster_df,
            betting_odds_df, full_teams_roster_df, starting_qb,
            star_player_df, superstar_player_df)
