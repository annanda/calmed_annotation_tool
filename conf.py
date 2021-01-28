from decouple import config
from decouple import Csv

# VIDEO_FILE = config('VIDEO_FILE', default='to_annotate/ED_3_makes_sad.mp4')
# VIDEO_FILE = config('VIDEO_FILE', default='to_annotate/ED_dataset_makes_sad_small.mp4')
VIDEO_FILE = config('VIDEO_FILE', default='videos/ED_dataset_makes_sad_small.mp4')
video_list_default = [VIDEO_FILE]
video_list = ['videos/pilots_1/pilots_1_01.mp4', 'videos/pilots_1/pilots_1_02.mp4', 'videos/pilots_1/pilots_1_03.mp4',
              'videos/pilots_1/pilots_1_04.mp4', 'videos/pilots_1/pilots_1_05.mp4', 'videos/pilots_1/pilots_1_06.mp4']
VIDEO_LIST = config('VIDEO_LIST', default=video_list_default, cast=Csv())
# VIDEO_LIST = config('VIDEO_LIST', default=video_list)
