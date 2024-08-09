import requests
import pandas
import customtkinter
from customtkinter import filedialog
from datetime import datetime, timedelta, date
import json

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('dark-blue')

client = customtkinter.CTk()
client.title('Client')
client.geometry('600x600')

def label_id_color(val, dict):
    color_code = ''
    if val:
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

def browse_file():
    try:
        file = filedialog.askopenfilename()
        file_path_result.delete('0.0', 'end')
        file_path_result.insert('0.0', f'{file}')
    except FileNotFoundError:
        file_path_result.insert('0.0', 'Please choose a file')
        

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_result.delete('0.0', 'end')
    folder_path_result.insert('0.0', f'{folder_path}')

def send():
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    file_path = file_path_result.get('0.0', 'end').strip('\n')
    folder_path = folder_path_result.get('0.0', 'end').strip('\n')
    keys_input = keys_entry.get().split(', ')
    current_date = date.today()
    api_url = 'http://127.0.0.1:8000/upload'
    try:
        files = {"file": open(f'{file_path}', 'rb')}
    except FileNotFoundError:
        result.insert('0.0', f'{timestamp}: Please choose a file to send\n')      
        return

    api_response = requests.post(api_url, files=files, verify=False)

    try:
        data_frame = pandas.DataFrame(json.loads(api_response.json()))
    except (requests.exceptions.JSONDecodeError, TypeError):
        result.insert('0.0', f'{timestamp}: Please choose a .csv file to send\n')
        return

    styler = data_frame.sort_values(by='gruppe').style

    if 'labelIds' in keys_input:
        styler.applymap(label_id_color, subset='labelIds', dict=data_frame.to_dict())

    if 'rnr' not in keys_input:
        keys_input.insert(0, 'rnr')

    if colored_checkbox.get() == 1:
        styler.apply(background_color, axis=1)
    
    try:
        styler.to_excel(f'{folder_path}/vehicles_{current_date}.xlsx', index=False, columns=keys_input)
        result.insert('0.0', f'{timestamp}: File saved to {folder_path}\n')
    except KeyError:
        result.insert('0.0', f'{timestamp}: Please input correct keys\n')
    except PermissionError:
        result.insert('0.0', f'{timestamp}: Please choose a folder to save the file\n')

frame = customtkinter.CTkFrame(master=client)
frame.pack(padx=50, pady=20, fill='both', expand=True)

keys_label = customtkinter.CTkLabel(master=frame, text='Keys:')
keys_label.pack(padx=10, pady=10)

keys_entry = customtkinter.CTkEntry(master=frame, width=500, placeholder_text='ex: gruppe, info, labelIds...')
keys_entry.pack(padx=10, pady=10)

colored_checkbox = customtkinter.CTkCheckBox(master=frame, text='Colored?')
colored_checkbox.pack(padx=10, pady=10)
colored_checkbox.select()

browse_button = customtkinter.CTkButton(master=frame, text='Choose File', command=browse_file)
browse_button.pack(padx=10, pady=10)

file_path_result = customtkinter.CTkTextbox(master=frame, width=500, height=10)
file_path_result.pack(padx=10, pady=10)

save_to_button = customtkinter.CTkButton(master=frame, text='Save to', command=browse_folder)
save_to_button.pack(padx=10, pady=10)

folder_path_result = customtkinter.CTkTextbox(master=frame, width=500, height=10)
folder_path_result.pack(padx=10, pady=10)

send_button = customtkinter.CTkButton(master=frame, text='Send', command=send)
send_button.pack(padx=10, pady=10)

result = customtkinter.CTkTextbox(master=frame, width=500, height=200)
result.pack(padx=10, pady=10)

client.mainloop()