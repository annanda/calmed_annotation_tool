from decouple import config
from decouple import Csv

VIDEO_FILE = config('VIDEO_FILE', default='videos/ED_dataset_makes_sad_small.mp4')
video_list_default = [VIDEO_FILE]
VIDEO_LIST = config('VIDEO_LIST', default=video_list_default, cast=Csv())
