import zipfile
import os
import zlib
from pathlib import Path
import shutil
import time

default_directory = Path(r'C:\Users\RU-PMiroshkin\PycharmProjects\pythonProject3\programms\Archives')
zip_content_path = Path(r'C:\Users\RU-PMiroshkin\PycharmProjects\pythonProject3\programms\Archives')
tmp_path = Path(r'C:\Users\RU-PMiroshkin\PycharmProjects\pythonProject3\programms\Archives\tmp')
image_directory = Path(r'C:\Users\RU-PMiroshkin\PycharmProjects\pythonProject3\programms\Archives\images')
backup_path = Path(r'C:\Users\RU-PMiroshkin\PycharmProjects\pythonProject3\programms\Archives\backup')
version_control = Path(r'C:\Users\RU-PMiroshkin\PycharmProjects\pythonProject3\programms\test.txt')

welcoming_phrase = 'Введите 1 для запуска программы\nВведите 2, чтобы узнать побольше об функционале скрипта: \n'
error_phrase = '\nВы ввели что-то непонятное, повторите ввод\n'
start_time = time.time()
image_to_count = 0
repository_to_exclude_list = []


def zip_file_arc(image_to_count):
    for file in zip_content_path.iterdir():

        if file.name not in repository_to_exclude_list:
            pass
        else:
            print(f'Архив {file.name} был исключен пользователем и будет пропущен\n')
            continue

        if file.suffix == '.zip' or file.suffix == '.rar':  # Проверяем, является ли файл архивом
            print(f'Работаем с архивом {file.name}')
        else:
            continue

        print('\nЧистим папку tmp')
        list_image_names = []
        file_to_create, file_extension = os.path.splitext(file)
        file_to_count = Path(file_to_create)

        for file_to_delete in tmp_path.iterdir():
            os.remove(file_to_delete)

        try:
            with zipfile.ZipFile(file, 'r') as zip_tmp:
                print('Разархивируем картинки в папку TMP...')
                zip_tmp.extractall(tmp_path)
        except zipfile.BadZipFile as BadZip:
            print(f"Архив {file.name} поврежден или не является zip архивом и будет пропущен\n"
                  f"Ошибка {BadZip}")
            continue
        except zlib.error as ZlibError:
            print(f"Архив {file.name} поврежден или не является zip архивом и будет пропущен\n"
                  f"Ошибка {ZlibError}")
            continue

        print(f'Делаем бэкап архива {file_to_count.name}')
        shutil.copy2(file, backup_path)
        os.remove(file)
        print('Проверяем, нужно сделать подмену картинки')

        for list_img in tmp_path.iterdir():
            list_image_names.append(list_img.name)

        for image in image_directory.iterdir():
            image_name = image.name
            if image_name in list_image_names:
                image_to_delete = os.path.join(tmp_path, image_name)
                os.remove(image_to_delete)
                print(f'Делаем подмену картинки {image_name}')
            if image.suffix == '.png':
                dest_path = os.path.join(tmp_path, image_name)
                shutil.copy2(image, dest_path)
                image_to_count += 1
                print(image_name, f'скопирована в архив {file_to_count.name}')

        print('Создаем новый архив', file_to_count.name, '\n')
        shutil.make_archive(file_to_create, 'zip', tmp_path)
    end_time = time.time()
    full_time = end_time - start_time
    print(f'\nСделано {image_to_count} копий картинок для всех архивов за {round(full_time)} секунд.')
    print('\nПрограмма успешно выполнено, можно закрывать консоль')
    time.sleep(120000)


# Создание менюшки для выбора папок для картинок
def folder_finder():
    folder = 0
    my_list = []
    for file in default_directory.iterdir():
        if os.path.isdir(file):
            my_list.append(file.name)
    for names in my_list:
        folder += 1
        print(folder, names)
    return my_list


# Создание менюшки для выбора архивов
def repository_finder():
    repository = 0
    repository_list = []
    for file in zip_content_path.iterdir():
        if file.suffix == '.zip':
            repository_list.append(file.name)
    for names in repository_list:
        repository += 1
        print(repository, ':', names)
    return repository_list


# Запуск скрипта
def start_script():
    print('Добро пожаловать в скрипт по упаковке картинок!')
    user_input = input(welcoming_phrase)
    flag = True
    rep_flag = True
    changelog = version_control.read_text()
    return user_input, flag, changelog, rep_flag


user_input, flag, changelog, rep_flag = start_script()

# Выбор пути для архивов
while flag:
    if user_input == '1':
        zip_input = input(f'Введите 1 если используем стандартный путь {zip_content_path.name}\n'
                          'Введите полный путь к архивам, куда нужно копировать картинки\n'
                          'Введите Q, если хотите вернуться в главное меню: \n')
        if zip_input == '1':
            print(f'\nПуть, откуда будем брать архивы: {zip_content_path}')
            break
        elif os.path.sep in zip_input:
            zip_content_path = Path(zip_input)
            print(f'Путь, откуда будем брать архивы: {zip_content_path}')
            rep_flag = False
            break
        elif zip_input.lower() == 'Q' or zip_input.lower() == 'Й':
            user_input = input(welcoming_phrase)
        else:
            user_input = '1'
            print(error_phrase)
    elif user_input == '2':
        print('\n', changelog, '\n')
        user_input = input(welcoming_phrase)
    else:
        user_input = input(error_phrase)

repository_choice = input(f'Введите 1, если будем копировать картинки во все репозитории в папке '
                          f'{zip_content_path.name}\nВведите 2, если необходимо исключить репозитории из списка\n')

# Выбор исключения для репозитория
while rep_flag:
    if repository_choice == '1':
        print(f'\nКопируем картинки во все репозитории по пути {zip_content_path.name}')
        break
    elif repository_choice == '2':
        repository_list = repository_finder()
        repository_to_exclude = input('Выберите номера репозиториев, которые необходимо исключить'
                                      '\nВведите Q для возврата на предыдущий шаг\n')
        if repository_to_exclude.isalpha():
            print(error_phrase)
            repository_choice = '2'
        elif repository_to_exclude.lower() == 'Q' or repository_to_exclude.lower() == 'Й':
            repository_choice = input(f'Введите 1, если будем копировать картинки во все репозитории в папке '
                                      f'{zip_content_path.name}\nВведите 2, если необходимо исключить репозитории из списка\n')
        else:
            repository_to_exclude_list.append(repository_list[int(repository_to_exclude) - 1])
            print('В исключения добавлен репозиторий:', repository_list[int(repository_to_exclude) - 1])
            repository_to_exclude = input('Введите 1, если указаны вы исключили все необходимые репозитории\n'
                                          'Введите 2, если необходимо продолжить исключение репозиториев\n')
            if repository_to_exclude == '1':
                print(f'Исключаем репозитории: {repository_to_exclude_list}')
                break
            elif repository_to_exclude == '2':
                repository_choice = '2'
            else:
                print(error_phrase)
                repository_choice = '2'
    else:
        repository_choice = input(f'Введите 1, если будем копировать картинки во все репозитории в папке '
                                  f'{zip_content_path.name}\nВведите 2, если необходимо исключить репозитории из списка\n')

# Выбор пути для картинок
while flag:
    if user_input == '1':
        image_input = input('\nВведите полный путь, откуда копируем картинки\n'
                            'или введите 1, если будем выбирать из папок в директории скрипта Delivery Images: \n')
        if image_input == '1':
            break
        elif os.path.sep in image_input:
            image_directory = Path(image_input)
            for image in image_directory.iterdir():
                print(f'В папке найдены картинки - {image.name}')
            time.sleep(2)
            print(f'Копируем из папки {image_directory}...')
            print('Начинаем работу...')
            time.sleep(3)
            zip_file_arc(image_to_count)
            break
        else:
            print(error_phrase)
    else:
        print(error_phrase)

# Выбор существующих папок для картинок
while flag:
    try:
        if user_input == '1':
            print('\nДоступные директории, откуда можем скопировать картинки: ')
            list_final = folder_finder()
            directory_input = input('\nВведите номер папки: \n')
            if directory_input.isalpha():
                print(error_phrase)
                user_input = '1'
            else:
                image_directory = default_directory / list_final[int(directory_input) - 1]
                print('\nВ папке найдены картинки:')
                for image in image_directory.iterdir():
                    print(f'{image.name}')
                print(
                    f'\nВыбранная папка: {image_directory} \n\nПодтвердите ввод, нажав клавишу 1, или нажмите любую клавишу, '
                    'чтобы вернуться к выбору папки')
                directory_input = input()
            if directory_input == '1':
                print('\nПрограмма начинает работу...\n')
                zip_file_arc(image_to_count)
                flag = False
                print(error_phrase)
                user_input = input()
        else:
            print(error_phrase)
            user_input = input()
    except IndexError:
        print(error_phrase)
        flag = True
