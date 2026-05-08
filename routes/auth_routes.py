from flask import Blueprint, request, jsonify
from database import get_connection
import bcrypt

auth_bp = Blueprint("auth", __name__)


# ===============================
# REGISTER USER
# ===============================
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    # Hash the password
    hashed_pw = bcrypt.hashpw(password.encode(
        'utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, email, hashed_pw, "user"))

        conn.commit()

        return jsonify({
            "message": "User registered successfully"
        })

    except Exception as e:
        print(e)
        return jsonify({
            "message": "Registration failed",
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


# ===============================
# LOGIN USER (ROLE-BASED RESPONSE)
# ===============================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, name, email, role, password as db_password
        FROM users
        WHERE email=%s
    """

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        db_password = user["db_password"]
        is_valid = False

        # Check compatibility with plaintext passwords vs bcrypt
        if db_password.startswith("$2") and len(db_password) == 60:
            is_valid = bcrypt.checkpw(password.encode(
                'utf-8'), db_password.encode('utf-8'))
        else:
            is_valid = (password == db_password)

        if is_valid:
            return jsonify({
                "message": "Login successful",
                "user_id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            })

    return jsonify({
        "message": "Invalid credentials"
    }), 401

# ===============================
# GET USER BY ID
# ===============================


@auth_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, email, role FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404
