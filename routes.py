from flask import jsonify
from models import Episodes
from sqlalchemy import or_, and_, not_

def configure_routes(app):

    @app.route('/')
    def get_home():
        return jsonify({'message': 'Welcome to the Happy Little API!'})
    
    # gets all episodes and returns them as a JSON
    @app.route('/episodes')
    def get_episodes():
        episodes = Episodes.query.all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets a single episode by id and returns it as a JSON
    @app.route('/episodes/<int:id>')
    def get_episode(id):
        episode = Episodes.query.get(id)
        return jsonify(episode.to_dict())
    
    # gets all episode titles and returns them as a JSON
    @app.route('/episodes/names')
    def get_episode_names():
        episodes = Episodes.query.all()
        episode_names = [episode.title for episode in episodes]
        return jsonify(episode_names)

    # gets all episodes using a specific color and returns them as a JSON
    @app.route('/colors/<color>')
    def get_episodes_by_color(color):
        episodes = Episodes.query.filter(Episodes.colors.contains(color)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)

    # gets all episodes using a specific subject and returns them as a JSON
    @app.route('/subjects/<subject>')
    def get_episodes_by_subject(subject):
        episodes = Episodes.query.filter(Episodes.subjects.contains(subject)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes using subjects and colors and returns them as a JSON
    # @app.route('/subjects/<subject>/colors/<color>')
    # def get_episodes_by_subject_and_color(subject, color):
    #     episodes = Episodes.query.filter(Episodes.subjects.contains(subject), Episodes.colors.contains(color)).all()
    #     episode_list = [episode.to_dict() for episode in episodes]
    #     return jsonify(episode_list)
    
    # gets all episodes aired in a specific month and returns them as a JSON
    @app.route('/episodes/month/<month>')
    def get_episodes_by_month(month):
        episodes = Episodes.query.filter(Episodes.date.contains(month)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes aired in a specific month with a specific color and returns them as a JSON
    @app.route('/episodes/month/<month>/colors/<color>')
    def get_episodes_by_month_and_color(month, color):
        episodes = Episodes.query.filter(Episodes.date.contains(month), Episodes.colors.contains(color)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes aired in a specific month with a specific subject and returns them as a JSON
    @app.route('/episodes/month/<month>/subjects/<subject>')
    def get_episodes_by_month_and_subject(month, subject):
        episodes = Episodes.query.filter(Episodes.date.contains(month), Episodes.subjects.contains(subject)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes aired in a specific month with a specific subject and color and returns them as a JSON
    @app.route('/episodes/month/<month>/subjects/<subject>/colors/<color>')
    def get_episodes_by_month_and_subject_and_color(month, subject, color):
        episodes = Episodes.query.filter(Episodes.date.contains(month), Episodes.subjects.contains(subject), Episodes.colors.contains(color)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes based with a specific title and returns them as a JSON
    @app.route('/episodes/<title>')
    def get_episodes_by_title(title):
        episodes = Episodes.query.filter(Episodes.title.contains(title)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes with any number of specific colors and returns them as a JSON
    @app.route('/colors/<path:colors>')
    def get_episodes_by_colors(colors):
        color_list = colors.split('/')
        conditions = [Episodes.colors.contains(color) for color in color_list]
        episodes = Episodes.query.filter(or_(*conditions)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes with any number of specific subjects and returns them as a JSON
    @app.route('/subjects/<path:subjects>')
    def get_episodes_by_subjects(subjects):
        subject_list = subjects.split('/')
        conditions = [Episodes.subjects.contains(subject) for subject in subject_list]
        episodes = Episodes.query.filter(or_(*conditions)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    #gets all episodes with any number of specific colors and subjects and returns them as a JSON
    @app.route('/colors/<path:colors>/subjects/<path:subjects>')
    def get_episodes_by_colors_and_subjects(colors, subjects):
        color_list = colors.split('/')
        subject_list = subjects.split('/')
        color_conditions = [Episodes.colors.contains(color) for color in color_list]
        subject_conditions = [Episodes.subjects.contains(subject) for subject in subject_list]
        episodes = Episodes.query.filter(or_(*color_conditions), or_(*subject_conditions)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes with exactly the specified colors and returns them as a JSON
    @app.route('/colors/exactly/<path:colors>')
    def get_episodes_by_colors_exactly(colors):
        color_list = colors.split('/')
        conditions = [Episodes.colors.contains(color) for color in color_list]
        episodes = Episodes.query.filter(and_(*conditions)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes with exactly the specified subjects and returns them as a JSON
    @app.route('/subjects/exactly/<path:subjects>')
    def get_episodes_by_subjects_exactly(subjects):
        subject_list = subjects.split('/')
        conditions = [Episodes.subjects.contains(subject) for subject in subject_list]
        episodes = Episodes.query.filter(and_(*conditions)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
    
    # gets all episodes with exactly the specified colors and subjects and returns them as a JSON
    @app.route('/colors/exactly/<path:colors>/subjects/exactly/<path:subjects>')
    def get_episodes_by_colors_and_subjects_exactly(colors, subjects):
        color_list = colors.split('/')
        subject_list = subjects.split('/')
        color_conditions = [Episodes.colors.contains(color) for color in color_list]
        subject_conditions = [Episodes.subjects.contains(subject) for subject in subject_list]
        episodes = Episodes.query.filter(and_(*color_conditions), and_(*subject_conditions)).all()
        episode_list = [episode.to_dict() for episode in episodes]
        return jsonify(episode_list)
