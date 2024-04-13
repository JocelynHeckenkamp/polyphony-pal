from api import db

class AnalysisError(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    location_measure = db.Column(db.Integer, nullable=False)
    location_offset = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    suggestion = db.Column(db.String(500))
    voices = db.Column(db.String(120))
    duration = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<AnalysisError {self.id}>'
#TODO table columns will be added here
