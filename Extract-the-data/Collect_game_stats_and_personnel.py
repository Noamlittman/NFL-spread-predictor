

def extract_pick_number(s):
    if s:
        # Extract the pick number, assume it's after the second slash
        parts = s.split('/')
        if len(parts) > 2:
            pick_part = parts[2].strip().split(' ')[0]
            # Remove any non-digit characters and convert to int
            pick_number = int(''.join(filter(str.isdigit, pick_part)))
            return pick_number
    return 400  # Default value for empty cells


def new_qb(row, df):
    if pd.isna(row['Years Pro']) or row['Years Pro'] == '':
        previous_year_record = df[(df['Name'] == row['Name']) & (df['year'] == row['year'] - 1)]
        if previous_year_record.empty:
            return '0'
        else:
            previous_years_pro = previous_year_record.iloc[0]['Years Pro']
            if pd.isna(previous_years_pro) or previous_years_pro == '' or previous_years_pro == '0':
                return '1'
            else:
                return str(int(previous_years_pro) + 1)
    return row['Years Pro']


def is_new_coach_year(row, df):
    # Check if it's the first record of the team in the dataset
    if df[(df['team name'] == row['team name']) & (df['year'] < row['year'])].empty:
        return 0
    elif row['week'] > 0:
        # Filter for the team's coach in week 17 of the previous year
        previous_year_coach = \
        df[(df['team name'] == row['team name']) & (df['year'] == row['year'] - 1) & (df['week'] == 17)]['coach']
        # If there is no such coach or the coach is different, mark as a new coach
        if previous_year_coach.empty or (not previous_year_coach.empty and previous_year_coach.iloc[0] != row['coach']):
            return 1
    return 0


def is_new_coach(row, df):
    # Check if it's the first record of the team in the dataset
    if row['week'] == 1:
        return 0
    if row['week'] == 2:
        return 0
    previous_coach = df[(df['team name'] == row['team name']) & (df['year'] == row['year']) & (df['week'] == 2)][
        'coach']

    # If there is no such coach or the coach is different, mark as a new coach
    if previous_coach.iloc[0] != row['coach']:
        return 1

    return 0


def has_multiindex(df):
    return isinstance(df.index, pd.MultiIndex) or isinstance(df.columns, pd.MultiIndex)


def find_team_rosters(start, end, teams_file_path, file_path, current_week, current_year):
    # Read the teams_file_path .xlsx file into a DataFrame
    team_names_table = pd.read_excel(teams_file_path, engine='openpyxl')

    coaches_df = pd.DataFrame(columns=['team', 'coach', 'year', 'week'])
    teams_standing_df = pd.DataFrame(columns=['team', 'year', 'week', 'winns', 'losses'])
    full_teams_roster_df = pd.DataFrame()

    # connet to the crome driver
    cService = webdriver.ChromeService()
    driver = webdriver.Chrome(service=cService)
    driver.set_window_position(-10000, 0)
    merged_df_all_games = []
    # keep only rows with nlf teams
    teams_to_keep = [
        'Atlanta Falcons', 'New Orleans Saints', 'New England Patriots',
        'Green Bay Packers', 'Dallas Cowboys', 'Arizona Cardinals',
        'Oakland Raiders', 'Indianapolis Colts', 'San Diego Chargers',
        'Buffalo Bills', 'Pittsburgh Steelers', 'Washington Redskins',
        'Kansas City Chiefs', 'Tennessee Titans', 'Carolina Panthers',
        'Philadelphia Eagles', 'Miami Dolphins', 'Seattle Seahawks',
        'Tampa Bay Buccaneers', 'Detroit Lions', 'Baltimore Ravens',
        'Denver Broncos', 'Minnesota Vikings', 'Cincinnati Bengals',
        'Jacksonville Jaguars', 'New York Giants', 'San Francisco 49ers',
        'Houston Texans', 'Chicago Bears', 'New York Jets',
        'Cleveland Browns', 'Los Angeles Rams', 'San Diego Chargers', 'Las Vegas Raiders'
    ]
    teams_to_keep_letters = [''.join(filter(str.isalpha, item))[:3].upper() for item in teams_to_keep]
    new_items = ['LAR', 'LAC', 'LVR', 'GBP', 'SDG', 'NWE', 'SFO', 'NOR', 'NYJ', 'NYG', 'STL']

    # Adding first letters teams Using extend()
    teams_to_keep_letters.extend(new_items)
    teams_to_keep.extend(teams_to_keep_letters)

    # Adding team names to the list Using extend()
    teams_to_keep_names_only = [item.split()[-1] for item in teams_to_keep]
    teams_to_keep.extend(teams_to_keep_names_only)
    # Loop through every year team general stats from pro-football-reference

    for y in range(start, end, 1):
        for w in range(1, 19, 1):
            if y < 2021 and w == 19:
                continue
            if current_year == y and w >= current_week:
                continue

            # enter the pro-football-reference website via chrome driver
            web_page = 'https://www.pro-football-reference.com/years/' + str(y) + '/week_' + str(w) + '.htm'
            try:
                driver.get(web_page)

            except TimeoutException:
                time.sleep(2)
                cService = webdriver.ChromeService()
                driver = webdriver.Chrome(service=cService)
                driver.get(web_page)
            time.sleep(5)
            # create the merged df
            links_nub = []
            # take the tables in the page
            soup = BeautifulSoup(driver.page_source, "html.parser")

            links = soup.find_all('div', class_='game_summaries')

            links = links[1]
            links = links.find_all('td', class_='right gamelink')
            # Create a ResultSet using the desired_divs list
            for g in links:
                k = 100
                web_page = 'https://www.pro-football-reference.com' + str(g.find('a')['href'])
                try:
                    driver.get(web_page)

                except TimeoutException:
                    time.sleep(2)
                    cService = webdriver.ChromeService()
                    driver = webdriver.Chrome(service=cService)
                    driver.get(web_page)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                table_elements = soup.find_all('table')
                # create the merged df
                merged_df = []
                table_elements_nub = []

                # find coach

                team_name_in_page = [tag.text.strip('\n') for tag in soup.find_all("strong") if
                                     tag.text.strip('\n') in team_names_table["full_names"].values]

                coaches_list = [tag.text.replace('Coach: ', '').strip('\n') for tag in
                                soup.find_all("div", class_="datapoint") if "Coach: " in tag.text.strip('\n')]

                coach_df = pd.DataFrame({
                    'team': team_name_in_page,
                    'coach': coaches_list,
                    'year': [y, y],
                    'week': [w, w]
                })

                coaches_df = coaches_df.append(coach_df)

                # find standings:
                # Find all <div class="scores">
                scores_divs = soup.find_all('div', class_='scores')

                # List to hold the text of following divs
                following_div_texts = []

                # Loop through all found divs with class 'scores'
                for scores_div in scores_divs:
                    # Find the next sibling that is a <div>
                    next_div = scores_div.find_next_sibling('div')

                    # If the next sibling is a div, extract its text
                    if next_div:
                        following_div_texts.append(next_div.get_text(strip=True))

                wins = []
                losses = []

                # Iterate through each score in the scores list
                for score in following_div_texts:
                    # Split the score on the hyphen
                    parts = score.split('-')

                    # Add the first part as a win
                    wins.append(int(parts[0]))

                    # Add the second part as a loss
                    # We assume that every score string contains at least two numbers separated by a hyphen
                    losses.append(int(parts[1]))

                team_standing_df = pd.DataFrame({
                    'team': team_name_in_page,
                    'winns': wins,
                    'losses': losses,
                    'year': [y, y],
                    'week': [w, w]
                })

                teams_standing_df = teams_standing_df.append(team_standing_df)

                # remove all the tables that are not relevent
                for i in range(len(table_elements)):
                    if "linescore nohover stats_table no_freeze" in str(table_elements[i]):
                        k = i

                    if k < i:
                        table_elements_nub.append(i)
                desired_divs = [soup.find_all('table')[i] for i in table_elements_nub]

                # Create a ResultSet using the desired_divs list
                table_elements = ResultSet(source=soup, result=desired_divs)
                # create a list of all the df
                dfs = [pd.read_html(str(table))[0] for table in table_elements]

                # orgenize the columns names
                for df in dfs:
                    if has_multiindex(df) == False:
                        continue
                    combined_idx = [x[1] if "Unnamed" in x[0] else "_".join(x) for x in df]
                    df.columns = combined_idx

                # remove tables that dont have a column Tm
                dfs = [df for df in dfs if 'Tm' in df.columns and 'Player' in df.columns]

                pattern = '[^a-zA-Z]+$'

                # For each DataFrame in dfs, clean the 'Tm' column
                for df in dfs:
                    if 'Tm' in df.columns:
                        df['Tm'] = df['Tm'].str.replace(pattern, '', regex=True)

                for df in dfs:
                    # Drop rows where 'Tm' is not in teams_to_keep
                    df.drop(df[~df['Tm'].isin(teams_to_keep)].index, inplace=True)

                merged_df = dfs[0]

                # Loop through the rest of the DataFrames and merge them one by one
                for df in dfs[1:]:
                    if 'Tm' in df.columns:
                        merged_df = pd.merge(merged_df, df, on=['Tm', 'Player'], how='outer')
                # Get positions of all columns
                cols_positions = list(range(merged_df.shape[1]))
                # Get positions of duplicated columns (only keeps the first occurrence)
                _, unique_idx = np.unique(merged_df.columns, return_index=True)
                duplicated_positions = set(cols_positions) - set(unique_idx)

                # Drop columns by position
                merged_df = merged_df.drop(merged_df.columns[list(duplicated_positions)], axis=1)
                merged_df['year'] = y
                merged_df['week'] = w
                merged_df = merged_df.dropna(subset=['Player'])

                if w == 1 and y == start and len(merged_df_all_games) == 0:
                    merged_df_all_games = merged_df
                    continue
                merged_df_all_games = merged_df_all_games.reset_index(drop=True)
                merged_df = merged_df.reset_index(drop=True)
                # teams_rosters = merged_df.iloc[:, [0, 1]]
                # teams_rosters = teams_rosters.drop_duplicates()
                merged_df_all_games = merged_df_all_games.append(merged_df, ignore_index=True)
        # testing
        merged_df_all_games_1 = merged_df_all_games
        merged_df_all_games_1 = pd.merge(merged_df_all_games, team_names_table, left_on='Tm', right_on='short',
                                         how='outer')
        merged_df_all_games_1["full_team_name"] = merged_df_all_games_1["city"] + " " + merged_df_all_games_1[
            "team name"]
        merged_df_all_games_1 = merged_df_all_games_1.dropna(subset=['Player'])
        # get team rosters and injuries
        # enter the pro-football-reference website via chrome driver
        web_page = 'https://www.pro-football-reference.com/years/' + str(y) + '/week_1.htm'
        try:
            driver.get(web_page)

        except TimeoutException:
            time.sleep(2)
            cService = webdriver.ChromeService()
            driver = webdriver.Chrome(service=cService)
            driver.get(web_page)
        time.sleep(2)
        # create the merged df
        links_nub = []
        # take the tables in the page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # get_injuries
        links_nub = []
        teams_playing = soup.find_all('tr', class_=['draw', 'loser', 'winner'])
        for i in range(len(teams_playing)):
            if "/players/" in str(teams_playing[i]):
                continue
            if "/" + str(y) in str(teams_playing[i]):
                links_nub.append(i)
        desired_divs = [soup.find_all('tr', class_=['draw', 'loser', 'winner'])[i] for i in links_nub]
        teams_playing_links = ResultSet(source=soup, result=desired_divs)
        for g in teams_playing_links:
            works = 1
            team_name = g.find('a').get_text(strip=True)
            web_page = 'https://www.pro-football-reference.com' + str(g.find('a')['href'])
            web_page = web_page.replace('.htm', '_injuries.htm')
            try:
                driver.get(web_page)

            except TimeoutException:
                time.sleep(2)
                cService = webdriver.ChromeService()
                driver = webdriver.Chrome(service=cService)
                driver.get(web_page)

            # Handle the timeout

            driver.set_page_load_timeout(2)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find('table', {'id': 'team_injuries'})
            # Find the table

            # Extract the header (column names)
            if y < 2021:
                gam = 17
            if y >= 2021:
                gam = 18
            if y == current_year:
                gam = current_week - 1
            try:
                headers = [th.text.strip() for th in table.find_all('th')][:gam]  # Adjust the slice as needed
            except AttributeError:
                works = 0
            # Extract the rows
            if works == 1:
                rows = []
                for tr in table.find_all('tr'):
                    cells = tr.find_all(['th', 'td'])
                    row = [cell.get_text(strip=True) for cell in cells[:gam]]
                    if len(row) == len(headers):  # Ensure the row has the same number of columns as the headers
                        rows.append(row)

                # Create a DataFrame
                injuries_df = pd.DataFrame(rows, columns=headers)
                injuries_df.columns = [col[-3:] if col != 'Player' else col for col in injuries_df.columns]
                injuries_df = injuries_df[injuries_df['Player'] != 'Player']
                injuries_df["full_team_name"] = team_name
            temp_table = merged_df_all_games_1[
                (merged_df_all_games_1["full_team_name"] == team_name) & (merged_df_all_games_1["year"] == y)]

            # find_full_team_roster
            web_page = 'https://www.pro-football-reference.com' + str(g.find('a')['href'])
            web_page = web_page.replace('.htm', '_roster.htm')
            try:
                driver.get(web_page)

            except TimeoutException:
                time.sleep(2)
                cService = webdriver.ChromeService()
                driver = webdriver.Chrome(service=cService)
                driver.get(web_page)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all tables
            tables = soup.find_all('table')
            full_team_roster = pd.DataFrame()
            # Loop through each table and check if it has the desired column
            for table in tables:
                headers = [th.get_text(strip=True) for th in table.find_all('th')]
                if 'College/Univ' in headers:
                    headers = [th.text.strip() for th in table.find_all('th')][:13]  # Adjust the slice as needed
                    # Extract the rows
                    rows = []
                    for tr in table.find_all('tr'):
                        # current_table.find_all('tr')[40]
                        cells = tr.find_all(['th', 'td'])
                        row = [cell.get_text(strip=True) for cell in cells]
                        if len(row) == len(headers):  # Ensure the row has the same number of columns as the headers
                            rows.append(row)

                    # Create DataFrame
                    full_team_roster = pd.DataFrame(rows, columns=headers)
                    full_team_roster = full_team_roster[full_team_roster['Player'] != 'Player']
                    full_team_roster = full_team_roster[full_team_roster['Player'] != 'Team Total']
                    full_team_roster['Drafted (tm/rnd/yr)'] = full_team_roster['Drafted (tm/rnd/yr)'].apply(
                        extract_pick_number)
                    full_team_roster["full_team_name"] = team_name
                    full_team_roster['Yrs'] = full_team_roster['Yrs'].replace('Rook', 0)

                    # Break the loop if you only need the first matching table
                    break

            df2 = full_team_roster
            df1 = temp_table
            df3 = injuries_df
            # Get all unique weeks
            weeks = df1['week'].unique()

            # Creating a new DataFrame with all combinations of Player and week
            player_week_combinations = pd.MultiIndex.from_product([df2['Player'], weeks],
                                                                  names=["Player", "week"]).to_frame(index=False)

            # Merging with df1 to find if the player played in each week
            merged_df = pd.merge(player_week_combinations, df1[['Player', 'week']], on=['Player', 'week'], how='left',
                                 indicator=True)

            # Set 'played' column based on merge
            merged_df['played'] = (merged_df['_merge'] == 'both').astype(int)

            # Dropping the merge indicator column
            merged_df.drop(columns=['_merge'], inplace=True)

            # Merge with df2 to add other columns
            final_df = pd.merge(merged_df, df2, on='Player', how='left')
            final_df["year"] = y

            week_to_column = {week: i for i, week in enumerate(sorted(final_df['week'].unique()), start=1)}

            # Update the status in final_df based on df3
            for index, row in final_df.iterrows():
                player = row['Player']
                week = row['week']

                # Find the corresponding player row in df3
                df3_player_row = df3[df3['Player'] == player]

                if not df3_player_row.empty:
                    # Get the corresponding column index for the week
                    col_index = week_to_column.get(week)

                    if col_index and col_index <= len(df3_player_row.columns):
                        # Update the status
                        final_df.at[index, 'status'] = df3_player_row.iloc[0, col_index]
                    else:
                        # If the week does not have a corresponding column in df3
                        final_df.at[index, 'status'] = None

            if full_teams_roster_df.empty:
                full_teams_roster_df = final_df
            else:
                full_teams_roster_df = full_teams_roster_df.append(final_df, ignore_index=True)

    full_teams_roster_df["status"] = full_teams_roster_df["status"].fillna("")
    merged_df_all_games = pd.merge(merged_df_all_games, team_names_table, left_on='Tm', right_on='short', how='outer')
    merged_df_all_games = merged_df_all_games.dropna(subset=['Player'])
    merged_df_all_games = merged_df_all_games[["Player", "team name", "city", 'year', 'week', 'full_names']]

    df = merged_df_all_games
    df1 = full_teams_roster_df

    # organize coaching data
    coaches_df = pd.merge(coaches_df, team_names_table, left_on='team', right_on='full_names', how='outer')
    coaches_df = coaches_df.dropna(subset=['team'])

    # Applying the function to create the 'new_year_coach' column
    coaches_df['new year coach'] = coaches_df.apply(lambda row: is_new_coach_year(row, coaches_df), axis=1)
    coaches_df['new coach'] = coaches_df.apply(lambda row: is_new_coach(row, coaches_df), axis=1)
    coaches_df = coaches_df[['city', 'team name', 'coach', 'year', 'week', 'new coach', 'new year coach']]
    file_coaches_name = file_path + "\\coaches.xlsx"
    #  writer = pd.ExcelWriter(file_coaches_name, engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    #   coaches_df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel file
    #   writer.save()
    #    writer.close()

    # organize standings data

    teams_standing_df_test = pd.merge(teams_standing_df, team_names_table, left_on='team', right_on='full_names',
                                      how='outer')
    teams_standing_df_test = teams_standing_df_test.dropna(subset=['team'])
    teams_standing_df_test = teams_standing_df_test.dropna(subset=['week'])
    teams_standing_df_test = teams_standing_df_test[
        ['city', 'team name', 'full_names', 'year', 'week', 'winns', 'losses']]
    df = teams_standing_df_test

    # Copy and sort the DataFrame
    df_sorted = df.copy()
    df_sorted.sort_values(by=['team name', 'year', 'week'], inplace=True)

    # Initialize a dictionary to hold the last wins/losses for each team and year
    last_win_loss = {}

    # Create a new DataFrame for updated wins/losses values
    win_loss_updates = []

    # Iterate over the sorted DataFrame
    for index, row in df_sorted.iterrows():
        team_year = (row['team name'], row['year'])

        # Initialize wins/losses for week 1
        if row['week'] == 1:
            last_win_loss[team_year] = {'winns': 0, 'losses': 0}
            win_loss_updates.append({'team name': row['team name'], 'year': row['year'], 'week': row['week'],
                                     'winns': last_win_loss[team_year]['winns'],
                                     'losses': last_win_loss[team_year]['losses']})
        else:
            if team_year in last_win_loss:
                current_sum = last_win_loss[team_year]['winns'] + last_win_loss[team_year]['losses']

                # Check if current_sum + 1 or current_sum + 2 equals the current week
                if current_sum < row['week']:
                    win_loss_updates.append({'team name': row['team name'], 'year': row['year'], 'week': row['week'],
                                             'winns': last_win_loss[team_year]['winns'],
                                             'losses': last_win_loss[team_year]['losses']})
                else:
                    # If the condition doesn't hold, use the values from the row
                    win_loss_updates.append({'team name': row['team name'], 'year': row['year'], 'week': row['week'],
                                             'winns': row['winns'], 'losses': row['losses']})

        # Update the last known wins/losses
        last_win_loss[team_year] = {'winns': row['winns'], 'losses': row['losses']}

    # Convert the updates list to a DataFrame
    updates_df = pd.DataFrame(win_loss_updates)

    # Merge the update DataFrame with the original DataFrame
    df_final = df.merge(updates_df, on=['team name', 'year', 'week'], how='left', suffixes=('', '_updated'))

    # Drop the original 'wins' and 'losses' columns and rename the updated columns
    df_final.drop(columns=['winns', 'losses'], inplace=True)
    df_final.rename(columns={'winns_updated': 'winns', 'losses_updated': 'losses'}, inplace=True)

    teams_standing_df_test = df_final

    file_standings_name = file_path + "\\standings.xlsx"
    writer = pd.ExcelWriter(file_standings_name, engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    teams_standing_df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel file
    writer.save()
    writer.close()

    file_rosters_name = file_path + "\\rosters.xlsx"
    writer = pd.ExcelWriter(file_rosters_name, engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    merged_df_all_games.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel file
    writer.save()
    writer.close()

    return teams_standing_df_test, coaches_df, merged_df_all_games, full_teams_roster_df

