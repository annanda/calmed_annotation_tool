# How to generate working datasets from video annotation in the database

1. Extract the content of the database to a CSV file
* ```sqlite3 video_annotation.db```
* ```sqlite> .headers on```
* ```sqlite> .mode csv```
* ```sqlite> .output data_annotation_videos.csv```
* ```sqlite> select id,video_file_name,emotion_zone,time_of_video_seconds,timestamp_annotation from  emotion_indices_annotation;```