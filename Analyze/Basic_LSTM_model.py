import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

# Load and preprocess data
# Replace 'your_data.csv' with your actual data file
data = pd.read_excel('C:\\Users\\Administrator\\Desktop\\NFL Project\\data_for_NN_3.xlsx')
team_names_table_merger = team_names_table[['city', 'id']]
data_for_lstm = data.merge(team_names_table_merger, left_on='Favorite_city', right_on='city')
data_for_lstm = data_for_lstm.merge(team_names_table_merger, left_on='Underdog_city', right_on='city')
data_for_lstm_favorite = data_for_lstm[['Day', 'Time (ET)', 'home_1', 'conference_Favorite',
                                        'division_Favorite', 'conference_Underdog', 'division_Underdog',
                                        'Favorite', 'Spread', 'home_2', 'Underdog', 'Over/Under', 'week_number',
                                        'Year', 'OT', 'European game', 'Favorite_city', 'Favorite_team',
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
                                        'Year', 'OT', 'European game', 'Favorite_city', 'Favorite_team',
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

df = data_for_lstm
data_for_lstm = df
data_for_lstm = data_for_lstm.drop_duplicates()
# Preparing the sequence data
# This is a simplified example; you'll need to adjust it to handle multiple teams and multiple metrics

from tensorflow.keras.preprocessing.sequence import pad_sequences

number_of_features = 54
max_weeks = 17

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
                aggregated_week_data = week_data.mean().drop(['id', 'Year', 'week_number', 'Score Difference binary'])
                week_features = aggregated_week_data.values
                if len(week_features) != number_of_features:
                    week_features = np.pad(week_features, (0, number_of_features - len(week_features)), 'constant')
                year_scores.append(week_data['Score Difference binary'].values[0])  # Append score for the week
            year_sequence.append(week_features)

        sequences.append(year_sequence)
        scores.append(year_scores)  # Append the scores for the year

# Pad sequences to the same length
padded_sequences = pad_sequences(sequences, maxlen=max_weeks, padding='post', dtype='float32')

# Reshape for LSTM input
X = np.array(padded_sequences)
X = X.reshape(X.shape[0], max_weeks, number_of_features)

# Prepare target variable y
y = pad_sequences(scores, maxlen=max_weeks, padding='post',
                  dtype='float32')  # Pad the scores to ensure they have the same length
# Prepare target variable y
y = np.array(scores)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Redefine the model with the correct input shape
model = Sequential()
model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(17, number_of_features)))
model.add(Dropout(0.2))
model.add(LSTM(50, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(17, activation='sigmoid'))  # or Dense(units=num_classes, activation='softmax') for classification

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')  # or 'binary_crossentropy' for classification

# Adjust your training data shape accordingly (X_train and y_train)

# Retrain the model
history = model.fit(X, y, epochs=15, batch_size=32, validation_split=0.2)  # Adjust as needed

# Evaluate the model using your test data
test_loss = model.evaluate(X_test, y_test)
print(f'Test Loss: {test_loss}')
# Make predictions
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f'MSE: {mse}, MAE: {mae}')

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Over Epochs')
plt.legend()

# If accuracy metric is available
if 'accuracy' in history.history:
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Accuracy Over Epochs')
    plt.legend()

plt.show()
# Train the model
history = model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)  # Adjust epochs, batch_size as needed
