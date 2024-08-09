from fastapi import FastAPI, File, UploadFile
import pandas
import os
import requests
import json

app = FastAPI()

@app.post('/upload')
def upload(file: UploadFile = File()):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {'message': 'There was an error uploading the file'}
    finally:
        file.file.close()

    if not file.filename.endswith('.csv'):
        os.remove(f'{file.filename}')
        return {'message': 'You must upload a .csv file'}

    data_frame = pandas.DataFrame(pandas.read_csv(f'./{file.filename}', sep=';', index_col=False).to_dict())
    access_token = baubuddy_login()
    baubuddy_resources(access_token)
    resourses_data_frame = pandas.DataFrame(pandas.read_csv('./response.csv', sep=';', index_col=False).to_dict())
    merged_data_frames = pandas.merge(data_frame, resourses_data_frame, how='right')
    filtered_data_frame = merged_data_frames[merged_data_frames['hu'].str.len() > 0]
    filtered_dict = filtered_data_frame.to_dict()
    dict_with_color_codes = add_color_codes_to_dict(filtered_dict, access_token)
    result_data_frame = pandas.DataFrame(dict_with_color_codes)
    os.remove(f'{file.filename}')
    os.remove('response.csv')
    return result_data_frame.to_json()


def baubuddy_login():
    login_url = "https://api.baubuddy.de/index.php/login"
    login_payload = {
        "username": "365",
        "password": "1"
    }
    login_headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    login_response = requests.request("POST", login_url, json=login_payload, headers=login_headers)
    dict_response = login_response.json()
    access_token = dict_response['oauth']['access_token']
    return access_token

def baubuddy_resources(access_token):
    resources_url = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'
    resources_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"    
    }

    resources_response = requests.request("GET", resources_url, headers=resources_headers)
    data_frame = pandas.DataFrame(resources_response.json())
    data_frame.to_csv('response.csv', sep=';', index=False)

def label_id_color_code(val, access_token):
    color_code = ''
    resources_url = f'https://api.baubuddy.de/dev/index.php/v1/labels/{val}'
    resources_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"    
    }

    resources_response = requests.request("GET", resources_url, headers=resources_headers)
    data = resources_response.json()
    color_code = data[0]['colorCode']
    if color_code:
        return color_code

def add_color_codes_to_dict(dict, access_token):
    color_codes = {}
    for val in dict['labelIds'].keys():
        if dict['labelIds'][val] > 0:
            color_codes[val] = label_id_color_code(int(dict['labelIds'][val]), access_token)
        else:
            color_codes[val] = None
    dict['colorCodes'] = color_codes
    return dict
