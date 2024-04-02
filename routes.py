from flask import jsonify
from models import Episodes

def configure_routes(app):

    @app.route('/')
    def get_home():
        return jsonify({'message': 'Welcome to the Happy Little API!'})
    
    @app.route('/episodes')
    def get_episodes():
        episodes = Episodes.query.all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # @app.route('/colors')
    # def get_colors():
    #     colors = Episodes.query.all()
    #     color_list = [color.to_dict() for color in colors]
    #     return jsonify(color_list)
    
    # @app.route('/subjects')
    # def get_subjects():
    #     subjects = Episodes.query.all()
    #     subject_list = [subject.to_dict() for subject in subjects]
    #     return jsonify(subject_list)