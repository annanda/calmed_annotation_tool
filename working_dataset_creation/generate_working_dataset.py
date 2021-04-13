import pandas as pd
import pathlib
import os.path
import cv2
import glob

main_folder = pathlib.Path(__file__).parent.parent.absolute()
path_videos_directory = os.path.join(main_folder, 'static', 'videos')


def get_video_duration(filename, folder_name):
    video_path = os.path.join(path_videos_directory, folder_name, filename)
    video = cv2.VideoCapture(video_path)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps
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


def fill_emotions_from_time(output_df, annotation_df):
    time_to_skip = 5
    step_of_time = 0.2
    annotation_df = pd.read_csv(annotation_df)
    annotation_sorted = annotation_df.sort_values(['video_file_name', 'time_of_video_seconds'])
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


def split_annotation_by_video_files(annotation_file, target_video):
    annotation_df_from_db = pd.read_csv(annotation_file)
    video_files = annotation_df_from_db.video_file_name.unique()
    output_folder = pathlib.Path(__file__).parent.absolute()
    output_folder = os.path.join(output_folder, 'output_from_db', 'by_video_file', target_video)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for video in video_files:
        if target_video in video:
            new_df = annotation_df_from_db[annotation_df_from_db['video_file_name'] == video]
            df_len = len(new_df)
            new_indexes = list(range(0, df_len))
            new_df.index = new_indexes
            csv_name = f'{output_folder}/{video}.csv'
            new_df.to_csv(csv_name, index=True)


def create_working_datasets(annotation_file, target_video):
    # split_annotation_by_video_files(annotation_file, target_video)
    annotation_per_video_files = glob.glob(
        f'{main_folder}/working_dataset_creation/output_from_db/by_video_file/{target_video}/*.csv')
    for annotation_video_path in annotation_per_video_files:
        video_name = annotation_video_path.split('/')[-1]
        video_name = video_name.split('.csv')[0]
        folder_name = target_video
        time_video = get_video_duration(video_name, folder_name)
        list_times = generate_dataset_entries(time_video)
        output_df = create_df_from_time_entries(time_video, list_times)
        working_dataset = fill_emotions_from_time(output_df, annotation_video_path)
        output_folder_path = os.path.join(main_folder, 'working_dataset', target_video)
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        working_dataset.to_csv(f'{output_folder_path}/{video_name}.csv')


if __name__ == '__main__':
    # annotation_file = '/Users/user/PycharmProjects/annotation_tool/working_dataset_creation/output_from_db/data_annotation_time_test.csv'
    annotation_file = '/Users/user/PycharmProjects/annotation_tool/working_dataset_creation/output_from_db/pilot_1.csv'
    target_video = 'pilots_1'
    split_annotation_by_video_files(annotation_file, target_video)
    create_working_datasets(annotation_file, target_video)
