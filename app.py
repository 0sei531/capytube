import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load CSV data
movies_df = pd.read_csv(os.path.join(current_dir, 'Movie', 'Movies.csv'))
ratings_df = pd.read_csv(os.path.join(current_dir, 'Movie', 'Ratings.csv'))

# Define function to process user ratings
def process_ratings(x):
    if isinstance(x, str):
        return [float(r) for r in x.split(',')]
    elif isinstance(x, float):
        return [x]
    else:
        return []  # or handle other cases as needed

# Process user ratings
ratings_df['user_ratings'] = ratings_df['user_ratings'].apply(process_ratings)
ratings_df['mean_rating'] = ratings_df['user_ratings'].apply(np.mean)

# Combine features for content-based filtering
movies_df['combined_features'] = movies_df['genres'] + ' ' + movies_df['overview']

# Create count matrix from combined features
count_vectorizer = CountVectorizer(stop_words='english')
count_matrix = count_vectorizer.fit_transform(movies_df['combined_features'])

# Compute cosine similarity
cosine_sim = cosine_similarity(count_matrix)

def get_movie_recommendations(movie_id, n=5):
    movie_index = movies_df[movies_df['id'] == movie_id].index[0]
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
    similar_movies = similar_movies[1:n+1]  # Exclude the movie itself and get top n
    recommended_movie_ids = [movies_df.iloc[movie[0]]['id'] for movie in similar_movies]
    return recommended_movie_ids

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    movie_title = request.form.get('movie')
    movie = movies_df[movies_df['title'].str.contains(movie_title, case=False)].iloc[0]
    recommended_movie_ids = get_movie_recommendations(movie['id'])
    recommendations = movies_df[movies_df['id'].isin(recommended_movie_ids)]
    recommendations = recommendations.merge(ratings_df[['id', 'mean_rating']], on='id', how='left')
    return render_template('result.html', prediction=recommendations)

@app.route('/svd', methods=['GET', 'POST'])
def svd():
    if request.method == 'POST':
        # Since we don't have user-specific data, we'll return top-rated movies instead
        top_movies = ratings_df.sort_values('mean_rating', ascending=False).head(10)
        recommendations = movies_df[movies_df['id'].isin(top_movies['id'])]
        recommendations = recommendations.merge(top_movies[['id', 'mean_rating']], on='id', how='left')
        return render_template('resultSvd.html', prediction=recommendations)
    return render_template('svd.html')

@app.route('/svdIndex')
def svdIndex():
    return render_template('svd.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

