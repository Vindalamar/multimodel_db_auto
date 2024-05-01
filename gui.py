# hello_psg.py
from datetime import datetime


import PySimpleGUI as sg
import couchbar
import json
import postegue
import neo


def neohi():
    direc = neo.find_direc()
    admin = neo.find_admin()
    wash = neo.find_washer()
    layout = [[sg.Text("Директора:", font="Helvitica 10 bold")],[sg.Text(d.data()['n']['name']) for d in direc], [sg.Text("Администраторы:", font="Helvitica 10 bold")], [sg.Text(a.data()['n']['name']) for a in admin],
              [sg.Text("Мойщики:", font="Helvitica 10 bold")], [sg.Text(w.data()['n']['name']) for w in wash], [sg.Button("Назад")]]
    window = sg.Window("Title", layout, finalize=True, size=(600, 335))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Назад":
            break
    window.close()


def table(name):
    data = postegue.open_table(name)
    headings = postegue.get_headings(name)
    text = '{'
    for x in range(1, len(headings)):
        text += f'"{headings[x]}" : {x},'
    if name == 'orgs':
        text = '{'
        for x in range(len(headings) - 1):
            text += f'"{headings[x]}" : {x},'
    text = text[:-1] + "}"

    layout = [[sg.Table(data, headings=headings, justification='left', key='-TABLE-')],
              [sg.Multiline(text, key='-ADD-', expand_x=True, expand_y=True, enable_events=True, justification='left' , no_scrollbar = True),
              sg.Button("Добавить")],
              [sg.Text('Удаление по id:'), sg.Push(), sg.Input(key='-DELETE-'), sg.Button("Удалить")],
              [sg.Text('Изменение по id:'), sg.Multiline(key='-MOD_ID-', size=(2, 1), no_scrollbar = True),
               sg.Multiline(text, key='-MOD-', expand_x=True, expand_y=True, enable_events=True, justification='left', no_scrollbar = True, size=(20, 0)),
               sg.Button("Изменить")],
              [sg.Button("Назад")]]
    window = sg.Window("Title", layout, finalize=True, size=(600, 335))


    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Назад":
            break
        while event == "Добавить":
            try:
                js_txt = json.loads(values["-ADD-"])
            except Exception as e:
                sg.popup("Что-то не так с форматом", title='Bad auth')
                break
            res = postegue.insert_into(name, js_txt)
            sg.popup(res, title='Bad auth')
            window.close()
            table(name)
            break

        if event == "Удалить":
            id_name = headings[0]
            if name == 'orgs':
                id_name = headings[-1]
            res = postegue.delete_from(name, id_name, values["-DELETE-"])
            sg.popup(res, title='Bad auth')
            window.close()
            try:
                table(name)
            except Exception as e:
                break

        while event == "Изменить":
            id_name = headings[0]
            if name == 'orgs':
                id_name = headings[-1]
            try:
                js_txt = json.loads(values["-MOD-"])
            except Exception as e:
                sg.popup("Что-то не так с форматом", title='Bad auth')
                break
            res = postegue.modify(name, id_name, values["-MOD_ID-"], js_txt)
            sg.popup(res, title='Bad auth')
            window.close()
            table(name)
            break

    window.close()


def zapros_table(data, head):
    layout = [[sg.Table(data, headings=head, justification='left', key='-TABLE-', def_col_width=30)], [sg.Button("Назад")]]
    window = sg.Window("Title", layout, finalize=True, size=(500, 335))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Назад":
            break
    window.close()


def zapros():
    layout = [[sg.Button("Автомобили с организацией"), sg.Input(key='-org_name-')],
              [sg.Button("Доставки опред. товара"), sg.Input(key='-ad_name-')], [sg.Button("Авто по услуге"), sg.Input(key='-us-')], [sg.Button("Рабочие боксы")],
              [sg.Button("Авто по клиенту"), sg.Input(key='-auto-')], [sg.Button("Бокс по номеру авто"), sg.Input(key='-box-')],
              [sg.Button("Организации по номеру авто"), sg.Input(key='-or_num-')],
              [sg.Button("Услуга по номеру авто"), sg.Input(key='-usnum-')], [sg.Button("Какие дни сотрудник работал"), sg.Input(key='-work-')],
              [sg.Button("Клиент по номеру авто"), sg.Input(key='-kus-')],
              [sg.Button("Назад")]]

    window = sg.Window("Demo", layout)

    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED or event == "Назад":
            break

        if event == "Автомобили с организацией":
            data = postegue.select_org(values["-org_name-"])
            zapros_table(data[0], data[1])
        if event == "Доставки опред. товара":
            data = postegue.select_ad(values["-ad_name-"])
            zapros_table(data[0], data[1])
        if event == "Авто по клиенту":
            data = postegue.select_auto(values["-auto-"])
            zapros_table(data[0], data[1])
        if event == "Авто по услуге":
            data = postegue.select_us(values["-us-"])
            zapros_table(data[0], data[1])
        if event == "Бокс по номеру авто":
            data = postegue.select_box(values["-box-"])
            zapros_table(data[0], data[1])

        if event == "Рабочие боксы":
            data = postegue.select_red()
            zapros_table(data[0], data[1])

        if event == "Организации по номеру авто":
            data = postegue.select_or_num(values["-or_num-"])
            zapros_table(data[0], data[1])

        if event == "Услуга по номеру авто":
            data = postegue.usnum(values["-usnum-"])
            zapros_table(data[0], data[1])

        if event == "Какие дни сотрудник работал":
            data = postegue.selec_work(values["-work-"])
            zapros_table(data[0], data[1])

        if event == "Клиент по номеру авто":
            data = postegue.select_kauto(values["-kus-"])
            zapros_table(data[0], data[1])

    window.close()

def main_menu():
    layout = [[sg.Button("доп. товары"), sg.Push(), sg.Button("Запросы")],
              [sg.Button("боксы")], [sg.Button("клиенты")], [sg.Button("клиентская история")],
              [sg.Button("доставки")], [sg.Button("машины организаций")], [sg.Button("организации")],
              [sg.Button("услуги")],  [sg.Button("сотрудники"), sg.Push(), sg.Button("Иерархия")], [sg.Button("график сотрудников")],
              [sg.Button("химия")], [sg.Button("категории машин")], [sg.Push(), sg.Button("Закрыть")]]

    # Create the window
    window = sg.Window("Demo", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED or event == "Закрыть":
            break
        if event == "Иерархия":
            neohi()
        if event == "доп. товары":
            table("ad_goods")
        if event == "Запросы":
            zapros()
        if event == "боксы":
            table("boxes")
        if event == "клиенты":
            table("customers")
        if event == "клиентская история":
            table("customers_autos")
        if event == "доставки":
            table("deliveries")
        if event == "машины организаций":
            table("org_autos")
        if event == "организации":
            table("orgs")
        if event == "услуги":
            table("services")
        if event == "сотрудники":
            table("workers")
        if event == "график сотрудников":
            table("workers_at_boxes")
        if event == "химия":
            menu_docs(True)
        if event == "категории машин":
            menu_docs(False)

    window.close()



def menu_docs(check):
    new_cb = couchbar.cb_auto
    text = '{\n "id": 1, \n "type": "", \n  "name": "" \n }'
    if check:
        text = '{\n "id": 1, \n "name": "", \n "company": "", \n "description": "" \n \n}'
        new_cb = couchbar.cb_chime

    layout = [[sg.Text('Поиск:'), sg.Push(), sg.Input(key='-KEY-'), sg.Button("Найти")],
              [sg.Text('Добавление:'),
               sg.Multiline(text, key='-ADD-', expand_x=True, expand_y=True, enable_events=True, justification='left')],
              [sg.Button("Добавить или изменить")],
              [sg.Text('Удаление:'), sg.Push(), sg.Input(key='-DELETE-'), sg.Button('Удалить')],
              [sg.Button('Назад')]]

    # Create the window
    window = sg.Window("Demo", layout, size=(600, 300))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        if event == "Назад":
            break
        if event == "Найти":
            res = couchbar.get_airline_by_key(values["-KEY-"], new_cb)
            sg.popup(res, title='Bad auth')

        while event == "Добавить":
            try:
                ccc = json.loads(values["-ADD-"])
            except Exception as e:
                sg.popup(e, title='Bad auth')
                break
            res = couchbar.upsert_document(ccc, new_cb)
            sg.popup(res, title='Bad auth')
            break

        if event == "Удалить":
            res = couchbar.remove_doc(values["-DELETE-"], new_cb)
            sg.popup(res, title='Bad auth')

    window.close()


def auth():
    layout = [[sg.Text('Username:'), sg.Push(), sg.Input(key='-USER-')],
              [sg.Text('Password'), sg.Push(), sg.Input(password_char='*', key='-PW-')],
              [sg.Button('Login', bind_return_key=True), sg.Button('Quit')]]
    window = sg.Window('Login', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        if event == 'Login':
            if values["-USER-"] == "admin" and values["-PW-"] == "password":
                window.close()
                main_menu()
                break
            else:
                sg.popup("Wrong username or password", title='Bad auth')
    window.close()


if __name__ == '__main__':
    auth()
