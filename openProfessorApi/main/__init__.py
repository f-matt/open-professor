from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, get_jwt_identity, \
    set_access_cookies, verify_jwt_in_request
from flask_restful import Api

from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

import os
import logging
import traceback


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)

# SqlAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
db = SQLAlchemy(app)

# flask-restful
api = Api(app)

# flask-jwt-extended
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Marshmallow
ma = Marshmallow(app)

# Logging
handler = logging.FileHandler("/var/log/open_professor.log")
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)


# Routes
from auth.services import LoginService
from courses.services import CoursesService
from questions.services import QuestionsService
from answers.services import AnswersService
from downloads.services import DownloadsService

@app.route("/api")
def index():
    return "Status: online"

api.add_resource(LoginService, "/api/login")
api.add_resource(CoursesService, "/api/courses")
api.add_resource(QuestionsService, "/api/questions")
api.add_resource(AnswersService, "/api/answers")
api.add_resource(DownloadsService, "/api/download-all")
