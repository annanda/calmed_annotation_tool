# Annotation Tool software for the project Personal-independent Emotion Detection Model for Children with High-Functioning ASD

## How to extract a .CSV file from .db file 
(Extract from SQLITE3 to CSV file) 

The original ```.db``` file is stored in the ```db_from_server``` folder by session number.

command:
```
sqlite3 video_annotation_with_annotator_session_03_01_18052022.db
```
And then:
```
.headers on
.mode csv
.output data_annotation_session_XX_XX.csv
select id,video_file_name, annotator, emotion_zone,time_of_video_seconds,timestamp_annotation from emotion_indices_annotation;
```
Save the ```.csv``` in the folder ```working_dataset_creation/output_from_db```.


## How to create a working dataset from the annotated .csv

Key file: ```working_dataset_creation/generate_working_dataset.py```

1. Change the values of (to reflect desired working dataset and session):
- annotation_file
- target_session_video
2. run the file ```working_dataset_creation/generate_working_dataset.py```