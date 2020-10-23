import pandas as pd
import numpy as np

# TODO put relative paths here
path_videos_directory = '/Users/user/PycharmProjects/annotation_tool/static/to_annotate'
annotation_file = '/Users/user/PycharmProjects/annotation_tool/working_dataset_creation/output_from_db/data_annotation_time_test.csv'
filename = '/Users/user/PycharmProjects/annotation_tool/static/to_annotate/ED_3_makes_sad.mp4'


def get_video_duration(filename):
    import cv2
    video = cv2.VideoCapture(filename)

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps
    # print(duration)
    return duration


def generate_dataset_entries(stop, start=0, step=0.2):
    list_generated = []
    count = 0
    while True:
        temp = start + count * step
        temp = float("{:.2f}".format(temp))
        if temp > stop:
            break
        list_generated.append(temp)
        count += 1
    return list_generated


def generate_working_dataset_all_videos(annotation_db):
    video_files = annotation_db.video_file_name.unique()
    video_duration = {}
    for video in video_files:
        video_duration[video] = get_video_duration(video)
    # TODO finish this here


def fill_emotions_from_time(output_df, annotation_df):
    annotation_sorted = annotation_df.sort_values(['video_file_name', 'time_of_video_seconds'])
    index_annotation_df = 0
    for index, row in output_df.iterrows():
        # print(annotation_sorted.iloc[index_annotation_df]['time_of_video_seconds'])
        # TODO include the tine the emotion is manifested before annotation
        if row['time_of_video_seconds'] > annotation_sorted.iloc[index_annotation_df]['time_of_video_seconds']:
            if index_annotation_df < (len(annotation_sorted) - 1):
                index_annotation_df += 1
        emotion = annotation_sorted.iloc[index_annotation_df]['emotion_zone']
        output_df.loc[index, 'emotion_zone'] = emotion

        # if row['time_of_video_seconds'] <= annotation_sorted.iloc[index_annotation_df]['time_of_video_seconds']:
        #     emotion = annotation_sorted.iloc[index_annotation_df]['emotion_zone']
        #     output_df.loc[index, 'emotion_zone'] = emotion
        # else:
        #     if index_annotation_df >= (len(annotation_sorted) - 1):
        #         emotion = annotation_sorted.iloc[index_annotation_df]['emotion_zone']
        #         output_df.loc[index, 'emotion_zone'] = emotion
        #     else:
        #         index_annotation_df += 1
        #         emotion = annotation_sorted.iloc[index_annotation_df]['emotion_zone']
        #         output_df.loc[index, 'emotion_zone'] = emotion

    return output_df


def create_df_from_time_entries(video_duration, list_times):
    data = {'time_of_video_seconds': list_times}
    new_df = pd.DataFrame(data)
    new_df['emotion_zone'] = ''
    return new_df


if __name__ == '__main__':
    annotation = pd.read_csv(annotation_file)
    time_video = get_video_duration(filename)
    list_times = generate_dataset_entries(time_video)
    output_df = create_df_from_time_entries(time_video, list_times)
    working_dataset = fill_emotions_from_time(output_df, annotation)
    print(working_dataset)