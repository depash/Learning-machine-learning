import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

df = pd.read_csv("hf://datasets/Pablinho/movies-dataset/9000plus.csv")

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['Overview'].fillna(''), convert_to_tensor=True)

cosine_sim = cosine_similarity(embeddings)

def recommend(titles, top_n=5):
    # List of indexes of titles
    idx_list = [df[df['Title'] == title].index[0] for title in titles]
    # List of vectors that are similir
    #               Inception  Matrix   Shrek   Looper   Barbie
    # Inception     1.0      0.91     0.12     0.84     0.02
    # Matrix        0.91     1.0      0.10     0.88     0.01
    # Shrek         0.12     0.10     1.0      0.08     0.03
    # Looper        0.84     0.88     0.08     1.0      0.07
    # Barbie        0.02     0.01     0.03     0.07     1.0

    # [
    #  (0, 1.0),         Inception vs Inception
    #  (1, 0.91),        Inception vs Matrix
    #  (2, 0.12),        Inception vs Shrek
    #  (3, 0.84),        Inception vs Looper
    #  (4, 0.02),        Inception vs Barbie
    # ]
    sim_scores = cosine_sim[idx_list]
    # we get the mean of the similarity scores for each movie
    mean_sim_scores = sim_scores.mean(axis=0)
    # [
    #  (0, 1.00),
    #  (240, 0.87),
    #  (378, 0.51),
    #  (12, 0.45),
    #  ...
    # ]
    # Sort that list in order of similarity scores
    recommended_indices = mean_sim_scores.argsort()[::-1]
    # Get the indices of the top_n most similar movies
    recommended_indices = [i for i in recommended_indices if i not in idx_list][:top_n]
    # keying into the dataframe to get the titles. Which will always be the same order as the cosine vectors due to being from the same dataframe.
    return df['Title'].iloc[recommended_indices]

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend_endpoint():
    data = request.json
    liked_movies = data.get('liked', [])
    recommended_movies = recommend(liked_movies)
    return jsonify(recommended_movies.tolist())