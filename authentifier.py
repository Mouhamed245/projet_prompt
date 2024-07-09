from flask import Flask, jsonify, request
import psycopg2
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Fonction pour obtenir une connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        dbname='projetfinal',
        user='postgres',
        password='postgres'
    )
    return conn

# Route pour authentifier un administrateur et obtenir un JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (data['username'], data['password']))
        admin = cursor.fetchone()
        if admin:
            access_token = create_access_token(identity={'username': data['username']})
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': f'Error during authentication: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Utilisation du port 5002
