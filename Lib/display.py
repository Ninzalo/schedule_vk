def display_schedule(data: dict, subgroup: str, date: str) -> str:
    text = 'Ошибка'
    times_of_lesson = ['8:30 - 10:00', '10:10 - 11:40', '12:40 - 14:10', 
            '14:20 - 15:50', '16:20 - 17:50', '18:00 - 19:30']

    if data['date'] == date:
        lessons_list = [item for item in data['lessons']]
        new_list = []
        for _ in range(1, len(lessons_list) + 1):
            min_num = {
                'num': 1000
            }
            min_index = 100
            for entry in enumerate(lessons_list):
                if int(entry[1]['num']) < int(min_num['num']):
                    min_num = entry[1]
                    min_index = int(entry[0])
            new_list.append(min_num)
            lessons_list.pop(min_index)
        text = f"{data['date']}  "\
                f"{data['lessons'][0]['day_of_week'].capitalize()}\n\n"
        for entry in new_list:
            if entry['subgroup'] == subgroup or entry['subgroup'] == "":
                text += f'{entry["num"]} - '\
                        f'({times_of_lesson[int(entry["num"]) - 1]})\n'\
                        f'{entry["lesson_name"]} - {entry["type_of_lesson"]}'\
                        f'\n{entry["name"]}\n{entry["room"]}\n\n'
    return text.strip()
