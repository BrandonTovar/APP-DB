# Documentación de funciones del programa UpdateDB

Nombre de error, descripción y como solucionarlo
    
    E_DEI   | Hubo un problema al copiar el archivo

    Nombre:         E_DEI
    Descripcion:    Error al copiar {nameFile} a la carpeta destino.
    Motivo:         Este error puede ser provocado:
                        1.- cuando el archivo de origen ha sido eliminado.
                        2.- cuando el usuario no tiene permisos de escritura sobre la carpeta destino.
    Solución:       1.- Detener el proceso de copiado, reiniciar la cola e iniciar denuevo.
                    2.- Verificar que el usuario tenga los permisos necesarios para escribir en la carpeta destino.


    E_DEI_A | Directorios inaccesibles

    Nombre:         E_DEI_A
    Descripcion:    Los directorios establecidos son inaccesibles
    Motivo:         Este error puede ser provocado:
                        1.- Cuando se cambian los nombres de los directorios origen y destino.
                        2.- Cuando se perdio la conexion con el equipo anfitrion y reseptor.
    Solución:       Este error se solucionara si el equipo anfitrion y reseptor vuelve a estar en linea o seleccionando otras carpetas.


    E_DEI_O | Directorio origen inaccesible

    Nombre:         E_DEI_O
    Descripcion:    Verifica el directorio de origen.
    Motivo:         Este error es provocado cuando:
                        1.- Se cambio el nombre a la carpeta origen.
                        2.- Se perdio la conexion con el equipo anfitrion.
    Solución:       Este error se solucionara si el equipo anfitrion vuelve a estar en linea o seleccionando otra carpeta.


    E_DEI_D | Directorio destino inaccesible

    Nombre:         E_DEI_D
    Descripcion:    Verifica el directorio de destino.
    Motivo:         Este error es provocado cuando:
                        1.- Se cambio el nombre a la carpeta destino.
                        2.- Se perdio la conexion con el equipo reseptor.
    Solución:       Este error se solucionara si el equipo reseptor vuelve a estar en linea o seleccionando otra carpeta.


## Codigos de error y sus significados
>Lista con los errores documentados durante el desarrollo



    E001: | Error al conectar con la base de datos
    E002: | Error al buscar bases de datos                                      
    E003: | Error al buscar tablas
    E004: | Error al borrar la base de datos
    E005: | Error al borrar la tabla
    E006: | Error al limpiar la base de datos
    E007: | Error al limpiar la tabla
    E008: | Error al crear la copia de la base de datos
    E009: | Error al crear la copia de la tabla
    E010: | Error al restablecer la base de datos
    E011: | Error al restablecer la tabla 
    E012: | Error al iniciar el servicio
    E013: | Error al detener el servicio
    E014: | Error al subir los valores
    E015: | Error al eliminar los valores
    E016: | Error al crear la tabla
    E017: | Error al buscar la columna
    E018: | Error al crear la columna
    E019: | Error al actualizar el folio
    E020: | Se elimino el folio de la tabla por que el nombre del archivo no lo contiene
    E021: | El archivo eliminado en origen no existe en destino
    E022: | El archivo renombrado no tiene el folio en su nombre
    E023: | Error al crear la base de datos
    E024: | Error al crear la tabla
    E025: | El folio extraido no coincide con el del nombre
    E026: | No cuentas con los permisos necesarios
    E000: | Ocurrio un error inesperado, verifica tu informacion
    E027: | Se altero el archivo compañero en origen y en destino no existen como grupo



# 