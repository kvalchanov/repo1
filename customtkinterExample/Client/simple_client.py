import requests
import pandas
import json
from os import path
from datetime import datetime, timedelta, date

def label_id_color(val, dict):
    color_code = ''
    if val > 0:
        color_code = dict['colorCodes'][val]
    if color_code:
        return f'color: {color_code}'

def background_color(row):
    green_style = 'background-color: #007500;'
    orange_style = 'background-color: #FFA500'
    red_style = 'background-color: #b30000'
    green = timedelta(days=90)
    orange = timedelta(days=364)
    red = timedelta(days=365)
    hu = pandas.to_datetime(row.hu)
    if datetime.now() - hu <= green:
        return [green_style]*len(row)
    elif green < datetime.now() - hu <= orange:
        return [orange_style]*len(row)
    elif datetime.now() - hu >= red:
        return [red_style]*len(row)


timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
keys_input = input('Please enter keys: ').split(', ')
filename = input('Please enter file name: ')

while True:
    if not filename.endswith('.csv'):
        filename = input('Please enter a valid .csv file: ')
    else:
        break

folder_path = path.dirname(__file__)
current_date = date.today()
api_url = 'http://127.0.0.1:8000/upload'

while True:
    try:
        file_path = f'{path.dirname(__file__)}/{filename}'
        files = {"file": open(f'{file_path}', 'rb')}
        break
    except FileNotFoundError:
        filename = input('Please enter a valid file name: ')
        
api_response = requests.post(api_url, files=files, verify=False)
data_frame = pandas.DataFrame(json.loads(api_response.json()))
styler = data_frame.sort_values(by='gruppe').style

while True: 
    if 'labelIds' in keys_input:
        styler.applymap(label_id_color, subset='labelIds', dict=data_frame.to_dict())

    if 'rnr' not in keys_input:
        keys_input.insert(0, 'rnr')

    if '-c' in keys_input:
        styler.apply(background_color, axis=1)
        keys_input.remove('-c')

    try:
        styler.to_excel(f'{folder_path}/vehicles_{current_date}.xlsx', index=False, columns=keys_input)
        print(f'{timestamp}: File saved to {folder_path}')
        break
    except KeyError:
        keys_input = input('Please enter valid keys: ').split(', ')

