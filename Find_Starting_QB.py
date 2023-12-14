def determine_starting(group):
    # Check if all 'status' are empty
    if (group['status'] == '').all():
        return ['S', group['Overall'].max()]
    elif (group['status'] != '').any() and (group[group['status'] != '']['Overall'].max() < group['Overall'].max()):
        return ['S',group['Overall'].max()]
    elif (group['status'] == 'Q').any():
        return ['Q',group[group['status'] == '']['Overall'].max()]
    return ['O',group[group['status'] == '']['Overall'].max()]


def find_starting_qb(full_teams_roster_df,player_team_stats_madden_years):

    qb_in_rosters = full_teams_roster_df[full_teams_roster_df['Pos'] == 'QB']
    player_team_stats_madden_years_qb = player_team_stats_madden_years[
        player_team_stats_madden_years['Position'] == 'QB']
    player_team_stats_madden_years_qb = player_team_stats_madden_years_qb[['Name', 'Overall', 'year']]
    qb_in_rosters = qb_in_rosters.merge(player_team_stats_madden_years_qb, left_on=('Player', 'year'),
                                        right_on=('Name', 'year'))

    starting_series = qb_in_rosters.groupby(['year', 'week', 'full_team_name']).apply(determine_starting)

    starting_df = starting_series.reset_index(name='starting')
    starting_df['starting'] = starting_df['starting'].astype(str)

    # Now apply the string methods
    starting_df[['starting', 'starting_overall']] = starting_df['starting'].str.strip('[]').str.split(',', expand=True)

    # The 'starting' part should be fine, but let's trim any whitespace
    starting_df['starting'] = starting_df['starting'].str.strip("'")

    # Strip whitespace and convert 'nan' strings to actual NaN values
    starting_df['starting_overall'] = starting_df['starting_overall'].str.strip().replace('nan', pd.NA)

    # Now fill NaN values with 0 and convert to int
    starting_df['starting_overall'] = starting_df['starting_overall'].fillna(0).astype(float).astype(int)

    # Merge with the original DataFrame
    qb_in_rosters = qb_in_rosters.merge(starting_df, on=['year', 'week', 'full_team_name'], how='left')

    starting_qb = qb_in_rosters[['year', 'week', 'full_team_name', 'starting', 'starting_overall']]
    starting_qb = starting_qb.drop_duplicates()

    return starting_qb
