# Módulo 3: Gestión de reservas


# Importamos las herramientas necesarias.
from math import isfinite
from FASE4 import Cliente


# Creamos la clase Reserva para gestionar las reservas del sistema.
class Reserva:

    # Inicializamos los datos de la reserva.
    def __init__(self, identificacion, cliente, servicio, duracion):

        # Verificamos que la identificación no esté vacía.
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("La identificación de la reserva es obligatoria.")

        # Verificamos que el cliente sea válido.
        if not isinstance(cliente, Cliente):
            raise TypeError("La reserva debe tener un cliente válido.")

        # Comprobamos que se haya seleccionado un servicio.
        if servicio is None:
            raise ValueError("Debe seleccionar un servicio.")

        # Verificamos que la duración sea un número válido.
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not isfinite(duracion)
            or duracion <= 0
        ):
            raise ValueError("La duración debe ser mayor que cero.")

        # Guardamos los datos de la reserva.
        self.__identificacion = identificacion.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion

        # Todas las reservas comienzan pendientes.
        self.__estado = "Pendiente"
    