# Módulo 4: Manejo de excepciones y registro de errores


# Importamos la herramienta para registrar eventos y errores.
from pathlib import Path
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

        # Definimos la ruta del archivo de log
        ruta_log = Path(__file__).parent / "eventos_errores.log"
        # Creamos el archivo donde se guardarán los eventos.
        archivo = logging.FileHandler(
            ruta_log,
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

# Validamos que los parámetros obligatorios tengan información.
def validar_parametros_obligatorios(**parametros):

    for nombre, valor in parametros.items():

        if valor is None or (
            isinstance(valor, str) and not valor.strip()
        ):
            raise ParametroFaltanteError(
                f"Falta el parámetro obligatorio: {nombre}."
            )

    return True


# Verificamos que un servicio esté disponible.
def validar_servicio_disponible(disponible):

    if not isinstance(disponible, bool):
        raise DatosInvalidosError(
            "La disponibilidad debe ser verdadera o falsa."
        )

    if not disponible:
        raise ServicioNoDisponibleError(
            "El servicio seleccionado no está disponible."
        )

    return True


# Verificamos que una operación esté permitida.
def validar_operacion_permitida(permitida):

    if not isinstance(permitida, bool):
        raise DatosInvalidosError(
            "El permiso de operación debe ser verdadero o falso."
        )

    if not permitida:
        raise OperacionNoPermitidaError(
            "La operación solicitada no está permitida."
        )

    return True


# Verificamos que el estado de una reserva sea válido.
def validar_estado_reserva(estado, estados_permitidos):

    if not isinstance(estado, str) or estado not in estados_permitidos:
        raise ReservaIncorrectaError(
            "La reserva tiene un estado incorrecto."
        )

    return True


# Ejecutamos operaciones controlando los posibles errores.
def ejecutar_operacion(operacion, *args, **kwargs):

    try:
        # Comprobamos que se pueda ejecutar la operación.
        if not callable(operacion):
            raise ParametroFaltanteError(
                "Debe proporcionar una función válida."
            )

        # Ejecutamos la operación solicitada.
        resultado = operacion(*args, **kwargs)

    except ErrorSistema as error:

        # Registramos los errores personalizados.
        registrar_error(f"Error controlado: {error}")
        raise

    except Exception as error:

        # Registramos los errores inesperados.
        registrador.exception("Se produjo un error inesperado.")

        # Encadenamos la excepción original.
        raise ErrorSistema(
            "Ocurrió un error inesperado durante la operación."
        ) from error

    else:

        # Registramos cuando la operación termina correctamente.
        registrar_evento("La operación se ejecutó correctamente.")
        return resultado

    finally:

        # Registramos el final de cada intento.
        registrar_evento("Finalizó el intento de operación.")    