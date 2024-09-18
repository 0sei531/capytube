 # Movie Recommendation System

A movie recommendation system built with Flask that leverages a third-party API to fetch movie data and provides personalized movie recommendations using collaborative filtering techniques.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Tech Stack](#tech-stack)
5. [Installation](#installation)
6. [API Integration](#api-integration)
7. [Usage](#usage)
8. [Recommendation Techniques](#recommendation-techniques)
9. [Future Enhancements](#future-enhancements)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

This Movie Recommendation System uses data from a third-party movie API (The Movie Database) to recommend movies to users based on collaborative filtering techniques such as k-Nearest Neighbors (kNN) and Singular Value Decomposition (SVD).

## Features

* Fetches movie data from The Movie Database API
* Stores movie data in a CSV file for efficient access
* Provides top-rated movie recommendations
* Offers personalized recommendations based on user preferences using kNN and SVD algorithms
* Simple and intuitive user interface

## Project Structure

capytube/
├── app.py
├── debug_api.py
├── Movie/
│   ├── Debug/
│   ├── Debug.CSV_files.py
│   ├── Movies.csv
│   ├── Ratings.csv
│   ├── Users.csv
│   └── scripts/
├── static/
│   ├── css/
│   ├── datatables/
│   ├── externalCss/
│   └── fontawesome-free/
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── resultSvd.html
│   └── svd.html
└── README.md

## Tech Stack

* **Backend**: Flask
* **Frontend**: HTML, CSS, Bootstrap
* **Data Processing**: Pandas, NumPy, SciPy, Scikit-learn
* **API**: The Movie Database API

## Installation

### Prerequisites

* Python 3.x
* Flask
* Pip (Python package installer)

### Steps

1. Clone the repository:
git clone https://github.com/0sei531/capytube.git


2. Navigate to the project directory:


3. Install the required dependencies:


4. Set up the API keys and environment variables:
- Create a `.env` file in the root directory
- Add your The Movie Database API key and any other necessary configuration

5. Run the application:


6. Open your browser and navigate to `http://127.0.0.1:5000/` to access the application.

## API Integration

This project uses The Movie Database API to fetch movie data. The `debug_api.py` file is used for API debugging purposes. Ensure you have the correct API keys and endpoints configured in your `.env` file.

## Usage

1. **Home Page**: Search for movies using the search bar.
2. **Top-rated Movies**: Get recommendations for top-rated movies.
3. **Personalized Recommendations**: Enter your preferences and get personalized recommendations based on collaborative filtering techniques.

## Recommendation Techniques

This system uses two main collaborative filtering techniques:

1. **k-Nearest Neighbors (kNN)**: Recommends movies based on the similarity of user preferences.
2. **Singular Value Decomposition (SVD)**: Decomposes the user-item interaction matrix to provide recommendations based on latent factors.

[More details about the implementation of these techniques can be added here.]

## Future Enhancements

- Add more advanced recommendation techniques like matrix factorization
- Implement a user login and history tracking system
- Integrate more movie metadata (e.g., genres, directors) for better recommendations
- Improve the UI/UX design for better user engagement

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Commit your changes and submit a pull request

