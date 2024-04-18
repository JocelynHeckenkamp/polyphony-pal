from .ext import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash' : self.password_hash,
        }

class GraderScore(db.Model):
    __tablename__ = 'GraderScore'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    xml = db.Column(db.Text, nullable=False)  # Text type for XML content

    def __repr__(self):
        return f'<GraderScore {self.score_id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'xml' : self.xml,
        }
    
class RomanScore(db.Model):
    __tablename__ = 'RomanScore'
    id = db.Column(db.Integer, primary_key=True)
    roman = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    xmls = relationship('XML', backref='RomanScore', info={'fulltext_indexed': True})

    def __repr__(self):
        return f'<RomanScore {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'roman': self.roman,
            'key': self.key,
            'finished': self.finished,
        }

class XML(db.Model):
    __tablename__ = 'XML'
    id = db.Column(db.Integer, primary_key=True)
    roman_id = db.Column(db.Integer, db.ForeignKey('RomanScore.id'))
    xml = db.Column(db.Text, nullable=False)  # Text type for XML content

    def __repr__(self):
            return f'<XML {self.id}>'
        
    def serialize(self):
        return {
            'id': self.id,
            'roman_id': self.roman_id,
            'xml': self.xml,
        }

# class AnalysisError(db.Model):
#     error_id = db.Column(db.Integer, primary_key=True)
#     score_id = db.Column(db.Integer, db.ForeignKey('score.score_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     measure = db.Column(db.Integer, nullable=False)
#     offset = db.Column(db.Float, nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     suggestion = db.Column(db.String(500))
#     #voices = db.Column(db.String(120))  # This could be a comma-separated list of voices if needed
#     voice1 = db.Column(db.Boolean)
#     voice2 = db.Column(db.Boolean)
#     voice3 = db.Column(db.Boolean)
#     voice4 = db.Column(db.Boolean)
#     duration = db.Column(db.Float)
#     timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<AnalysisError {self.error_id}>'