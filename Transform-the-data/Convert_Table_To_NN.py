
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def convert_table_for_nn(df):
    print("First few rows of problematic columns:")
    print(df[['win_Underdog', 'loss_Underdog', 'new_year_coach_Favorite']].head())

    print("\nData types of problematic columns:")
    print(df[['win_Underdog', 'loss_Underdog', 'new_year_coach_Favorite']].dtypes)

    # Test conversion for individual columns
    try:
        df['win_Underdog'] = pd.to_numeric(df['win_Underdog'], errors='coerce')
        print("\nConversion successful for 'win_Underdog'")
    except Exception as e:
        print(f"\nError converting 'win_Underdog': {e}")

    try:
        df['loss_Underdog'] = pd.to_numeric(df['loss_Underdog'], errors='coerce')
        print("\nConversion successful for 'loss_Underdog'")
    except Exception as e:
        print(f"\nError converting 'loss_Underdog': {e}")

    try:
        df['new_year_coach_Favorite'] = pd.to_numeric(df['new_year_coach_Favorite'], errors='coerce')
        print("\nConversion successful for 'new_year_coach_Favorite'")
    except Exception as e:
        print(f"\nError converting 'new_year_coach_Favorite': {e}")

    # Assuming df is your DataFrame
    for col in df.columns:
        # Skip the column if it is already numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            continue

        # Convert to numeric, non-numeric values will become NaN
        numeric_col = pd.to_numeric(df[col], errors='coerce')

        if numeric_col.isna().any():
            # Handle non-numeric data
            df[col] = df[col].astype('category')
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
        else:
            # Handle numeric data
            df[col] = numeric_col.astype('int')

    for col in df.columns:
        # Check if the column is non-numeric
        if not pd.api.types.is_numeric_dtype(df[col]):
            try:
                # Convert non-numeric columns to category and then to numerical codes
                df[col] = df[col].astype('category')
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
            except Exception as e:
                print(f"Error processing column {col}: {e}")

    return df
