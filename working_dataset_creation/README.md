# How to generate working datasets from video annotation in the database

1. Extract the content of the database to a CSV file
* ```sqlite3 video_annotation.db```
* ```sqlite> .headers on```
* ```sqlite> .mode csv```
* ```sqlite> .output working_dataset_creation/output_from_db/data_annotation_videos_small.csv```
* ```sqlite> select id,video_file_name,emotion_zone,time_of_video_seconds,timestamp_annotation from  emotion_indices_annotation;```
2. Run the python file to generate the working dataset (adding the path for the CSV input file)

``` python generate_working_dataset.py```