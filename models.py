from database import db
import json

class Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    colors = db.Column(db.Text)
    subjects = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'description': self.description,
            'colors': json.loads(self.colors) if self.colors else [],
            'subjects': json.loads(self.subjects) if self.subjects else []
            }
