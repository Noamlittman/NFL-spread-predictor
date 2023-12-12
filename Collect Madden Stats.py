import pandas as pd
import requests
from bs4 import BeautifulSoup, ResultSet
import time
import re




def update_years_pro(row, df):
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



def take_madden_stats(start ,end ,file_path):

    # Start the request session
    s = requests.Session()
    # Start parameters
    count = 0
    start_y = start - 1999
    end_y = end - 1999
    for y in range(start_y ,end_y ,1):
        if y <10:
            url = 'https://maddenratings.weebly.com/madden-nfl-0' + str(y) + '.html'
        else:
            url = 'https://maddenratings.weebly.com/madden-nfl-' + str(y) + '.html'

        response = s.get(url)
        time.sleep(5)  # Wait before gathering info
        soup = BeautifulSoup(response.content, "html.parser")
        docu = soup.find_all('td', class_="wsite-multicol-col")
        links_html = [df for df in docu if ' OVR' in df.text]
        links = [a['href'] for td in links_html for a in td.find_all('a', href=True)]

        team_ovr = [df.text for df in docu if ' OVR' in df.text]

        # Extract team name and OVR using regex
        extracted_data = []
        for item in team_ovr:
            match = re.search(r'\n([A-Z][a-zA-Z\s\d.]+)(\d{2})\sOVR', item)
            if match:
                extracted_data.append(match.groups())

        # Convert to DataFrame
        team_ovr_df = pd.DataFrame(extracted_data, columns=['Team Name', 'Number'])
        team_ovr_df["year"] = 1999 + y
        file_name = file_path + "\\madden\\" + str(1999 + y) + "\\Teams Rating.xlsx"

        # Write the content of the request to a file
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Write the DataFrame to the Excel file
        team_ovr_df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Save the Excel file
        writer.save()
        writer.close()
        if y == start_y:
            team_ovr_df_years = team_ovr_df
        if y > start_y:
            team_ovr_df_years = team_ovr_df_years.append(team_ovr_df)
        if y == 22:
            links = ['/uploads/1/4/0/9/14097292/madden_nfl_22_final_roster.xlsx']
        count = 0
        for i in links:
            count += 1
            if count > 32:
                continue
            url = 'https://maddenratings.weebly.com' + i

            # Send a GET request
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for failed requests

            # name = i.split('/')[-1].rsplit('.xlsx', 1)[0]
            name = i.split('/')[-1].rsplit('_.xlsx', 1)[0].replace("__madden_nfl", "")
            # Path to save the file (you can specify your desired file name here)
            file_name = file_path + "\\madden\\" + str(1999 + y) + "\\" + name + ".xlsx"

            # Write the content of the request to a file
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            # Load the .xlsx file
            file_path_load = file_name
            try:
                player_team_stats_madden = pd.read_excel(file_path_load, engine='openpyxl')
            except Exception as e:
                player_team_stats_madden = pd.read_excel(file_path_load, engine='xlrd')
                file_path_load = file_path_load.replace('.xls.xlsx', ".xlsx")

            # Orgenize column names
            player_team_stats_madden.rename(columns=lambda x: 'Last' if 'LAST' in x.upper() else x, inplace=True)
            player_team_stats_madden.rename(columns=lambda x: 'First' if 'FIRST' in x.upper() else x, inplace=True)
            player_team_stats_madden.rename(columns=lambda x: 'Overall' if 'OVERALL' in x.upper() else x, inplace=True)
            player_team_stats_madden.rename(columns=lambda x: 'Overall' if 'OVR' == x.upper() else x, inplace=True)
            player_team_stats_madden.rename(columns=lambda x: 'Name' if 'FULL' in x.upper() else x, inplace=True)
            player_team_stats_madden.rename(
                columns=lambda x: 'Name' if ('NAME' in x.upper()) and ('UNNAMED' not in x.upper()) else x, inplace=True)
            player_team_stats_madden.rename(columns=lambda x: 'Position' if 'POS' in x.upper() else x, inplace=True)
            # List of desired columns
            desired_columns = ['Years Pro', 'Age', 'First', 'Last', 'Position', 'Overall', 'Name']

            # Filter out columns that don't exist in the DataFrame
            existing_columns = [col for col in desired_columns if col in player_team_stats_madden.columns]
            player_team_stats_madden = player_team_stats_madden[existing_columns]
            player_team_stats_madden = player_team_stats_madden.dropna(subset="Overall")
            player_team_stats_madden = player_team_stats_madden[player_team_stats_madden["Overall"] != 'Overall']
            player_team_stats_madden.reset_index(drop=True, inplace=True)

            # Subset the DataFrame using only existing columns
            player_team_stats_madden['year'] = 1999 + y

            writer = pd.ExcelWriter(file_path_load, engine='xlsxwriter')

            # Write the DataFrame to the Excel file
            player_team_stats_madden.to_excel(writer, sheet_name='Sheet1', index=False)

            # Save the Excel file
            writer.save()
            writer.close()
            if y == start_y and count == 1:
                player_team_stats_madden_years = player_team_stats_madden
            if y > start_y or count > 1:
                player_team_stats_madden_years = player_team_stats_madden_years.append(player_team_stats_madden)

    player_team_stats_madden_years_1 = player_team_stats_madden_years

    player_team_stats_madden_years_1['Name'] = player_team_stats_madden_years_1.apply(
        lambda row: (row['First'] + ' ' + row['Last']).strip() if pd.isna(row['Name']) or row['Name'] == '' else row[
            'Name'],
        axis=1)
    player_team_stats_madden_years_1['Years Pro'] = player_team_stats_madden_years_1.apply(
        lambda row: update_years_pro(row, player_team_stats_madden_years_1), axis=1)

    columns_to_keep = ['Years Pro', 'Age', 'year', 'Position', 'Overall', 'Name']

    player_team_stats_madden_years_1 = player_team_stats_madden_years_1[columns_to_keep]
    file_name = file_path + "\\madden\\player Rating.xlsx"

    # Write the content of the request to a file
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    player_team_stats_madden_years_1.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel file
    writer.save()
    writer.close()
    file_name = file_path + "\\madden\\Teams Rating.xlsx"

    # Write the content of the request to a file
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Write the DataFrame to the Excel file
    team_ovr_df_years.to_excel(writer, sheet_name='Sheet1', index=False)
    # Save the Excel file
    writer.save()
    writer.close()
    team_ovr_df_years.loc[
        team_ovr_df_years['Team Name'] == 'Washington Football', 'Team Name'] = 'Washington Football Team'

    team_ovr_df_years["Team Name"].unique()
    return team_ovr_df_years, player_team_stats_madden_years_1