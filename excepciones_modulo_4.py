# Módulo 4: Manejo de excepciones y registro de errores


# Importamos la herramienta para registrar eventos y errores.
import logging


# Creamos una excepción general para el sistema.
class ErrorSistema(Exception):
    pass


# Representamos errores causados por datos incorrectos.
class DatosInvalidosError(ErrorSistema):
    pass


# Representamos errores por parámetros faltantes.
class ParametroFaltanteError(ErrorSistema):
    pass


# Representamos operaciones que no están permitidas.
class OperacionNoPermitidaError(ErrorSistema):
    pass


# Representamos errores en las reservas.
class ReservaIncorrectaError(ErrorSistema):
    pass


# Representamos servicios que no están disponibles.
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Representamos errores en los cálculos.
class CalculoInconsistenteError(ErrorSistema):
    pass


# Configuramos el registro de eventos y errores.
def configurar_registro():

    # Creamos el registrador del sistema.
    registrador = logging.getLogger("SoftwareFJ")

    registrador.setLevel(logging.INFO)
    registrador.propagate = False

    # Evitamos crear varios archivos de registro.
    if not registrador.handlers:

        # Creamos el archivo donde se guardarán los eventos.
        archivo = logging.FileHandler(
            "eventos_errores.log",
            encoding="utf-8"
        )

        # Definimos el formato de los registros.
        formato = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        archivo.setFormatter(formato)
        registrador.addHandler(archivo)

    return registrador


# Inicializamos el registrador del sistema.
registrador = configurar_registro()


# Registramos un evento importante.
def registrar_evento(mensaje):
    registrador.info(mensaje)


# Registramos un error ocurrido durante la ejecución.
def registrar_error(mensaje):
    registrador.error(mensaje)