
from Collect_game_stats_and_personnel import *
from Colle import *
from Collect_Betting_Odds import *
def Collect_the_data:
    team_ovr_df_years, player_team_stats_madden_years_1 = take_madden_stats(start, end, file_path)
    madden_data = player_team_stats_madden_years_1
    teams_standing_df_test, coaches_df, merged_df_all_games, full_teams_roster_df = find_team_rosters(start, end,
                                                                                                      teams_file_path,
                                                                                                      file_path,
                                                                                                      current_week,
                                                                                                      current_year)
    betting_odds_df = get_betting_odds(start, end, file_path, current_year, current_week)
