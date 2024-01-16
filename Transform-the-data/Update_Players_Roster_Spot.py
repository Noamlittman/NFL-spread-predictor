def is_active(row):
    if (pd.isna(row['next_team_min_week']) and pd.isna(row['min_week']) and row['more_teams'] == 0) or (
            row['week'] < row['next_team_min_week'] and pd.isna(row['min_week'])):
        return 1
    elif pd.isna(row['next_team_min_week']) and row['min_week'] <= row['week']:
        return 1
    elif row['week'] < row['next_team_min_week'] and row['min_week'] <= row['week']:
        return 1
    return 0


def update_players_on_teams(full_teams_roster_df):

    grouped = full_teams_roster_df.groupby(['year', 'Player', 'week','BirthDate']).size().reset_index(name='counts')
    eligible_groups = grouped[grouped['counts'] > 1]
    full_teams_roster_df = full_teams_roster_df.merge(eligible_groups[['year', 'Player', 'week', 'BirthDate']], on=['year', 'Player', 'week', 'BirthDate'], how='left', indicator=True)

    # Create the 'more_teams' column, where 1 indicates the condition is met
    full_teams_roster_df['more_teams'] = (full_teams_roster_df['_merge'] == 'both').astype(int)

    # Drop the merge indicator column
    full_teams_roster_df = full_teams_roster_df.drop(columns=['_merge'])
    eligible_df = pd.merge(eligible_groups, full_teams_roster_df, on=['year', 'Player', 'week','BirthDate'])
    # Filter eligible_df based on the conditions
    eligible_df = eligible_df[(eligible_df['played'] == 1) | (eligible_df['status'] != '')]

    # Group by player, year, and full_team_name to find the minimum week
    min_weeks = eligible_df.groupby(['Player', 'year' ,'BirthDate','full_team_name'])['week'].min().reset_index().rename(columns={'week': 'min_week'})

    min_weeks = min_weeks.sort_values(by=['Player', 'year', 'min_week','BirthDate'])
    min_weeks['next_team_min_week'] = min_weeks.groupby(['Player','BirthDate', 'year'])['min_week'].shift(-1)

    full_teams_roster_df = full_teams_roster_df.merge(min_weeks, on=['Player', 'year', 'full_team_name','BirthDate'], how='left')

    full_teams_roster_df['active'] = full_teams_roster_df.apply(is_active, axis=1)

    full_teams_roster_df = full_teams_roster_df[full_teams_roster_df['active'] == 1]

    # Identify rows with players marked as "(IR" before making changes
    condition = full_teams_roster_df['Player'].str.contains(r"\(IR")

    # Remove everything after "(IR" in the 'Player' column
    full_teams_roster_df['Player'] = full_teams_roster_df['Player'].str.replace(r"\(IR.*", "", regex=True)

    # Update 'status' and 'active' only for those rows where "(IR" was originally found
    full_teams_roster_df.loc[condition, 'status'] = 'IR'
    full_teams_roster_df.loc[condition, 'active'] = 0
    full_teams_roster_df['status'].fillna('', inplace=True)
    full_teams_roster_df["status"].replace("D", "O", inplace=True)
    full_teams_roster_df["status"].replace("P", "", inplace=True)
    full_teams_roster_df["status"].replace("IR", "O", inplace=True)

    condition = ~full_teams_roster_df["status"].isin(["Q", "O", "IR", ""])

    # Set status to empty string where condition is True
    full_teams_roster_df.loc[condition, "status"] = ""

    return full_teams_roster_df
