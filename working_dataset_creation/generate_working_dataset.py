import pandas as pd
import pathlib
import os.path
import cv2
import glob

main_folder = pathlib.Path(__file__).parent.parent.absolute()
path_videos_directory = os.path.join(main_folder, 'static', 'to_annotate')


def get_video_duration(filename):
    video_path = os.path.join(path_videos_directory, filename)
    video = cv2.VideoCapture(video_path)
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


# def generate_working_dataset_all_videos(annotation_db):
#     video_files = annotation_db.video_file_name.unique()
#     video_duration = {}
#     for video in video_files:
#         video_duration[video] = get_video_duration(video)
#     # TODO finish this here


def fill_emotions_from_time(annotation_df, video):
    annotation_sorted = annotation_df.sort_values(['video_file_name', 'time_of_video_seconds'])
    index_annotation_df = 0
    output_df = 'create the output df only here'
    for index, row in output_df.iterrows():
        # TODO include the tine the emotion is manifested before annotation
        if row['time_of_video_seconds'] > annotation_sorted.iloc[index_annotation_df]['time_of_video_seconds']:
            if index_annotation_df < (len(annotation_sorted) - 1):
                index_annotation_df += 1
        emotion = annotation_sorted.iloc[index_annotation_df]['emotion_zone']
        output_df.loc[index, 'emotion_zone'] = emotion

    return output_df


def create_df_from_time_entries(video_duration, list_times):
    data = {'time_of_video_seconds': list_times}
    new_df = pd.DataFrame(data)
    new_df['emotion_zone'] = ''
    return new_df


def create_working_datasets(annotation_file):
    split_annotation_by_video_files(annotation_file)
    video_duration = {}
    for video in video_files:
        video_duration[video] = get_video_duration(video)
        time_video = get_video_duration(video)
        list_times = generate_dataset_entries(time_video)
        output_df = create_df_from_time_entries(time_video, list_times)
        working_dataset = fill_emotions_from_time(output_df, annotation_df, video)
        working_dataset.to_csv('testing.csv')


def split_annotation_by_video_files(annotation_file):
    annotation_df_from_db = pd.read_csv(annotation_file)
    video_files = annotation_df_from_db.video_file_name.unique()
    output_folder = pathlib.Path(__file__).parent.absolute()
    output_folder = os.path.join(output_folder, 'output_from_db', 'by_video_file')
    for video in video_files:
        new_df = annotation_df_from_db[annotation_df_from_db['video_file_name'] == video]
        df_len = len(new_df)
        new_indexes = list(range(0, df_len))
        new_df.index = new_indexes
        csv_name = f'{output_folder}/{video}.csv'
        new_df.to_csv(csv_name, index=True)


if __name__ == '__main__':
    annotation_file = '/Users/user/PycharmProjects/annotation_tool/working_dataset_creation/output_from_db/data_annotation_time_test.csv'
    create_working_datasets(annotation_file)
