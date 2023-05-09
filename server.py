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
# CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="Content-Type")

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
# main_app_url = "http://localhost:8501/"

API_KEY = "c3ed154bde1307169e62092fa886bb9c"
poster_path_base_url = "https://image.tmdb.org/t/p/original"

movies_dict = pickle.load(open('pickle/movie_dict.pkl', 'rb')) # rb = read binary mode
movies =pd.DataFrame(movies_dict)
similarity = pickle.load(open('pickle/similarity.pkl', 'rb'))

cmb_movie_list = movies['title'].values

# poster_url = ''
def get_movie_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c3ed154bde1307169e62092fa886bb9c&language=en-US'.format(movie_id))
    data = response.json()
    # print(data)
    poster_url = poster_path_base_url + data['poster_path']
    # print(poster_url)
    return poster_url

def recommend_movies(movie_selected):
    movie_index = movies[movies['title'] == movie_selected].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x:x[1])[1:21]

    recommended_movies_list = []
    recommended_movies_poster_list = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_list.append(movies.iloc[i[0]].title)

        # fetch poster from API
        recommended_movies_poster_list.append(get_movie_poster(movie_id))
    return recommended_movies_list, recommended_movies_poster_list


def getUser(id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE id = %s', (id,))
    customer = cursor.fetchone()
    print(customer)

    if customer == None:
        print("-------1------------")
        return jsonify({'status': 404, 'message': f"No such customer with id: {id}"})

    print("-------2------------")
    return jsonify({'status' : 202, 'customer' : customer})

def createCustomerDict(customer):
    customerDict = {
        'id': customer[0],
        'name': customer[1],
        'email': customer[2],
        'password': customer[3],
        'address': customer[4],
        'contact': customer[5]
    }

    return customerDict

@app.route('/')
@cross_origin()
def index():
    # return 'Lets\'s play with some CRUD operations....'
    return render_template('server_index.html')

@app.route('/index')
@cross_origin()
def getIndexPage():
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


@app.route('/getId', methods=["GET"])
@cross_origin()
def getLastId():
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM customers ORDER BY id desc LIMIT 1')

    lastId = cursor.fetchone()

    if lastId == None:
        return jsonify({'status': 404, 'message': "No any customers found."})

    print(lastId[0])
    return jsonify({'status': 200, 'lastId':lastId[0]})


@app.route('/getAll')
@cross_origin()
def getAllUsers():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers')
    allCustomers = cursor.fetchall()

    customerList = []
    for customer in allCustomers:
        customerDict = {
            'id': customer[0],
            'name': customer[1],
            'address': customer[2],
            'email': customer[3],
            'contact': customer[4]
        }
        customerList.append(customerDict)

    # responseDict = {'customers': customerList}
    # return jsonify(responseDict)
    #  --- OR  ---
    return jsonify({'status': 200, 'customers': customerList})


@app.route('/search/<int:id>', methods=["GET"])
@cross_origin()
def searchUser(id):
    resp = getUser(id)
    data = json.loads(resp.data)
    # print(data) # {'customer': [1, 'David', 'Highway 23', 'david@example.com', '6422345678'], 'status': 202}
    
    status = data['status']

    if status == 404:
        return jsonify({'status': 404, 'message': f"No such customer with id: {id}"})

    if resp != None:
        customer = data['customer']
        # print(customer) # [1, 'David', 'Highway 23', 'david@example.com', '6422345678']
        # print(customer[0]) # 1
        
        customerDict = createCustomerDict(customer)
        return jsonify({'status': 200, 'customer': customerDict})

@app.route('/login', methods=["POST"])
@cross_origin()
def login():
    if request.method == "POST":
        email = request.json['email']
        password = request.json['pwd']
        print(email,password)

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE email = %s AND password = %s', (email, password))
        customer = cursor.fetchone()
        print(customer)

        if customer:
            return jsonify({'status' : 200, 'message' : "Valid credentials."})
        else:
            return jsonify({'status': 404, 'message': "Please check your credentials and try again!"})

@app.route('/save', methods=["POST"])
@cross_origin()
def saveUser():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        password = request.form['pwd']
        contact = request.form['contact']

        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, address, email, password, contact) VALUES (%s, %s, %s, %s, %s)', (name, address, email, password, contact))
        conn.commit()

        return jsonify({'status': 201, 'message': f'{name} saved successfully!'})

    return jsonify({'status': 404, 'message': "Sign Up failed."})


@app.route('/update', methods=["PUT"])
@cross_origin()
def updateUser():
    print(request.json)
   
    if request.method == "PUT":
    #     id = request.form['id']
    #     name = request.form['name']
    #     address = request.form['address']
    #     email = request.form['email']
    #     contact = request.form['contact']

        id = request.json['id']
        name = request.json['name']
        address = request.json['address']
        email = request.json['email']
        password = request.json['pwd']
        contact = request.json['contact']

        resp = getUser(id)
        data = json.loads(resp.data)
        status = data['status']

        if (status == 404) :
            return jsonify({'status': status, 'message':f"No such customer with id: {id}"})

        cursor = conn.cursor()
        cursor.execute('UPDATE customers SET name = %s, address = %s, email = %s, password = %s, contact = %s WHERE id = %s', (name, address, email, password, contact, id))
        conn.commit()
       
        data = json.loads(resp.data)
        customer = data['customer']
        customerDict = createCustomerDict(customer)

        return jsonify({'status':200, 'customer': customerDict, 'message': 'Your changes have been updated successfully!'})


@app.route('/delete/<int:id>', methods=["DELETE"])
@cross_origin()
# @cross_origin(origin='*', headers=['Access-Control-Allow-Methods','DELETE'])
def deleteUser(id):
    resp = getUser(id)
    data = json.loads(resp.data)
    status = data['status']

    if (status == 404) :
        return jsonify({'status': status, 'message':f"No such customer with id: {id}"})
    

    cursor = conn.cursor()
    cursor.execute('DELETE FROM customers WHERE id = %s', (id,))
    conn.commit()
    
    return jsonify({'status': 200, 'message': f'User with id: {id} deleted successfully!'})
    

if __name__ == '__main__':
    mycursor = conn.cursor()
    # mycursor.execute("DROP TABLE IF EXISTS customers")
    mycursor.execute("CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255), address VARCHAR(255), contact VARCHAR(10))")
    app.run(debug=True)
    # host="0.0.0.0" - accept any request that comes from outside to the EC2 instance
    # app.run(debug=True, host="0.0.0.0") in EC2 instance