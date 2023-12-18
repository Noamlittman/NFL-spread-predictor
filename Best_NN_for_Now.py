import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


def time_decay_weight(row, current_year, current_week, max_weight=10):
    # Calculate the total number of weeks from the row year/week to the current year/week
    year_difference = current_year - row['Year']
    week_difference = current_week - row['week_number']
    total_weeks_passed = year_difference * 18 + week_difference

    # Calculate the maximum number of weeks possible
    max_weeks = (current_year - df['Year'].min()) * 18 + current_week

    # Normalize weeks passed to a scale of 0 to 1
    normalized_time = total_weeks_passed / max_weeks

    # Apply an exponential decay to emphasize recent observations more
    decay_factor = 0.682  # Adjust this value to change the decay rate
    # weight = 1 + (max_weight - 1) * (1 - (normalized_time ** decay_factor))
    weight = 1 + (max_weight - 1) * ((1 - normalized_time) ** 2)
    return weight


# data = pd.read_csv('historical_games.csv')
for v in range(0, 100, 1):
    X_train = pd.DataFrame()
    y_train = pd.Series()
    current_week_games = df[df['Year'] < 2022]
    current_week_games = current_week_games.astype('float32')
    weekly_targets = current_week_games['Score Difference binary']
    # Split your data into features (X) and target (y)
    X = current_week_games.drop('Score Difference binary',
                                axis=1)  # Replace 'target' with the name of your outcome column
    y = weekly_targets

    # Split the historical data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    X_train = X_train.astype('float32')
    y_train = y_train.astype('float32')



    # Example usage
    current_year = X['Year'].max()
    current_week = X['week_number'].max()  # Assuming you have the current week information

    # Apply the time decay weight to each row in the DataFrame
    weights = X.apply(lambda row: time_decay_weight(row, current_year, current_week), axis=1)
    # Build the initial model
    model = Sequential([
        Dense(64, activation='relu', input_dim=X_train.shape[1], kernel_regularizer=l2(0.0002)),
        BatchNormalization(),

        #    Dropout(0.4),
        Dense(1, activation='sigmoid')
    ])

    # Create and compile the model
    model.compile(optimizer=Adam(learning_rate=0.0005), loss='binary_crossentropy', metrics=['accuracy'],
                  weighted_metrics=['accuracy'])

    # Retrain or fine-tune the model with the updated data
    # model.fit([X_train_A, X_train_B, X_train_C], y_train, epochs=16, batch_size=64)
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6)

    early_stopping = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
    model.fit(X_train, y_train, sample_weight=weights.values, epochs=200, batch_size=16, validation_split=0.1,
              callbacks=[early_stopping])

    y_train = pd.Series()
    X_train = pd.DataFrame(columns=X_train.columns)

    predictions_df = pd.DataFrame(columns=['Predictions', 'Score Difference binary'])

    # Weekly loop
    for year in range(2022, df['Year'].max() + 1, 1):
        for week in range(df[df['Year'] == year]['week_number'].min(), df[df['Year'] == year]['week_number'].max() + 1,
                          1):
            current_week_games = df[(df['Year'] == year) & (df['week_number'] == week)]
            current_week_games = current_week_games.astype('float32')
            weekly_features = current_week_games.drop('Score Difference binary', axis=1)
            weekly_targets = current_week_games['Score Difference binary']
            predictions = model.predict(weekly_features)
            if year > 2022:
                predictions = model.predict([weekly_features])
                predictions_series = pd.Series(predictions.flatten(), name='Predictions')

                # Reset index on weekly_targets if needed
                weekly_targets_reset = weekly_targets.reset_index(drop=True)

                # Concatenate predictions and targets into a new DataFrame
                prediction_df = pd.concat([predictions_series, weekly_targets_reset], axis=1)
                predictions_df = predictions_df.append(prediction_df)

                # Reset index on weekly_targets if needed
                weekly_targets_reset = weekly_targets.reset_index(drop=True)

                # Concatenate predictions and targets into a new DataFrame
                prediction_df = pd.concat([predictions_series, weekly_targets_reset], axis=1)
                predictions_df = predictions_df.append(prediction_df)
            # Update the training dataset with the new week's data

            # Assume you have current_year and current_week variables representing the current year and week

            # Update the training dataset with the new week's data
            X_train = pd.concat([X_train, weekly_features])
            y_train = pd.concat([y_train, weekly_targets])
            # current_week_games = ... load the current week's games
            current_year = X_train['Year'].max()
            current_week = week  # Replace with the actual current week number

            # Apply the time decay weight to each row in the DataFrame
            weights = X_train.apply(lambda row: time_decay_weight(row, current_year, current_week), axis=1)

            X_train = X_train.astype('float32')
            y_train = y_train.astype('float32')
            # Retrain or fine-tune the model with updated data
            model.fit(X_train, y_train, sample_weight=weights.values, epochs=200, batch_size=16, validation_split=0.1,
                      callbacks=[early_stopping])

    predictions_df = predictions_df[['Predictions', 'Score Difference binary']]
    # Assuming 'predictions' is a numpy array with your model's output
    predictions_df['Confidence'] = predictions_df['Predictions'].apply(lambda x: abs(x - 0.5))

    predictions_df['Prediction'] = (predictions_df['Predictions'] > 0.5).astype(int)

    # Define confidence bins
    # confidence_bins = [0,  0.03, 0.06, 0.09, 0.12,0.15,0.18,0.21,0.24,0.27,0.30,0.33,0.36,0.39]
    confidence_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

    predictions_df['Confidence_Bin'] = pd.cut(predictions_df['Confidence'], bins=confidence_bins)

    # Calculate accuracy within each bin
    accuracy_per_bin = predictions_df.groupby('Confidence_Bin').apply(
        lambda x: (x['Prediction'] == x['Score Difference binary']).mean())
    bin_counts = predictions_df['Confidence_Bin'].value_counts()

    # Sort the counts based on the bin order
    bin_counts = bin_counts.reindex(confidence_bins, fill_value=0)

    # Display the counts
    print(bin_counts)
    file_tests_name = file_path + "\\tests_pro_1.xlsx"
    writer = pd.ExcelWriter(file_tests_name, engine='xlsxwriter')
    predictions_df["accuracy"] = 1 - abs(predictions_df['Prediction'] - predictions_df['Score Difference binary'])

    print(predictions_df["accuracy"].mean())

    # Write the DataFrame to the Excel file
    predictions_df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel file
    writer.save()
    writer.close()

    import matplotlib.pyplot as plt

    # Calculate accuracy within each bin
    accuracy_per_bin = predictions_df.groupby('Confidence_Bin').apply(
        lambda x: (x['Prediction'] == x['Score Difference binary']).mean())

    accuracy_per_bin.plot(kind='bar')
    plt.xlabel('Confidence Level')
    plt.ylabel('Accuracy')
    plt.title('Model Accuracy at Different Confidence Levels')
    plt.show()

    # Reset the index to ensure it's unique
    predictions_df = predictions_df.reset_index(drop=True)

    # Ensure 'predictions_df' has the 'Row_Accuracy' column calculated as before
    # predictions_df['Row_Accuracy'] = (predictions_df['Prediction'] == predictions_df['Score Difference binary']).astype(int)

    # Initialize a list to hold the cumulative accuracies
    cumulative_accuracies = []

    # Calculate cumulative accuracy from each row to the end
    for i in range(len(predictions_df)):
        mean_accuracy = predictions_df['accuracy'].iloc[i:].mean()
        cumulative_accuracies.append(mean_accuracy)

    # Now, plot this list against the new index
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(cumulative_accuracies)), cumulative_accuracies, label='Mean Accuracy from Row to End')
    plt.xlabel('Row Number')
    plt.ylabel('Mean Accuracy')
    plt.title('Model Mean Accuracy from Row to End Over Time')
    plt.legend()
    plt.show()

    bin_counts_df = bin_counts.reset_index()
    bin_counts_df.columns = ['Confidence_Bin', 'Count']

    # Reset index of accuracy_per_bin for merging
    accuracy_per_bin_df = accuracy_per_bin.reset_index()
    accuracy_per_bin_df.columns = ['Confidence_Bin', 'Accuracy']

    # Merge the two DataFrames on Confidence_Bin
    combined_df = pd.merge(bin_counts_df, accuracy_per_bin_df, on='Confidence_Bin')
    combined_df['accuracy_total'] = predictions_df["accuracy"].mean()
    if v == 0:
        combined_df_dd = combined_df
    # Now, combined_df contains both count and accuracy for each bin
    else:
        combined_df_dd = combined_df_dd.append(combined_df)
    # Now, plot this list against the new index
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(combined_df_dd)), combined_df_dd['accuracy_total'], label='Mean Accuracy from Row to End')
    plt.xlabel('Row Number')
    plt.ylabel('Mean Accuracy')
    plt.title('Model Mean Accuracy from Row to End Over Time')
    plt.legend()
    plt.show()
