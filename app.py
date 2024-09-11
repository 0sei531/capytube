from flask import Flask, render_template, request
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Updated template name

@app.route('/svdIndex')
def svdIndex():
    return render_template('svd.html')  # Updated template name

class Movies:
    def __init__(self):
        self.movies = pd.read_csv('./Movie/Movies.csv')  # Changed path and name
        self.users = pd.read_csv('./Movie/Users.csv')    # Changed path and name
        self.ratings = pd.read_csv('./Movie/Ratings.csv')  # Changed path and name

        # Splitting Explicit and Implicit user ratings
        self.ratings_explicit = self.ratings[self.ratings.rating != 0]
        self.ratings_implicit = self.ratings[self.ratings.rating == 0]

        # Each Movie Mean ratings and Total Rating Count
        self.average_rating = pd.DataFrame(
            self.ratings_explicit.groupby('movieId')['rating'].mean())
        self.average_rating['ratingCount'] = pd.DataFrame(
            self.ratings_explicit.groupby('movieId')['rating'].count())
        self.average_rating = self.average_rating.rename(
            columns={'rating': 'MeanRating'})

        # To get a stronger similarity
        counts1 = self.ratings_explicit['userId'].value_counts()
        self.ratings_explicit = self.ratings_explicit[
            self.ratings_explicit['userId'].isin(counts1[counts1 >= 50].index)]

        # Explicit Movies and movieId
        self.explicit_movieId = self.ratings_explicit.movieId.unique()
        self.explicit_movies = self.movies.loc[self.movies['movieId'].isin(
            self.explicit_movieId)]

        # Look up dict for Movie and MovieID
        self.Movie_lookup = dict(
            zip(self.explicit_movies["movieId"], self.explicit_movies["title"]))
        self.ID_lookup = dict(
            zip(self.explicit_movies["title"], self.explicit_movies["movieId"]))

    def Top_Movies(self, n=10, RatingCount=100, MeanRating=3):
        MOVIES = self.movies.merge(self.average_rating, how='right', on='movieId')
        M_Rating = MOVIES.loc[MOVIES.ratingCount >= RatingCount].sort_values(
            'MeanRating', ascending=False).head(n)

        H_Rating = MOVIES.loc[MOVIES.MeanRating >= MeanRating].sort_values(
            'ratingCount', ascending=False).head(n)

        return M_Rating, H_Rating

class KNN(Movies):

    def __init__(self, n_neighbors=5):
        super().__init__()
        self.n_neighbors = n_neighbors
        self.ratings_mat = self.ratings_explicit.pivot(
            index="movieId", columns="userId", values="rating").fillna(0)
        self.uti_mat = csr_matrix(self.ratings_mat.values)
        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model_knn.fit(self.uti_mat)

    def Recommend_Movies(self, movie, n_neighbors=5):
        mID = self.ID_lookup[movie]
        query_index = self.ratings_mat.index.get_loc(mID)
        KN = self.ratings_mat.iloc[query_index, :].values.reshape(1, -1)
        distances, indices = self.model_knn.kneighbors(
            KN, n_neighbors=n_neighbors + 1)

        Rec_movies = list()
        Movie_dis = list()

        for i in range(1, len(distances.flatten())):
            Rec_movies.append(self.ratings_mat.index[indices.flatten()[i]])
            Movie_dis.append(distances.flatten()[i])

        Movie = self.Movie_lookup[mID]
        Recommended_Movies = self.movies[self.movies['movieId'].isin(Rec_movies)]

        return Movie, Recommended_Movies, Movie_dis

class SVD(Movies):

    def __init__(self, n_latent_factor=50):
        super().__init__()
        self.n_latent_factor = n_latent_factor
        self.ratings_mat = self.ratings_explicit.pivot(
            index="userId", columns="movieId", values="rating").fillna(0)
        self.uti_mat = self.ratings_mat.values
        self.user_ratings_mean = np.mean(self.uti_mat, axis=1)
        self.mat = self.uti_mat - self.user_ratings_mean.reshape(-1, 1)

        self.explicit_users = np.sort(self.ratings_explicit.userId.unique())
        self.User_lookup = dict(
            zip(range(1, len(self.explicit_users)), self.explicit_users))

        self.predictions = None

    def scipy_SVD(self):
        U, S, Vt = svds(self.mat, k=self.n_latent_factor)
        S_diag_matrix = np.diag(S)
        X_pred = np.dot(np.dot(U, S_diag_matrix), Vt) + \
                 self.user_ratings_mean.reshape(-1, 1)

        self.predictions = pd.DataFrame(
            X_pred, columns=self.ratings_mat.columns, index=self.ratings_mat.index)

        return

    def Recommend_Movies(self, userId, num_recommendations=5):
        user_row_number = self.User_lookup[userId]
        sorted_user_predictions = self.predictions.loc[user_row_number].sort_values(
            ascending=False)

        user_data = self.ratings_explicit[self.ratings_explicit.userId == (
            self.User_lookup[userId])]
        user_full = (user_data.merge(self.movies, how='left', left_on='movieId', right_on='movieId').sort_values(['rating'], ascending=False))

        recom = (self.movies[~self.movies['movieId'].isin(user_full['movieId'])].merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                       left_on='movieId', right_on='movieId'))
        recom = recom.rename(columns={user_row_number: 'Predictions'})
        recommend = recom.sort_values(by=['Predictions'], ascending=False)
        recommendations = recommend.iloc[:num_recommendations, :-1]

        return user_full, recommendations

@app.route('/predict', methods=['POST'])
def predict():
    global KNN_Recommended_Movies
    if request.method == 'POST':
        ICF = KNN()
        movie = request.form['movie']
        data = movie

        _, KNN_Recommended_Movies, _ = ICF.Recommend_Movies(data)

        KNN_Recommended_Movies = KNN_Recommended_Movies.merge(
            ICF.average_rating, how='left', on='movieId')
        KNN_Recommended_Movies = KNN_Recommended_Movies.rename(
            columns={'rating': 'MeanRating'})

        df = pd.DataFrame(KNN_Recommended_Movies, columns=['title', 'genres', 'MeanRating'])

    return render_template('result.html', predictionT=KNN_Recommended_Movies[['title']],
                           predictionG=KNN_Recommended_Movies[['genres']],
                           predictionR=KNN_Recommended_Movies[['MeanRating']],
                           prediction=df)

@app.route('/svd', methods=['POST'])
def svd():
    global SVD_Recommended_Movies
    if request.method == 'POST':
        userCollaborativeFiltering = SVD()
        userCollaborativeFiltering.scipy_SVD()
        userId = request.form['svd']
        data = int(userId)

        Rated_Movies, SVD_Recommended_Movies = userCollaborativeFiltering.Recommend_Movies(
            userId=data)

        pd.set_option('display.max_colwidth', -1)

        SVD_Recommended_Movies = SVD_Recommended_Movies.merge(
            userCollaborativeFiltering.average_rating, how='left', on='movieId')
        SVD_Recommended_Movies = SVD_Recomended_Movies.rename(
            columns={'rating': 'MeanRating'})

        lst = list(SVD_Recommended_Movies[['title', 'genres', 'genres']])
        print(lst)
        for k in lst:
            print(k)

    return render_template('resultSvd.html', predictionT=SVD_Recommended_Movies[['title']],
                           predictionG=SVD_Recommended_Movies[['genres']],
                           predictionR=SVD_Recommended_Movies[['MeanRating']],
                           prediction=SVD_Recommended_Movies)

if __name__ == '__main__':
    app.run(debug=True)

