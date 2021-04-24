from app import create_app
from cli import cli

app = create_app()
cli(app)

# if __name__ == '__main__':
#     app.run(debug=True, ssl_context='adhoc')
