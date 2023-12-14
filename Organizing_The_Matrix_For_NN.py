def Organize_all_the_data(coaches_df, team_names_table, team_ovr_df_years, teams_standing_df, starting_qb,
                          superstar_player_df, star_player_df, betting_odds_df, city_teams_stats, file_path):

    coaches_df = pd.merge(coaches_df, team_names_table,
                          left_on='team', right_on='full_names', how='inner')
    team_ovr_df_years_df = pd.merge(
        team_ovr_df_years, team_names_table, left_on='Team Name', right_on='full_names', how='inner')
    team_ovr_df_years_df = team_ovr_df_years_df[['Number', 'year', 'city', 'team name', 'short',
                                                 'full_names']]

    teams_standing_df = pd.merge(teams_standing_df, team_names_table,
                                 left_on='team', right_on='full_names', how='inner')
    teams_standing_df = teams_standing_df[[
        'year', 'week', 'winns', 'losses',  'team name']]

    starting_qb = pd.merge(starting_qb, team_names_table,
                           left_on='full_team_name', right_on='full_names', how='inner')
    starting_qb = starting_qb[['week', 'year',
                               'team name', 'starting', 'starting_overall']]
    starting_qb['starting'].isna(axis=1)

    superstar_player_df = pd.merge(superstar_player_df, team_names_table,
                           left_on='full_team_name', right_on='full_names', how='inner')

    superstar_player_df = superstar_player_df[['year', 'week', 'team name', 'count_superstars', 'superstars ""',
           'superstars "O"', 'superstars "Q"']]

    star_player_df = pd.merge(star_player_df, team_names_table,
                           left_on='full_team_name', right_on='full_names', how='inner')

    star_player_df = star_player_df[['year', 'week', 'team name', 'count_stars', 'stars ""',
           'stars "O"', 'stars "Q"']]

    betting_odds_df_merge = pd.merge(betting_odds_df, teams_standing_df, left_on=[
                                     'Favorite_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')

    # Rename the columns
    betting_odds_df_merge.rename(
        columns={'winns': 'win_Favorite', 'losses': 'loss_Favorite'}, inplace=True)

    betting_odds_df_merge = pd.merge(betting_odds_df_merge, teams_standing_df, left_on=[
                                     'Underdog_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')

    # Rename the columns
    betting_odds_df_merge.rename(
        columns={'winns': 'win_Underdog', 'losses': 'loss_Underdog'}, inplace=True)

    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog']]


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, city_teams_stats, left_on=[
                                     'Underdog_team', 'Underdog_city'], right_on=['team name', 'city'], how='left')
    betting_odds_df_merge.rename(columns={'team worth': 'worth_Underdog', 'size of the city': 'size_Underdog',
                                 'cold weather': 'cold_Underdog', 'conference': 'conference_Underdog', 'division': 'division_Underdog'}, inplace=True)


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, city_teams_stats, left_on=[
                                     'Favorite_team', 'Favorite_city'], right_on=['team name', 'city'], how='left')
    betting_odds_df_merge.rename(columns={'team worth': 'worth_Favorite', 'size of the city': 'size_Favorite',
                                 'cold weather': 'cold_Favorite', 'conference': 'conference_Favorite', 'division': 'division_Favorite'}, inplace=True)


    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog']]


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, coaches_df, left_on=[
                                     'Favorite_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'new coach': 'new_coach_Favorite', 'new year coach': 'new_year_coach_Favorite'}, inplace=True)

    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite']]


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, coaches_df, left_on=[
                                     'Underdog_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'new coach': 'new_coach_Underdog', 'new year coach': 'new_year_coach_Underdog'}, inplace=True)

    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog']]


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, team_ovr_df_years_df, left_on=[
                                     'Favorite_team', 'Year'], right_on=['team name', 'year'], how='left')
    betting_odds_df_merge.rename(
        columns={'Number': 'Rating_Favorite'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite']]

    betting_odds_df_merge = pd.merge(betting_odds_df_merge, team_ovr_df_years_df, left_on=[
                                     'Underdog_team', 'Year'], right_on=['team name', 'year'], how='left')
    betting_odds_df_merge.rename(
        columns={'Number': 'Rating_Underdog'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog']]


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, starting_qb, left_on=[
                                     'Favorite_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'starting': 'starting_qb_Favorite', 'starting_overall': 'Overall_qb_Favorite'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'Overall_qb_Favorite'
                                                   ]]

    betting_odds_df_merge = pd.merge(betting_odds_df_merge, starting_qb, left_on=[
                                     'Underdog_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'starting': 'starting_qb_Underdog', 'starting_overall': 'Overall_qb_Underdog'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'Overall_qb_Favorite',
                                                   'starting_qb_Underdog', 'Overall_qb_Underdog'
                                                   ]]


    betting_odds_df_merge = pd.merge(betting_odds_df_merge, star_player_df, left_on=[
                                     'Underdog_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'count_stars': 'count_stars_Underdog', 'stars ""': 'stars_""_Underdog'
                                 ,'stars "Q"': 'stars_"Q"_Underdog', 'stars "O"': 'stars_"O"_Underdog'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'Overall_qb_Favorite',
                                                   'starting_qb_Underdog', 'Overall_qb_Underdog', 'count_stars_Underdog',
                                                   'stars_""_Underdog', 'stars_"Q"_Underdog','stars_"O"_Underdog'
                                                   ]]

    betting_odds_df_merge = pd.merge(betting_odds_df_merge, star_player_df, left_on=[
                                     'Favorite_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'count_stars': 'count_stars_Favorite', 'stars ""': 'stars_""_Favorite'
                                 ,'stars "Q"': 'stars_"Q"_Favorite', 'stars "O"': 'stars_"O"_Favorite'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'Overall_qb_Favorite',
                                                   'starting_qb_Underdog', 'Overall_qb_Underdog', 'count_stars_Underdog',
                                                   'stars_""_Underdog', 'stars_"Q"_Underdog','stars_"O"_Underdog', 'count_stars_Favorite',
                                                   'stars_""_Favorite', 'stars_"Q"_Favorite','stars_"O"_Favorite'
                                                   ]]

    betting_odds_df_merge = pd.merge(betting_odds_df_merge, superstar_player_df, left_on=[
                                     'Underdog_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'count_superstars': 'count_superstars_Underdog', 'superstars ""': 'superstars_""_Underdog'
                                 ,'superstars "Q"': 'superstars_"Q"_Underdog', 'superstars "O"': 'superstars_"O"_Underdog'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                                   'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'Overall_qb_Favorite',
                                                   'starting_qb_Underdog', 'Overall_qb_Underdog', 'count_stars_Underdog',
                                                   'stars_""_Underdog', 'stars_"Q"_Underdog','stars_"O"_Underdog', 'count_stars_Favorite',
                                                   'stars_""_Favorite', 'stars_"Q"_Favorite','stars_"O"_Favorite', 'count_superstars_Underdog',
                                                   'superstars_""_Underdog', 'superstars_"Q"_Underdog','superstars_"O"_Underdog'
                                                   ]]

    betting_odds_df_merge = pd.merge(betting_odds_df_merge, superstar_player_df, left_on=[
                                     'Favorite_team', 'Year', 'week_number'], right_on=['team name', 'year', 'week'], how='left')
    betting_odds_df_merge.rename(columns={
                                 'count_superstars': 'count_superstars_Favorite', 'superstars ""': 'superstars_""_Favorite'
                                 ,'superstars "Q"': 'superstars_"Q"_Favorite', 'superstars "O"': 'superstars_"O"_Favorite'}, inplace=True)
    betting_odds_df_merge = betting_odds_df_merge[['Day', 'Date', 'Time (ET)', 'home_1', 'conference_Favorite',
                                                   'division_Favorite', 'conference_Underdog', 'division_Underdog',
                                                   'Favorite', 'Spread', 'home_2',
                                                   'Underdog', 'Over/Under', 'week_number', 'Year', 'Team 1 Score',
                                                   'Team 2 Score', 'Score Difference', 'OT', 'European game',
                                                   'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team',
                                                   'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                                   'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog',
                                                   'size_Underdog', 'cold_Underdog', 'new_coach_Favorite',
                                                   'new_year_coach_Favorite', 'new_coach_Underdog', 'new_year_coach_Underdog',
                                                   'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'Overall_qb_Favorite',
                                                   'starting_qb_Underdog', 'Overall_qb_Underdog', 'count_stars_Underdog',
                                                   'stars_""_Underdog', 'stars_"Q"_Underdog','stars_"O"_Underdog',
                                                   'count_stars_Favorite',
                                                   'stars_""_Favorite', 'stars_"Q"_Favorite','stars_"O"_Favorite', 'count_superstars_Underdog',
                                                   'superstars_""_Underdog', 'superstars_"Q"_Underdog', 'superstars_"O"_Underdog', 'count_superstars_Favorite',
                                                   'superstars_""_Favorite', 'superstars_"Q"_Favorite', 'superstars_"O"_Favorite'
                                                   ]]
    #Fill in the missing Data

    betting_odds_df_merge['starting_qb_Underdog'].fillna('O', inplace=True)
    betting_odds_df_merge['starting_qb_Favorite'].fillna('O', inplace=True)
    betting_odds_df_merge['Overall_qb_Favorite'].fillna(0, inplace=True)
    betting_odds_df_merge['Overall_qb_Underdog'].fillna(0, inplace=True)

    betting_odds_df_merge['count_stars_Underdog'].fillna('O', inplace=True)
    betting_odds_df_merge['stars_""_Underdog'].fillna('O', inplace=True)
    betting_odds_df_merge['stars_"Q"_Underdog'].fillna(0, inplace=True)
    betting_odds_df_merge['stars_"O"_Underdog'].fillna(0, inplace=True)

    betting_odds_df_merge['count_stars_Favorite'].fillna('O', inplace=True)
    betting_odds_df_merge['stars_""_Favorite'].fillna('O', inplace=True)
    betting_odds_df_merge['stars_"Q"_Favorite'].fillna(0, inplace=True)
    betting_odds_df_merge['stars_"O"_Favorite'].fillna(0, inplace=True)

    betting_odds_df_merge['count_superstars_Favorite'].fillna('O', inplace=True)
    betting_odds_df_merge['superstars_""_Favorite'].fillna('O', inplace=True)
    betting_odds_df_merge['superstars_"Q"_Favorite'].fillna(0, inplace=True)
    betting_odds_df_merge['superstars_"O"_Favorite'].fillna(0, inplace=True)

    betting_odds_df_merge['count_superstars_Underdog'].fillna('O', inplace=True)
    betting_odds_df_merge['superstars_""_Underdog'].fillna('O', inplace=True)
    betting_odds_df_merge['superstars_"Q"_Underdog'].fillna(0, inplace=True)
    betting_odds_df_merge['superstars_"O"_Underdog'].fillna(0, inplace=True)
    # Drop all rows with NA
    betting_odds_df_merge = betting_odds_df_merge.dropna()

    data_for_nn = betting_odds_df_merge[['Day',  'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                                         'Underdog', 'Over/Under', 'week_number', 'Year', 'OT', 'European game',
                                         'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                                         'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                                         'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'starting_qb_Underdog', 'Overall_qb_Favorite', 'Overall_qb_Underdog', 'Score Difference'
                                         , 'count_stars_Underdog',
                                         'stars_""_Underdog', 'stars_"Q"_Underdog','stars_"O"_Underdog', 'count_stars_Favorite',
                                         'stars_""_Favorite', 'stars_"Q"_Favorite','stars_"O"_Favorite', 'count_superstars_Underdog',
                                         'superstars_""_Underdog', 'superstars_"Q"_Underdog','superstars_"O"_Underdog', 'count_superstars_Favorite',
                                         'superstars_""_Favorite', 'superstars_"Q"_Favorite','superstars_"O"_Favorite']]

    data_for_nn['Score Difference binary'] = np.where(
        data_for_nn['Score Difference'] - data_for_nn['Spread'] < 0, 1, 0)
    filter_results_for_NN = data_for_NN['Score Difference'] - \
        data_for_nn['Spread'] != 0

    data_for_nn = data_for_nn[filter_results_for_NN]
    data_for_nn = data_for_nn[['Day', 'Time (ET)', 'home_1', 'conference_Favorite', 'division_Favorite', 'conference_Underdog', 'division_Underdog', 'Favorite', 'Spread', 'home_2',
                               'Underdog', 'Over/Under', 'week_number', 'Year', 'OT', 'European game',
                               'Favorite_city', 'Favorite_team', 'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite', 'win_Underdog', 'loss_Underdog',
                               'worth_Favorite', 'size_Favorite', 'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog', 'new_coach_Favorite', 'new_year_coach_Favorite',
                               'new_coach_Underdog', 'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog', 'starting_qb_Favorite', 'starting_qb_Underdog', 'Overall_qb_Favorite', 'Overall_qb_Underdog', 'Score Difference binary'
                               , 'count_stars_Underdog',
                               'stars_""_Underdog', 'stars_"Q"_Underdog','stars_"O"_Underdog', 'count_stars_Favorite',
                               'stars_""_Favorite', 'stars_"Q"_Favorite','stars_"O"_Favorite', 'count_superstars_Underdog',
                               'superstars_""_Underdog', 'superstars_"Q"_Underdog','superstars_"O"_Underdog', 'count_superstars_Favorite',
                               'superstars_""_Favorite', 'superstars_"Q"_Favorite','superstars_"O"_Favorite']]
    file_tests_name = file_path + "\\data_for_NN_2.xlsx"
    writer = pd.ExcelWriter(file_tests_name, engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    data_for_nn.to_excel(writer, sheet_name='Sheet1', index=False)
    # Save the Excel file
    writer.save()
    writer.close()

    return data_for_nn
