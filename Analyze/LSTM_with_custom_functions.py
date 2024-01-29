from tensorflow.keras.layers import LSTM, Dense, Dropout, Masking
from keras.regularizers import l2
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.losses import binary_crossentropy
import scipy.stats as stats


def prepare_lstm_data(data_for_lstm, number_of_features, max_weeks):
    sequences = []
    scores = []

    for team in data_for_lstm['id'].unique():
        team_data = data_for_lstm[data_for_lstm['id'] == team]
        for year in team_data['Year'].unique():
            year_data = team_data[team_data['Year'] == year]
            year_sequence = []
            year_scores = []  # Initialize an array for scores for each week
            for week in range(1, max_weeks + 1):
                week_data = year_data[year_data['week_number'] == week]
                if week_data.empty:
                    week_features = np.zeros(number_of_features)
                    year_scores.append(0)  # Append 0 or a placeholder for the score
                else:
                    aggregated_week_data = week_data.mean().drop(
                        ['id', 'Year', 'week_number', 'Score Difference binary'])
                    week_features = aggregated_week_data.values
                    if len(week_features) != number_of_features:
                        week_features = np.pad(week_features, (0, number_of_features - len(week_features)), 'constant')
                    year_scores.append(week_data['Score Difference binary'].values[0])  # Append score for the week
                year_sequence.append(week_features)

            sequences.append(year_sequence)
            scores.append(year_scores)  # Append the scores for the year

    # Pad sequences to the same length
    padded_sequences = pad_sequences(sequences, maxlen=max_weeks, padding='post', dtype='float32')
    return padded_sequences, scores


def prepare_lstm_data(data_for_lstm, number_of_features, max_weeks):
    sequences = []
    scores = []

    for team in data_for_lstm['id'].unique():
        team_data = data_for_lstm[data_for_lstm['id'] == team]
        for year in team_data['Year'].unique():
            year_data = team_data[team_data['Year'] == year]
            year_sequence = []
            year_scores = []  # Initialize an array for scores for each week

            for week in range(1, max_weeks + 1):
                week_data = year_data[year_data['week_number'] == week]
                if week_data.empty:
                    week_features = np.full(number_of_features, -1)  # Use -1 for feature padding
                    year_scores.append(-1)  # Append -1 for the score if data is missing
                else:
                    aggregated_week_data = week_data.mean().drop(
                        ['id', 'Year', 'week_number', 'Score Difference binary'])
                    week_features = aggregated_week_data.values
                    if len(week_features) != number_of_features:
                        week_features = np.pad(week_features, (0, number_of_features - len(week_features)), 'constant',
                                               constant_values=(-1, -1))
                    year_scores.append(week_data['Score Difference binary'].values[0])  # Append score for the week
                year_sequence.append(week_features)

            sequences.append(year_sequence)
            scores.append(year_scores)  # Append the scores for the year

    # Pad sequences to the same length with -1
    padded_sequences = pad_sequences(sequences, maxlen=max_weeks, padding='post', value=-1, dtype='float32')

    # Pad scores to the same length with -1
    padded_scores = pad_sequences(scores, maxlen=max_weeks, padding='post', value=-1, dtype='float32')

    return padded_sequences, padded_scores


# Load and preprocess data
# Replace 'your_data.csv' with your actual data file
data = pd.read_excel('C:\\Users\\Administrator\\Desktop\\NFL Project\\data_for_NN_3.xlsx')
team_names_table_merger = team_names_table[['city', 'id']]
data_for_lstm = data.merge(team_names_table_merger, left_on='Favorite_city', right_on='city')
data_for_lstm = data_for_lstm.merge(team_names_table_merger, left_on='Underdog_city', right_on='city')
data_for_lstm_favorite = data_for_lstm[['Day', 'Time (ET)', 'home_1', 'conference_Favorite',
                                        'division_Favorite', 'conference_Underdog', 'division_Underdog',
                                        'Favorite', 'Spread', 'home_2', 'Underdog', 'Over/Under', 'week_number',
                                        'Year', 'European game', 'Favorite_city', 'Favorite_team',
                                        'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite',
                                        'win_Underdog', 'loss_Underdog', 'worth_Favorite', 'size_Favorite',
                                        'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog',
                                        'new_coach_Favorite', 'new_year_coach_Favorite', 'new_coach_Underdog',
                                        'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog',
                                        'starting_qb_Favorite', 'starting_qb_Underdog', 'Overall_qb_Favorite',
                                        'Overall_qb_Underdog', 'Score Difference binary',
                                        'count_stars_Underdog', 'stars_""_Underdog', 'stars_"Q"_Underdog',
                                        'stars_"O"_Underdog', 'count_stars_Favorite', 'stars_""_Favorite',
                                        'stars_"Q"_Favorite', 'stars_"O"_Favorite', 'count_superstars_Underdog',
                                        'superstars_""_Underdog', 'superstars_"Q"_Underdog',
                                        'superstars_"O"_Underdog', 'count_superstars_Favorite',
                                        'superstars_""_Favorite', 'superstars_"Q"_Favorite',
                                        'superstars_"O"_Favorite', 'id_x']]

data_for_lstm_underdog = data_for_lstm[['Day', 'Time (ET)', 'home_1', 'conference_Favorite',
                                        'division_Favorite', 'conference_Underdog', 'division_Underdog',
                                        'Favorite', 'Spread', 'home_2', 'Underdog', 'Over/Under', 'week_number',
                                        'Year', 'European game', 'Favorite_city', 'Favorite_team',
                                        'Underdog_city', 'Underdog_team', 'win_Favorite', 'loss_Favorite',
                                        'win_Underdog', 'loss_Underdog', 'worth_Favorite', 'size_Favorite',
                                        'cold_Favorite', 'worth_Underdog', 'size_Underdog', 'cold_Underdog',
                                        'new_coach_Favorite', 'new_year_coach_Favorite', 'new_coach_Underdog',
                                        'new_year_coach_Underdog', 'Rating_Favorite', 'Rating_Underdog',
                                        'starting_qb_Favorite', 'starting_qb_Underdog', 'Overall_qb_Favorite',
                                        'Overall_qb_Underdog', 'Score Difference binary',
                                        'count_stars_Underdog', 'stars_""_Underdog', 'stars_"Q"_Underdog',
                                        'stars_"O"_Underdog', 'count_stars_Favorite', 'stars_""_Favorite',
                                        'stars_"Q"_Favorite', 'stars_"O"_Favorite', 'count_superstars_Underdog',
                                        'superstars_""_Underdog', 'superstars_"Q"_Underdog',
                                        'superstars_"O"_Underdog', 'count_superstars_Favorite',
                                        'superstars_""_Favorite', 'superstars_"Q"_Favorite',
                                        'superstars_"O"_Favorite', 'id_y']]

data_for_lstm_favorite.rename(columns={
    'id_x': 'id'}, inplace=True)
data_for_lstm_underdog.rename(columns={
    'id_y': 'id'}, inplace=True)

data_for_lstm = data_for_lstm_favorite.append(data_for_lstm_underdog)
data_for_lstm = data_for_lstm[~data_for_lstm.apply(lambda row: row.astype(str).str.contains('favorite').any(), axis=1)]
number_of_features = 54
max_weeks = 17

data_for_lstm = convert_table_to_nn(data_for_lstm)
data_for_lstm = data_for_lstm.drop_duplicates()

# Preparing the sequence data
# This is a simplified example; you'll need to adjust it to handle multiple teams and multiple metrics
train_data = data_for_lstm[data_for_lstm['Year'] < 2022]
test_data = data_for_lstm[data_for_lstm['Year'] >= 2022]
train_data, train_scores = prepare_lstm_data(train_data, number_of_features, max_weeks)
test_data, test_scores = prepare_lstm_data(test_data, number_of_features, max_weeks)
# Reshape for LSTM input
X_train = np.array(train_data)
X_train = X_train.reshape(X_train.shape[0], max_weeks, number_of_features)

# Prepare target variable y
y_train = pad_sequences(train_scores, maxlen=max_weeks, padding='post', dtype='float32',
                        value=-1)  # Pad the scores to ensure they have the same length
# Prepare target variable y
y_train = np.array(y_train)

X_test = np.array(test_data)
X_test = X_test.reshape(X_test.shape[0], max_weeks, number_of_features)

# Prepare target variable y
y_test = pad_sequences(test_scores, maxlen=max_weeks, padding='post', dtype='float32',
                       value=-1)  # Pad the scores to ensure they have the same length
# Prepare target variable y
y_test = np.array(y_test)

# Redefine the model for binary classification based on selected features
model = Sequential()

model.add(Masking(mask_value=-1, input_shape=(max_weeks, number_of_features)))

model.add(LSTM(159, activation='swish', return_sequences=True, input_shape=(17, number_of_features),
               ))
model.add(Dropout(0.1))
model.add(LSTM(53, activation='swish'))
model.add(Dropout(0.1))

model.add(Dense(17, activation='sigmoid'))

model.compile(optimizer='adam', loss=custom_loss, metrics=['binary_accuracy'])
model.compile(optimizer='adam', loss=custom_loss, metrics=[custom_binary_accuracy])
history = model.fit(X_train, y_train, epochs=30, batch_size=1)

# After training your model, you can evaluate it on the test data

# Calculate accuracy without considering any padded results
# Predict on test data
y_pred = model.predict(X_test)
# Convert predictions to binary (0 or 1)
y_pred_binary = (y_pred > 0.5).astype(int)

# Initialize variables for accuracy calculation
total_correct_predictions = 0
total_predictions = 0

# Iterate over each sequence
for i in range(y_test.shape[0]):
    # Identify indices that are not padded
    non_padded_indices = np.where(y_test[i] != -1)[0]

    if len(non_padded_indices) > 0:
        # Select only non-padded values for both true and predicted
        true_values = y_test[i, non_padded_indices]
        predicted_values = y_pred_binary[i, non_padded_indices]

        # Calculate correct predictions and total predictions
        total_correct_predictions += np.sum(true_values == predicted_values)
        total_predictions += len(non_padded_indices)

# Calculate accuracy
custom_accuracy = total_correct_predictions / total_predictions if total_predictions != 0 else 0
print(f'Custom Accuracy (excluding padded data): {custom_accuracy:.4f}')

observed_accuracy = custom_accuracy  # Observed accuracy
expected_accuracy = 0.5  # Expected accuracy by random chance
n_trials = total_predictions  # Number of trials

# Calculate the test statistic
test_statistic = (observed_accuracy - expected_accuracy) / (
            (expected_accuracy * (1 - expected_accuracy)) / n_trials) ** 0.5

# Calculate the p-value for a one-tailed test
p_value = 1 - stats.norm.cdf(test_statistic)

test_statistic, p_value
