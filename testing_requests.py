import requests
from flask import json

data = {'video_file_name': 'video1.mpeg',
        'emotional_zone': 'yellow',
        'time_seconds': 1560,
        'behaviours': {
            'jump': 1,
            'laugh': 1,
            'head_movement': 1,
            'other': 'I see he is agitated more now'
        }
        }
data_json = json.dumps(data)
# data = "hello"
r = requests.post('http://0.0.0.0:90/store_annotation', json=data)
print(r.content)
