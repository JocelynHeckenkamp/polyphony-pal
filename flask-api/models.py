from api import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    scores = db.relationship('Score', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Score(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    score_id = db.Column(db.Integer, primary_key=True)
    old_xml = db.Column(db.Text)  # Text type for XML content
    new_xml = db.Column(db.Text)
    errors = db.relationship('AnalysisError', backref='score', lazy='dynamic')

    def __repr__(self):
        return f'<Score {self.score_id}>'

class AnalysisError(db.Model):
    error_id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('score.score_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    measure = db.Column(db.Integer, nullable=False)
    offset = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    suggestion = db.Column(db.String(500))
    #voices = db.Column(db.String(120))  # This could be a comma-separated list of voices if needed
    voice1 = db.Column(db.Boolean)
    voice2 = db.Column(db.Boolean)
    voice3 = db.Column(db.Boolean)
    voice4 = db.Column(db.Boolean)
    duration = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<AnalysisError {self.error_id}>'