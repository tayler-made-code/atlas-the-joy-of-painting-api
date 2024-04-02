from flask import Flask, g
from factory import create_app
from data_cleaner import load_data_into_db
from database import db
from routes import configure_routes

app = create_app()
configure_routes(app)

def create_tables_and_load_data():
    with app.app_context():
        db.create_all()
        load_data_into_db()

# @app.before_request
# def bofre_request():
#     if not hasattr(g, 'init_done'):
#         create_tables_and_load_data()
#         g.init_done = True

if __name__ == '__main__':
    app.run(debug=True)