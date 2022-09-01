import os
import datetime
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from typing import List, Dict, Any

def schedule_week(path: str, group, schedule, font_path: str) -> None:
    qualities = ['q1', 'q2']
    if not os.path.exists(f'{path}/{group}'):
        os.mkdir(f'{path}/{group}')

    subgroups = schedule[0]['all_subgroups']
    first_date = schedule[0]['date']
    first_date = datetime.datetime.strptime(first_date, '%Y-%m-%d')
    last_date = schedule[-1]['date']
    last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d')

    delta = 1
    date = first_date
    while True:
        date = date + datetime.timedelta(days=delta)
        if date >= last_date:
            break
    max_delta = date - first_date
    max_delta = int(str(max_delta).split(' ')[0])

    for subgroup in range(1, subgroups + 1): 
        subgroup = str(subgroup)
        if not os.path.exists(f'{path}/{group}/s{subgroup}'):
            os.mkdir(f'{path}/{group}/s{subgroup}')
        for quality in qualities:
            if not os.path.exists(f'{path}/{group}/'\
                    f's{subgroup}/{quality}'):
                os.mkdir(f'{path}/{group}/s{subgroup}/{quality}')
            for delta in range(0, max_delta + 1, 7):
                today_date = first_date + datetime.timedelta(days=delta)
                today_date = today_date.strftime('%Y-%m-%d') 
                today_date = datetime.datetime.strptime(
                        today_date, '%Y-%m-%d')
                today_num = today_date.weekday()
                days = []
                days = [(
                            today_date - datetime.timedelta(days=delta)
                        ).strftime('%Y-%m-%d') for delta in reversed(
                                range(0, today_num + 1)
                            )
                        ] 
                days += (
                            [
                                (today_date + datetime.timedelta(
                                    days=delta
                                    )
                                ).strftime(
                                    '%Y-%m-%d'
                                    ) for delta in range(1, 7 - today_num)
                            ]
                        )
                dates = []
                for date in days:
                    date = date.split('-')
                    year = int(date[0])
                    month = int(date[1])
                    day = int(date[2])
                    date = f'{year}-{month}-{day}'
                    dates.append(date)

                dict_file = file_input(file_path=schedule, days=dates, 
                                            subgroup=subgroup
                                        )

                modes = ['day', 'night']
                for mode in modes:
                    if mode != 'night' and mode != 'day':
                        return print('Mode error')
                    if not os.path.exists(f'{path}/{group}/'\
                                f's{subgroup}/{quality}/{mode}'
                            ):
                        os.mkdir(
                                    f'{path}/{group}/s{subgroup}/'\
                                    f'{quality}/{mode}'
                                )
                    output_path = f'{path}/{group}/s{subgroup}/'\
                                  f'{quality}/{mode}/week_'\
                                  f'{dates[0]}_{dates[-1]}.jpg' 
                    try:
                        gen_image(
                                    output_path=output_path, 
                                    font_path=font_path,
                                    mode=mode,
                                    dict_file=dict_file,
                                    quality=quality
                                    )
                    except Exception as _gen_image_exception:
                        print(_gen_image_exception)



def file_input(
                file_path: List[dict], days, subgroup
        ) -> List[Dict[str, Any]]:
    schedule_data = file_path
    cards = []
    for card in schedule_data:
        for day in days:
            if card['date'] == day:
                write_data = {}
                write_data['date'] = card['date']
                write_data['lessons'] = []
                for lesson in card['lessons']:
                    if (lesson['subgroup'] == subgroup or 
                            lesson['subgroup'] == ''
                        ):
                        write_data['lessons'].append(lesson)
                if not write_data['lessons'] == []:
                    cards.append(write_data)
    return cards


def gen_image(output_path, font_path, mode, dict_file, quality):
    if quality == 'q2':
        font_size = 20
    else:
        font_size = 10
    days_in_week_list = [[[], [['1 - (8.30-10.00)']], 
        [['2 - (10.10-11.40)']], [['3 - (12.40-14.10)']], 
        [['4 - (14.20-15.50)']], [['5 - (16.00-17.30)']], 
        [['6 - (18.00-19.30)']], [['7 - (19.40-21.10)']]
    ]]

    for card in dict_file:
        date = card['date']
        lessons_list = card['lessons']
        date_block = [[f'{lessons_list[0]["day_of_week"].capitalize()}'], 
                [f'{date}'], [f'{lessons_list[0]["type_of_week"]}']]
        day_in_week = [date_block, [], [], [], [], [], [], []]
        max_len_line = 0
        for input_json in lessons_list:
            lesson_in_day = []
            input_data_list = [input_json['lesson_name'], 
                    input_json['type_of_lesson'], input_json['name'], 
                    input_json['room']]
            lesson_num = int(input_json['num'])
            for text in input_data_list:
                if len(text) > 25:
                    text_list = []
                    line = ''
                    letter_counter = 0
                    for letter_num, letter in enumerate(text):
                        letter_counter += 1
                        line += letter
                        if letter_counter > 25 and letter == ' ':
                            line = line[:-1]
                            text_list.append(line)
                            if len(line) >= max_len_line:
                                max_len_line = len(line)
                            line = ''
                            letter_counter = 0
                        if letter_counter > 25 and letter == '-':
                            line = line[:-1]
                            text_list.append(line)
                            if len(line) >= max_len_line:
                                max_len_line = len(line)
                            line = ''
                            letter_counter = 0
                        if letter_num == len(text) - 1:
                            text_list.append(line)
                            if len(line) >= max_len_line:
                                max_len_line = len(line)
                            line = ''
                            letter_counter = 0
                else:
                    text_list = [text]
                    if len(text) > max_len_line:
                        max_len_line = len(text)
                lesson_in_day.append(text_list)
            day_in_week[lesson_num] = lesson_in_day 

        days_in_week_list.append(day_in_week)

    letter_width = int(font_size * 6 / 10)
    letter_height = int(font_size * 72 / 60)
    gap = letter_width
    height_gap = int(font_size / 2)
    line_width = int(font_size / 20)

    all_raws = 0
    for day_in_week in days_in_week_list:
        rows = 0
        for lesson_in_day in day_in_week:
            rows_in_lesson = 0
            for lines in lesson_in_day:
                for line in lines:
                    rows_in_lesson += 1
            if rows_in_lesson >= rows:
                rows = rows_in_lesson
        all_raws += rows

    start_height = 0
    start_width = 0
    start_width_for_new_row = start_width

    # gets max len
    col_width_char = []
    for day_in_week in days_in_week_list:
        for num_of_col, lesson_in_day in enumerate(day_in_week):
            max_len_line = 0
            for text_list in lesson_in_day:
                for text in text_list:
                    if len(text) >= max_len_line:
                        max_len_line = len(text)
            col_width_char.append([max_len_line, num_of_col])

    max_col = 0
    for len_of_col, num_of_col in col_width_char:
        for len_of_col, num_of_col in col_width_char:
            if num_of_col >= max_col:
                max_col = num_of_col
    num_width_col = [] 
    for col in range(0, max_col + 1):
        max_width_per_col = 0
        for len_of_col, num_of_col in col_width_char:
            if len_of_col >= max_width_per_col and num_of_col == col:
                max_width_per_col = len_of_col
        num_width_col.append([col, max_width_per_col])

    # gen image
    font = ImageFont.truetype(font=f'{font_path}/mono.ttf', 
                                size=font_size)
    start_image_width = start_width
    final_image_width = start_image_width
    for day_in_week in days_in_week_list:
        image_width = 0
        for num_of_lesson, lesson_in_day in enumerate(day_in_week):
            max_len_line = 0
            for num, width_of_col in num_width_col:
                if num == num_of_lesson:
                    max_len_line = width_of_col
            image_width += gap + max_len_line * letter_width + gap
        if image_width >= final_image_width:
            final_image_width = start_width + image_width

    start_image_height = 0
    final_image_height = start_image_height
    for day_in_week in days_in_week_list:
        # image_height = 0
        rows = 0
        for lesson_in_day in day_in_week:
            rows_in_lesson = 0
            for lines in lesson_in_day:
                for line in lines:
                    rows_in_lesson += 1
            if rows_in_lesson >= rows:
                rows = rows_in_lesson
        final_image_height += letter_height * rows + height_gap
    if (final_image_width == 0 or 
        final_image_height == 0 or 
        len(days_in_week_list) == 1):
        return

    if mode == 'night':
        fill_color = 'white'
        image = Image.new('RGB', 
            (final_image_width,
            final_image_height), 
            (0, 0, 0))
    else:
        fill_color = 'black'
        image = Image.new('RGB', 
            (final_image_width,
            final_image_height), 
            (255, 255, 255))
    # draw text
    rows = 0
    idraw = ImageDraw.Draw(image)
    for day_in_week in days_in_week_list:
        for num_of_lesson, lesson_in_day in enumerate(day_in_week):
            height = start_height
            for text_list in lesson_in_day:
                for iteration in text_list:
                    idraw.text((start_width + gap, height), iteration, 
                            font=font, fill=fill_color)
                    height += letter_height
            rows = 0
            for lesson_in_day in day_in_week:
                rows_in_lesson = 0
                for lines in lesson_in_day:
                    for line in lines:
                        rows_in_lesson += 1
                if rows_in_lesson >= rows:
                    rows = rows_in_lesson
            # vertical line
            max_len_line = 0
            for num, width_of_col in num_width_col:
                if num == num_of_lesson:
                    max_len_line = width_of_col
            idraw.line(xy=(
                (start_width + gap + max_len_line * letter_width + gap, 
                start_height), 
                (start_width + gap + max_len_line * letter_width + gap,
                start_height + letter_height * rows + height_gap)), 
                fill=fill_color, 
                width=line_width)
            # horizontal line
            idraw.line(xy=(
                (start_width, 
                start_height + letter_height * rows + height_gap), 
                (start_width + gap + max_len_line * letter_width + gap, 
                start_height + letter_height * rows + height_gap)), 
                fill=fill_color, 
                width=line_width)
            start_width = start_width+gap+max_len_line * letter_width+gap
        start_width = start_width_for_new_row
        start_height = start_height + letter_height * rows + height_gap
    image.save(output_path)
