from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
app = Flask(__name__)
CORS(app) # Allows React frontend to communicate with Flask
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
# Recommendation Function
def recommend(movie_name):
    try:
        index = movies[movies['title'] == movie_name].index[0]
        distances = list(enumerate(similarity[index]))
        movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies
    except IndexError:
        return ["Movie not found"]
    except Exception as e:
        return [f"Error: {str(e)}"]
@app.route('/', methods=['GET'])
def home():
    return "Movie Recommendation API is Running with TMDB Dataset! "

@app.route('/recommend', methods=['GET'])
def recommend_api():
    movie = request.args.get('movie')

    if not movie:
        return jsonify({"error": "Movie name is required"}), 400

    result = recommend(movie)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)