
def table_to_dataframe(table):
    rows = table.find_all('tr')
    header = [th.text.strip() for th in rows[0].find_all('th')]
    data = []
    for row in rows[1:]:
        data.append([td.text.strip() for td in row.find_all('td')])

    return pd.DataFrame(data, columns=header)

def get_betting_odds(start, end, file_path, current_year, current_week):
    s = requests.Session()

    final_df = []
    for y in range(start, end, 1):
        url = 'https://www.sportsoddshistory.com/nfl-game-season/?y=' + str(y)
        response = s.get(url)
        time.sleep(5)  # Wait before gathering info
        soup = BeautifulSoup(response.content, "html.parser")
        docu = soup.find_all('table')
        # Collect data from the webpage
        tables_list = [df for df in docu if 'Super Bowl' not in df.get_text() and 'Day' in df.get_text()]

        if current_year - 1 == y and current_week < 19:
            tables_list = tables_list[2:]
        dataframes = [table_to_dataframe(table) for table in tables_list]
        for i, df in enumerate(dataframes):
            df['week_number'] = i + 1  # 1-indexed table numbers, use i for 0-indexed
        # Concatenating the list of dataframes
        df_for_year = pd.concat(dataframes, ignore_index=True)
        # add year to the dataframe
        df_for_year["Year"] = y
        if y == start:
            final_df = df_for_year
        else:
            final_df = final_df.append(df_for_year)
    # Organize the data
    final_df["W 0" == final_df['Spread']]
    final_df['Spread'] = final_df['Spread'].str.replace('PK', '0')

    df['Favorite'] = df['Favorite'].apply(lambda x: x.split()[-1])
    df['Underdog'] = df['Underdog'].apply(lambda x: x.split()[-1])

    final_df['Spread'] = final_df['Spread'].str.split().str.get(1).astype(float)
    final_df['Over/Under'] = final_df['Over/Under'].str.split().str.get(1).astype(float)
    # Extract the scores into two new columns
    final_df[['Team 1 Score', 'Team 2 Score']] = final_df['Score'].str.extract(r'(\d+)-(\d+)').astype(int)
    final_df['Score Difference'] = final_df['Team 2 Score'] - final_df['Team 1 Score']

    # Create an "OT" column based on the presence of "(OT)" in the original  OT is Over Time
    final_df['OT'] = final_df['Score'].str.contains(r'\(OT\)').astype(int)
    # Check if the column name is empty and rename accordingly
    new_cols = final_df.columns.tolist()
    for i, col_name in enumerate(new_cols):
        if col_name == "":
            if 'home_1' not in new_cols:
                new_cols[i] = 'home_1'
            else:
                new_cols[i] = 'home_2'

    if len(new_cols) == len(final_df.columns):
        final_df.columns = new_cols
    final_df['European game'] = np.where(final_df['home_1'] == 'N', 1, 0)
    final_df['home_1'] = final_df['home_1'].replace('N', '', regex=False)
    # Convert cells in 'home_1' and 'home_2' columns
    final_df['home_1'] = final_df['home_1'].str.contains('@').astype(bool)
    final_df['home_2'] = final_df['home_2'].str.contains('@').astype(bool)
    final_df.columns
    final_df[['Favorite_city', 'Favorite_team']] = final_df['Favorite'].str.rsplit(n=1, expand=True)
    final_df[['Underdog_city', 'Underdog_team']] = final_df['Underdog'].str.rsplit(n=1, expand=True)

    final_df['Favorite_city'] = final_df['Favorite_city'].replace('Washington Football', 'Washington', regex=False)
    final_df['Favorite_team'] = final_df['Favorite_team'].replace('Team', 'Football Team', regex=False)
    final_df['Underdog_city'] = final_df['Underdog_city'].replace('Washington Football', 'Washington', regex=False)
    final_df['Underdog_team'] = final_df['Underdog_team'].replace('Team', 'Football Team', regex=False)

    final_df = final_df.drop('Score', axis=1)
    final_df = final_df.drop('Notes', axis=1)
    betting_odds_df = final_df
    filename = file_path + "\\Betting Odds\\betting_odds.xlsx"  # Replace with your variable name
    betting_odds_df.to_excel(filename, engine='openpyxl', index=False)
    return betting_odds_df
