from flask import Flask, jsonify, request
from data_dict_simple import simple
from db import read
import requests
import sqlite3

app = Flask(__name__)

def get_github_repos(username, token=None, include_private=False):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {}

    if token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return []



# routes CRUD operationer GET, PUT, PATCH, DELETE

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the API!"})


@app.route('/members')
def read_all():
    return jsonify(read())


#GET route (READ)
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        #connect database
        with sqlite3.connect('students.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM members WHERE id = ?", (id,))
            member = cur.fetchone()

        if not member:
            return jsonify({"message": "Member not found"}), 404
        
        #check if current user is authenticated
        current_user_id = 1
        is_self = (id == current_user_id)

        response_data = {
            "id": member[0],
            "first_name": member[1],
            "last_name": member[2],
            "birth_date": member[3],
            "gender": member[4],
            "email": member[5],
            "phonenumber": member[6],
            "address": member[7],
            "nationality": member[8],
            "active": member[9],
            "github_username": member[10],
            "is_self": is_self,
        }
    
        #check if memeber i yourself
        if is_self:
            private_repos = get_github_repos(member[10], token=current_user_token, include_private=True) #replace current_user_token with generated token
            response_data["private_repositories"] = private_repos

        return jsonify(response_data), 200
    
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500 
    except KeyError as e:
        return jsonify({"erro": "An unexpected error ocurred", "details": str(e)}), 500

        


#POST route 
@app.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400  # Bad request
    
    # Insert into DB
    with sqlite3.connect('students.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO members (first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (data['first_name'], data['last_name'], data['birth_date'], data['gender'], data['email'], 
            data['phonenumber'], data['address'], data['nationality'], data['active'], data['github_username']))
        conn.commit()
        new_id = cur.lastrowid
    
    return jsonify({"message": "Member created", "id": new_id}), 201  # Return 201 for successful creation



#DELETE route
@app.route('/members/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        with sqlite3.connect('students.db') as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM members WHERE id = ?", (id,))
            if cur.rowcount == 0:
                return jsonify({"message": "Member not found"}), 404
            
        
        return jsonify({"message": "Member deleted succesfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500 



#PUT ROUTE - update an entire member resource by ID (UPDATE)
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No inout data provided"}),

        with sqlite3.connect('students.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM members WHERE id = ?", (id,))
            member = cur.fetchone()

            if not member:
                return jsonify({"message": "Member not found"}), 404

            #perfom update
            cur.execute('''
                UPDATE members SET first_name = ?, last_name = ?, birth_date = ?, gender = ?, email = ?, 
                phonenumber = ?, address = ?, nationality = ?, active = ?, github_username = ?
                WHERE id = ?''', 
                (data['first_name'], data['last_name'], data['birth_date'], data['gender'], data['email'], 
                data['phonenumber'], data['address'], data['nationality'], data['active'], data['github_username'], id))
            conn.commit()

        return jsonify({"message": "Members updated succesfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500 
    except KeyError as e:
        return jsonify({"error": f"Missing key in request data: {str(e)}"}), 400



#PATCH route - partially update a student resource by ID (PARTIAL UPDATE)
@app.route('/members/<int:id>', methods=['PATCH'])
def patch(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        with sqlite3.connect('students.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM members WHERE id = ?", (id,))
            member = cur.fetchone()

            if not member:
                return jsonify({"message": "Member not found"}), 404

            for key, value in data.items():
                cur.execute(f"UPDATE members SET {key} = ? WHERE id = ?", (value, id))
            conn.commit()
        
        return jsonify({"message": f"Member with id: {id} is successfully updated", "member": member}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500     

if __name__ == '__main__':
    app.run(debug=True)


