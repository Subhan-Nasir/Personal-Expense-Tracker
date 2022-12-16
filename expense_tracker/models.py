from datetime import datetime
from .extensions import db, login_manager
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    expenses = db.relationship("Expenses", backref = 'user', lazy=True)

    def __repr__(self):
        return f"User: {self.username} - {self.email}"

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    category = db.Column(db.String(50), nullable = False)
    amount = db.Column(db.Float, nullable = False)

    date = db.Column(db.Date, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"User: {self.user_id} - {self.category} - {self.date} - {self.name} - {self.amount}"
   

    
