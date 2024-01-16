def correlation_analysis(data_for_nn):
    correlations = data_for_nn.corr()
    target_correlations = correlations["Score Difference binary"].sort_values(ascending=False)  # Replace 'target_variable' with your actual target variable name

    # Plotting
    plt.figure(figsize=(12, 10))
    sns.barplot(x=target_correlations.values, y=target_correlations.index)
    plt.title("Feature Correlation with Target")
    plt.show()
    return target_correlations