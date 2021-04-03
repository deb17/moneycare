from app.extensions import db


def cli(app):

    @app.cli.command('reset-db')
    def reset_db():

        with app.app_context():
            db.drop_all()
            db.create_all()
