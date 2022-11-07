from flask import Flask, render_template, request, json
from models import db, EmotionIndicesAnnotation
from conf import VIDEO_FILE, VIDEO_LIST
from datetime import datetime
import base64

app = Flask(__name__, template_folder="./templates", static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_annotation_with_annotator.db'
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
    # raise Exception()
    return render_template('video_annotation_index.html', video_name=VIDEO_FILE, video_list=VIDEO_LIST)


@app.route('/store_annotation', methods=['POST'])
def store_annotation():
    # print(request.is_json)
    annotator = get_annotator()
    app.logger.info(annotator)
    req_data = request.get_json()
    video_file_name = req_data['video_file_name']
    emotion_zone = req_data['emotional_zone']
    time = req_data['time_seconds']
    behaviours = req_data['behaviours']
    save_in_db(video_file_name=video_file_name, emotion_zone=emotion_zone, time_seconds=time, behaviours=behaviours,
               annotator=annotator)
    return 'annotation saved on DB'


def get_annotator():
    authorization_header = request.headers.get('Authorization')
    annotator = 'admin'
    if authorization_header:
        auth64 = authorization_header.replace('Basic ', '')
        annotator_byte = base64.b64decode(auth64)
        annotator = annotator_byte.decode('utf-8').split(':')[0]
    return annotator


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


def save_in_db(video_file_name, emotion_zone, time_seconds, behaviours, annotator):
    time = datetime.now()
    db_new_entry = EmotionIndicesAnnotation(video_file_name=video_file_name, emotion_zone=emotion_zone,
                                            time_of_video_seconds=time_seconds, behaviour_markes=behaviours,
                                            timestamp_annotation=time,
                                            annotator=annotator)
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
    # localrun
    # app.run(debug=True, host='0.0.0.0', port=5050)
