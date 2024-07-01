import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def merge_dataframes(df_a, df_b, date_column):
    # Convert the date column in df_b to match the format in df_a
    df_b[date_column] = pd.to_datetime(df_b[date_column], format='%m/%d/%y').dt.strftime('%Y-%m-%d')
    
    # Merge df_b into df_a based on the date column
    df_merged = pd.merge(df_a, df_b, on=date_column, how='left')
    
    # Drop the specified columns from the merged dataframe
    columns_to_drop = [date_column, 'Data Quality']
    df_merged.drop(columns_to_drop, axis=1, inplace=True)
    
    return df_merged


def convert_day_to_numeric(df, column):
    day_mapping = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    df[column] = df[column].map(day_mapping)
    return df


def split_data(df, target_column, test_size=0.35, random_state=42):
    # Split the data into features (X) and target variable (y)
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, shuffle=True)
    
    return X_train, X_test, y_train, y_test


def train_random_forest(X_train, y_train, X_test, random_state=45, min_samples_split=3):
    # Create a decision tree classifier
    clf = RandomForestClassifier(
        random_state=random_state,
        min_samples_split=min_samples_split
    )
    
    # Train the classifier
    clf.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = clf.predict(X_test)
    
    return clf, y_pred


def evaluate_model(y_test, y_pred):
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("Accuracy:", round(accuracy, 2))
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    
    return accuracy, precision, recall, f1