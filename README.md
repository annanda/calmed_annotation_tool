# Annotation Tool software for the project Ethically-driven Multimodal Emotion Detection for Children with Autism

This web-based system supports the annotation task to create annotated dataset. The annotator accesses a URL address
containing an authentication-protected system with
the study session recordings that need to be annotated. The system records the video time along with the assigned
emotion class identified by the annotator and the annotator's identification. This information is then saved in a
database and can be retrieved later when creating the working dataset with the annotations.

This repository includes the web-based annotation task system and a Python script to create working annotated datasets
from
the annotations collected during annotation session.

## User Manual

## Pre-requisites

- Python 3.8
- Docker

### Development (Local Run)

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

## Generating the working dataset from the collected annotation marks

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

## Licence

This repository is released under dual-licencing:

For non-commercial use of the Software, it is released under
the [3-Cause BSD Licence](https://opensource.org/license/bsd-3-clause/).

For commercial use of the Software, you are required to contact the University of Galway to arrange a commercial
licence.

Please refer to [LICENSE.md](LICENSE.md) file for details on the licence.

----

Author: Annanda Sousa

Author's contact: [annanda.sousa@gmail.com](mailto:annanda.sousa@gmail.com)

----