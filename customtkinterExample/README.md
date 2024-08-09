The API uses FastAPI and consist of just one '/upload' endpoint, which receives the csv file, get resources, merges them, filters and resolves color codes.

There are two clients. One is very simple console client. The .csv file needs to be in the same directory as the client and the end result .xlsx file is saved in the same directory. The keys need to be entered seperated by a ', ' (gruppe, info, labelIds). If '-c' is entered as a seperate key in the keys sequence the 'colored' flag will be True and the .xlsx file will be colored.

The other client is a bit more complex. It uses the customTKInter library for a simple UI. Keys are entered in a string seperated by ', ' (gruppe, info, labelIds). There is a checkbox for the 'colored' flag. A browse button to choose the .csv file to send, another one to choose where to save the .xlsx file and an output text field at the bottom.
