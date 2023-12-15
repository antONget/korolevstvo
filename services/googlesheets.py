import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd

gp = gspread.service_account(filename='resources/kingdom.json')
#Open Google spreadsheet
gsheet = gp.open("Kingdom")


#Select worksheet
client_sheet = gsheet.worksheet("Данные_клиентов")
start_sheet = gsheet.worksheet("/start")


# добавить значения
def append_client(ID, name):
    client_sheet.append_row([ID, name])


# поиск строки и столбца положения значения
def values_row_col(value):
    values = client_sheet.get_all_values()
    res = []
    for i, r in enumerate(values):
        for j, c in enumerate(r):
            if str(value) in c:
                res.append({'row': i, 'col': j})
    return res

# добавления значения
def update_phone(message):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"]+1
    if message.contact != None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    client_sheet.update(f'D{row}', phone)

# добавления значения
def update_birthday(message):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"]+1
    birthday = message.text
    client_sheet.update(f'C{row}', birthday)

# добавления значения
def update_zapros(message):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"] + 1
    zapros = message.text
    client_sheet.update(f'E{row}', zapros)

# добавления значения
def update_photo(message, photo):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"] + 1
    client_sheet.update(f'F{row}', photo)

def update_chekin(message):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"] + 1
    client_sheet.update(f'G{row}', '✅')

if __name__ == '__main__':
    values_row_col(value='anna')
