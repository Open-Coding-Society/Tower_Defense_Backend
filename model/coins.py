from sqlalchemy import Column, Integer, String
from __init__ import db

class Coins(db.Model):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True)
    user = Column(String, unique=True, nullable=False)
    coins = Column(Integer, nullable=False)

    def __init__(self, user, coins):
        self.user = user
        self.coins = coins

    def create(self):
        """
        Save the current state of the object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def read(self):
        """
        Return a dictionary representation of the object.
        """
        return {
            'user': self.user,
            'coins': self.coins
        }

    def delete(self):
        """
        Delete the object from the database.
        """
        db.session.delete(self)
        db.session.commit()
