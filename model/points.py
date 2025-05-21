from __init__ import db

class Points(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __init__(self, user, points):
        self.user = user
        self.points = points

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {
            "id": self.id,
            "user": self.user,
            "points": self.points
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
