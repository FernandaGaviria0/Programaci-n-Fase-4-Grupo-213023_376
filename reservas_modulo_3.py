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

        # Consultamos la identificación de la reserva.
    @property
    def identificacion(self):
        return self.__identificacion

    # Consultamos el cliente de la reserva.
    @property
    def cliente(self):
        return self.__cliente

    # Consultamos el servicio seleccionado.
    @property
    def servicio(self):
        return self.__servicio

    # Consultamos la duración de la reserva.
    @property
    def duracion(self):
        return self.__duracion

    # Consultamos el estado de la reserva.
    @property
    def estado(self):
        return self.__estado

    # Confirmamos una reserva pendiente.
    def confirmar(self):

        if self.__estado != "Pendiente":
            raise ValueError("La reserva no se puede confirmar.")

        self.__estado = "Confirmada"

        return "Reserva confirmada correctamente."

    # Cancelamos una reserva.
    def cancelar(self):

        if self.__estado not in ("Pendiente", "Confirmada"):
            raise ValueError("La reserva no se puede cancelar.")

        self.__estado = "Cancelada"

        return "Reserva cancelada correctamente."

    # Procesamos una reserva que ya fue confirmada.
    def procesar(self):

        try:
            if self.__estado != "Confirmada":
                raise ValueError(
                    "La reserva debe estar confirmada para procesarse."
                )

            if self.__cliente is None or self.__servicio is None:
                raise ValueError("Los datos de la reserva están incompletos.")

        except ValueError as error:
            raise RuntimeError(
                "No fue posible procesar la reserva."
            ) from error

        else:
            self.__estado = "Procesada"
            return "Reserva procesada correctamente."

