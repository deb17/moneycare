from app.extensions import db


class Social(db.Model):
    __tablename__ = 'social'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gname = db.Column(db.String(64))
    gmail = db.Column(db.String(128), unique=True, index=True)
    handle = db.Column(db.String(64), unique=True, index=True)  # twitter
    tmail = db.Column(db.String(128), unique=True, index=True)  # twitter
