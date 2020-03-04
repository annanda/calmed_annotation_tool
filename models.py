from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_jsonfield

db = SQLAlchemy()


class EmotionIndicesAnnotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_file_name = db.Column(db.String(150), unique=False, nullable=False)
    emotion_zone = db.Column(db.String(80), unique=False, nullable=False)
    time_of_video_seconds = db.Column(db.Float, unique=False, nullable=False)
    behaviour_markes = db.Column(db.JSON)
    timestamp_annotation = db.Column(db.DateTime, nullable=False)

    behaviour_markes = db.Column(
        sqlalchemy_jsonfield.JSONField(
            enforce_string=True,
            enforce_unicode=False
        ),
        nullable=False
    )

    # example of format for behaviour markers json
    # {
    #     jumping: 0,
    #     other : " hshsjhsksjslsklsk "
    # }

    def __repr__(self):
        return f"<id: {self.id}, video_file: {self.video_file_name}, emotion_zone: {self.emotion_zone}, " \
               f"time_seconds: {self.time_of_video_seconds}, behaviour markers: {self.behaviour_markes}," \
               f"timestamp_annotation: {self.timestamp_annotation} >"
