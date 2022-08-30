import json
import os
import datetime

from Lib.schedule.download import download
from Lib.schedule.find import (find_file_with_ext, find_folder_with_name, 
        create_empty_folders)
from Lib.schedule.delete import delete_old_files, remove_empty_folders
from Lib.schedule.data_fetch import book_to_list, get_teachers_data
from Lib.schedule.schedule_create import schedule_create, compress
from Lib.schedule.week import schedule_week

from config import data_folder, font_path


def main(test):
    start_time = datetime.datetime.now()
    start_time_str = str(datetime.datetime.ctime(start_time)).split(' ')
    start_time_str = [i for i in start_time_str if i != '']
    start_day = int(start_time_str[2])
    start_hour = int(start_time_str[3].split(':')[0])
    start_minute = int(start_time_str[3].split(':')[1])

    all_files_iteration = 0

    all_data_folder = data_folder

    if not os.path.exists(all_data_folder):
        os.mkdir(all_data_folder)

    if not test:
        """downloads files"""
        download()

        all_files = find_file_with_ext(location=all_data_folder, 
                ext_to_find='.xls', ext_to_miss='.xlsx')

        delete_old_files(files=all_files, start_day=start_day, 
                start_hour=start_hour, start_minute=start_minute)


    xls_folders = find_folder_with_name(location=all_data_folder, 
                                    folder_name='xls')

    for item in xls_folders[:]:
        print(str(os.path.dirname(item)).split(r'/data/')[1])

        # iter = 1
        folder_iteration = 1

        xls_folder = f'{os.path.dirname(item)}/xls'
        item_schedule_folder = f'{os.path.dirname(item)}/data'
        json_folder = f'{item_schedule_folder}/json'
        week_folder = f'{item_schedule_folder}/week'
        teachers_folder = f'{json_folder}/teachers'
        path_to_schedule = f'{json_folder}/schedule'


        if not test:
            """ Creates empty folders if needed """
            folders = [item_schedule_folder, json_folder, 
                    week_folder, font_path,
                    teachers_folder, path_to_schedule]
            create_empty_folders(folders=folders)

        list_of_files = os.listdir(xls_folder)
        list_of_files.sort()

        for name in list_of_files[:]:
            start_file_fetch_time = datetime.datetime.now()
            name_without_ext = name.split('.x')[0]

            try:
                """ gets all data from xls """
                src = f'{xls_folder}/{name}'
                book_data = book_to_list(path=src)

                """ gets teachers data """
                teachers_data = get_teachers_data(book_data=book_data)
                with open(f'{teachers_folder}/teachers_'\
                    f'{name_without_ext}.json', "w") as f:
                    json.dump(teachers_data, f, indent=4, 
                        ensure_ascii=False)

                """ gets schedule """
                # print(len(teachers_data))
                schedule = schedule_create(teachers_data=teachers_data)
                # print(len(schedule))
                schedule = compress(data=schedule)
                # print(len(schedule))
                with open(f'{path_to_schedule}/schedule_'\
                        f'{name_without_ext}.json', "w") as f:
                    json.dump(schedule, f, indent=4, ensure_ascii=False)

                """ gens images """
                try:
                    schedule_week(path=week_folder, group=name_without_ext, 
                            schedule=schedule, font_path=font_path)
                except Exception as _image_ex:
                    print(_image_ex)

            except Exception as _xls_error:
                print(_xls_error)

            file_fetch_time = datetime.datetime.now()-start_file_fetch_time
            print(f'[INFO] Processed {" " if folder_iteration <10 else ""}'\
                    f'{folder_iteration} / {len(list_of_files)} '\
                    f'book ( {name_without_ext} ) '\
                    f'in {file_fetch_time}')
            folder_iteration += 1
            all_files_iteration += 1

    if not test:
        all_files = find_file_with_ext(location=all_data_folder, 
                ext_to_find=['.xls', '.json', '.jpg'])

        delete_old_files(files=all_files, start_day=start_day, 
                start_hour=start_hour, start_minute=start_minute)

        remove_empty_folders(path=all_data_folder)

    print(f'[INFO] Finished {all_files_iteration} files '\
            f'in {datetime.datetime.now() - start_time}')



if __name__ == '__main__':
    test = False
    # test = True
    main(test=test)
