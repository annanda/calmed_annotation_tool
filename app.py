from flask import Flask, render_template, request, json
from models import db, EmotionIndicesAnnotation
from conf import VIDEO_FILE, VIDEO_LIST
from datetime import datetime

app = Flask(__name__, template_folder="./templates", static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_annotation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# @app.route('/', methods=['GET'])
def index_page():
    info = {}
    # return render_template('index.html', **info)
    # test_db()
    return "Hello World!"


@app.route('/annotation', methods=['GET'])
def video_main():
    video_path = request.args.get('video')
    return render_template('video_annotation_main.html', video_path=video_path)


@app.route('/', methods=['GET'])
def video_list():
    return render_template('video_annotation_index.html', video_name=VIDEO_FILE, video_list=VIDEO_LIST)


@app.route('/store_annotation', methods=['POST'])
def store_annotation():
    # print(request.is_json)
    req_data = request.get_json()
    video_file_name = req_data['video_file_name']
    emotion_zone = req_data['emotional_zone']
    time = req_data['time_seconds']
    behaviours = req_data['behaviours']
    save_in_db(video_file_name=video_file_name, emotion_zone=emotion_zone, time_seconds=time, behaviours=behaviours)
    return 'annotation saved on DB'


def test_db():
    video_file_name = 'my_test.avi'
    emotion_zone = 'blue'
    time_seconds = 110
    # send a dictionary to DB
    behaviours = {
        'jump': 0,
        'laugh': 1,
        'head_movement': 1,
        'other': 'I see he is agitated'
    }
    save_in_db(video_file_name, emotion_zone, time_seconds, behaviours)


def save_in_db(video_file_name, emotion_zone, time_seconds, behaviours):
    time = datetime.now()
    db_new_entry = EmotionIndicesAnnotation(video_file_name=video_file_name, emotion_zone=emotion_zone,
                                            time_of_video_seconds=time_seconds, behaviour_markes=behaviours,
                                            timestamp_annotation=time)
    db.session.add(db_new_entry)
    db.session.commit()


# to query the last entry on DB
# last_execution = db.session.query(EmotionIndicesAnnotation).order_by(EmotionIndicesAnnotation.id.desc()).first()
# print(last_execution)
# print(last_execution.behaviour_markes)
# print(type(last_execution.behaviour_markes))


if __name__ == '__main__':
    # TODO comment the lines below
    app.app_context().push()
    # db.drop_all()
    # db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
