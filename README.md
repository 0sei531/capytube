# Movie Recommendation System

A movie recommendation system built with Flask that leverages a third-party API to fetch movie data and provides personalized movie recommendations using collaborative filtering techniques.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [API Integration](#api-integration)
- [Usage](#usage)
- [Recommendation Techniques](#recommendation-techniques)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This Movie Recommendation System uses data from a third-party movie API to recommend movies to users based on collaborative filtering techniques such as k-Nearest Neighbors (kNN) and Singular Value Decomposition (SVD).

## Features
- Fetches movie data from a third-party API.
- Provides top-rated movie recommendations.
- Offers personalized recommendations based on user preferences using kNN and SVD algorithms.
- Simple and intuitive user interface.

## Tech Stack
- **Backend:** Flask
- **Frontend:** HTML, CSS, Bootstrap (optional)
- **Data Processing:** Pandas, NumPy, Scipy, Scikit-learn
- **API:** Movies-Verse API (or any other movie API)

## Installation

### Prerequisites
- Python 3.x
- Flask
- Pip (Python package installer)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/movie-recommendation-system.git
    ```
2. Navigate to the project directory:
    ```bash
    cd movie-recommendation-system
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the API keys and environment variables:
    - Create a `.env` file in the root directory.
    - Add your API key, host, and endpoint to the file:
      ```
      API_KEY=your_api_key_here
      API_HOST=your_api_host_here
      API_ENDPOINT=your_api_endpoint_here
      ```
5. Run the application:
    ```bash
    python app.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:5000/` to access the application.

## API Integration
This project uses the Movies-Verse API to fetch movie data such as upcoming movies, top-rated movies, and movie genres. Ensure you have the correct API keys and endpoints configured.

### Example API Request
```python
import requests

api_key = "your_api_key_here"
api_host = "your_api_host_here"
endpoint = "your_api_endpoint_here"

url = "https://Movies-Verse.proxy-production.allthingsdev.co/api/movies/top-250-movies"

headers = {
    "x-apihub-key": api_key,
    "x-apihub-host": api_host,
    "x-apihub-endpoint": endpoint
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Success!")
    movies = response.json()
    print(movies)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
