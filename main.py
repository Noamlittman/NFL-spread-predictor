from Collect_all_the_data import *
from Organizing_The_Matrix_For_NN import *
from Convert_Table_To_NN import *
from Analyze.Best_NN_for_Now import *
from Constants import *

(team_ovr_df_years, player_team_stats_madden_years, teams_standing_df, coaches_df,
 merged_df_all_games, full_teams_roster_df, betting_odds_df, starting_qb,
 star_player_df, superstar_player_df) = collect_the_data()
data_for_nn = Organize_all_the_data(team_ovr_df_years, player_team_stats_madden_years,
                                    teams_standing_df, coaches_df,
                                    merged_df_all_games, full_teams_roster_df,
                                    betting_odds_df, starting_qb,
                                    star_player_df, superstar_player_df)
data_in_nn = convert_table_for_nn(data_for_nn)

predictions_after_nn(desired_week, desired_year, data_in_nn, file_path)



