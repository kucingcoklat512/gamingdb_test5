from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='user')  # Added role field, default to 'user'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'role': self.role  # Include role in the dict
        }
