from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Fonction pour obtenir une connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        dbname='projetfinal',
        user='postgres',
        password='postgres'
    )
    return conn

# Route d'accueil
@app.route('/')
def home():
    return jsonify({'message': 'Bienvenue dans l\'API REST!'})

# Route pour ajouter un administrateur
@app.route('/add-admin', methods=['POST'])
def add_admin():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO admin (username, password) VALUES (%s, %s)',
            (data['username'], data['password'])
        )
        conn.commit()  # Enregistrer les modifications dans la base de données
        return jsonify({'message': 'Admin created'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating admin: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

# Route pour récupérer tous les administrateurs
@app.route('/admins', methods=['GET'])
def get_admins():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT idadmin, username FROM admin')
        admins = cursor.fetchall()
        output = [{'idadmin': a[0], 'username': a[1]} for a in admins]
        return jsonify({'admins': output})
    except Exception as e:
        return jsonify({'message': f'Error retrieving admins: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

# Route pour supprimer un administrateur
@app.route('/delete-admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM admin WHERE idadmin = %s', (admin_id,))
        conn.commit()  # Enregistrer les modifications dans la base de données
        return jsonify({'message': 'Admin deleted'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting admin: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
