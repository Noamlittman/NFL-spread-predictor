def madden_stars_data(full_teams_roster_df,player_team_stats_madden_years):
    superstar_player_roster = full_teams_roster_df[['Player', 'week', 'Age', 'Pos', 'Wt', 'Ht',
                                                    'Yrs', 'Drafted (tm/rnd/yr)', 'full_team_name',
                                                    'year', 'status']]
    superstar_player_team_madden_years = player_team_stats_madden_years[player_team_stats_madden_years['Overall'] > 93]
    superstar_player_team_madden_years = superstar_player_team_madden_years[['Name', 'Overall', 'year', 'Position']]
    superstar_player_roster = (superstar_player_roster.merge
                               (superstar_player_team_madden_years,
                                left_on=('Player', 'year', 'Pos'), right_on=('Name', 'year', 'Position')))
    superstar_player_roster['status'].fillna('', inplace=True)
    superstar_player_roster = superstar_player_roster[['Player', 'week', 'Age', 'Pos',  'Yrs',
                                                       'Drafted (tm/rnd/yr)', 'full_team_name', 'year', 'status',
                                                       'Overall']]

    count_all_players = superstar_player_roster.groupby(['year', 'week', 'full_team_name']).size().reset_index(name='count_superstars')

    # Count players with each status using pivot_table
    count_status = superstar_player_roster.pivot_table(index=['year', 'week', 'full_team_name'],
                                                       columns='status',
                                                       aggfunc='size',
                                                       fill_value=0).reset_index()

    # Rename columns for clarity
    count_status.rename(columns={'O': 'superstars "O"',
                                 'Q': 'superstars "Q"',
                                 '': 'superstars ""'}, inplace=True)

    # Merge the two DataFrames on 'year', 'week', 'full_team_name'
    superstar_player_df = pd.merge(count_all_players, count_status, on=['year', 'week', 'full_team_name'])

    superstar_player_df = superstar_player_df.drop_duplicates()

    star_player_roster = full_teams_roster_df[['Player', 'week', 'Age', 'Pos', 'Wt', 'Ht',
                                               'Yrs', 'Drafted (tm/rnd/yr)', 'full_team_name', 'year', 'status']]
    star_player_team_madden_years = player_team_stats_madden_years[(player_team_stats_madden_years['Overall'] > 87) &
                                                                   (player_team_stats_madden_years['Overall'] < 94)]
    star_player_team_madden_years = star_player_team_madden_years[['Name', 'Overall', 'year', 'Position']]
    star_player_roster = star_player_roster.merge(star_player_team_madden_years,
                                                  left_on=('Player', 'year', 'Pos'),
                                                  right_on=('Name', 'year', 'Position'))
    star_player_roster['status'].fillna('', inplace=True)
    star_player_roster = star_player_roster[['Player', 'week', 'Age', 'Pos',  'Yrs',
                                             'Drafted (tm/rnd/yr)', 'full_team_name', 'year', 'status',
                                             'Overall']]

    count_all_players = star_player_roster.groupby(['year', 'week', 'full_team_name']).size().reset_index(name='count_stars')

    # Count players with each status using pivot_table
    count_status = star_player_roster.pivot_table(index=['year', 'week', 'full_team_name'],
                                                  columns='status',
                                                  aggfunc='size',
                                                  fill_value=0).reset_index()

    # Rename columns for clarity
    count_status.rename(columns={'O': 'stars "O"',
                                 'Q': 'stars "Q"',
                                 '': 'stars ""'}, inplace=True)

    # Merge the two DataFrames on 'year', 'week', 'full_team_name'
    star_player_df = pd.merge(count_all_players, count_status, on=['year', 'week', 'full_team_name'])
    star_player_df = star_player_df.drop_duplicates()

    return star_player_df, superstar_player_df
