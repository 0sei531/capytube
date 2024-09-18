import pandas as pd
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load CSV data
movies_df = pd.read_csv(os.path.join(current_dir, 'Movies.csv'))
ratings_df = pd.read_csv(os.path.join(current_dir, 'Ratings.csv'))

print("Movies DataFrame Columns:")
print(movies_df.columns)
print("\nRatings DataFrame Columns:")
print(ratings_df.columns)

print("\nFirst few rows of Movies DataFrame:")
print(movies_df.head())
print("\nFirst few rows of Ratings DataFrame:")
print(ratings_df.head())
