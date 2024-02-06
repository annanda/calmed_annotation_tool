import pandas as pd
import pathlib
import os.path
import cv2
import glob

main_folder = pathlib.Path(__file__).parent.parent.absolute()
path_videos_directory = os.path.join(main_folder, 'static', 'videos')
path_annotation_directory = os.path.join(main_folder, 'working_dataset_creation', 'output_from_db')


def get_video_duration(filename, folder_name):
    video_path = os.path.join(path_videos_directory, folder_name, filename)
    if os.path.isfile(video_path):
        video = cv2.VideoCapture(video_path)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps
        return duration
    else:
        raise Exception('Your video folder name is not valid! It cannot read the video.')


def find_missing(lst):
    return [x for x in range(lst[0], lst[-1] + 1)
            if x not in lst]


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


def fill_emotions_from_time(output_df, annotation_df_path):
    time_to_skip = 5
    step_of_time = 0.2
    annotation_df_path = pd.read_csv(annotation_df_path)
    annotation_sorted = annotation_df_path.sort_values(['video_file_name', 'time_of_video_seconds'])
    index_annotation_df = 0
    len_output_df = len(output_df)

    count = 0
    # for index in range(len(annotation_sorted)):
    #     print(index)
    for _, annotation in annotation_sorted.iterrows():
        if count == len(annotation_sorted) - 1:
            current_time = annotation["time_of_video_seconds"]
            next_time = output_df.iloc[len_output_df - 1]['time_of_video_seconds'] + (time_to_skip * step_of_time)
        else:
            current_time = annotation["time_of_video_seconds"]
            next_time = annotation_sorted.iloc[count + 1]['time_of_video_seconds']
        if count == 0:
            output_df.loc[output_df['time_of_video_seconds'] <= (
                    current_time - (time_to_skip * step_of_time)), 'emotion_zone'] = 'green'
            inferior_limit = current_time - time_to_skip * step_of_time
            superior_limit = next_time - time_to_skip * step_of_time
            output_df.loc[(output_df['time_of_video_seconds'] > inferior_limit) & (
                    output_df['time_of_video_seconds'] <= superior_limit), 'emotion_zone'] = annotation['emotion_zone']
            count += 1
        else:
            inferior_limit = current_time - time_to_skip * step_of_time
            superior_limit = next_time - time_to_skip * step_of_time
            output_df.loc[(output_df['time_of_video_seconds'] > inferior_limit) & (
                    output_df['time_of_video_seconds'] <= superior_limit), 'emotion_zone'] = annotation['emotion_zone']
            count += 1
    return output_df


def create_df_from_time_entries(video_duration, list_times):
    data = {'time_of_video_seconds': list_times}
    new_df = pd.DataFrame(data)
    new_df['emotion_zone'] = ''
    return new_df


def split_annotation_by_video_files(original_annotation, session_number, target_video, annotation_type):
    # annotation_file = path_annotation_directory + '/' + session_number + '.csv'
    annotation_file = original_annotation

    annotation_df_from_db = pd.read_csv(annotation_file)
    video_files = annotation_df_from_db.video_file_name.unique()
    output_folder = pathlib.Path(__file__).parent.absolute()
    output_folder = os.path.join(output_folder, 'output_from_db', 'by_video_file', annotation_type, session_number)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_parts = []
    for video in video_files:
        if target_video in video:
            new_df = annotation_df_from_db[annotation_df_from_db['video_file_name'] == video]
            df_len = len(new_df)
            new_indexes = list(range(0, df_len))
            new_df.index = new_indexes
            video_name = video.split('.mp4')[0]
            file_part = video_name.split('_')[-1]
            file_parts.append(int(file_part))
            file_name = f'{session_number}_{file_part}.csv'
            csv_name = f'{output_folder}/{file_name}'
            new_df.to_csv(csv_name, index=False)
    file_parts.sort()
    missing_parts = find_missing(file_parts)
    # ! It only works if the missing annotation part is in the middle of the videos.
    if missing_parts:
        for part in missing_parts:
            data = {'id': [0],
                    'video_file_name': [session_number],
                    'annotator': ['admin'],
                    'emotion_zone': ['green'],
                    'time_of_video_seconds': [0.0],
                    'timestamp_annotation': [0]}
            missing_df = pd.DataFrame.from_dict(data)
            file_name = f'{session_number}_0{part}.csv'
            csv_name = f'{output_folder}/{file_name}'
            missing_df.to_csv(csv_name, index=False)


def check_annotation_video_sequence(session, annotation_type):
    """
    In here the function split_annotation_by_video has already run. So you have a separated .csv file
    for each part of the study session videos with the annotation from each video part. They are stored in
    output_from_db >> by_video_file
    :param session:
    :return:
    """
    folder = os.path.join(main_folder, 'working_dataset_creation', 'output_from_db', 'by_video_file', annotation_type,
                          session)
    output_folder = os.path.join(main_folder, 'working_dataset_creation', 'output_from_db',
                                 'after_annotation_check', annotation_type,
                                 session)
    files = os.listdir(folder)
    files.sort()
    prev_emotion = 'green'
    for file in files:
        df = pd.read_csv(os.path.join(folder, file))
        last_row = df.iloc[-1]
        if prev_emotion != 'green':
            video_name = last_row['video_file_name']
            size = len(df.columns)
            if size == 5:
                df.loc[-1] = [0, video_name, prev_emotion, 0, 0]
                df.index = df.index + 1
                df.sort_index(inplace=True)
            elif size == 6:
                df.loc[-1] = [0, video_name, 'admin', prev_emotion, 0, 0]
                df.index = df.index + 1
                df.sort_index(inplace=True)
            else:
                raise ValueError('Something is wrong with the dataframe format')
        prev_emotion = last_row['emotion_zone']
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        df.to_csv(f'{output_folder}/{file}', index=True)


def create_working_datasets(session_number, annotation_type):
    path_dir = os.path.join(main_folder, 'working_dataset_creation', 'output_from_db', 'after_annotation_check',
                            annotation_type,
                            session_number)
    annotation_per_video_files = os.listdir(path_dir)
    for annotation_video_path in annotation_per_video_files:
        video_name = annotation_video_path.split('.csv')[0] + '.mp4'
        folder_name = session_number
        time_video = get_video_duration(video_name, folder_name)
        list_times = generate_dataset_entries(time_video)
        output_df = create_df_from_time_entries(time_video, list_times)
        working_dataset = fill_emotions_from_time(output_df, os.path.join(path_dir, annotation_video_path))
        video_part = video_name.split('.mp4')[0]
        video_part = video_part.split('_')[-1]
        working_dataset['video_part'] = video_part
        output_folder_path = os.path.join(main_folder, 'working_dataset', annotation_type, session_number)
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        file_name = video_name.replace('.mp4', '')
        working_dataset.to_csv(f'{output_folder_path}/{file_name}.csv', index=True)


if __name__ == '__main__':
    # session = 'session_01_01'
    # target_session_video = 'session_01_01'

    #  TODO save the video sizes for I dont need to open the videos every time.
    # 1. Put the videos used for annotation into the folder static/videos (with the right pattern for name)

    # Define the origin file - to extract annotations
    file_annotation = path_annotation_directory + '/' + 'annotation_specialist_complete.csv'
    annotation_type = 'specialist'
    sessions = [
        # 'session_01_01',
        # 'session_02_01',
        # 'session_02_02',
        # 'session_03_01',
        'session_03_02',
        # 'session_04_01',
        # 'session_04_02',
    ]

    for session in sessions:
        # 2. First Run just the function below:
        split_annotation_by_video_files(file_annotation, session, session, annotation_type)

        # 3. Correct annotation, if needed
        check_annotation_video_sequence(session, annotation_type)

        # 4. Second run just the function below:
        create_working_datasets(session, annotation_type)
