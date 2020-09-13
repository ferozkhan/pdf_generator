from sqlalchemy import JSON

from src.app import db


class Invoice(db.models):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    data = db.Column(JSON)

    def __init__(self, url, data):
        self.data = data
        self.url = url

    def __repr__(self):
        return f"<id: {self.id}>, url: {self.url}"
