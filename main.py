'''
programa UpdateDB para multielectrico, codigo parchado y ajustado a la necesidad. no se esperan modificaciones o que se trate como material de analisis. 
De ser posible recomiendo rehacer el mismo siguiendo las pautas indicadas en el nicho e indiferentemente de lo que se llegue a necesitar en un desarrollo posterior, 
espero que este, mi primer programa sirva como una guia mas bien de lo que no se debe de hacer.

'''


# Importar librerias
from pathlib import Path
from datetime import date, datetime
from glob import glob
from os import mkdir, popen, remove
from os.path import basename, getmtime, split
from shutil import copy
import sys
from threading import Thread
from tkinter import (BOTH, DISABLED, END, NORMAL, SINGLE, Button, Canvas, Entry, IntVar, Label, Listbox, PhotoImage, Radiobutton, Scrollbar, StringVar, Text, Tk, W)
from tkinter.filedialog import askdirectory as askdir
from tkinter.filedialog import askopenfile
from tkinter.messagebox import NO, askokcancel, askyesnocancel, showerror, showwarning
from tkinter.ttk import Treeview
from xml.dom import minidom
from idlelib.tooltip import Hovertip
import requests
from genericpath import exists, isfile
from MySQLdb import connect
from watchdog.events import *
from watchdog.observers import Observer
import base64
# Definicion de constantes
GETDATE = datetime.fromtimestamp

# Definicion de variables
global files, switch, attCounter, conn_st, F_0stop
files = ""; switch = False; attCounter = 0; conn_st = False; F_0stop = None
global first, slopes, active, pause; first = True; slopes = {}; actieve = False; pause = False
global S_Files, S_DBa

# Valores para crear los iconos
b_b_bookmark = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACRElEQVR4AW2TA4w3SRTEfz1/nm2bf5xt+y52zrYVnRWezeBsfbZt21rvzkzrm5fOeiepqdeqrnqZUd57bnzky5My/tFDA55zPR7vQV6BfBec1eikafnIb144EiBP2HC3h+MrJx6qNm1uknPhgDDCDu+gsamNjsTjfP4IALoE4MLKiYeoS6qHcOgBFXxQwMlBYecR3mf3HdmxnOe8m+6llwDe71E56TD+nbKEhoZ2vHMAuE4Xws7T2NxOnKTQ9XRFQOWLeY45+TCO3m9PrEVsy81ZncE5TFZ3xJoffhoxkIBsdKzc1EwxKhDHMTpJMS7MG3LkC0X23qkkrgYQAJxstJokSbjlzKODfeiK8NXwBehyQcYDO9DWYbXB2IjvRswjkVrsG3GgKBSLpCY0dUABYxyp1qQOfFRCFQoQeZySXjhSqzL0F4iCAGhjMbEh0ZbYZMhYXCQm4zRD+zjWrnmHI477j8qlm7j2udqLvR1Yh060CIQ41iM3Gqk7xnDgfvM47YSzOHjPYxg+9zcmzBn98tkPHrh71DOCToOAZO0QFhdZ3d4ylPrxNWxkqR1wBVZpzq6cC/BA1PnBpBIhkQgOsa+1C/YTS0PrRgpqZ2484SEAnrjsE47atwpQ7uqBWLaSVQfEkj9xpKljW3MDc9eN443BtwHwxqDbWLppFkDc1QOiiDPOquKVQsRMBhcYldzMhFn/cW71fP6c/QFFlWfMjJEA7ys5fNHt73+W0R3hzxMQGClCTXkklKaDSgFagA8mvLfu2e0EQs+EWyEy7gAAAABJRU5ErkJggg=="
b_b_drop = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACRElEQVR4AWL4//8/RRhDANA5OTDJDQdw9LPUtm0rd9nz2q7dZGvbtm3bttfGtGsXv7N9mXnDvPe3RaVqYpYrKL1cqtUJBaGfQl7oh4Cl/SrIoT7zM5vUGLAqVaRRLnf83rQW8Ud3kfj0GolXjxG+fBKWSWJ8YJOOtyyCLOuUk00yeTh45iT+6b4jefMskoc2ILlnFf6c2I2/z27CPXcSXueMDb/MHEmWC5iVysZ5sj107BD+aT8juXMZ/Bs0CKydg/hmDRIbacRXz0D86nFY1QI8yxhmf5I+qHFJIE+mPYso/P38pmDE2CYa3pXTEV2sLEdotgDxc4fxfkJ/PGT0p0sCBrlEGzl3BMlTe+BfPRO/OIwqCc4UILx2AdyaWbhP9taWBLQyYTRx4xySmzTwL5mE6j531jh45WwE9mzF3QndoyWBnwJONHbqAOJLJyG6UFpjwCNmIrB7K24TnUsD3/hMrXf1AsQ20AhNZeX/WDU5E+BfNBeWudNxc0z70iV85mbS2vQxiJ46CL8wHV5xaiXZkTkWjuxURA7tw2OiK66Pbl26iR85jMbveKTdquAhcvpAwYZ5mEShmDUejvSxeRAIH9yLr1xGvmy/MqZV6THm8yZ7HPkqa1TYJGIicvQAfEtpuAU5cLKy4F1MIbx/L76xUnBtdJtwnkxWeZWfZw4nn6YNdrxO7QvXnOnwblxXgG3WZDwY1yVfdpTK1TymR4wBTR4Svam7ZE/tnZRuodtjOoauj2+vvTa2DXVlZIvqHlPDyQUd0s650Sy/tQAAAABJRU5ErkJggg=="
b_b_empty = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAB0ElEQVR4AZyTA49cURiG70/ZGO0PqRVUQW3btsa8ahqubXvHwdrW2J6v59xk7PmS5/h9Zq6IaAlEvN5vPz5DIeCzRGrhDbvdDkajMcbu7m4aOzs7nCQWLDvw9e153ii3uLW1BVNTUzA5OZnExMQEx+zsLMzPz3NncQZnCTygOhfgxaunMDMzA93d3Ul0dXXF6O3thb6+PnwWZzhJTHDk7A1QqVRAUVQMkiQzgc+mC/ae+AJ7jqeD1zOQLjj1Q10UaYIiSRc8YA1FEROU7f/ahwelgLNEtG7fuQE6nTZw7fplV2VVhf/O3VuR2rqa4O07N8P1DXWB+w/uhBsbG4J3790KE5nq8ZMHgTHVqPHlm+fbDMvs8Hh/PNU11eZfv3/Za2prtt6+ewWtba3GZ8+fuDMKvn3/bFVrVP8+f/u4PTQ0tIN6m0arNlI0uY1eniUsWFtbdfz+89OWFubxfymQwOTxeIIkpYCq6kpAgq3FpUUzw1IjOr12TknK8fdhkyukmzKZ5GqqIBwIBEAmF/uRYBJhlSulYLGY7TKFWEMzJGAB+nVAtSgU8brS/oFILIDauurYVyYU84H9S4eVlHwjuvZ/y1csTa+tqz4JNGwJTAwAUh9vVhiI0RwAAAAASUVORK5CYII="
b_b_export = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAByUlEQVR4AaSTQ7xXURDHf9c327ZtLcMm2162y7b3LbPrcZ1dm2y7Z+tguvM+f2Z8DwbHGIOI8D8YBy9mryXCQkW6sdYaSgOSpWKdIAMZLQpKUuDXtwD03TKjDWxNtGh83yq18ResP/68a1i3ldY8GMkv90NqCakkhA6KElEZ+MJtywdsgRDKi5mAwEzrOB9/QmGJhJAKYWw+K3P0chr+hFG9a6IsdgK+nDBTB9fFiStfMGlQPYQ5ff0LxveP2hl5JfE7EEpDE8G2gs7X0mBZJhKup8EwgSCDSb6ZBhDBsYEOjSqiTChE2J38jnKLyijhRhoxSSxjOHXtc5z97EMuDdnYjyZuvYrAhLEt4Q0dPjcMYTzfg1fBhV/RAxfW2ef6DhzXwZIee7Bw33CEGGELqcGMmzAOTGWnEqq4VVHFqxqyK6OiUxGWaWH9wbVYeGc4mjdtCtdx8PTFi8M2/zom4VTCb3fQtlvLuB1cXHO9NlYeekJZ+aV09m46MefusYwSXGyc/fhtTvkdzN4duoMl+x/R8rEtQv+ei2YZiYUfseXYAw3AOrBkIH8kurLh6LPuZUpX4vfloqSGKJ9I4kfk5JekhnXj6yjNzgDJilEHxeVEjwAAAABJRU5ErkJggg=="
b_b_import = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAB80lEQVR4AaSSA8weMQBA32G2bdu2bSMYo9nBrGjxbNu2bdu2ecXaLPfjC6Z3V7evdLTW/A/+ooPvRhhHD6lVZqUUUoGwqbR5jTBpdJBIoU29Ojm+c56yWIHSunersklS8+cwavmtomHeNzY7mPV35iOUQEhBoEyQQXRq6sK2YRXGEwQyXgyBxtKxYDf+hM/fjFRIogVSYVl66AV/QtPSKfkRU2APJ6RD5bSsOPyctpXSEbL62HNalY8uv/rwLfYKAiNQWuN7sProCzzPZc2xFzgumN/C+hMvQGvi+FAgU0J+BBFb0DbjObQom8Z0fknDaUOJM2duuAKalU1LyK0nHxBCxV6BVibjwqbTL6kzqisyYQK2m7yleqtKvE2cCC9ZYrzkScmcLCmLTV72W6rdBPGMwNi01jQpnYb3JcvzNn9mvPgetcb0xDWiT0CigT1wEiTASZQQjMwx9cSPB6s34ttXZ9l5/hXO3E2U7lzfDIzP7ilrsVQ4UIHPk2aGKzCpCSbvGhF2BUIINL+2UKNIavYt3UaxNnVoXCoNljWrj9KyfBpCrj98z8QVV5g3sIITfQZaUzhrYp6++UqudAl4t/cgrx9/wD6yQpniYgfFRCmtYtyCPjx66c3iP6RKZO/XBikUVmyf7s9hAx8+/9gMY1OcnQEDBxOf4tVcwwAAAABJRU5ErkJggg=="
b_b_search = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAB4UlEQVR4AaRQtUEEQRR967i7t0GCptcABRBRz3VyKVoI7u6MfGFucYsY12eRquI/5R1gY4tjEakSa4WZh4gFnviQiGve89LCZI/8CbBe/8yy0l7odGdThDRWIDRDir1zg92zp3VPNLc4P/IDJAYAZqm2FTLd1xLBeMb5PeMk9EcnmOhtRF97Nm0dVQHgV4Ags9LVGOHO1j8pSBTMioewvnxiDHc3IgBU/gQIXoeSGOVnlnoHqJwDiBXkWQLnaAi/lBQAnCeIZuUnEYD1Y9ZyBmx486eCgH5ovITwoldmvM9ZGuHReJBzp38DeKptnzyitYiRJxH4VUkRPnc0JnjelbtvGMS/XhDY2+qjjs0AUABl33/x5eDVhx8YgN5lEONlAYY8CwMbMDpPXXvB8OXtCwZnqZccP39+O7Khwkoda0KasPkeEzCupwITjc8vYKD++f0XFLjPRb5f/eXEf1lRRtOM4dnN0wy3zux68/v3D5uYKddvwg3AB3Y0uLL9+vVjuYicRpC8liXD4xsnGa6d2fkmadYDUYgXCACPht2/gE6PfHDt+LobZ3YwiMkoAwP9pwiaFwiD+enKbH/+/FzOzMoe9O3L+46cJe8q4QYQC6bFiTL//ftHPHfp+2coLqAEAACbiTqbKsCMvAAAAABJRU5ErkJggg=="
pause = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wD/AP83WBt9AAAAtElEQVR4AWL8//8/AymAAg1pcx79/vXv528g+rO2RA2LCBgwwbV+//5PW47DUYcXQPcYcCAAxkCUBEH//zcGqS9tt223BmTYAI/3zg5qI0P4wuBpzo/YQqbQGbGC8yAXMoXOqKU638KFTOEleb9d4BniG+m7/hfAo9kBCjcyFjrzeJpFFWwjQ+gMkBYszYVMoTNhRJDCjUxB052eLI+FzKc789uxfc//Ax3w/z8WERigfWoFACaxEqKJ7Q1bAAAAAElFTkSuQmCC"
b_s_reload = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAB1klEQVR4AbWTA5YcARBAc445QGzbXNu2bdu2bdu2jb7MvJ9BuGbjofDLV4Bz/ZcDcBmzdHQaMhPs+02w6TbEsl1PMG3WdjwW4DZhJXIZtViMnQuifDOHBqGM2p0S8lfS8BtwQ69SdVGrVFF0KMBZ4py0EEGjUE7FVj4120VUbRVSuJZByXoO/n3uqOV/WzwQ4Dxi4Rg9G0j9rjxq2Xou4WO+hAx5k7uUQuFqJnmSTOwbzfmW+t5xH8BhwFQoXs+ibCNHFs24QVOsX6MWoVOuHKFRpCBOno0hazGJqLFgPsW/FvYBbHqMJOkWUbGZT8iID/rVahG/dSq5X30VMj7yNfkdH+Nf8TbqOfsAkk5LGpcnix444IF2mdIfwI/0jxw7RtMmbSFjPp7MxUQyFhJRK/guVsr+XCPVfUl6y4fYlxwJMKxVd/TotidnKUUGSV2Iw7rWmM+JbzAp08OgWIsXwY84cg80ixUW3TvsSZ2PJWoqmPiZCGKnQomaDCFiIhDNHGUeeN7mUIBK3leRQuanRctqQwIHvYmWOQYRNu5PyKgvqhkK3HG5sQ+w75d02lHS6c1XoU94FvgA9SwlVNJ/SJyvc6Zjuud+i9vO+5xPDrjtdO3QMf4EDtK86uthiPsAAAAASUVORK5CYII="


# Variables contenedoras para el correo
global e_to; e_to = ""
global e_host; e_host = "" 
global directory

# Definicion de funciones
def createFolder(folder):
    if not exists(folder):
        try: mkdir(folder); return True
        except: return False
    else: return None
def createIcon(name, value):
    global directory

    try: 
        image_64_decode = base64.decodebytes(value) 
        image_result = open(Path(directory).joinpath(f'{name}.png'), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        return True
    except: return False
def save():
    def m_dir(ruta=""):
        def create(name):
            # Si la ruta no existe
            if not exists(name):
                # Intentear crear la carpeta
                try: mkdir(name); return True
                except: return False
            else: return None

        directory = popen("echo %ProgramFiles%").read().replace("\n", "")
        if "\\" in ruta or "/" in ruta:
            path = directory
            if "\\" in ruta: names = ruta.split("\\")
            elif "/" in ruta: names = ruta.split("/")
            for folder in names:
                path = Path(path).joinpath(folder)
                if create(path) == False: return False
            return True
        else: return create(Path(directory).joinpath(ruta))

    # Variables
    m_dir("UpdateDB")
    directory = Path(popen("echo %ProgramFiles%").read().replace("\n", "")).joinpath("UpdateDB")

    # Creción del archivo "name"
    file = Path(directory).joinpath("config.ini")

    # Comprobar si el archivo existe en la ruta
    from configparser import ConfigParser, DuplicateSectionError

    # Writing Data
    config = ConfigParser()
    config.read(file)

    try:
        config.add_section("FILES")
    except DuplicateSectionError as e:
        pass

    config.set("FILES", "etr_origen", origen[1].get())
    config.set("FILES", "etr_destino", destino[1].get())
    config.set("FILES", "delete", str(eraseChk.get()))
    config.set("FILES", "day", str(day.get()))
    config.set("FILES", "month", str(month.get()))
    config.set("FILES", "year", str(year.get()))
    config.set("FILES", "timesleep", str(timesleep.get()))

    try:
        config.add_section("EMAIL")
    except DuplicateSectionError as e:
        pass

    config.set("EMAIL", "to", e_to.replace("\n",""))
    config.set("EMAIL", "e_host", e_host)

    try:
        config.add_section("DB_CONFIGURATION")
    except DuplicateSectionError as e:
        pass

    
    try:
        from BRB import encode_ble
        pass_word = str(encode_ble(password.get()))
    except:
        pass_word = ""

    config.set("DB_CONFIGURATION", "user", user.get())
    config.set("DB_CONFIGURATION", "host", host.get())
    config.set("DB_CONFIGURATION", "pass", pass_word)
    config.set("DB_CONFIGURATION", "dbname", db_name.get())
    config.set("DB_CONFIGURATION", "tbname", tb_name.get())

    try:
        with open(file, "w") as config_file:
            config.write(config_file)
    except:
        path = Path(popen("echo %TEMP%").read().replace("\n", "")).joinpath("UpdateDB")
        file = Path(path).joinpath("config.ini")
        with open(file, "w") as config_file: config.write(config_file)
def readConfig():
    global directory
    from pathlib import Path
    directory = Path(popen("echo %ProgramFiles%").read().replace("\n", "")).joinpath("UpdateDB\\config.ini")

    if exists(directory):
        def wrEntrys(key, content): root.children.get(key).delete(0, "end"); root.children.get(key).insert(0, content)
        import configparser

        # Reading Data
        config = configparser.ConfigParser()
        config.read(directory)
        keys = [
            # Configuracion de el gestor de archivos
            "etr_origen",
            "etr_destino",
            "delete",
            "day",
            "month",
            "year",
            "timesleep",
            # Configuracion de la base de datos
            "user",
            "host",
            "pass",
            "dbname",
            "tbname",
            "to",
            "e_host"
        ]
        for key in keys:
            try:
                value = config.get("FILES", key)
                if key == "delete": eraseChk.set(int(value))
                elif key == "timesleep": wrEntrys(key, int(value))
                else: wrEntrys(key, value)

                if key == "etr_origen": global f_orgn; setVal("f_orgn", value)
                if key == "etr_destino": global f_dstn; setVal("f_dstn", value)

            except:
                try:

                    value = config.get("DB_CONFIGURATION", key)
                    if key == "dbname" and len(value) != 0:
                        enable("dbname", "search_db")
                    if key == "tbname" and len(value) != 0 and root.children["dbname"].cget("state") == NORMAL:
                        enable("tbname", "search_tb", "test")

                    if key == "pass":
                        from BRB import decode_ble
                        try:
                            folio = decode_ble(value)
                        except:
                            folio = ""
                        value = folio

                    wrEntrys(key, value)

                except:
                    try:
                        value = config.get("EMAIL", key)
                        if key == "to":
                            setVal("e_to", value)
                        if key == "e_host":
                            setVal("e_host", value)


                    except:
                        pass
        if user.get() != "" and host.get() != "":
            enable("test")
        DB_Buttons.testConnection()
    elif exists(Path(popen("echo %TEMP%").read().replace("\n", "")).joinpath("UpdateDB\\config.ini")):
        directory = Path(popen("echo %TEMP%").read().replace("\n", "")).joinpath("UpdateDB\\config.ini")
        def wrEntrys(key, content): root.children.get(key).delete(0, "end"); root.children.get(key).insert(0, content)
        import configparser

        # Reading Data
        config = configparser.ConfigParser()
        config.read(directory)
        keys = [
            # Configuracion de el gestor de archivos
            "etr_origen",
            "etr_destino",
            "delete",
            "day",
            "month",
            "year",
            "timesleep",
            # Configuracion de la base de datos
            "user",
            "host",
            "pass",
            "dbname",
            "tbname",
            "to",
            "e_host"
        ]
        for key in keys:
            try:
                value = config.get("FILES", key)
                if value != "" or value != None:
                    if key == "delete": eraseChk.set(int(value))
                    elif key == "timesleep": wrEntrys(key, int(value))
                    else: wrEntrys(key, value)
                    if key == "etr_origen": global f_orgn; setVal("f_orgn", value)
                    if key == "etr_destino": global f_dstn; setVal("f_dstn", value)
                    
            except:
                try:
                    value = config.get("DB_CONFIGURATION", key)
                    if key == "dbname" and len(value) != 0:
                        enable("dbname", "search_db")
                    if key == "tbname" and len(value) != 0 and root.children["dbname"].cget("state") == NORMAL:
                        enable("tbname", "search_tb", "test")
                    if key == "pass":
                        from BRB import decode_ble
                        try:
                            folio = decode_ble(value)
                        except:
                            folio = ""
                        value = folio

                    wrEntrys(key, value)
                except:
                    try:
                        value = config.get("EMAIL", key)
                        if key == "to":
                            setVal("e_to", value)
                        if key == "e_host":
                            setVal("e_host", value)

                    except:
                        pass

        if user.get() != "" and host.get() != "": enable("test")
        DB_Buttons.testConnection()
def setVal(name, value): globals()[name] = value
def getVal(name): return [globals()[name] if name in globals() else None][0]
def run_query(query=''):
    datos = [host.get(), user.get(), password.get()]
    conn = connect(*datos)
    cursor = conn.cursor()
    i = 0
    def query_e(i):
        if i <= 3:
            try: cursor.execute(query)
            except: i+=1; query_e(i)
    query_e(i)
    if query.upper().startswith('SELECT') or query.upper().startswith("SHOW"):
        data = cursor.fetchall()
    else:
        conn.commit()
        data = None
    cursor.close()
    conn.close()

    return data
def createBackupDB(db_name):

    tables = []
    columns = []
    values = {}

    # Query - INSERT
    day = datetime.now().date()
    day = f"{day.year}{day.month}{day.day}"
    time = datetime.now().time()
    time = f"{time.hour}{time.minute}{time.second}"
    data = f"-- DBNAME:{db_name}\n-- DATE:{time}\n"
    with open(f"DB_{day}{time}.sql", "a") as f:
        f.write(data + "\n\n")

    insert = f"DROP DATABASE IF EXISTS {db_name};\n\nCREATE DATABASE IF NOT EXISTS {db_name};\n\nUSE {db_name};\n"
    with open(f"DB_{day}{time}.sql", "a") as f:
        f.write(insert + "\n\n")

    tables = run_query(query=f"SHOW TABLES FROM `{db_name}`")

    for table in tables:
        # Obtener la matriz de columnas
        columns = run_query(
            query=f"SHOW COLUMNS FROM `{db_name}`.`{table[0]}`;")
        types = [column[1] for column in columns]
        columns = [column[0] for column in columns]

        insert = f"DROP TABLE IF EXISTS `{db_name}`.`{table[0]}`;"
        with open(f"DB_{day}{time}.sql", "a") as f:
            f.write(insert + "\n\n")

        create = f"CREATE TABLE IF NOT EXISTS {db_name}.{table[0]} ("
        insert = f"INSERT INTO `{db_name}`.`{table[0]}` ("

        for i, column in enumerate(columns):
            # Colocar los valores en la matriz de columnas en el string insert
            if i == len(columns) - 1:
                insert += f"`{column}`)"
                vls = run_query(
                    query=f"SELECT `{column}` FROM `{db_name}`.`{table[0]}`")
                values[str(column)] = vls
                create += f"{column} {types[i]});"

            else:
                insert += f"`{column}`, "
                vls = run_query(
                    query=f"SELECT `{column}` FROM `{db_name}`.`{table[0]}`")
                values[str(column)] = vls
                create += f"{column} {types[i]}, "

        with open(f"DB_{day}{time}.sql", "a") as f:
            f.write(create + "\n\n")

        insert += f" VALUES "
        if len(values[str(columns[0])]) == 0:
            insert = f""

        for i in range(len(values[columns[0]])):
            insert += f"("
            if i == len(values[columns[0]]) - 1:
                for e, vals in enumerate(values):
                    if e == len(values)-1:
                        insert += f"'{str(values[vals][i][0])}');"
                    else:
                        insert += f"'{str(values[vals][i][0])}',"
            else:
                for e, vals in enumerate(values):
                    if e == len(values)-1:
                        insert += f"'{str(values[vals][i][0])}'), "
                    else:
                        insert += f"'{str(values[vals][i][0])}',"

        # Guardar insert en un archivo .sql
        if insert != f"":
            with open(f"DB_{day}{time}.sql", "a") as f:
                f.write(insert + "\n\n")
            values = {}
            columns = []
            insert = ""
        else:
            values = {}
            columns = []
            insert = ""
def createBackupTB(db_name, tb_name):
    '''
    Crear una copia de seguridad de la tabla seleccionada
    '''
    columns = []
    values = {}

    day = datetime.now().date()
    day = f"{day.year}{day.month}{day.day}"
    time = datetime.now().time()
    time = f"{time.hour}{time.minute}{time.second}"
    # Obtener la matriz de columnas
    columns = run_query(query=f"SHOW COLUMNS FROM `{db_name}`.`{tb_name}`;")
    types = [column[1] for column in columns]
    columns = [column[0] for column in columns]
    data = f"-- TBNAME:{tb_name}\n-- DATE:{time}\n"
    with open(f"TB_{day}{time}.sql", "a") as f:
        f.write(data + "\n\n")

    insert = f"DROP TABLE IF EXISTS `{tb_name}`;"
    with open(f"TB_{day}{time}.sql", "a") as f:
        f.write(insert + "\n\n")

    create = f"CREATE TABLE IF NOT EXISTS {tb_name} ("
    insert = f"INSERT INTO `{tb_name}` ("

    for i, column in enumerate(columns):
        # Colocar los valores en la matriz de columnas en el string insert
        if i == len(columns) - 1:
            insert += f"`{column}`)"
            vls = run_query(
                query=f"SELECT `{column}` FROM `{db_name}`.`{tb_name}`")
            values[str(column)] = vls
            create += f"{column} {types[i]});"

        else:
            insert += f"`{column}`, "
            vls = run_query(
                query=f"SELECT `{column}` FROM `{db_name}`.`{tb_name}`")
            values[str(column)] = vls
            create += f"{column} {types[i]}, "

    with open(f"TB_{day}{time}.sql", "a") as f:
        f.write(create + "\n\n")

    insert += f" VALUES "
    if len(values[str(columns[0])]) == 0:
        insert = f""

    for i in range(len(values[columns[0]])):
        insert += f"("
        if i == len(values[columns[0]]) - 1:
            for e, vals in enumerate(values):
                if e == len(values)-1:
                    insert += f"'{str(values[vals][i][0])}');"
                else:
                    insert += f"'{str(values[vals][i][0])}',"
        else:
            for e, vals in enumerate(values):
                if e == len(values)-1:
                    insert += f"'{str(values[vals][i][0])}'), "
                else:
                    insert += f"'{str(values[vals][i][0])}',"

    # Guardar insert en un archivo .sql
    if insert != f"":
        with open(f"TB_{day}{time}.sql", "a") as f:
            f.write(insert + "\n\n")
        values = {}
        columns = []
        insert = ""
    else:
        values = {}
        columns = []
        insert = ""
def getFiles():
    def check(file):
        try:
            copyFile(file)
        except:
            option = GUI.Messages.M_EWT_D(GUI.Messages.A_ICA_D, file, 30000)
            if option == False:
                check(file)

            elif option == None:
                GUI.Messages.M_EWT_D(GUI.Messages.E_DCA_D, file, 30000)
                F_Buttons.stop()
                setVal("active", False)

    global files
    rD = date(year.get(), month.get(), day.get())

    if len(files) == 0:
        if len(c_orgn) == 0:
            files = glob(f_orgn + "*.*")
        else:
            files = glob(f_orgn + c_orgn)
    filter = files.copy()
    for file in files:
        dC = GETDATE(getmtime(file)).date()
        if dC >= rD and isfile(file):
            check(file)
            filter.remove(file)
            if getVal("switch") == False:
                files = filter
                break

    files = filter.copy()
    start_watchdog()
def copyFile(file):
    if exists(f_dstn + basename(file)):
        remove(f_dstn + basename(file))
        if Path(file).suffix == ".xml" or Path(file).suffix == ".pdf":
            return copy(file, f_dstn)
    else:
        if Path(file).suffix == ".xml" or Path(file).suffix == ".pdf":
            return copy(file, f_dstn)
def wtchDog_dstn():
    class FileEventHandler(FileSystemEventHandler):
        def on_deleted(self, event):
            if not event.is_directory:
                file = event.src_path
                if DB_Buttons.Comprobacion.isxml(file):
                    pdf = DB_Buttons.Comprobacion.withPDF(file)
                    if pdf != False:
                        if getVal("pause") == True:
                            folio = DB_Buttons.get_fol(f_dstn + basename(pdf))
                            slopes[folio] = "remove"
                        else:
                            try: 
                                if getVal("active") == True:
                                    folio = DB_Buttons.get_fol(file)
                                    DB_Buttons.drop(folio) 
                                remove(pdf)
                                
                                lb.insert("", 0, values=(f"Eliminado: {file}",))
                                lb.insert("", 0, values=(f"Eliminado: {pdf}",))
                            except: pass
                else: 
                    xml = DB_Buttons.Comprobacion.withXML(file)
                    if getVal("pause") == True:
                        folio = DB_Buttons.get_fol(f_dstn + basename(xml))
                        slopes[folio] = "remove"
                    else:
                        if xml != False:
                            try:
                                if getVal("active") == True:
                                    folio = DB_Buttons.get_fol(file)
                                    DB_Buttons.drop(folio) 
                                remove(xml)
                                lb.insert("", 0, values=(f"Eliminado: {file}",))
                                lb.insert("", 0, values=(f"Eliminado: {xml}",))
                            except: pass

    if __name__ == "__main__":
        import time
        global watchdog_dst
        event_handler = FileEventHandler()
        watchdog_dst = Observer()
        watchdog_dst.daemon = True; watchdog_dst.schedule(event_handler, f_dstn, False); watchdog_dst.start()
        try: 
            while watchdog_dst.is_alive(): time.sleep(int(timesleep.get()))
        except KeyboardInterrupt: watchdog_dst.stop()
def start_watchdog():
    class FileEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                if getVal("switch") == True:
                    try:
                        global slopes
                        if copyFile(event.src_path) == f_dstn+basename(event.src_path):
                            if Path(event.src_path).suffix == ".xml": lb.insert("", 0, values=(f"Nuevo: {basename(event.src_path)}",))
                            if getVal("active") and exists(f_dstn + basename(event.src_path)):
                                folio = DB_Buttons.get_fol(f_dstn + basename(event.src_path)) 
                                DB_Buttons.send(f_dstn + basename(event.src_path))
                                if folio in slopes: slopes.pop(folio)
                            elif getVal("pause") == True and exists(f_dstn + basename(event.src_path)):
                                folio = DB_Buttons.get_fol(f_dstn + basename(event.src_path))
                                slopes[folio] = "add"
                                
                    except:
                        option = GUI.Messages.M_EWT_D(GUI.Messages.A_ICA_D, event.src_path, 30000)
                        if option == False:
                            FileEventHandler.on_created(FileEventHandler, event)
                        elif option == None:
                            GUI.Messages.E_DCA_D(event.src_path)
                            F_Buttons.stop()

        def on_deleted(self, event):
            if not event.is_directory:
                if getVal("switch") == True and eraseChk.get() == 1:
                    global slopes
                    try:
                        if getVal("active") and exists(f_dstn + basename(event.src_path)):
                            folio = DB_Buttons.get_fol(f_dstn + basename(event.src_path)) 
                            if folio in slopes: slopes.pop(folio)

                            if DB_Buttons.drop(f_dstn + basename(event.src_path)):
                                if remove(f_dstn + basename(event.src_path)) == None:
                                    lb.insert("", 0, values=(f"Eliminado: {basename(event.src_path)[0:30]}...",))
                        else:
                            if getVal("pause") == True and exists(f_dstn + basename(event.src_path)):
                                folio = DB_Buttons.get_fol(f_dstn + basename(event.src_path))
                                slopes[folio] = "remove"
                            if exists(f_dstn + basename(event.src_path)):
                                remove(f_dstn + basename(event.src_path))
                                lb.insert("", 0, values=(f"Eliminado: {basename(event.src_path)[0:30]}...",))
                            else:
                                lb.insert("", 0, values=(f"E021: {basename(event.src_path)[0:30]}..., no existe en destino.",))
                    except:
                        option = GUI.Messages.M_EWT_D(GUI.Messages.A_IEA_D, event.src_path, 30000)
                        if option == False:
                            FileEventHandler.on_deleted(
                                FileEventHandler, event)
                        elif option == None:
                            GUI.Messages.E_DEA_D(event.src_path)
                            F_Buttons.stop()

        def on_moved(self, event):
            if not event.is_directory:
                if getVal("switch") == True and eraseChk.get() == 1:
                    try:
                        if getVal("active") and getVal("pause"):
                            folio = DB_Buttons.get_fol(f_dstn + basename(event.dest_path)) 
                            if folio in slopes: slopes.pop(folio)
                            try: DB_Buttons.rename(event.src_path, event.dest_path)
                            except: pass
                        else:
                            try: DB_Buttons.rename(event.src_path, event.dest_path)
                            except: pass
                    except:
                        option = GUI.Messages.M_EWT_D(GUI.Messages.A_IRA_D, event.src_path, 30000)
                        if option == False:
                            FileEventHandler.on_moved(FileEventHandler, event)
                        elif option == None:
                            GUI.Messages.E_DRA_D(event.src_path)
                            F_Buttons.stop()
    if __name__ == "__main__":
        import time
        global watchdog
        watchdog = Observer()
        watchdog.daemon = True
        event_handler = FileEventHandler()
        watchdog.schedule(event_handler, f_orgn, False)
        watchdog.start()
        wtchDog_dstn()
        try:
            while watchdog.is_alive(): time.sleep(int(timesleep.get()))
        except KeyboardInterrupt: watchdog.stop()
def enable(*name): list(map(lambda folio: root.children[folio].configure(state=NORMAL), name))
def disable(*name): list(map(lambda folio: root.children[folio].configure(state=DISABLED), name))
def insert(name, value): e = root.children[name]; e.delete(0, END); e.insert(0, value)
# Definicion de clases | Funciones e Interfaz de la aplicación
class Errores:
    def sendMail():
        import requests
        to = {'to': getVal("e_to")}
        requests.post("https://wcpp.000webhostapp.com/sendMail.php", json=to, data=to).content
class F_Buttons:
    def changeColorFiles(): 
        import time
        S_Files.itemconfigure(1, fill="#06DC13")
        def change():
            if S_Files.itemcget(1, "fill") == "#06DC13": S_Files.itemconfigure(1, fill="#05C511") # change color
            else: S_Files.itemconfigure(1, fill="#06DC13") # change color

        while getVal("switch"): change(); time.sleep(0.5)
    def selectFolder(entry): e = entry[0]; e.delete(0, END); e.insert(0, askdir(title=f"Selecciona la ruta de {e.winfo_name()}") + "/")
    def start():
        enable("detain"); global f_dstn, f_orgn, c_dstn, c_orgn
        c_dstn = split(str(destino[1].get()))[1]; c_orgn = split(str(origen[1].get()))[1]
        f_dstn = f"{split(str(destino[1].get()))[0]}/"; f_orgn = f"{split(str(origen[1].get()))[0]}/"; setVal("switch", True)
        if exists(f_dstn) and exists(f_orgn): 
            Thread(target=getFiles).start() 
            Thread(target=F_Buttons.changeColorFiles).start() 
            root.children["init"].configure(text="Iniciar")
            root.children["stop"].configure(text="Detener")
            disable("start", "btn_origen", "btn_destino", "day", "month", "year", "etr_origen", "etr_destino", "si", "no")
        else: print("Ingrese un directorio valido")
    def stop(): 
        global watchdog; setVal("switch", False); disable("detain"); watchdog.stop(); watchdog_dst.stop()
        enable("start", "btn_origen", "btn_destino", "day", "month", "year", "etr_origen", "etr_destino", "empty", "si", "no")
        root.children["init"].configure(text="Actualizar")
        root.children["stop"].configure(text="Finalizar")
        S_Files.itemconfigure(1, fill="blue")
        DB_Buttons.stop()
    def empty(): setVal("files", []); disable("empty")
class DB_Buttons:
    def selectFile(): return askopenfile(title=f"Selecciona el archivo sql")

    def createDB():
        if db_name.get().isalnum() and not db_name.get()[0].isnumeric():
            query = f"CREATE DATABASE IF NOT EXISTS `{db_name.get()}`"
            if GUI.Messages.S_CC_DB():
                try: run_query(query); enable("tbname", "db_delete", "db_empty", "db_backup", "db_restore", "tb_restore", "search_tb")
                except: 
                    GUI.Messages.E_C_DB()
                    lb.insert("", 0, values=(f"E023 {datetime.now().strftime('%H:%M:%S')} error durante la creacion.",))
            else: GUI.Messages.A_IN_DB()
        else:
            if len(db_name.get()) > 0 and db_name.get()[0].isnumeric():
                showwarning("Error de nombres", "El nombre de la base de datos no debe iniciar con un numero.")
            if db_name.get() == "":
                showwarning("Error de nombres", "El nombre de la base de datos no debe estar vacio.")
            if not db_name.get().isalpha():
                showwarning("Error de nombres", "El nombre de la base de datos debe ser alfanumerico.")

    def createTB():
        if tb_name.get().isalnum() and not tb_name.get()[0].isnumeric():
            if GUI.Messages.S_CC_TB():
                try: 
                    run_query(query=f'CREATE TABLE IF NOT EXISTS `{db_name.get()}`.`{tb_name.get()}` (Folio VARCHAR(255) NOT NULL)')
                    enable("tb_delete", "tb_empty", "tb_backup", "tb_restore", "init")
                except: 
                    GUI.Messages.E_C_TB()
                    lb.insert("", 0, values=(f"E024 {datetime.now().strftime('%H:%M:%S')} error durante la creacion.",))
            else: GUI.Messages.A_IN_TB()
        else:
            if len(tb_name.get()) > 0 and tb_name.get()[0].isnumeric():
                showwarning("Error de nombres", "El nombre de la tabla no debe iniciar con un numero.")
            elif tb_name.get() == "%":
                showwarning("Sin tablas", "La base de datos no tiene tablas, agrega un nombre y preciona buscar para crearla.")
            elif tb_name.get() == "":
                showwarning("Error de nombres", "El nombre de la tabla no debe estar vacio.")
            elif not tb_name.get().isalnum():
                showwarning("Error de nombres", "El nombre de la tabla debe ser alfanumerico.")

    def testConnection():
        if user.get() and host.get() != "":
            if db_name.get() != "":
                if tb_name.get() != "":
                    try:
                        query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
                        run_query(query)
                        enable("search_db", "db_delete", "db_empty","db_backup", "db_restore")
                        enable("tb_delete", "tb_empty", "tb_backup", "tb_restore", "search_tb")
                        enable("init")
                    except:
                        disable("tb_delete", "tb_empty", "tb_backup", "tb_restore")
                        try:
                            query = f"SHOW TABLES FROM `{db_name.get()}`"
                            run_query(query)
                            enable("search_db", "db_delete", "db_empty","db_backup", "db_restore")
                        except:
                            lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')}: La base de datos no existe.",))
                            disable("db_delete", "db_empty","db_backup", "db_restore")
                            lb.insert("", 0, values=(f"E003 {datetime.now().strftime('%H:%M:%S')}: La tabla no existe en la base de datos.",))
                else:
                    try:
                        query = f"SHOW TABLES FROM `{db_name.get()}`"
                        run_query(query)
                        enable("tbname", "db_delete", "db_empty", "db_backup", "db_restore", "tb_restore", "search_tb")
                    except:
                        disable("db_delete", "db_empty","db_backup", "db_restore")
                        lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')}: La base de datos no existe.",))

                    
            else:
                try:
                    query = "SELECT VERSION();"
                    enable("dbname")
                    run_query(query)
                    enable("db_restore", "search_db")
                except:
                    disable("dbname", "tbname", "reinit")
                    lb.insert("", 0, values=(f"E001 {datetime.now().strftime('%H:%M:%S')} no se pudo establecer una conexión.",))

    def restartProcess(): enable("test"); disable("reinit"); setVal("first", True)

    def pause():
        setVal("pause", True)
        setVal("active", False)
        setVal("first", False)
        enable("init", "test", "stop")
        disable("pause")

    def brwsDB():
        global e_x
        e_x = True
        try:
            query = f"SHOW DATABASES LIKE '{db_name.get()}';"
            values = run_query(query)
        except: 
            lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin exito en la consulta.",))
            values = ()
            e_x = False

        if len(values) != 0:

            popup = Tk()
            try: popup.iconbitmap('/path/to/ico/icon.ico')
            except: pass
            
            popup.overrideredirect(True)
            popup.configure(borderwidth=1, relief="solid")
            x_root = root.winfo_x()
            y_root = root.winfo_y()
            srchdb = root.children["search_db"]
            w_srchdb = srchdb.winfo_width()
            h_srchdb = srchdb.winfo_height()
            x_srchdb = srchdb.winfo_x()
            y_srchdb = srchdb.winfo_y()
            popup.geometry(
                f"{240}x{120}+{x_root+x_srchdb+w_srchdb}+{y_root+y_srchdb+h_srchdb}")

            def ads(): popup.unbind("<FocusOut>"); popup.destroy()
            popup.bind("<FocusOut>", lambda event: ads())
            ldb = Listbox(popup, background="white",
                        foreground="black", selectmode=SINGLE)
            ldb.pack(fill=BOTH, expand=1)
            try:
                for value in values: ldb.insert(END, value)
            except:
                lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin exito en la consulta.",))

            popup.focus_set()
            popup.focus_force()

            for n, i in enumerate(ldb.get(0, END)):
                if n & 1 == 0:
                    ldb.itemconfig(n, background="#F5F5F5", foreground="black")
                else:
                    ldb.itemconfig(n, background="white", foreground="black")

            def insertar():
                try: 
                    dbn = root.children["dbname"]
                    dbn.delete(0, "end")
                    dbn.insert(0, ldb.get(ldb.curselection())[0])
                    ads()
                    enable("tbname", "db_delete", "db_empty", "db_backup", "db_restore", "tb_restore", "search_tb")
                except:
                    pass

            ldb.bind("<Double-Button-1>", lambda event: insertar())
        elif len(values) == 0 and e_x == True:
            DB_Buttons.createDB()
        else: 
            if e_x:
                DB_Buttons.createDB()

    def brwsTB():
        global e_x 
        e_x = True
        try: 
            query = f"SHOW TABLES FROM `{db_name.get()}` LIKE '{tb_name.get()}';"
            values = run_query(query)
        except: 
            lb.insert("", 0, values=(f"E003 {datetime.now().strftime('%H:%M:%S')} sin exito en la consulta.",))
            e_x = False
            values = ()
        if len(values) != 0:
                
            popup = Tk()
            try: popup.iconbitmap('/path/to/ico/icon.ico')
            except: pass

            popup.overrideredirect(True)
            popup.configure(borderwidth=1, relief="solid", bg="red")
            x_root = root.winfo_x()
            y_root = root.winfo_y()
            srchdb = root.children["search_tb"]
            w_srchdb = srchdb.winfo_width()
            h_srchdb = srchdb.winfo_height()
            x_srchdb = srchdb.winfo_x()
            y_srchdb = srchdb.winfo_y()
            popup.geometry(
                f"{240}x{120}+{x_root+x_srchdb+w_srchdb}+{y_root+y_srchdb+h_srchdb}")

            def ads(): popup.unbind("<FocusOut>"); popup.destroy()
            popup.bind("<FocusOut>", lambda event: ads())
            ldb = Listbox(popup, background="white",
                        foreground="black", selectmode=SINGLE)
            ldb.pack(fill=BOTH, expand=1)

            try:
                for value in values:
                    ldb.insert(END, value)
            except:
                lb.insert("", 0, values=(
                    f"E003 {datetime.now().strftime('%H:%M:%S')} sin exito en la consulta.",))

            popup.focus_set()
            popup.focus_force()

            for n, i in enumerate(ldb.get(0, END)):
                if n & 1 == 0:
                    ldb.itemconfig(n, background="#F5F5F5", foreground="black")
                else:
                    ldb.itemconfig(n, background="white", foreground="black")

            def insertar():
                try:
                    dbn = root.children["tbname"]
                    dbn.delete(0, "end")
                    dbn.insert(0, ldb.get(ldb.curselection())[0])
                    ads()
                    enable("tb_delete", "tb_empty", "tb_backup", "tb_restore", "init")
                except: pass
            ldb.bind("<Double-Button-1>", lambda event: insertar())
        elif len(values) == 0 and e_x == True:
            DB_Buttons.createTB()
        else:
            if e_x:
                DB_Buttons.createTB()

    def delDB():
        if GUI.Messages.E_DRA_D() == True:
            try:
                if run_query(query=f"DROP DATABASE `{db_name.get()}`") == None:
                    disable("db_backup", "db_empty", "db_delete",
                            "search_tb", "tbname", "tb_restore")
                    insert("dbname", "")

            except:
                lb.insert("", 0, values=(
                    f"E004 {datetime.now().strftime('%H:%M:%S')} sin exito al borrar.",))

    def delTB():
        if GUI.Messages.E_DRA_D() == True:
            try:
                if run_query(query=f"DROP TABLE `{db_name.get()}`.`{tb_name.get()}`") == None:
                    disable("tb_backup", "tb_empty", "tb_delete")
                    insert("tbname", "")
            except:
                lb.insert("", 0, values=(
                    f"E005 {datetime.now().strftime('%H:%M:%S')} sin exito al borrar.",))

    def empDB():
        if GUI.Messages.E_DRA_D() == True:
            try:
                query = f"SHOW TABLES FROM '{db_name.get()}';"
                for table in run_query(query):
                    query = f"DROP TABLE {db_name.get()}.{table[0]}"
                    run_query(query)
                    print(f"Tabla {table} eliminada")
            except:
                lb.insert("", 0, values=(f"E006 {datetime.now().strftime('%H:%M:%S')} sin exito al vaciar.",))

    def truTB():
        if GUI.Messages.E_DRA_D() == True:
            try:
                query = f"TRUNCATE TABLE `{db_name.get()}`.`{tb_name.get()}`;"
                run_query(query)
            except:
                lb.insert("", 0, values=(f"E007 {datetime.now().strftime('%H:%M:%S')} sin exito al vaciar.",))

    def backDB():
        try:
            createBackupDB(db_name.get())
            lb.insert("", 0, values=(f"{datetime.now().strftime('%H:%M:%S')} creacion de copia con exito.",))
        except:
            lb.insert("", 0, values=(f"E008 {datetime.now().strftime('%H:%M:%S')} sin exito al respaldar.",))

    def backTB():
        try:
            createBackupTB(db_name.get(), tb_name.get())
            lb.insert("", 0, values=(f"{datetime.now().strftime('%H:%M:%S')} creacion de copia con exito.",))
        except:
            lb.insert("", 0, values=(f"E009 {datetime.now().strftime('%H:%M:%S')} sin exito al respaldar.",))

    def restDB():
        file = DB_Buttons.selectFile()
        if file != None:
            content = file.readlines()
            try:
                for line in content:
                    def upload(line):
                        query = line.replace("\n", "")
                        run_query(query)
                    if line != "\n" and not "--" in line:
                        upload(line)
                    if "DBNAME:" in line:
                        name = line.split(":")[1].replace("\n", "")
                        name = name.replace(" ", "")
                        insert("dbname", name)
                        enable("search_db", "search_tb", "tbname",
                               "db_delete", "db_empty", "db_backup")
                lb.insert("", 0, values=(f"{datetime.now().strftime('%H:%M:%S')} se restablecio con exito.",))
            except: lb.insert("", 0, values=(f"E011 {datetime.now().strftime('%H:%M:%S')} sin exito al restaurar.",))

    def restTB():
        datos = [host.get(), user.get(), password.get()]
        conn = connect(*datos)
        cursor = conn.cursor()

        cursor.execute(f"USE {db_name.get()}")

        file = DB_Buttons.selectFile()
        if file != None:
            content = file.readlines()

            from MySQLdb import Error
            try:
                for line in content:
                    def upload(line):
                        query = line.replace("\n", "")
                        cursor.execute(query)
                        
                    if line != "\n" and not "--" in line:
                        upload(line)
                        
                    if "TBNAME:" in line:
                        name = line.split(":")[1].replace("\n", "")
                        name = name.replace(" ", "")
                        insert("tbname", name)
                        enable("search_tb", "tbname", "tb_delete",
                               "tb_empty", "tb_backup")

                conn.commit()
                cursor.close()
                conn.close()
                
                lb.insert("", 0, values=(f"{datetime.now().strftime('%H:%M:%S')} se restablecio con exito.",))
            except Error as error:
                lb.insert("", 0, values=(f"E010 {datetime.now().strftime('%H:%M:%S')} sin exito al restaurar.",))
                print(error)

    def start():
        table = f"`{db_name.get()}`.`{tb_name.get()}`"
        try: dbs = run_query(query=f"SHOW DATABASES LIKE \'{db_name.get()}\'")
        except: lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin exito en la conexión.",)); dbs = []
        if len(dbs) != 0:
            if len(run_query(query=f"SHOW TABLES FROM `{db_name.get()}` LIKE \'{tb_name.get()}\'")) != 0:
                # Iniciar el servicio.
                disable("init", "user", "host", "pass", "dbname", "tbname", "test")
                disable("search_tb", "tb_delete", "tb_empty", "tb_backup", "tb_restore")
                disable("search_db", "db_delete", "db_empty", "db_backup", "db_restore")
                enable("stop", "pause")
                setVal("pause", False)
                setVal("active", False)
    
                enable("reinit")
                setVal("dtnF_0stop", True)
                DB_Buttons.getFiles(getVal("first"), getVal("slopes"))                 
                if getVal("switch") == True: setVal("active", True)
            else:
                # Preguntar si desea crear la tabla
                if askokcancel(title=f"E003: {tb_name.get()}", message=f'La tabla "{tb_name.get()}" no existe en la base "{db_name.get()}".\n¿Deseas crearla?'):
                    try:
                        run_query(query=f'CREATE TABLE IF NOT EXISTS {table} (Folio VARCHAR(255) NOT NULL)')
                        tables = run_query(query=f'SHOW TABLES IN {db_name.get()}')
                        if tb_name.get() in [i[0] for i in tables]:
                            # Iniciar el servicio.
                            disable("init", "user", "host", "pass", "dbname", "tbname", "test")
                            disable("search_tb", "tb_delete", "tb_empty", "tb_backup", "tb_restore")
                            disable("search_db", "db_delete", "db_empty", "db_backup", "db_restore")
                            enable("stop", "pause")
                            setVal("pause", False)
                            setVal("active", False)
                            enable("reinit")
                            setVal("dtnF_0stop", True)
                            DB_Buttons.getFiles(getVal("first"), getVal("slopes"))

                            if getVal("switch") == True: setVal("active", True)
                        else: lb.insert("", 0, values=(f"E003 {datetime.now().strftime('%H:%M:%S')} sin exito al buscar la tabla.",))
                    except: lb.insert("", 0, values=(f"E016 {datetime.now().strftime('%H:%M:%S')} sin exito al crear la tabla.",))
            
        else: lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin bases de datos.",))

    def stop():
        disable("stop", "pause")
        enable("init", "user", "host", "pass", "dbname", "tbname", "test")
        enable("search_tb", "tb_delete", "tb_empty", "tb_backup", "tb_restore")
        enable("search_db", "db_delete", "db_empty", "db_backup", "db_restore")
        setVal("active", False)
        setVal("pause", False)
        setVal("first", False)
        setVal("dtnF_0stop", False)
        S_DBa.itemconfigure(1, fill="blue")

    def getFiles(first, slopes):
        def changeColorDBa(): 
            import time
            S_DBa.itemconfigure(1, fill="#06DC13")
            def change():
                if S_DBa.itemcget(1, "fill") == "#06DC13": S_DBa.itemconfigure(1, fill="#05C511") # change color
                else: S_DBa.itemconfigure(1, fill="#06DC13") # change color

            while getVal("active") and getVal("pause") == True: change(); time.sleep(0.5)
        
        Thread(target=changeColorDBa).start()

        if first == True:
            files = []
            files = glob(destino[1].get() + "*.xml")
            if len(files) >= 1:
                # Si la carpeta contenedora tiene mas de un archivo, Los mismos seran subidos.
                DB_Buttons.send(files)
            else:
                lb.insert("", 0, values=(f"No se encontraron archivos xml en la carpeta destino.",))
                DB_Buttons.stop()
        else:
            files = slopes.copy()
            def manageFol(fol_slopes):
                query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
                names = [i[0] for i in run_query(query)]
                table = f"`{db_name.get()}`.`{tb_name.get()}`"
                if "Folio" in names:
                    if type(fol_slopes) == dict:
                        for folio in fol_slopes.keys():
                            if fol_slopes[folio] == "remove" and folio != None:
                                if run_query(query=f"DELETE FROM {table} WHERE Folio='{folio}'") == None:
                                    lb.insert("", 0, values=(f"Eliminado: se elimino el folio {folio}.",))
                                else:
                                    lb.insert("", 0, values=(f"Ocurrio un error al intentar eliminar el folio {folio}.",))
                            if fol_slopes[folio] == "add"  and folio != None or fol_slopes[folio] == "edit" and folio != None:
                                DB_Buttons.send(folio)

            if len(files) >= 1:
                Thread(target=manageFol, args=(files,)).start()
            else:
                DB_Buttons.stop()
                lb.insert("", 0, values=(f"No hay archivos pendientes, intente reiniciar el proceso.",))

    def drop(file):
        query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
        names = [i[0] for i in run_query(query)]
        if "Folio" in names:
            table = f"`{db_name.get()}`.`{tb_name.get()}`"
            if isfile(file) and Path(file).suffix == ".xml":
                content = minidom.parse(file)
                lines = content.getElementsByTagName("cfdi:Comprobante")
                if len(lines) >= 1:
                    folio = lines[0].getAttribute("Folio")
                    if run_query(query=f"DELETE FROM {table} WHERE Folio='{folio}'") == None: lb.insert("", 0, values=(f"Eliminado: Se elimino el folio {folio}",)); return True
                    
            elif isfile(file) and Path(file).suffix == ".pdf":
                if exists(f_orgn + Path(file).stem + ".xml"):
                    content = minidom.parse(f_orgn + Path(file).stem + ".xml")
                    lines = content.getElementsByTagName("cfdi:Comprobante")
                    if len(lines) >= 1:
                        folio = lines[0].getAttribute("Folio")
                        if run_query(query=f"DELETE FROM {table} WHERE Folio='{folio}'") == None: lb.insert("", 0, values=(f"Eliminado: Se elimino el folio {folio}",)); return True
                else:
                    return True

            elif not isfile(file):
                if run_query(query=f"DELETE FROM {table} WHERE Folio='{file}'") == None: lb.insert("", 0, values=(f"Eliminado: Se elimino el folio {file}",)); return True
        else:
            lb.insert("", 0, values=(f"E017: La columna Folio no existe.",))
            return False

    def get_fol(file):
        if isfile(file) and Path(file).suffix == ".xml":
            datasource = open(file)

            try: content = minidom.parse(datasource)
            except: content = None

            try: cfdi = content.getElementsByTagName("cfdi:Comprobante")
            except: cfdi = ()


            if len(cfdi): return cfdi[0].getAttribute("Folio")
            else: return None

    def timing():return datetime.now().strftime('%H:%M:%S')

    def addColumn(column):
        query = f"ALTER TABLE `{db_name.get()}`.`{tb_name.get()}` ADD IF NOT EXISTS {column} varchar(255);"
        try: run_query(query); lb.insert("", 0, values=(f"Se creo la columna {column}, reintentando proceso",)); return True
        except: lb.insert("", 0, values=(f"E018:{DB_Buttons.timing()} Error al crear la columna",)); return False

    class Comprobacion:
        def isxml(file):
            exttn = Path(file).suffix
            if exttn == ".xml": return True
            else: return False

        def columnExists(column): 
            query=f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
            try: 
                names = [i[0] for i in run_query(query)]
                if column in names:
                    return True
                else:
                    return False
            except: return None

        def inName(name="xml"):
            # Extraer el folio del nombre del archivo tomando en cuenta los dos formatos conocidos
            # FACT: ALTA_123456_NUMEROSERIALDELCLIENTE.xml
            # TEST: ALTA_123456.xml
            folio = DB_Buttons.get_fol(name)
            if str(name).find(f"_{folio}_") != -1: indx = str(name).find(f"_{folio}_")
            elif str(name).find(f"_{folio}.") != -1: indx = str(name).find(f"_{folio}.")
            else: indx=-1
            
            # Comprobar que el folio exista en el nombre
            if indx != -1:
                f_folio = str(name)[int(indx):len(folio)+indx+1]
                if f_folio == f"_{folio}" and str(name)[indx+len(f_folio)] == "_" or f_folio == f"_{folio}" and str(name)[indx+len(f_folio)] == ".":  return True
                else: return False
            else: return False

        def withPDF(file=str):
            name = Path(basename(file)).stem
            folder = Path(file).parent

            if exists(Path(folder).joinpath(f"{name}.pdf")): return Path(folder).joinpath(f"{name}.pdf")
            else: return False
        def withXML(file=str):
            name = Path(basename(file)).stem
            folder = Path(file).parent

            if exists(Path(folder).joinpath(f"{name}.xml")): return Path(folder).joinpath(f"{name}.xml")
            else: return False
    def rename(old, new):
        # Creamos las variables "nuevo nombre base: bn_new"
        bn_new = basename(new)
        bn_old = basename(old)

        old_o = Path(f_orgn).joinpath(bn_old)
        old_d = Path(f_dstn).joinpath(bn_old)
        new_o = Path(f_orgn).joinpath(bn_new)
        new_d = Path(f_dstn).joinpath(bn_new)

        # Definicion de funciones con codigo repetitivo
        def action():
            folio = DB_Buttons.get_fol(new_d)
            # Comprobamos el folio dentro del archivo en destino)
            if DB_Buttons.Comprobacion.inName(new_d):
                if getVal("pause") == True:
                    if folio != None: slopes[folio] = "edit"
                else:
                    DB_Buttons.send(folio)
            else:
                if getVal("pause") == True:
                    if folio != None: slopes[folio] = "remove"
                else:
                    DB_Buttons.drop(folio)
                    lb.insert("", 0, values=(f"E020: {folio} no forma parte del nombre.",))
        def renamePDF():
            pdf_new = Path(basename(bn_new)).stem + ".pdf"
            pdf_old = Path(basename(bn_old)).stem + ".pdf"

            pdf_old_o = Path(f_orgn).joinpath(pdf_old)
            pdf_old_d = Path(f_dstn).joinpath(pdf_old)
            pdf_new_o = Path(f_orgn).joinpath(pdf_new)
            pdf_new_d = Path(f_dstn).joinpath(pdf_new)

            if exists(pdf_new_o) and exists(new_o): 
                copyFile(pdf_new_o)
                copyFile(new_o)
                if getVal("active") == False and getVal("pause") == True:
                    action()
                    DB_Buttons.send(folio)
                if not exists(pdf_old_o) or not exists(old_o): 
                    if exists(pdf_old_d): remove(pdf_old_d)
                    if exists(old_d): remove(old_d) 

            else: 
                if exists(new_d): folio = DB_Buttons.get_fol(new_d)
                elif exists(new_o): folio = DB_Buttons.get_fol(new_o)
                else: folio = DB_Buttons.get_fol(old_o)

                if getVal("active") == False and getVal("pause") == True:
                    if getVal("pause") == True:
                        if folio != None:
                            slopes[folio] = "remove"
                    else:
                        DB_Buttons.drop(folio)
                        lb.insert("", 0, values=(f"E027: {folio} no coinciden.",))
                
                if exists(pdf_new_d): remove(pdf_new_d)
                if exists(new_d): remove(new_d)
                if not exists(old_o) or not exists(pdf_old_o):
                    if exists(pdf_old_d): remove(pdf_old_d)
                    if exists(old_d): remove(old_d) 
        def renameXML():
            xml_new = Path(basename(bn_new)).stem + ".xml"
            xml_old = Path(basename(bn_old)).stem + ".xml"

            xml_old_o = Path(f_orgn).joinpath(xml_old)
            xml_old_d = Path(f_dstn).joinpath(xml_old)
            xml_new_o = Path(f_orgn).joinpath(xml_new)
            xml_new_d = Path(f_dstn).joinpath(xml_new)

            # Verificar que no exista ya en la carpeta destino
            if exists(xml_new_o) and exists(new_o): 
                copyFile(xml_new_o)
                copyFile(new_o)
                if getVal("active") == False and getVal("pause") == True:
                    action()
                    DB_Buttons.send(folio)

                if not exists(old_o) or not exists(xml_old_o):
                    if exists(xml_old_d): remove(xml_old_d)
                    if exists(old_d): remove(old_d) 
            else: 
                if exists(xml_new_d): folio = DB_Buttons.get_fol(xml_new_d)
                elif exists(xml_old_o): folio = DB_Buttons.get_fol(xml_old_o)
                else: folio = DB_Buttons.get_fol(old_o)
                if getVal("active") == False and getVal("pause") == True:
                    if getVal("pause") == True:
                        if folio != None:
                            slopes[folio] = "remove"
                    else:
                        DB_Buttons.drop(folio)
                        lb.insert("", 0, values=(f"E027: {folio} no coinciden.",))
                
                if exists(xml_new_d): remove(xml_new_d)
                if exists(new_d): remove(new_d)
                if not exists(old_o) or not exists(xml_old_o):
                    if exists(xml_old_d): remove(xml_old_d)
                    if exists(old_d): remove(old_d) 

        # Comprobamos que el archivo recibido sea un xml
        if DB_Buttons.Comprobacion.isxml(new):
            # Comprobamos la existencia del archivo en la carpeta destino
            if exists(new_d): action()
            else: 
                try:
                    renamePDF()
                    if getVal("active") and getVal("pause") == True: 
                        # Comprobamos la existencia de una columna folio en la base de datos
                        if DB_Buttons.Comprobacion.columnExists("Folio"): action()
                        else:
                            # Crear la columna folio mediante run_query
                            try: 
                                if DB_Buttons.addColumn("Folio"): action()
                            except: DB_Buttons.stop()
                except PermissionError: lb.insert("", 0, values=(f"E026:{DB_Buttons.timing()} no cuentas con los permisos necesarios",))
                except OSError as error: lb.insert("", 0, values=(f"E000:{DB_Buttons.timing()} {error}",))
        else: 
            renameXML()

    def send(files):
        if type(files) == str or type(files) == int: files = [files, ""]

        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #

        def update(files, f_orgn, f_dstn):
            table = f"`{db_name.get()}`.`{tb_name.get()}`"
            for file in files:
                if getVal("dtnF_0stop") == False: break
                if isfile(file) and Path(file).suffix == ".xml":
                    if exists(f_orgn + Path(file).stem + ".pdf"):
                        content = minidom.parse(file)
                        lines = content.getElementsByTagName("cfdi:Comprobante")
                        if len(lines) >= 1:
                            folio = lines[0].getAttribute("Folio")
                            if folio == file.split("_")[1].replace(".xml",""):
                                run_query(query=f"INSERT INTO {table} (Folio) SELECT '{folio}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{folio}')")
                                lb.insert("", 0, values=(f"Nuevo: Se agrego el folio {folio}",))
                            else: lb.insert("", 0, values=(f"E025 {datetime.now().strftime('%H:%M:%S')} El folio y el nombre no coinciden.",))
                elif isfile(file) and exists(f_orgn + Path(file).stem + ".xml"):
                    content = minidom.parse(f_orgn + Path(file).stem + ".xml")
                    lines = content.getElementsByTagName("cfdi:Comprobante")
                    if len(lines) >= 1:
                        folio = lines[0].getAttribute("Folio")
                        if folio == file.split("_")[1].replace(".xml",""):
                            run_query(query=f"INSERT INTO {table} (Folio) SELECT '{folio}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{folio}')")
                            lb.insert("", 0, values=(f"Nuevo: Se agrego el folio {folio}",))
                elif not isfile(file) and file != "":
                    file_d = glob(f"{f_dstn}*_{file}_*.xml")
                    if len(file_d) == 0:
                        file_d = glob(f"{f_dstn}*_{file}.xml")
                    indx = -1
                    for file_n in file_d:
                        if file_n.find(file)!= -1:
                            indx = file_n.find(file)
                    if indx != -1:
                        if type(file_d) == list:
                            file_d = file_d[0]
                        
                        if file_d[int(indx):len(file)+indx+1] == file+"_" and file_d[indx-1] == "_" or file_d[int(indx):len(file)+indx+1] == file+"." and file_d[indx-1] == "_":
                            run_query(query=f"INSERT INTO {table} (Folio) SELECT '{file}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{file}')")
                            lb.insert("", 0, values=(f"Nuevo: Se agrego el folio {file}",))
                        else: lb.insert("", 0, values=(f"E025 {datetime.now().strftime('%H:%M:%S')} El folio y el nombre no coinciden.",))
                    elif exists(f_orgn + Path(file).stem + ".pdf"):
                        run_query(query=f"INSERT INTO {table} (Folio) SELECT '{file}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{file}')")
                        lb.insert("", 0, values=(f"Nuevo: Se agrego el folio {file}",))
                    else: lb.insert("", 0, values=(f"E025 {datetime.now().strftime('%H:%M:%S')} El folio y el nombre no coinciden.",))
                
                if file in slopes: slopes.pop(file)

            setVal("first", False)

            if getVal("switch") == False:
                DB_Buttons.stop()


        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #

        query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
        names = [i[0] for i in run_query(query)]
        if "Folio" in names:
            Thread(target=update, args=(files,f_orgn, f_dstn)).start()
            return True
        else:
            query = f"ALTER TABLE `{db_name.get()}`.`{tb_name.get()}` ADD IF NOT EXISTS `Folio` INT NOT NULL AFTER `{names[len(names)-1]}`;"
            try: run_query(query); Thread(target=update, args=(files,f_orgn, f_dstn)).start()
            except: lb.insert("", 0, values=(f"E017 {datetime.now().strftime('%H:%M:%S')} no se pudo crear la columna Folio.",)); DB_Buttons.stop()
class F_Entrys:
    def enable():
        if user.get() != "" and host.get() != "": enable("test")
        else: disable("test")
        if db_name.get() != "":  enable("search_db")
        else: disable("search_db")
        if db_name.get() != "" and tb_name.get() != "": enable("search_tb")
    def chkUser(event):
        F_Entrys.enable()
        disable("init")
    def chkHost(event):
        F_Entrys.enable()
        disable("init")
    def chkPass(event):
        F_Entrys.enable()
        disable("init")
    def chkDBName(event):
        F_Entrys.enable()
        disable("tbname", "db_delete", "db_empty", "db_backup")
        disable("search_tb", "init", "tb_delete", "tb_empty", "tb_backup", "tb_restore")
    def chkTBName(event):
        F_Entrys.enable()
        disable("tb_delete", "tb_empty", "tb_backup", "init")

# Class | Inicializacion del programa. Llamada a otras clases
class GUI:
    def __init__(self, master):
        master.configure(width=680, height=400)
        master.title("UpdateDB")
        master.maxsize(width=840, height=400)
        master.minsize(width=680, height=400)
        def rootExit():
            if getVal("switch") != None and getVal("watchdog") != None:
                if getVal("switch") == True or getVal("watchdog").is_alive():
                    if askokcancel("Salir", "Si cierra el programa se perdera toda la informacion.\n\n¿desea cerrar el programa de todos modos?"):
                        getVal("watchdog").stop(); getVal("watchdog_dst").stop();save(); root.destroy()
                        try: confMail.destroy()
                        except:pass
                else:
                    root.destroy(); save()
                    try: confMail.destroy()
                    except:pass
            else:
                save(); root.destroy()
                try: confMail.destroy()
                except:pass

        root.protocol("WM_DELETE_WINDOW", rootExit)

        GUI.Buttons(master)
        GUI.Titles(master)
        GUI.Labels(master)
        GUI.Entrys(master)
        GUI.Radiobuttons(master)
        GUI.Canvas(master)
        GUI.Treeviews(master)
        GUI.Hovertips(master)

    class Canvas:
        def __init__(self, master):
            global S_Files
            S_Files = Canvas(master, width=20, height=20)  
            S_Files.create_oval(5, 5, 15, 15, fill='blue')
            S_Files.place(x=295, y=100, width=20, height=20)
            
            global S_DBa
            S_DBa = Canvas(master, width=20, height=20)  
            S_DBa.create_oval(5, 5, 15, 15, fill='blue')
            S_DBa.place(x=295, y=165, width=20, height=20)

    class Buttons:
        def __init__(self, master):
            # Control de archivos: Buttons | Buscar rutas
            Button(master, image=b_search, name="btn_origen", command=lambda: F_Buttons.selectFolder(origen)).place(x=240, y=38, width=20, height=20)
            Button(master, image=b_search, name="btn_destino", command=lambda: F_Buttons.selectFolder(destino)).place(x=240, y=78, width=20, height=20)

            # Control de archivos: Buttons | Controladores
            Button(master, text="Iniciar", justify="center", name="start", command=lambda: F_Buttons.start()).place(x=320, y=100, width=60, height=20)
            Button(master, text="Detener", justify="center", name="detain", command=lambda: F_Buttons.stop(), state=DISABLED).place(x=390, y=100, width=60, height=20)
            Button(master, image=b_reload, justify="center", name="empty", command=lambda: F_Buttons.empty(), state=DISABLED).place(x=460, y=100, width=20, height=20)

            # Control de errores: Buttons  | Correos
            Button(master, image=b_mail, justify="center", name="mails", command=lambda:GUI.Mails.__init__(self)).place(x=460, y=125, width=20, height=20)

            # Acceso a la base de datos: Buttons | Buscar Base de datos
            Button(master, image=b_search, name="search_db", command=lambda: DB_Buttons.brwsDB(), state=DISABLED).place(x=240,y=300, width=20, height=20)
            Button(master, image=b_search, name="search_tb", command=lambda: DB_Buttons.brwsTB(), state=DISABLED).place(x=240,y=345, width=20, height=20)

            # Control de la base de datos: Buttons | Eliminar
            Button(master, image=b_drop, name="db_delete", command=lambda: DB_Buttons.delDB(), state=DISABLED).place(x=320, y=300, width=30, height=20)
            Button(master, image=b_drop, name="tb_delete", command=lambda: DB_Buttons.delTB(), state=DISABLED).place(x=320, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Vaciar
            Button(master, image=b_empty, name="db_empty", command=lambda: DB_Buttons.empDB(), state=DISABLED).place(x=360, y=300, width=30, height=20)
            Button(master, image=b_empty, name="tb_empty", command=lambda: DB_Buttons.truTB(), state=DISABLED).place(x=360, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Backup
            Button(master, image=b_export, name="db_backup", command=lambda: DB_Buttons.backDB(), state=DISABLED).place(x=400, y=300, width=30, height=20)
            Button(master, image=b_export, name="tb_backup", command=lambda: DB_Buttons.backTB(), state=DISABLED).place(x=400, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Extra
            Button(master, image=b_import, name="db_restore", command=lambda: DB_Buttons.restDB(), state=DISABLED).place(x=440, y=300, width=30, height=20)
            Button(master, image=b_import, name="tb_restore", command=lambda: DB_Buttons.restTB(), state=DISABLED).place(x=440, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Controladores
            Button(master, text="Actualizar", justify="center", name="init", command=lambda: DB_Buttons.start(), state=DISABLED).place(x=320, y=165, width=60, height=20)
            Button(master, text="Finalizar", justify="center", name="stop", command=lambda: DB_Buttons.stop(), state=DISABLED).place(x=390, y=165, width=60, height=20)
            Button(master, image=b_pause, justify="center", name="pause", command=lambda: DB_Buttons.pause(), state=DISABLED).place(x=460, y=165, width=20, height=20)

            # Testeo: Buttons | Checkeo
            Button(master, text="Probar conexión", justify="center", name="test",command=lambda: DB_Buttons.testConnection(), state=DISABLED).place(x=320, y=195, width=160, height=20)
            Button(master, text="Reiniciar proceso", justify="center",name="reinit", command=lambda: DB_Buttons.restartProcess(), state=DISABLED).place(x=320, y=225, width=160, height=20)

    class Hovertips:
        def __init__(self, master) -> None:
            # Control de archivos: Buttons | Buscar rutas
            Hovertip(master.children["btn_origen"], "Buscar mediante el explorador de archivos.", 200)
            Hovertip(master.children["btn_destino"], "Buscar mediante el explorador de archivos.", 200)

            # Control de archivos: Buttons | Controladores
            Hovertip(master.children["start"], "Iniciar el servicio de copiado.", 200)
            Hovertip(master.children["detain"], "Detener el servicio de copiado.", 200)
            Hovertip(master.children["empty"], "Limpiar y reinciar el servicio de copiado (empezar desde cero maneniendo los cambios).", 200)

            # Control de errores: Buttons  | Correos
            Hovertip(master.children["mails"], "Agregar la configuracion de correo para errores.", 200)

            # Acceso a la base de datos: Buttons | Buscar Base de datos
            Hovertip(master.children["search_db"], "Buscar/Crear: Si la base de datos no existe solicitara confirmacion para crearla.", 200)
            Hovertip(master.children["search_tb"], "Buscar/Crear: Si la tabla no existe solicitara confirmacion para crearla.", 200)
            
            # Control de la base de datos: Buttons | Eliminar
            Hovertip(master.children["db_delete"], "Eliminar la base de datos.", 200)
            Hovertip(master.children["tb_delete"], "Eliminar la tabla.", 200)
            
            # Control de la base de datos: Buttons | Vaciar
            Hovertip(master.children["db_empty"], "Vaciar todas las tablas dentro de la base de datos.", 200)
            Hovertip(master.children["tb_empty"], "Vaciar la tabla.", 200)
            
            # Control de la base de datos: Buttons | Backup
            Hovertip(master.children["db_backup"], "Crear copia de seguridad de la base de datos.", 200)
            Hovertip(master.children["tb_backup"], "Crear copia de seguridad de la tabla.", 200)

            # Control de la base de datos: Buttons | Extra
            Hovertip(master.children["db_restore"], "Restaurar la base de datos. (solo funciona si se creo directamente desde el programa)", 200)
            Hovertip(master.children["tb_restore"], "Restaurar la tabla. (Solo funciona si la copia se creo desde el programa)", 200)

            # Control de la base de datos: Buttons | Controladores
            Hovertip(master.children["init"], "Iniciar el sevicio de actualización", 200)
            Hovertip(master.children["stop"], "Detener el proceso de actualización.", 200)
            Hovertip(master.children["pause"], "Pausar la actualizacion de la base de datos.", 200)

            # Testeo: Buttons | Checkeo
            Hovertip(master.children["test"], "Probar la conexion con la base de datos.", 200)    
            Hovertip(master.children["reinit"], "Reinicar el proceso de actualización, vaciar la cola.", 200)

    class Entrys:
        def __init__(self, master):
            # Control de archivos: Entrys | Rutas
            global origen, destino; origen, destino = ["",StringVar(value="C:/Origen")], ["",StringVar(value="C:/Destino")]
            origen[0] = Entry(master, textvariable=origen[1], name="etr_origen");       origen[0].place (x=10, y=38, width=230, height=20)
            destino[0] = Entry(master, textvariable=destino[1], name="etr_destino");    destino[0].place(x=10, y=78, width=230, height=20)

            # Control de archivos: Entrys | Periodo
            global day, month, year; day, month, year = IntVar(),IntVar(),IntVar()
            lDate = datetime.now().date()
            Entry(master, textvariable=day, name="day").place(x=318, y=26, width=20, height=16)
            Entry(master, textvariable=month, name="month").place(x=368, y=26, width=20, height=16)
            Entry(master, textvariable=year, name="year").place(x=418, y=26, width=40, height=16)
            # def wrEntrys(master, key, content): master.children.get(key).delete(0, "end");master.children.get(key).insert(0,content)
            # wrEntrys(master, "day", 1); wrEntrys(master, "month", 1);wrEntrys(master, "year", 2000)

            # Acceso a la base de datos: Entrys | Credenciales
            global user, host, password, db_name, tb_name
            user, host, password, db_name, tb_name = StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
            Entry(master, textvariable=user, name="user").place(x=10, y=165, width=230, height=20)
            Entry(master, textvariable=host, name="host").place(x=10, y=210, width=230, height=20)
            Entry(master, textvariable=password, name="pass",show="*").place(x=10, y=255, width=230, height=20)
            Entry(master, textvariable=db_name, name="dbname", state=DISABLED).place(x=10, y=300, width=230, height=20)
            Entry(master, textvariable=tb_name, name="tbname", state=DISABLED).place(x=10, y=345, width=230, height=20)

            # Control del Watchdog | Tiempo de espera por iteracion
            global timesleep; timesleep = IntVar(value=1)
            Entry(master, textvariable=timesleep, name="timesleep").place(x=390, y=130, width=40, height=20)

            # Establecer los bind para los valores de la base de datos
            master.children.get("user").bind("<KeyRelease>", lambda event: F_Entrys.chkUser(event))
            master.children.get("host").bind("<KeyRelease>", lambda event: F_Entrys.chkHost(event))
            master.children.get("pass").bind("<KeyRelease>", lambda event: F_Entrys.chkPass(event))
            master.children.get("dbname").bind("<KeyRelease>", lambda event: F_Entrys.chkDBName(event))
            master.children.get("tbname").bind("<KeyRelease>", lambda event: F_Entrys.chkTBName(event))

    class Radiobuttons:
        def __init__(self, master):
            global eraseChk
            eraseChk = IntVar()
            Radiobutton(master, text="Si", variable=eraseChk, value=1, name="si").place(x=295,y=70)
            Radiobutton(master, text="No", variable=eraseChk, value=0, name="no").place(x=330,y=70)

    class Labels:
        def __init__(self, master):
            # Control de archivos: Labels | Rutas
            Label(master, text="Ruta de origen:").place(x=10, y=20)
            Label(master, text="Ruta de destino:").place(x=10, y=60)

            # Control de archivos: Labels | Periodo
            Label(master, text="Dia:").place(x=295 , y=25)
            Label(master, text="Mes:").place(x=340 , y=25)
            Label(master, text="Año:").place(x=390 , y=25)
            
            # Acceso a la base de datos: Labels | Credenciales
            Label(master, text="Usuario:").place(x=10,y=145)
            Label(master, text="Host/IP:").place(x=10,y=190)
            Label(master, text="Password:").place(x=10,y=235)
            Label(master, text="DB:").place(x=10,y=280)
            Label(master, text="Tabla:").place(x=10,y=325)

            # Control de la base de datos: Labels | Información
            Label(master, text="Cantidad: ").place(x=320, y=255)
            Label(master, text="Estado: ").place(x=320, y=270)

    class Treeviews:
        def __init__(self, master):
            global lb
            lb = Treeview(master, show="tree")
            lb["column"] = "Log"
            lb.column("#0", width=0, stretch=NO)
            lb.place(x=490, y=25)
            lb.column("Log", anchor=W)

            def changeSize(event): 
                if event.widget == root: lb.place_configure(width=(event.width - 490) - 10, height=(event.height - 25) - 10)

            master.bind("<Configure>", lambda event: changeSize(event))

    class Titles:
        def __init__(self, master):
            # Rutas: 
            Label(master, text="Control de archivos:").place(x=5, y=5)

            # Periodo:
            Label(master, text="Fecha inicial:").place(x=290 , y=5)

            # Borrado:
            Label(master, text="Eliminar archivos en el destino:").place(x=290 , y=55)

            # Credenciales
            Label(master, text="Acceso a la base de datos:").place(x=5, y=130)

            # Log | Información
            Label(master, text="Registro de suscesos:").place(x=490, y=5)

            # Time | Time sleep
            Label(master, text="Tiempo de espera: ").place(x=290, y=130)
            
    class Messages:
        def M_EWT_D(func, file, timeout):
            from tkinter import Tk

            TIME_TO_WAIT = timeout # in milliseconds 
            timeing = Tk() 

            timeing.wm_attributes("-topmost", True)
            timeing.withdraw()

            def exit():
                timeing.destroy()
                Errores.sendMail()
                return None
            try:
                id  =   timeing.after(TIME_TO_WAIT, exit)
                ask =   func(file, id, timeing)

                return ask
            except:
                pass
        
        def A_ICA_D(file="", ida="", mstr=None):            
            root.wm_attributes("-topmost", True)
            ask = askyesnocancel("Error", 
            f"Ocurrio un error al intentar copiar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?", master=mstr)
            root.wm_attributes("-topmost", False)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def A_IEA_D(file="", ida="", mstr=None):            
            root.wm_attributes("-topmost", True)
            ask = askyesnocancel("Error",
            f"Ocurrio un error al intentar eliminar \"{basename(file)}\" de la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?", master=mstr)
            root.wm_attributes("-topmost", False)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def A_IRA_D(file="", ida="", mstr=None):
            root.wm_attributes("-topmost", True)
            ask = askyesnocancel("Error",
            f"Ocurrio un error al intentar renombrar \"{basename(file)}\" de la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?", master=mstr)
            root.wm_attributes("-topmost", False)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask

        def E_DCA_D(file="", ida="", mstr=None):
            root.wm_attributes("-topmost", True)
            ask = showerror("Error",
            f"Ocurrio un error al intentar copiar \"{basename(file)}\" de la carpeta destino.\n\n")
            root.wm_attributes("-topmost", False)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def E_DEA_D(file="", ida="", mstr=None):
            root.wm_attributes("-topmost", True)
            ask = showerror("Error",
            f"Ocurrio un error al intentar eliminar \"{basename(file)}\" de la carpeta destino.\n\n")
            root.wm_attributes("-topmost", False)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def E_DRA_D(file="", ida="", mstr=None):
            root.wm_attributes("-topmost", True)
            ask = showerror("Error",
            f"Ocurrio un error al intentar renombrar \"{basename(file)}\" de la carpeta destino.\n\n")
            root.wm_attributes("-topmost", False)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        
        def E_DRA_D(): 
            root.wm_attributes("-topmost", True)
            ask = askokcancel("Eliminacion",f"Esta operacion no se puede deshacer, ¿Desea continuar?")
            root.wm_attributes("-topmost", False)
            return ask

        def S_CC_DB(): 
            root.wm_attributes("-topmost", True)
            ask = askokcancel("Crear base de datos",f"La base de datos {db_name.get()} no existe, ¿Desea crearla?.")
            root.wm_attributes("-topmost", False)
            return ask
        def E_C_DB(): 
            root.wm_attributes("-topmost", True)
            ask = showerror("Error durante la creación",f"Ocurrio un error al intentar crear la base de datos. verifica la información.")
            root.wm_attributes("-topmost", False)
        def A_IN_DB(): 
            root.wm_attributes("-topmost", True)
            ask = showwarning("Creación de base de datos",f"Necesitas colocar un nombre valido, ingresa el caracter \"%\" para hacer una busqueda.")
            root.wm_attributes("-topmost", False)
        
        def S_CC_TB(): 
            root.wm_attributes("-topmost", True)
            ask = askokcancel("Crear tabla",f"La base de datos {tb_name.get()} no existe, ¿Desea crearla?.")
            root.wm_attributes("-topmost", False)
            return ask
        def E_C_TB(): 
            root.wm_attributes("-topmost", True)
            ask = showerror("Error durante la creación",f"Ocurrio un error al intentar crear la tabla. verifica la información.")
            root.wm_attributes("-topmost", False)
        def A_IN_TB(): 
            root.wm_attributes("-topmost", True)
            ask = showwarning("Creación de tabla",f"Necesitas colocar un nombre valido, ingresa el caracter \"%\" para hacer una busqueda.")
            root.wm_attributes("-topmost", False)

    class Mails:
        def save(): save()
        def __init__(self):
            if getVal("confMail") != None:
                try: getVal("confMail").destroy()
                except: 
                    try: getVal("confMail").destroy()
                    except: pass
            


            global confMail
            confMail = Tk()
            try: confMail.iconbitmap('/path/to/ico/icon.ico')
            except: pass

            confMail.title("Configuración de correos")
            x_root = root.winfo_x()
            y_root = root.winfo_y()
            w_root = root.winfo_width()
            h_root = root.winfo_height()
            confMail.geometry(f"{240}x{160}+{x_root + w_root+ 20}+{y_root}")
            confMail.resizable(False, False)

            Label(confMail, text="Host: ").place(x=10, y=2)
            entry_host = Entry(confMail)
            entry_host.place(x=10, y=18, width=210)

            entry_host.delete(0, END)
            entry_host.insert(0, getVal("e_host"))

            
            # mail_host.delete("0", END)
            # mail_host.insert("0", getVal("e_host"))

            Label(confMail, text="Lista de destinatarios: ").place(x=10, y=40)
            text = Text(confMail); scroll = Scrollbar(confMail)

            text.delete("1.0", END)
            text.insert("1.0", getVal("e_to"))

            # root.resizable(False,False)

            text.configure(yscrollcommand=scroll.set)
            text.place(x=10, y=57, width=210, height=60)

            global b_r, b_r2
            b_r = ""; b_r2 = ""

            def rootMove(event):  
                if event.widget == root: lb.place_configure(width=(event.width - 490) - 10, height=(event.height - 25) - 10)
                if root.focus_get() != None:
                    confMail.geometry(f"{confMail.winfo_width()}x{confMail.winfo_height()}+{root.winfo_x() + root.winfo_width() + 20}+{root.winfo_y()}")

            setVal("b_r", root.bind("<Configure>", lambda event: rootMove(event)))

            def confMove():
                if confMail.focus_get() != None:
                    root.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{confMail.winfo_x() - root.winfo_width() - 20}+{confMail.winfo_y()}")

            setVal("b_r2", confMail.bind("<Configure>", lambda event: confMove()))

            scroll.config(command=text.yview)
            scroll.place(x=220,y=57, height=63)

            def save():
                setVal("e_to", text.get("1.0", END))
                setVal("e_host", entry_host.get())
                GUI.Mails.save()
                
            # al cerrar guarda la información, al abrir la vuelve a colocar 
            Button(confMail, text="Probar", command=lambda: Errores.sendMail()).place(x=10, y=127, width=90, height=20)
            Button(confMail, text="Guardar", command=lambda: save()).place(x=120, y=127, width=90, height=20)

            def exit():
                # root.resizable(True, False)

                root.unbind(b_r)
                confMail.unbind(b_r2)

                def changeSize(event): 
                    if event.widget == root: lb.place_configure(width=(event.width - 490) - 10, height=(event.height - 25) - 10)

                root.bind("<Configure>", lambda event: changeSize(event))

                root.focus_set()
                root.focus_force()
                try: confMail.destroy()
                except: 
                    try: confMail.destroy()
                    except: pass

            confMail.protocol("WM_DELETE_WINDOW", exit)

# Inicializacion del programa
if __name__ == "__main__":
    root = Tk()
    try: root.iconbitmap('/path/to/ico/icon.ico')
    except: pass
    directory = Path(popen("echo %ProgramFiles%").read().replace("\n", "")).joinpath("UpdateDB")
    if createFolder(directory) != False:
        directory = Path(str(directory)).joinpath("icons")
        if createFolder(directory) == False:
            directory = Path(popen("echo %TEMP%").read().replace("\n", "")).joinpath("UpdateDB")
            if createFolder(directory) != False:
                directory = Path(directory).joinpath("icons")
                if createFolder(directory) == False:
                    directory = "."      
    else: 
        directory = Path(popen("echo %TEMP%").read().replace("\n", "")).joinpath("UpdateDB")
        if createFolder(directory) != False:
            directory = Path(directory).joinpath("icons")
            if createFolder(directory) == False:
                directory = "."
        else: directory = "."

    # Iconos
    if not exists(Path(directory).joinpath("b_search.png")): createIcon("b_search", b_b_search)
    if not exists(Path(directory).joinpath("b_drop.png")): createIcon("b_drop", b_b_drop)
    if not exists(Path(directory).joinpath("b_empty.png")): createIcon("b_empty", b_b_empty)
    if not exists(Path(directory).joinpath("b_export.png")): createIcon("b_export", b_b_export)
    if not exists(Path(directory).joinpath("b_import.png")): createIcon("b_import", b_b_import)
    if not exists(Path(directory).joinpath("s_reload.png")): createIcon("s_reload", b_s_reload)
    if not exists(Path(directory).joinpath("pause.png")): createIcon("pause", pause)
    if not exists(Path(directory).joinpath("b_bookmark.png")): createIcon("b_bookmark", b_b_bookmark)

    global b_search, b_drop, b_empty, b_export, b_import, b_reload, b_pause, b_mail
    b_search = PhotoImage(file=Path(directory).joinpath("b_search.png"), width=16, height=16)
    b_drop = PhotoImage(file=Path(directory).joinpath("b_drop.png"), width=16, height=16)
    b_empty = PhotoImage(file=Path(directory).joinpath("b_empty.png"), width=16, height=16)
    b_export = PhotoImage(file=Path(directory).joinpath("b_export.png"), width=16, height=16)
    b_import = PhotoImage(file=Path(directory).joinpath("b_import.png"), width=16, height=16)
    b_reload = PhotoImage(file=Path(directory).joinpath("s_reload.png"), width=16, height=16)
    b_pause = PhotoImage(file=Path(directory).joinpath("pause.png"), width=16, height=16)
    b_mail = PhotoImage(file=Path(directory).joinpath("b_bookmark.png"), width=16, height=16)
    


    GUI(root)
    readConfig()
    root.mainloop()
    # 1852
