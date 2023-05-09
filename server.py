from flask import Flask, request, Response, render_template, jsonify, json
from flask_cors import CORS, cross_origin
import mysql.connector
import webbrowser

import pickle
import pandas as pd
import requests


app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MYSQL_HOST'] = 'database-2.cu4p7tdmk9ix.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ptsisAdmin456'
app.config['MYSQL_DB'] = 'movie_db'

conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

login_page_url = "http://127.0.0.1:5000/"
main_app_url = "http://localhost:8501/"

movies_dict = pickle.load(open('pickle/movie_dict.pkl', 'rb')) # rb = read binary mode
movies =pd.DataFrame(movies_dict)
similarity = pickle.load(open('pickle/similarity.pkl', 'rb'))

cmb_movie_list = movies['title'].values

poster_url = ''
def get_movie_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c3ed154bde1307169e62092fa886bb9c&language=en-US'.format(movie_id))
    data = response.json()
    # print(data)
    # st.text(data)
    poster_url = poster_path_base_url + data['poster_path']
    # print(poster_url)
    # st.text(poster_url)
    return poster_url

def recommend_movies(movie_selected):
    movie_index = movies[movies['title'] == movie_selected].index[0]
    # print(movie_index)
    distances = similarity[movie_index]
    # st.text(distances)
    movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x:x[1])[1:21]
    # st.text(movies_list)

    recommended_movies_list = []
    recommended_movies_poster_list = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # st.text(movie_id)
        recommended_movies_list.append(movies.iloc[i[0]].title)
        # st.text(recommended_movies_list)

        # fetch poster from API
        recommended_movies_poster_list.append(get_movie_poster(movie_id))
        # st.text(len(recommended_movies_list))
    return recommended_movies_list, recommended_movies_poster_list


API_KEY = "c3ed154bde1307169e62092fa886bb9c"
poster_path_base_url = "https://image.tmdb.org/t/p/original"


@app.route('/')
@cross_origin()
def index():
    # return 'Lets\'s play with some CRUD operations....'
    mycursor = conn.cursor()
    mycursor.execute("DROP TABLE IF EXISTS customers")
    mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), address VARCHAR(255), contact VARCHAR(10))")
    return render_template('server_index.html')

@app.route('/movies/home', methods=["GET"])
@cross_origin()
def getMovieHomePage():
    return render_template('movies.html')

@app.route('/profile', methods=["GET"])
@cross_origin()
def getProfilePage():
    return render_template('profile.html')

@app.route('/movies', methods=["GET"])
@cross_origin()
def getMovieTitles(): 
    # Convert the ndarray to a list
    x = cmb_movie_list.tolist()

    # Serialize the list using JSON
    y = json.dumps(x)

    # print(cmb_movie_list)
    return jsonify({'status': 200, 'titleList': y})

@app.route('/recommendations/<string:movie_selected>', methods=["GET"])
@cross_origin()
def getRecommendedMovies(movie_selected):
    print(movie_selected)
    titles,posters = recommend_movies(movie_selected)
    return jsonify({'status': 200, 'movieList': titles, 'posterList': posters })
    # return recommended_movies_list, recommended_movies_poster_list




@app.route('/save', methods=["POST"])
@cross_origin()
def saveUser():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']

        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, address, email, contact) VALUES (%s, %s, %s, %s)', (name, address, email, contact))

        conn.commit()

        return jsonify({'status': 201, 'message': f'{name} saved successfully!'})

    return jsonify({'status': 404, 'message': "Invalid request method."})


if __name__ == '__main__':
    # webbrowser.open('http://localhost:5000', new=2)
    app.run(debug=True)
    # host="0.0.0.0" - accept any request that comes from outside to the EC2 instance
    # app.run(debug=True, host="0.0.0.0") in EC2 instance