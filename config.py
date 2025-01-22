from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

# Initialize app and database connection
app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "*"}}, supports_credentials=True)

# Konfigurasi MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://apigames2comp2_colonyhard:999e8fc3a619e3587ce746e51507f4d942a31e83@98a82.h.filess.io:3305/apigames2comp2_colonyhard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'test123'
db = SQLAlchemy(app)

app.app_context().push()
