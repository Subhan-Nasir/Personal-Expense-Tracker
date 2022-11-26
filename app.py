from flask import Flask
from views import views

app = Flask(__name__)
app.config["SECRET_KEY"] = "09c33a216982eff0f88ce875467a9ab4"
app.register_blueprint(views, url_prefix="/")
print("test commit")

if __name__ == "__main__":
    app.run(debug=True)
