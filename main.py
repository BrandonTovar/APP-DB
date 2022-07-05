# Importar librerias
import pathlib
from datetime import date, datetime
from glob import glob
from os import getcwd, popen, remove, rename
from os.path import basename, getmtime, isdir, split
from pprint import pprint
from shutil import copy
from threading import Thread
from tkinter import (BOTH, DISABLED, END, NORMAL, SINGLE, Button, Canvas,
                     Entry, IntVar, Label, Listbox, Radiobutton, Scrollbar,
                     StringVar, Text, Tk, W)
from tkinter.filedialog import askdirectory as askdir
from tkinter.filedialog import askopenfile
from tkinter.messagebox import NO, askokcancel, askyesnocancel, showerror
from tkinter.ttk import Treeview
from xml.dom import minidom

import requests
from genericpath import exists, isfile
from MySQLdb import connect
from watchdog.events import *
from watchdog.observers import Observer

# Definicion de constantes
GETDATE = datetime.fromtimestamp

# Definicion de variables
global files, attCounter, conn_st, slopes, active
files = ""; switch = False; attCounter = 0; conn_st = False; slopes = 0; actieve = False

# Variables contenedoras para el correo
global e_to; e_to = ""

# Definicion de funciones
def save():
    def m_dir(ruta=""):
        def create(name):
            from os import mkdir

            from genericpath import exists

            # Si la ruta no existe
            if not exists(name):
                # Intentear crear la carpeta
                try:
                    mkdir(name)
                    return True
                except:
                    return False
            else:
                return None

        from os import popen
        from pathlib import Path
        directory = popen("echo %ProgramFiles%").read().replace("\n", "")
        if "\\" in ruta or "/" in ruta:
            path = directory
            if "\\" in ruta:
                names = ruta.split("\\")
            elif "/" in ruta:
                names = ruta.split("/")
            for folder in names:
                path = Path(path).joinpath(folder)
                if create(path) == False:
                    return False
            return True

        else:
            return create(Path(directory).joinpath(ruta))

    # Create directory in init
    from os import popen
    from pathlib import Path

    # Variables
    m_dir("UpdateDB")
    directory = Path(popen("echo %ProgramFiles%").read().replace(
        "\n", "")).joinpath("UpdateDB")

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

    try:
        config.add_section("EMAIL")
    except DuplicateSectionError as e:
        pass

    config.set("EMAIL", "to", e_to)

    try:
        config.add_section("DB_CONFIGURATION")
    except DuplicateSectionError as e:
        pass

    from BRB import encode_ble
    try:
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
        path = getcwd()
        file = Path(path).joinpath("config.ini")
        with open(file, "w") as config_file:
            config.write(config_file)
def readConfig():
    from pathlib import Path
    directory = Path(popen("echo %ProgramFiles%").read().replace(
        "\n", "")).joinpath("UpdateDB\\config.ini")

    if exists(directory):
        def wrEntrys(key, content): root.children.get(key).delete(
            0, "end"); root.children.get(key).insert(0, content)
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
            # Configuracion de la base de datos
            "user",
            "host",
            "pass",
            "dbname",
            "tbname",
            "to"
        ]
        for key in keys:
            try:
                value = config.get("FILES", key)
                if key == "delete":

                    eraseChk.set(int(value))
                else:
                    wrEntrys(key, value)
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
                            val = decode_ble(value)
                        except:
                            val = ""
                        print(val)
                        value = val

                    wrEntrys(key, value)

                except:
                    try:
                        value = config.get("EMAIL", key)
                        if key == "to":
                            setVal("e_to", value)

                    except:
                        pass
        if user.get() != "" and host.get() != "":
            enable("test")
        DB_Buttons.testConnection()
    elif exists(Path(getcwd()).joinpath("config.ini")):
        directory = Path(getcwd()).joinpath("config.ini")
        def wrEntrys(key, content): root.children.get(key).delete(
            0, "end"); root.children.get(key).insert(0, content)
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
            # Configuracion de la base de datos
            "user",
            "host",
            "pass",
            "dbname",
            "tbname",
            "to"
        ]
        for key in keys:
            try:
                value = config.get("FILES", key)
                if value != "" or value != None:
                    if key == "delete":

                        eraseChk.set(int(value))
                    else:
                        wrEntrys(key, value)
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
                            val = decode_ble(value)
                        except:
                            val = ""
                        value = val

                    wrEntrys(key, value)
                except:
                    try:
                        value = config.get("EMAIL", key)
                        if key == "to":
                            setVal("e_to", value)

                    except:
                        pass

        if user.get() != "" and host.get() != "":
            enable("test")
        DB_Buttons.testConnection()
def setVal(name, value): globals()[name] = value
def getVal(name): return [globals()[name] if name in globals() else None][0]
def run_query(query=''):
    datos = [host.get(), user.get(), password.get()]
    conn = connect(*datos)
    cursor = conn.cursor()
    cursor.execute(query)
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

    tb_name = "aaa"
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
    data = f"-- DBNAME:{db_name}\n-- TBNAME:{tb_name}\n-- DATE:{time}\n"
    with open(f"TB_{day}{time}.sql", "a") as f:
        f.write(data + "\n\n")

    insert = f"DROP TABLE IF EXISTS `{db_name}`.`{tb_name}`;"
    with open(f"TB_{day}{time}.sql", "a") as f:
        f.write(insert + "\n\n")

    create = f"CREATE TABLE IF NOT EXISTS {db_name}.{tb_name} ("
    insert = f"INSERT INTO `{db_name}`.`{tb_name}` ("

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
        if pathlib.Path(file).suffix == ".xml" or pathlib.Path(file).suffix == ".pdf":
            return copy(file, f_dstn)
    else:
        if pathlib.Path(file).suffix == ".xml" or pathlib.Path(file).suffix == ".pdf":
            return copy(file, f_dstn)
def start_watchdog():
    class FileEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                if getVal("switch") == True:
                    try:
                        if copyFile(event.src_path) == f_dstn+basename(event.src_path):
                            lb.insert("", 0, values=(
                                f"Nuevo: {basename(event.src_path)[0:15]}...",))
                            if getVal("active") and exists(f_dstn + basename(event.src_path)):
                                DB_Buttons.send(
                                    f_dstn + basename(event.src_path))
                    except:
                        option = GUI.Messages.M_EWT_D(
                            GUI.Messages.A_ICA_D, event.src_path, 30000)
                        if option == False:
                            FileEventHandler.on_created(
                                FileEventHandler, event)
                        elif option == None:
                            GUI.Messages.E_DCA_D(event.src_path)
                            F_Buttons.stop()

        def on_deleted(self, event):
            if not event.is_directory:
                if getVal("switch") == True and eraseChk.get() == 1:
                    try:
                        if getVal("active") and exists(f_dstn + basename(event.src_path)):
                            if DB_Buttons.drop(f_dstn + basename(event.src_path)):
                                if remove(f_dstn + basename(event.src_path)) == None:
                                    lb.insert("", 0, values=(
                                        f"Eliminado: {basename(event.src_path)[0:15]}...",))
                        else:
                            if exists(f_dstn + basename(event.src_path)):
                                remove(f_dstn + basename(event.src_path))
                                lb.insert("", 0, values=(
                                    f"Eliminado: {basename(event.src_path)[0:15]}...",))
                            else:
                                lb.insert("", 0, values=(
                                    f"E021: {basename(event.src_path)[0:15]}..., no existe en destino.",))
                    except:
                        option = GUI.Messages.A_IEA_D(event.src_path)
                        if option == False:
                            FileEventHandler.on_deleted(
                                FileEventHandler, event)
                        elif option == None:
                            GUI.Messages.E_DEA_D(event.src_path)
                            F_Buttons.stop()

        def on_moved(self, event):
            if not event.is_directory:
                if getVal("switch") == True and eraseChk.get() == 1:
                    if exists(f"{f_dstn}{basename(event.src_path)}"):
                        try:
                            if getVal("active"):
                                names = [i[0] for i in run_query(
                                    query=f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`")]
                                if "Folio" in names:
                                    extention = pathlib.Path(
                                        f_orgn + basename(event.dest_path)).suffix
                                    if isfile(f_orgn + basename(event.dest_path)) and extention == ".xml":
                                        content = minidom.parse(
                                            f_orgn + basename(event.dest_path))
                                        lines = content.getElementsByTagName(
                                            "cfdi:Comprobante")
                                        if len(lines) >= 1:
                                            folio = lines[0].getAttribute(
                                                "Folio")
                                            if not exists(f_dstn + basename(event.dest_path)):
                                                if rename(f_dstn + basename(event.src_path), f_dstn + basename(event.dest_path)) == None:
                                                    lb.insert("", 0, values=(
                                                        f"Renombrado: {basename(event.dest_path)[0:15]}...",))
                                                    if not folio in basename(event.dest_path):
                                                        if DB_Buttons.drop(folio):
                                                            lb.insert("", 0, values=(
                                                                f"E020: {folio} no forma parte del nombre.",))
                                                    else:
                                                        if DB_Buttons.send(folio):
                                                            lb.insert("", 0, values=(
                                                                f"Se agrego el folio {folio}.",))
                                            else:
                                                lb.insert("", 0, values=(
                                                    f"Ya existe {basename(event.dest_path)[0:15]}... en la ruta destino.",))
                                                if not folio in basename(event.dest_path):
                                                    if DB_Buttons.drop(folio):
                                                        lb.insert("", 0, values=(
                                                            f"E020: {folio} no forma parte del nombre.",))
                                                else:
                                                    if DB_Buttons.send(folio):
                                                        lb.insert("", 0, values=(
                                                            f"Se agrego el folio {folio}.",))
                                    elif isfile(f_orgn + basename(event.dest_path)) and extention == ".pdf":
                                        print("not exists, folio is null")

                                        def withFolio(folio):
                                            if not exists(f_dstn + basename(event.dest_path)):
                                                if rename(f_dstn + basename(event.src_path), f_dstn + basename(event.dest_path)) == None:
                                                    lb.insert("", 0, values=(
                                                        f"Renombrado: {basename(event.dest_path)[0:15]}...",))
                                                    if not folio in basename(event.dest_path):
                                                        if DB_Buttons.drop(folio):
                                                            lb.insert("", 0, values=(
                                                                f"E020: {folio} no forma parte del nombre.",))
                                                    else:
                                                        if DB_Buttons.send(folio):
                                                            lb.insert("", 0, values=(
                                                                f"Se agrego el folio {folio}.",))
                                            else:
                                                lb.insert("", 0, values=(
                                                    f"Ya existe {basename(event.dest_path)[0:15]}... en la ruta destino.",))
                                                if not folio in basename(event.dest_path):
                                                    if DB_Buttons.drop(folio):
                                                        lb.insert("", 0, values=(
                                                            f"E020: {folio} no forma parte del nombre.",))
                                                else:
                                                    if DB_Buttons.send(folio):
                                                        lb.insert("", 0, values=(
                                                            f"Se agrego el folio {folio}.",))

                                        befFile = f_orgn + \
                                            pathlib.Path(
                                                basename(event.src_path)).stem
                                        if exists(befFile + ".xml"):
                                            content = minidom.parse(
                                                befFile + ".xml")
                                            lines = content.getElementsByTagName(
                                                "cfdi:Comprobante")
                                            if len(lines) >= 1:
                                                folio = lines[0].getAttribute(
                                                    "Folio")
                                                withFolio(folio)
                                        else:
                                            if exists(f_orgn + pathlib.Path(basename(event.dest_path)).stem + ".xml"):
                                                content = minidom.parse(
                                                    f_orgn + pathlib.Path(basename(event.dest_path)).stem + ".xml")
                                                lines = content.getElementsByTagName(
                                                    "cfdi:Comprobante")
                                                if len(lines) >= 1:
                                                    folio = lines[0].getAttribute(
                                                        "Folio")
                                                    withFolio(folio)
                                            else:
                                                if not exists(f_dstn + basename(event.dest_path)):
                                                    if rename(f_dstn + basename(event.src_path), f_dstn + basename(event.dest_path)) == None:
                                                        lb.insert("", 0, values=(
                                                            f"Renombrado: {basename(event.dest_path)[0:15]}...",))
                                                        lb.insert("", 0, values=(
                                                            f"E022: El archivo no cuenta con un folio.",))
                                                else:
                                                    lb.insert("", 0, values=(
                                                        f"Ya existe {basename(event.dest_path)[0:15]}... en la ruta destino.",))
                                                    lb.insert("", 0, values=(
                                                        f"E022: El archivo no cuenta con un folio.",))

                                else:
                                    lb.insert("", 0, values=(
                                        f"E017: La columna Folio no existe.",))
                            else:
                                if rename(f_dstn + basename(event.src_path), f_dstn + basename(event.dest_path)) == None:
                                    lb.insert("", 0, values=(
                                        f"Renombrado: {basename(event.dest_path)[0:15]}...",))
                        except:
                            option = GUI.Messages.A_IRA_D(event.src_path)
                            if option == False:
                                FileEventHandler.on_moved(
                                    FileEventHandler, event)
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
        try:
            while watchdog.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            watchdog.stop()
def enable(
    *name): list(map(lambda val: root.children[val].configure(state=NORMAL), name))
def disable(
    *name): list(map(lambda val: root.children[val].configure(state=DISABLED), name))
def insert(name, value): e = root.children[name]; e.delete(0, END); e.insert(0, value)

# Definicion de clases | Funciones e Interfaz de la aplicación
class Errores:
    def sendMail():
        import requests
        to = {'to': getVal("e_to")}
        print(to)
        print(requests.post("https://www.wcpp.000webhostapp.com/sendMail.php", json=to, data=to).content)
class F_Buttons:
    def selectFolder(entry): e = entry[0]; e.delete(0, END); e.insert(0, askdir(title=f"Selecciona la ruta de {e.winfo_name()}") + "/")
    def start():
        enable("detain"); global f_dstn, f_orgn, c_dstn, c_orgn
        c_dstn = split(str(destino[1].get()))[1]; c_orgn = split(str(origen[1].get()))[1]
        f_dstn = f"{split(str(destino[1].get()))[0]}/"; f_orgn = f"{split(str(origen[1].get()))[0]}/"; setVal("switch", True)
        if exists(f_dstn) and exists(f_orgn): 
            Thread(target=getFiles).start() 
            root.children["init"].configure(text="Iniciar")
            root.children["stop"].configure(text="Pausar")
            disable("start", "btn_origen", "btn_destino", "day", "month", "year", "etr_origen", "etr_destino", "si", "no")
        else: print("Ingrese un directorio valido")
    def stop(): 
        global watchdog; setVal("switch", False); disable("detain"); watchdog.stop()
        enable("start", "btn_origen", "btn_destino", "day", "month", "year", "etr_origen", "etr_destino", "empty", "si", "no")
        root.children["init"].configure(text="Actualizar")
        root.children["stop"].configure(text="Finalizar")

    def empty(): setVal("files", []); disable("empty")
class DB_Buttons:
    def selectFile(): return askopenfile(title=f"Selecciona el archivo sql")

    def testConnection():
        if user.get() and host.get() != "":
            if db_name.get() != "":
                if tb_name.get() != "":
                    try:
                        query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
                        run_query(query)
                        enable("search_db", "db_delete", "db_empty","db_backup", "db_restore")
                        enable("tb_delete", "tb_empty", "tb_backup", "tb_restore", "search_tb")
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
                        enable("search_db", "db_delete", "db_empty","db_backup", "db_restore")
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

    def restartProcess(): enable("test"); disable("reinit")

    def brwsDB():
        try:
            query = f"SHOW DATABASES LIKE '{db_name.get()}';"
            values = run_query(query)
        except: 
            lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin exito en la consulta.",))
            values = ()
        if len(values) != 0:

            popup = Tk()
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

    def brwsTB():
        try: 
            query = f"SHOW TABLES FROM `{db_name.get()}` LIKE '{tb_name.get()}';"
            values = run_query(query)
        except: 
            lb.insert("", 0, values=(f"E003 {datetime.now().strftime('%H:%M:%S')} sin exito en la consulta.",))
            values = ()
        if len(values) != 0:
                
            popup = Tk()
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
        except:
            lb.insert("", 0, values=(
                f"E008 {datetime.now().strftime('%H:%M:%S')} sin exito al respaldar.",))

    def backTB():
        try:
            createBackupTB(db_name.get(), tb_name.get())
        except:
            lb.insert("", 0, values=(
                f"E009 {datetime.now().strftime('%H:%M:%S')} sin exito al respaldar.",))

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
            except:
                lb.insert("", 0, values=(
                    f"E011 {datetime.now().strftime('%H:%M:%S')} sin exito al restaurar.",))

    def restTB():
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
                    if "TBNAME:" in line:
                        name = line.split(":")[1].replace("\n", "")
                        name = name.replace(" ", "")
                        insert("tbname", name)
                        enable("search_tb", "tbname", "tb_delete",
                               "tb_empty", "tb_backup")
            except:
                lb.insert("", 0, values=(
                    f"E010 {datetime.now().strftime('%H:%M:%S')} sin exito al restaurar.",))

    def start():
        table = f"`{db_name.get()}`.`{tb_name.get()}`"
        try:
            dbs = run_query(query=f"SHOW DATABASES LIKE \'{db_name.get()}\'")
            if len(dbs) != 0:
                if len(run_query(query=f"SHOW TABLES FROM `{db_name.get()}` LIKE \'{tb_name.get()}\'")) != 0:
                    # Iniciar el servicio.
                    DB_Buttons.getFiles(True, getVal("slopes"))
                    disable("init"); enable("stop")
                    if getVal("switch") == True: setVal("active", True)
                else:
                    # Preguntar si desea crear la tabla
                    if askokcancel(title=f"E003: {tb_name.get()}", message=f'La tabla "{tb_name.get()}" no existe en la base "{db_name.get()}".\n¿Deseas crearla?'):
                        try:
                            run_query(query=f'CREATE TABLE IF NOT EXISTS {table} (Folio VARCHAR(255) NOT NULL)')
                            tables = run_query(query=f'SHOW TABLES IN {db_name.get()}')
                            if tb_name.get() in [i[0] for i in tables]:
                                # Iniciar el servicio.
                                DB_Buttons.getFiles(True, getVal("slopes"))
                                disable("init"); enable("stop")
                                if getVal("switch") == True: setVal("active", True)
                            else: lb.insert("", 0, values=(f"E003 {datetime.now().strftime('%H:%M:%S')} sin exito al buscar la tabla.",))
                        except: lb.insert("", 0, values=(f"E016 {datetime.now().strftime('%H:%M:%S')} sin exito al crear la tabla.",))
            else: lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin bases de datos.",))
        except: lb.insert("", 0, values=(f"E002 {datetime.now().strftime('%H:%M:%S')} sin exito en la conexión.",))

    def getFiles(first, slopes):
        if first == True:
            files = glob(destino[1].get() + "*.xml")
            if len(files) >= 1:
                # Si la carpeta contenedora tiene mas de un archivo, Los mismos seran subidos.
                DB_Buttons.send(files)
            else:
                pass
        else:
            files = slopes
            if len(files) >= 1:
                DB_Buttons.send(files)

    def drop(file):
        query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
        names = [i[0] for i in run_query(query)]
        if "Folio" in names:
            table = f"`{db_name.get()}`.`{tb_name.get()}`"
            if isfile(file) and pathlib.Path(file).suffix == ".xml":
                content = minidom.parse(file)
                lines = content.getElementsByTagName("cfdi:Comprobante")
                if len(lines) >= 1:
                    folio = lines[0].getAttribute("Folio")
                    if run_query(query=f"DELETE FROM {table} WHERE Folio='{folio}'") == None: return True
            elif isfile(file) and pathlib.Path(file).suffix == ".pdf":
                if exists(f_orgn + pathlib.Path(file).stem + ".xml"):
                    content = minidom.parse(f_orgn + pathlib.Path(file).stem + ".xml")
                    lines = content.getElementsByTagName("cfdi:Comprobante")
                    if len(lines) >= 1:
                        folio = lines[0].getAttribute("Folio")
                        if run_query(query=f"DELETE FROM {table} WHERE Folio='{folio}'") == None: return True
                else:
                    return True

            elif not isfile(file):
                if run_query(query=f"DELETE FROM {table} WHERE Folio='{file}'") == None: return True
            

        else:
            lb.insert("", 0, values=(f"E017: La columna Folio no existe.",))
            return False

    # def rename(file, previous):
    #     query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
    #     names = [i[0] for i in run_query(query)]
    #     if "Folio" in names:
    #         table = f"`{db_name.get()}`.`{tb_name.get()}`"
    #         if isfile(file):
    #             content = minidom.parse(file)
    #             lines = content.getElementsByTagName("cfdi:Comprobante")
    #             if len(lines) >= 1:
    #                 folio = lines[0].getAttribute("Folio")
    #                 if folio != previous:
    #                     if run_query(query=f"UPDATE {table} SET Folio='{previous}' WHERE Folio='{folio}'") == None:
    #                         print(folio)
    #                         return True
    #                 else: 
    #                     return False
    #     else:
    #         lb.insert("", 0, values=(f"E017: La columna Folio no existe.",))

    def send(files):
        if type(files) == str or type(files) == int:
            files = [files, ""]
        def update():
            table = f"`{db_name.get()}`.`{tb_name.get()}`"
            for file in files:
                if isfile(file) and pathlib.Path(file).suffix == ".xml":
                    if exists(f_orgn + pathlib.Path(file).stem + ".pdf"):
                        content = minidom.parse(file)
                        lines = content.getElementsByTagName("cfdi:Comprobante")
                        if len(lines) >= 1:
                            folio = lines[0].getAttribute("Folio")
                            if run_query(query=f"INSERT INTO {table} (Folio) SELECT '{folio}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{folio}')") == None:
                                return True
                elif isfile(file) and exists(f_orgn + pathlib.Path(file).stem + ".xml"):
                    content = minidom.parse(f_orgn + pathlib.Path(file).stem + ".xml")
                    lines = content.getElementsByTagName("cfdi:Comprobante")
                    if len(lines) >= 1:
                        folio = lines[0].getAttribute("Folio")
                        if run_query(query=f"INSERT INTO {table} (Folio) SELECT '{folio}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{folio}')") == None:
                            return True

                elif not isfile(file) and file != "":
                    if exists(f_orgn + pathlib.Path(file).stem + ".pdf"):
                        if run_query(query=f"INSERT INTO {table} (Folio) SELECT '{file}' WHERE NOT EXISTS(SELECT Folio FROM {table} WHERE Folio='{file}')") == None:
                            return True
        query = f"SHOW COLUMNS FROM `{db_name.get()}`.`{tb_name.get()}`"
        names = [i[0] for i in run_query(query)]

        if "Folio" in names:
            update()
        else:
            query = f"ALTER TABLE `{db_name.get()}`.`{tb_name.get()}` ADD IF NOT EXISTS `Folio` INT NOT NULL AFTER `{names[len(names)-1]}`;"
            run_query(query)
            update()

    def stop():
        enable("init"); disable("stop")
        setVal("active", False)
class F_Entrys:
    def enable():
        if user.get() != "" and host.get() != "": enable("test")
        else: disable("test")
        if db_name.get() != "":  enable("search_db")
        else: disable("search_db")
        if db_name.get() != "" and tb_name.get() != "": enable("search_tb")
        if db_name.get() != "" and tb_name.get() != "" and user.get() != "" and host.get() != "": enable("init")
        else: disable("init")
    def chkUser(event):
        F_Entrys.enable()
    def chkHost(event):
        F_Entrys.enable()
    def chkPass(event):
        F_Entrys.enable()
    def chkDBName(event):
        F_Entrys.enable()
        disable("tbname", "db_delete", "db_empty", "db_backup")
        disable("search_tb", "init", "tb_delete", "tb_empty", "tb_backup", "tb_restore")
    def chkTBName(event):
        F_Entrys.enable()
        disable("tb_delete", "tb_empty", "tb_backup")

# Class | Inicializacion del programa. Llamada a otras clases
class GUI:
    def __init__(self, master):
        master.configure(width=680, height=400)
        master.title("Test GUI")
        master.maxsize(width=840, height=400)
        master.minsize(width=680, height=400)
        def rootExit():
            if getVal("switch") != None and getVal("watchdog") != None:
                if getVal("switch") == True or getVal("watchdog").is_alive():
                    if askokcancel("Salir", "Si cierra el programa se perdera toda la informacion.\n\n¿desea cerrar el programa de todos modos?"):
                        getVal("watchdog").stop()
                        save()
                        root.destroy()
                        try: confMail.destroy()
                        except:pass
                else:
                    root.destroy()
                    save()
                    try: confMail.destroy()
                    except:pass
            else:
                save()
                root.destroy()
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

    class Canvas:
        def __init__(self, master):
            S_Files = Canvas(master, width=20, height=20)  
            S_Files.create_oval(5, 5, 15, 15, fill='blue')
            S_Files.place(x=295, y=100, width=20, height=20)

            S_DBa = Canvas(master, width=20, height=20)  
            S_DBa.create_oval(5, 5, 15, 15, fill='blue')
            S_DBa.place(x=295, y=165, width=20, height=20)

    class Buttons:
        def __init__(self, master):
            # Control de archivos: Buttons | Buscar rutas
            Button(master, text="+", name="btn_origen", command=lambda: F_Buttons.selectFolder(origen)).place(x=240, y=38, width=20, height=20)
            Button(master, text="+", name="btn_destino", command=lambda: F_Buttons.selectFolder(destino)).place(x=240, y=78, width=20, height=20)

            # Control de archivos: Buttons | Controladores
            Button(master, text="Iniciar", justify="center", name="start", command=lambda: F_Buttons.start()).place(x=320, y=100, width=60, height=20)
            Button(master, text="Detener", justify="center", name="detain", command=lambda: F_Buttons.stop(), state=DISABLED).place(x=390, y=100, width=60, height=20)
            Button(master, text="+", justify="center", name="empty", command=lambda: F_Buttons.empty(), state=DISABLED).place(x=460, y=100, width=20, height=20)

            # Control de errores: Buttons  | Correos
            Button(master, text="+", justify="center", name="mails", command=lambda:GUI.Mails.__init__(self)).place(x=460, y=125, width=20, height=20)

            # Acceso a la base de datos: Buttons | Buscar Base de datos
            Button(master, text="+", name="search_db", command=lambda: DB_Buttons.brwsDB(), state=DISABLED).place(x=240,y=300, width=20, height=20)
            Button(master, text="+", name="search_tb", command=lambda: DB_Buttons.brwsTB(), state=DISABLED).place(x=240,y=345, width=20, height=20)

            # Control de la base de datos: Buttons | Eliminar
            Button(master, text="X", name="db_delete", command=lambda: DB_Buttons.delDB(), state=DISABLED).place(x=320, y=300, width=30, height=20)
            Button(master, text="X", name="tb_delete", command=lambda: DB_Buttons.delTB(), state=DISABLED).place(x=320, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Vaciar
            Button(master, text="-", name="db_empty", command=lambda: DB_Buttons.empDB(), state=DISABLED).place(x=360, y=300, width=30, height=20)
            Button(master, text="-", name="tb_empty", command=lambda: DB_Buttons.truTB(), state=DISABLED).place(x=360, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Backup
            Button(master, text="B", name="db_backup", command=lambda: DB_Buttons.backDB(), state=DISABLED).place(x=400, y=300, width=30, height=20)
            Button(master, text="B", name="tb_backup", command=lambda: DB_Buttons.backTB(), state=DISABLED).place(x=400, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Extra
            Button(master, text="S", name="db_restore", command=lambda: DB_Buttons.restDB(), state=DISABLED).place(x=440, y=300, width=30, height=20)
            Button(master, text="S", name="tb_restore", command=lambda: DB_Buttons.restTB(), state=DISABLED).place(x=440, y=345, width=30, height=20)

            # Control de la base de datos: Buttons | Controladores
            Button(master, text="Actualizar", justify="center", name="init", command=lambda: DB_Buttons.start(), state=DISABLED).place(x=320, y=165, width=60, height=20)
            Button(master, text="Finalizar", justify="center", name="stop", command=lambda: DB_Buttons.stop(), state=DISABLED).place(x=390, y=165, width=60, height=20)
            Button(master, text="+", justify="center", command=lambda: DB_Buttons.empty(), state=DISABLED).place(x=460, y=165, width=20, height=20)

            # Testeo: Buttons | Checkeo
            Button(master, text="Probar conexión", justify="center", name="test",command=lambda: DB_Buttons.testConnection(), state=DISABLED).place(x=320, y=195, width=160, height=20)
            Button(master, text="Reiniciar proceso", justify="center",name="reinit", command=lambda: DB_Buttons.restartProcess(), state=DISABLED).place(x=320, y=225, width=160, height=20)

    class Entrys:
        def __init__(self, master):
            # Control de archivos: Entrys | Rutas
            global origen, destino; origen, destino = ["",StringVar()], ["",StringVar()]
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


            # enable("dbname","tbname")

            # insert("user", "root")
            # insert("host", "localhost")
            # insert("dbname", "prueba")
            # insert("tbname", "aaa")
            


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
            
    class Messages:
        def M_EWT_D(func, file, timeout):
            from tkinter import Tk

            from _tkinter import TclError

            TIME_TO_WAIT = timeout # in milliseconds 
            timeing = Tk() 
            timeing.withdraw()

            def exit():
                timeing.destroy()
                Errores.sendMail()
                return None
            try:
                id  =   timeing.after(TIME_TO_WAIT, exit)
                ask =   func(file, id, timeing)
                try: root.destroy()
                except: pass


                return ask
            except TclError:
                pass

        def A_ICA_D(file, ida="", mstr=None):            
            ask = askyesnocancel("Error", 
            f"Ocurrio un error al intentar copiar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?", master=mstr)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def A_IEA_D(file, ida="", mstr=None):            
            ask = askyesnocancel("Error",
            f"Ocurrio un error al intentar eliminar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?", master=mstr)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def A_IRA_D(file, ida="", mstr=None):
            ask = askyesnocancel("Error",
            f"Ocurrio un error al intentar renombrar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?", master=mstr)
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask

        def E_DCA_D(file, ida="", mstr=None):
            ask = showerror("Error",
            f"Ocurrio un error al intentar copiar \"{basename(file)}\" a la carpeta destino.\n\n")
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def E_DEA_D(file, ida="", mstr=None):
            ask = showerror("Error",
            f"Ocurrio un error al intentar eliminar \"{basename(file)}\" a la carpeta destino.\n\n")
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        def E_DRA_D(file, ida="", mstr=None):
            ask = showerror("Error",
            f"Ocurrio un error al intentar renombrar \"{basename(file)}\" a la carpeta destino.\n\n")
            if ida != "":
                try: 
                    mstr.winfo_exists()
                    mstr.after_cancel(ida)
                    return ask
                except: return None
            else:
                return ask
        
        def E_DRA_D(): return askokcancel("Eliminacion",f"Esta operacion no se puede deshacer, ¿Desea continuar?")

    class Mails:
        def __init__(self):
            if getVal("confMail") != None:
                try: getVal("confMail").destroy()
                except: 
                    try: getVal("confMail").destroy()
                    except: pass

            global confMail
            confMail = Tk()
            confMail.title("Configuración de correos")
            x_root = root.winfo_x()
            y_root = root.winfo_y()
            w_root = root.winfo_width()
            h_root = root.winfo_height()
            confMail.geometry(f"{240}x{120}+{x_root + w_root+ 20}+{y_root}")
            confMail.resizable(False, False)

            Label(confMail, text="Lista de destinatarios: ").place(x=10, y=8)
            text = Text(confMail); scroll = Scrollbar(confMail)

            text.delete("1.0", END)
            text.insert("1.0", getVal("e_to"))

            # root.resizable(False,False)

            text.configure(yscrollcommand=scroll.set)
            text.place(x=10, y=25, width=210, height=60)

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
            scroll.place(x=220,y=23, height=63)
            def save():
                setVal("e_to", text.get("1.0", END))
            # al cerrar guarda la información, al abrir la vuelve a colocar 
            Button(confMail, text="Probar", command=lambda: Errores.sendMail()).place(x=10, y=90, width=90, height=20)
            Button(confMail, text="Guardar", command=lambda: save()).place(x=120, y=90, width=90, height=20)

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
    GUI(root)
    readConfig()
    root.mainloop()

        

