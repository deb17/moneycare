from app.extensions import db


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tagname = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Tag: {self.tagname}>'
