# Annotation Tool software for the project Ethically-driven Multimodal Emotion Detection for Children with Autism

## User Manual

### Development

1. Prepare the virtual environment (Create and activate virtual environment with venv).

`python -m venv ./venv`

`source ./venv/bin/activate`

2. Run the script

`python app.py`

### Deployment with Docker

1. Build the images

`docker compose build`

2. Start the services

`docker compose up -d`

A user can configure each task's content and time by adding/changing the variables values in
a `.env` file.

The `example.env` file contains examples of variable and values format.

### How to extract a .CSV file from .db file

(Extract from SQLITE3 to CSV file)

The original `.db` file is stored in the `db_from_server` folder by session number.

command:

```
sqlite3 video_annotation_with_annotator_session_xx_xx.db
```

And then:

```
.headers on
.mode csv
.output data_annotation_session_XX_XX.csv
select id,video_file_name, annotator, emotion_zone,time_of_video_seconds,timestamp_annotation from emotion_indices_annotation;
```

Save the `.csv` in the folder `working_dataset_creation/output_from_db`.

### How to create a working dataset from the annotated .csv

1. Change the values of (to reflect desired working dataset and session):

- annotation_file
- target_session_video

2. Run the file:

```python working_dataset_creation/generate_working_dataset.py```