from datetime import date, datetime
from genericpath import exists, isfile
from glob import glob
from os import remove, rename
from os.path import split, basename
from tkinter import BOTH, DISABLED, NORMAL, END, SINGLE, W, Button, Canvas, Entry, Label, Listbox, StringVar, IntVar, Tk, Radiobutton
from tkinter.filedialog import askdirectory as askdir, askopenfile
from tkinter.messagebox import NO, askokcancel, askyesnocancel, showerror
from tkinter.ttk import Treeview
from os.path import getmtime
from threading import Thread
from shutil import copy
from watchdog.observers import Observer
from watchdog.events import *
from MySQLdb import connect

def run_query(query=''): 
    datos = [host.get(), user.get(), password.get()] 
    conn = connect(*datos); cursor = conn.cursor(); cursor.execute(query)         
    if query.upper().startswith('SELECT') or query.upper().startswith("SHOW"): data = cursor.fetchall()
    else: conn.commit(); data = None 
    cursor.close()
    conn.close()

    return data

# Definicion de constantes

GETDATE = datetime.fromtimestamp

# Definicion de variables
global files, attCounter, conn_st
files = ""; switch = False; attCounter = 0; conn_st = False
# Definicion de funciones
def setVal(name, value): globals()[name] = value
def getVal(name): return [globals()[name] if name in globals() else None][0]

def createBackupDB(db_name):

    tables = []; columns = []; values = {}

    # Query - INSERT
    day = datetime.now().date(); day = f"{day.year}{day.month}{day.day}"
    time = datetime.now().time(); time = f"{time.hour}{time.minute}{time.second}"
    data = f"-- DBNAME:{db_name}\n-- DATE:{time}\n"
    with open(f"DB_{day}{time}.sql", "a") as f:
            f.write(data + "\n\n")

    insert = f"DROP DATABASE IF EXISTS {db_name};\n\nCREATE DATABASE IF NOT EXISTS {db_name};\n\nUSE {db_name};\n"
    with open(f"DB_{day}{time}.sql", "a") as f:
        f.write(insert + "\n\n")

    tables = run_query(query = f"SHOW TABLES FROM `{db_name}`")



    for table in tables:
        # Obtener la matriz de columnas
        columns = run_query(query = f"SHOW COLUMNS FROM `{db_name}`.`{table[0]}`;")
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
                vls = run_query(query = f"SELECT `{column}` FROM `{db_name}`.`{table[0]}`")
                values[str(column)] = vls; create += f"{column} {types[i]});"

            else:
                insert += f"`{column}`, "
                vls = run_query(query = f"SELECT `{column}` FROM `{db_name}`.`{table[0]}`")
                values[str(column)] = vls; create += f"{column} {types[i]}, "

        with open(f"DB_{day}{time}.sql", "a") as f: f.write(create + "\n\n")
        
        insert += f" VALUES "
        if len(values[str(columns[0])]) == 0: insert = f""

        for i in range(len(values[columns[0]])):
            insert += f"("
            if i == len(values[columns[0]]) - 1:
                for e, vals in enumerate(values):
                    if e == len(values)-1: insert += f"'{str(values[vals][i][0])}');"
                    else: insert += f"'{str(values[vals][i][0])}',"
            else:
                for e, vals in enumerate(values):
                    if e == len(values)-1: insert += f"'{str(values[vals][i][0])}'), "
                    else: insert += f"'{str(values[vals][i][0])}',"
        
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

    tb_name = "aaa"; columns = []; values = {}

    day = datetime.now().date(); day = f"{day.year}{day.month}{day.day}"
    time = datetime.now().time(); time = f"{time.hour}{time.minute}{time.second}"
    # Obtener la matriz de columnas
    columns = run_query(query = f"SHOW COLUMNS FROM `{db_name}`.`{tb_name}`;")
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
            vls = run_query(query = f"SELECT `{column}` FROM `{db_name}`.`{tb_name}`")
            values[str(column)] = vls; create += f"{column} {types[i]});"

        else:
            insert += f"`{column}`, "
            vls = run_query(query = f"SELECT `{column}` FROM `{db_name}`.`{tb_name}`")
            values[str(column)] = vls; create += f"{column} {types[i]}, "

    with open(f"TB_{day}{time}.sql", "a") as f: f.write(create + "\n\n")
    
    insert += f" VALUES "
    if len(values[str(columns[0])]) == 0: insert = f""

    for i in range(len(values[columns[0]])):
        insert += f"("
        if i == len(values[columns[0]]) - 1:
            for e, vals in enumerate(values):
                if e == len(values)-1: insert += f"'{str(values[vals][i][0])}');"
                else: insert += f"'{str(values[vals][i][0])}',"
        else:
            for e, vals in enumerate(values):
                if e == len(values)-1: insert += f"'{str(values[vals][i][0])}'), "
                else: insert += f"'{str(values[vals][i][0])}',"
    
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
    global files; rD = date(year.get(), month.get(), day.get())
    if len(files) == 0:
        if len(c_orgn) == 0: files = glob(f_orgn + "*.*")
        else: files = glob(f_orgn + c_orgn)
    filter = files.copy()
    for file in files:
        dC = GETDATE(getmtime(file)).date()
        if dC >= rD and isfile(file):
            copyFile(file); filter.remove(file)
            if getVal("switch") == False:files = filter; break

    files = filter.copy()
    start_watchdog()

def copyFile(file): copy(file, f_dstn)

def start_watchdog(): 
    class FileEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                if getVal("switch") == True:
                    try: 
                        if copyFile(event.src_path): 
                            lb.insert("",0, values=(f"Nuevo: {basename(event.src_path)}",))
                    except: 
                        option = GUI.Messages.A_ICA_D(event.src_path)
                        if option == False:
                            FileEventHandler.on_created(FileEventHandler, event)
                        elif option == None: 
                            GUI.Messages.E_DCA_D(event.src_path)
                            F_Buttons.stop()
        def on_deleted(self, event):
            if not event.is_directory:
                if getVal("switch") == True and eraseChk.get() == 1: 
                    try: 
                        if remove(f_dstn + basename(event.src_path)): 
                            lb.insert("",0, values=(f"Eliminado: {basename(event.src_path)}",))
                    except: 
                        option = GUI.Messages.A_IEA_D(event.src_path)
                        if option == False:
                            FileEventHandler.on_deleted(FileEventHandler, event)
                        elif option == None: 
                            GUI.Messages.E_DEA_D(event.src_path)
                            F_Buttons.stop()

        def on_moved(self, event):
            if not event.is_directory:
                if getVal("switch") == True and eraseChk.get() == 1:
                    if exists(f"{f_dstn}{basename(event.src_path)}"):
                        try: 
                            if rename(f_dstn + basename(event.src_path), f_dstn + basename(event.dest_path)):
                                lb.insert("",0, values=(f"Renombrado: {basename(event.dest_path)}",))
                        except:
                            option = GUI.Messages.A_IRA_D(event.src_path)
                            if option == False:
                                attCounter = attCounter + 1
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
        watchdog.schedule(event_handler, f_orgn, True)
        watchdog.start()
        try:
            while watchdog.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            watchdog.stop()

def enable(*name): list(map(lambda val: root.children[val].configure(state=NORMAL), name))
def disable(*name): list(map(lambda val: root.children[val].configure(state=DISABLED), name))

def insert(name, value): e=root.children[name]; e.delete(0,END); e.insert(0, value)

class F_Buttons:
    def selectFolder(entry): e = entry[0]; e.delete(0, END); e.insert(0, askdir(title=f"Selecciona la ruta de {e.winfo_name()}") + "/")
    def start():
        enable("detain"); global f_dstn, f_orgn, c_dstn, c_orgn
        c_dstn = split(str(destino[1].get()))[1]; c_orgn = split(str(origen[1].get()))[1]
        f_dstn = f"{split(str(destino[1].get()))[0]}/"; f_orgn = f"{split(str(origen[1].get()))[0]}/"; setVal("switch", True)
        if exists(f_dstn) and exists(f_orgn): 
            Thread(target=getFiles).start() 
            disable("start", "btn_origen", "btn_destino", "day", "month", "year", "etr_origen", "etr_destino", "si", "no")
        else: print("Ingrese un directorio valido")
    def stop(): 
        global watchdog; setVal("switch", False); disable("detain"); watchdog.stop()
        enable("start", "btn_origen", "btn_destino", "day", "month", "year", "etr_origen", "etr_destino", "empty", "si", "no")

    def empty(): setVal("files", []); disable("empty")

class DB_Buttons:
    def selectFile(): return askopenfile(title=f"Selecciona el archivo backup ")
    def testConnection():
        try:
            query = "SELECT VERSION();"; enable("dbname"); run_query(query)
            enable("db_restore", "search_db")
        except:
            disable("dbname", "tbname", "reinit")
            print("Error al conectar a la base de datos")
    def restartProcess():
        enable("test"); disable("reinit")
    def brwsDB():
        popup = Tk(); popup.overrideredirect(True); popup.configure(borderwidth=1, relief="solid")
        x_root = root.winfo_x(); y_root = root.winfo_y(); srchdb = root.children["search_db"]
        w_srchdb = srchdb.winfo_width(); h_srchdb = srchdb.winfo_height(); x_srchdb = srchdb.winfo_x(); y_srchdb = srchdb.winfo_y()
        popup.geometry(f"{240}x{120}+{x_root+x_srchdb+w_srchdb}+{y_root+y_srchdb+h_srchdb}")

        def ads(): popup.unbind("<FocusOut>"); popup.destroy()
        popup.bind("<FocusOut>", lambda event: ads()); 
        ldb = Listbox(popup, background="white", foreground="black", selectmode=SINGLE); ldb.pack(fill=BOTH, expand=1)
        try:
            query = f"SHOW DATABASES LIKE '{db_name.get()}';"
            values = run_query(query)
            for value in values:
                ldb.insert(END, value)
        except:
            lb.insert("",0, values=(f"Error E005: SHOW DATABASES, Verifica tu información.",))
        
        popup.focus_set(); popup.focus_force()

        for n, i in enumerate(ldb.get(0, END)):
            if n & 1 == 0:
                ldb.itemconfig(n, background="#F5F5F5", foreground="black")
            else:
                ldb.itemconfig(n, background="white", foreground="black")
        def insertar():
            dbn = root.children["dbname"]
            dbn.delete(0, "end")
            dbn.insert(0, ldb.get(ldb.curselection())[0])
            ads()
            enable("tbname", "db_delete", "db_empty", "db_backup", "db_restore", "tb_restore", "search_tb")
            
        ldb.bind("<Double-Button-1>", lambda event: insertar())

    def brwsTB():
        popup = Tk(); popup.overrideredirect(True); popup.configure(borderwidth=1, relief="solid", bg="red")
        x_root = root.winfo_x(); y_root = root.winfo_y(); srchdb = root.children["search_tb"]
        w_srchdb = srchdb.winfo_width(); h_srchdb = srchdb.winfo_height(); x_srchdb = srchdb.winfo_x(); y_srchdb = srchdb.winfo_y()
        popup.geometry(f"{240}x{120}+{x_root+x_srchdb+w_srchdb}+{y_root+y_srchdb+h_srchdb}")

        def ads(): popup.unbind("<FocusOut>"); popup.destroy()
        popup.bind("<FocusOut>", lambda event: ads()); 
        ldb = Listbox(popup, background="white", foreground="black", selectmode=SINGLE); ldb.pack(fill=BOTH, expand=1)
        
        try:
            query = f"SHOW TABLES FROM `{db_name.get()}` LIKE '{tb_name.get()}';"
            values = run_query(query)
            for value in values:
                ldb.insert(END, value)
        except:
            print("Error al conectar a la base de datos")
        
        popup.focus_set(); popup.focus_force()

        for n, i in enumerate(ldb.get(0, END)):
            if n & 1 == 0: ldb.itemconfig(n, background="#F5F5F5", foreground="black")
            else: ldb.itemconfig(n, background="white", foreground="black")
        def insertar():
            dbn = root.children["tbname"]
            dbn.delete(0, "end"); dbn.insert(0, ldb.get(ldb.curselection())[0])
            ads(); enable("tb_delete", "tb_empty", "tb_backup", "tb_restore")
        ldb.bind("<Double-Button-1>", lambda event: insertar())

    def delDB():
        try: 
            if run_query(query = f"DROP DATABASE `{db_name.get()}`") == None:
                disable("db_backup", "db_empty", "db_delete", "search_tb", "tbname", "tb_restore")
                insert("dbname", "")

        except: print("Error al eliminar la base de datos")
    def delTB():
        try: 
            if run_query(query = f"DROP TABLE `{db_name.get()}`.`{tb_name.get()}`") == None:
                disable("tb_backup", "tb_empty", "tb_delete")
                insert("tbname", "")
        except: print("Error al eliminar la tabla")
    def empDB():
        try: 
            query = f"SHOW TABLES FROM '{db_name.get()}';"
            for table in run_query(query):
                query = f"DROP TABLE {db_name.get()}.{table[0]}"
                run_query(query)
                print(f"Tabla {table} eliminada")
        except: print("Error al eliminar la base de datos")
    def truTB():
        try: 
            query = f"TRUNCATE TABLE `{db_name.get()}`.`{tb_name.get()}`;"
            run_query(query)
        except: print("Error al eliminar la base de datos")
    def backDB():
        try: createBackupDB(db_name.get())
        except: print("Error al crear el backup")
    def backTB():
        try: createBackupTB(db_name.get(), tb_name.get())
        except: print("Error al crear el backup")

    def restDB():
        file = DB_Buttons.selectFile()
        if file != None:
            content = file.readlines()
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
                    enable("search_db", "search_tb","tbname", "db_delete", "db_empty", "db_backup")

    def restTB():
        file = DB_Buttons.selectFile()
        if file != None:
            content = file.readlines()
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
                    enable("search_tb", "tbname", "tb_delete", "tb_empty", "tb_backup")

        
class F_Entrys:
    def enable():
        if user.get() != "" and host.get() != "": enable("test")
        else: disable("test")
        if db_name.get() != "":  enable("search_db")
        else: disable("search_db")
        if db_name.get() != "" and tb_name.get() != "": enable("search_tb")

    
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
        disable("init", "tb_delete", "tb_empty", "tb_backup")


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
                        root.destroy()
                else:
                    root.destroy()
            else:
                root.destroy()


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
            Button(master, text="Activar", justify="center", name="init", command=lambda: DB_Buttons.onUpld(), state=DISABLED).place(x=320, y=165, width=60, height=20)
            Button(master, text="Desactivar", justify="center", name="stop", command=lambda: DB_Buttons.offUpld(), state=DISABLED).place(x=390, y=165, width=60, height=20)
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
            origen[0].insert(0, "C:/Users/DELL/Desktop/DELL/Batch/")
            destino[0].insert(0, "C:/Users/DELL/Downloads/")

            # Control de archivos: Entrys | Periodo
            global day, month, year; day, month, year = IntVar(),IntVar(),IntVar()
            lDate = datetime.now().date()
            Entry(master, textvariable=day, name="day").place(x=318, y=26, width=20, height=16)
            Entry(master, textvariable=month, name="month").place(x=368, y=26, width=20, height=16)
            Entry(master, textvariable=year, name="year").place(x=418, y=26, width=40, height=16)
            def wrEntrys(master, key, content): master.children.get(key).delete(0, "end");master.children.get(key).insert(0,content)
            wrEntrys(master, "day", 1); wrEntrys(master, "month", 1);wrEntrys(master, "year", lDate.year)

            # Acceso a la base de datos: Entrys | Credenciales
            global user, host, password, db_name, tb_name
            user, host, password, db_name, tb_name = StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
            Entry(master, textvariable=user, name="user").place(x=10, y=165, width=230, height=20)
            Entry(master, textvariable=host, name="host").place(x=10, y=210, width=230, height=20)
            Entry(master, textvariable=password, name="pass").place(x=10, y=255, width=230, height=20)
            Entry(master, textvariable=db_name, name="dbname", state=DISABLED).place(x=10, y=300, width=230, height=20)
            Entry(master, textvariable=tb_name, name="tbname", state=DISABLED).place(x=10, y=345, width=230, height=20)

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
        def A_ICA_D(file):            
            return askyesnocancel("Error", 
            f"Ocurrio un error al intentar copiar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?")
        def A_IEA_D(file):            
            return askyesnocancel("Error",
            f"Ocurrio un error al intentar eliminar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?")
        def A_IRA_D(file):
            return askyesnocancel("Error",
            f"Ocurrio un error al intentar renombrar \"{basename(file)}\" a la carpeta destino.\n\n" +
            "¿Desea omitir este archivo?")

        def E_DCA_D(file):
            return showerror("Error",
            f"Ocurrio un error al intentar copiar \"{basename(file)}\" a la carpeta destino.\n\n")
        def E_DEA_D(file):
            return showerror("Error",
            f"Ocurrio un error al intentar eliminar \"{basename(file)}\" a la carpeta destino.\n\n")
        def E_DRA_D(file):
            return showerror("Error",
            f"Ocurrio un error al intentar renombrar \"{basename(file)}\" a la carpeta destino.\n\n")

        


if __name__ == "__main__":
    root = Tk()
    GUI(root)
    root.mainloop()

        
