from sklearn.ensemble import RandomForestClassifier  # or RandomForestRegressor for regression problems
import numpy as np
import matplotlib.pyplot as plt
def feature_analysis_randomforest(data_for_nn):
    X = data_for_nn.drop('Score Difference binary',
                                 axis=1)  # Replace 'target' with the name of your outcome column
    y = data_for_nn[['Score Difference binary']]


    model = RandomForestClassifier()
    model.fit(X, y)

    # Get feature importances
    importances = model.feature_importances_

    # Sort the feature importances in descending order
    sorted_indices = np.argsort(importances)[::-1]

    # Visualize the feature importances
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.bar(range(X.shape[1]), importances[sorted_indices], align="center")
    plt.xticks(range(X.shape[1]), X.columns[sorted_indices], rotation=90)
    plt.xlabel("Feature")
    plt.ylabel("Importance")
    plt.show()
    return sorted_indices