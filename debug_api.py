import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_movie_data(endpoint="/movie/top_rated"):
    api_key = os.getenv('API_KEY')
    api_read_access_token = os.getenv('API_READ_ACCESS_TOKEN')
    api_base_url = os.getenv('API_BASE_URL')

    if not all([api_key, api_read_access_token, api_base_url]):
        logger.error("Missing required environment variables")
        return None

    url = f"{api_base_url}{endpoint}"
    headers = {
        'Authorization': f'Bearer {api_read_access_token}',
        'accept': 'application/json'
    }
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'page': 1
    }

    try:
        logger.info(f"Sending request to: {url}")
        logger.info(f"With headers: {headers}")
        logger.info(f"With params: {params}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        logger.error(f"Response content: {response.content}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
    return None

# Run the debug code
if __name__ == "__main__":
    data = fetch_movie_data()
    if data:
        logger.info("Data fetched successfully")
        logger.info(f"Number of results: {len(data.get('results', []))}")
        if data.get('results'):
            logger.info(f"First movie title: {data['results'][0]['title']}")
    else:
        logger.error("Failed to fetch data")
