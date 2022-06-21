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
Solo visibles en las opciones para la base de datos.

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

