from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import bz2

app = Flask(__name__)
CORS(app) # Enables your React website to talk to this API

# 1. Load the TMDB Machine Learning Data
try:
    # Load the dictionary and convert it back to a Pandas DataFrame
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # 2. Load the COMPRESSED Similarity Matrix (the 31.5MB bz2 file)
    with bz2.BZ2File('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    
    print("Model and Similarity Matrix loaded successfully! 🚀")
except Exception as e:
    print(f"Error loading model files: {e}")

# Core Recommendation Function
def recommend(movie_name):
    try:
        # Find the index of the movie the user clicked
        # Case-insensitive matching to avoid simple errors
        movie_row = movies[movies['title'].str.lower() == movie_name.lower()]
        
        if movie_row.empty:
            return ["Movie not found"]
            
        index = movie_row.index[0]
        
        # Get similarity scores for that movie
        distances = list(enumerate(similarity[index]))
        
        # Sort movies based on similarity (Top 5 excluding itself)
        movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)

        return recommended_movies
    except Exception as e:
        return [f"Error: {str(e)}"]

# --- API ROUTES ---

@app.route('/', methods=['GET'])
def home():
    return "Movie Recommendation API is Running! 🚀"

@app.route('/recommend', methods=['GET'])
def recommend_api():
    movie = request.args.get('movie')

    if not movie:
        return jsonify({"error": "Movie name is required"}), 400

    result = recommend(movie)
    return jsonify(result)

# --- START SERVER ---

if __name__ == '__main__':
    # host='0.0.0.0' is required for Render deployment
    app.run(host='0.0.0.0', port=5000)