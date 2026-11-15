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

# Creamos una clase para administrar las reservas del sistema.
class GestorReservas:

# Inicializamos una lista para guardar las reservas.
    def __init__(self):
        self.__reservas = []

    # Registramos una nueva reserva.
    def registrar_reserva(self, reserva):

        # Verificamos que el objeto sea de tipo Reserva.
        if not isinstance(reserva, Reserva):
            raise TypeError("Debe registrar un objeto de tipo Reserva.")

        # Evitamos registrar reservas con la misma identificación.
        for reserva_registrada in self.__reservas:
            if reserva_registrada.identificacion == reserva.identificacion:
                raise ValueError("Ya existe una reserva con esa identificación.")

        # Agregamos la reserva a la lista.
        self.__reservas.append(reserva)

        return "Reserva registrada correctamente."

    # Buscamos una reserva por su identificación.
    def buscar_reserva(self, identificacion):

        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("Debe ingresar una identificación válida.")

        for reserva in self.__reservas:
            if reserva.identificacion == identificacion.strip():
                return reserva

        return None

    # Consultamos todas las reservas registradas.
    def listar_reservas(self):
        return tuple(self.__reservas)

    # Consultamos la cantidad de reservas.
    @property
    def total_reservas(self):
        return len(self.__reservas)

