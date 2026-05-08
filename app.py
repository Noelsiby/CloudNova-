from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.event_routes import event_bp
from routes.booking_routes import booking_bp

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Nova Events API is running successfully"


app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(booking_bp)

if __name__ == "__main__":
    app.run(debug=True)
