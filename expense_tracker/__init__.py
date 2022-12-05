from flask import Flask
from .extensions import db, bcrypt, login_manager




def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "09c33a216982eff0f88ce875467a9ab4"
    app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///site.db"

    from flask_sqlalchemy import SQLAlchemy
    db.init_app(app)
    bcrypt.init_app(app) 
    login_manager.init_app(app)

    from expense_tracker.views import views
    app.register_blueprint(views, url_prefix="/")

    db.create_all()

    # with app.app_context():
    #     db.create_all()

    return app        


