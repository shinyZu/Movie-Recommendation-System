from flask import Flask, request, Response, render_template, jsonify, json
from flask_cors import CORS, cross_origin
import mysql.connector
import webbrowser

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

@app.route('/')
@cross_origin()
def index():
    # return 'Lets\'s play with some CRUD operations....'
    mycursor = conn.cursor()
    mycursor.execute("DROP TABLE IF EXISTS customers")
    mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), address VARCHAR(255), contact VARCHAR(10))")
    return render_template('server_index.html')

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