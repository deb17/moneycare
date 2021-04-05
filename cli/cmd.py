import click

from app.extensions import db
from cli.loc import walk


def cli(app):

    @app.cli.command('reset-db')
    def reset_db():

        with app.app_context():
            db.drop_all()
            db.create_all()

    @app.cli.command('loc')
    @click.option('--path')
    def lines_of_code(path):
        '''Count the number of lines in the codebase.

        Usage: flask loc --path='absolute path to root of project'
        '''

        loc = walk(path)
        click.echo(f'Lines of code = {loc}')
