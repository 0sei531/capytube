import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
API_READ_ACCESS_TOKEN = os.getenv('API_READ_ACCESS_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.themoviedb.org/3')

def fetch_tmdb_data(endpoint, params=None):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        'Authorization': f'Bearer {API_READ_ACCESS_TOKEN}',
        'accept': 'application/json'
    }
    default_params = {'api_key': API_KEY, 'language': 'en-US'}
    if params:
        default_params.update(params)
    
    response = requests.get(url, headers=headers, params=default_params)
    response.raise_for_status()
    return response.json()

@app.route('/')
def home():
    # Fetch top-rated movies
    data = fetch_tmdb_data('/movie/top_rated', {'page': 1})
    movies = data.get('results', [])
    return render_template('index.html', movies=movies)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    if query:
        data = fetch_tmdb_data('/search/movie', {'query': query, 'page': 1})
        movies = data.get('results', [])
    else:
        movies = []
    return render_template('result.html', movies=movies, query=query)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie_data = fetch_tmdb_data(f'/movie/{movie_id}')
    recommendations = fetch_tmdb_data(f'/movie/{movie_id}/recommendations')['results']
    return render_template('resultSvd.html', movie=movie_data, recommendations=recommendations)

@app.route('/svd')
def svd():
    # This route might be for your SVD-based recommendations
    # You'll need to implement the SVD logic here
    return render_template('svd.html')

@app.errorhandler(requests.exceptions.RequestException)
def handle_api_error(error):
    return jsonify(error=str(error)), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Updated to run on all interfaces
