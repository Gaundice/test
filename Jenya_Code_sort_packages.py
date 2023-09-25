
from pathlib import Path
import datetime
import shutil

needed_day = datetime.date.today() + datetime.timedelta(days=1)
needed_day_str = needed_day.strftime('%Y%m%d')
packages_source_path = Path(r'd:\NEW_PACKAGES')
packages_destination_path = Path(r'd:\Temp\PMiroshkin\dev\sorted_packages')
store_numbers = input('Введите номера ПБО для отправки\n').split('+')
final_list = []

for file in packages_destination_path.glob("*"):
    file.unlink()

for package in packages_source_path.iterdir():
    if needed_day_str in package.name and package.name[6:11] in store_numbers:
        shutil.copy2(package, packages_destination_path)