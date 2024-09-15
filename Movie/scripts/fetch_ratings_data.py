import requests
import csv
import time

API_KEY = '5ebf5fe9668a3b7ad12544c31caf576c'
BASE_URL = 'https://api.themoviedb.org/3'

def get_popular_movies(page=1):
    endpoint = f'{BASE_URL}/movie/popular'
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': page
    }
    response = requests.get(endpoint, params=params)
    return response.json()

def get_movie_details(movie_id):
    endpoint = f'{BASE_URL}/movie/{movie_id}'
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'append_to_response': 'credits,reviews'
    }
    response = requests.get(endpoint, params=params)
    return response.json()

def get_movie_ratings(movie_id, page=1):
    endpoint = f'{BASE_URL}/movie/{movie_id}/reviews'
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': page
    }
    response = requests.get(endpoint, params=params)
    return response.json()

def fetch_and_save_movies_with_ratings(num_pages=5):
    with open('movies_with_ratings.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'overview', 'vote_average', 'genres', 'release_date', 'user_ratings'])

        for page in range(1, num_pages + 1):
            popular_movies = get_popular_movies(page)
            for movie in popular_movies['results']:
                movie_details = get_movie_details(movie['id'])
                genres = ', '.join([genre['name'] for genre in movie_details['genres']])
                
                # Fetch ratings
                ratings = get_movie_ratings(movie['id'])
                user_ratings = [review['author_details']['rating'] for review in ratings['results'] if review['author_details']['rating'] is not None]
                user_ratings_str = ', '.join(map(str, user_ratings))

                writer.writerow([
                    movie_details['id'],
                    movie_details['title'],
                    movie_details['overview'],
                    movie_details['vote_average'],
                    genres,
                    movie_details['release_date'],
                    user_ratings_str
                ])
            print(f"Processed page {page}")
            time.sleep(1)  # To avoid hitting rate limits

fetch_and_save_movies_with_ratings()
print("Data saved to movies_with_ratings.csv")
