# Fase 4 - Programación
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Grupo: 213023_376


#  Importamos lo necesario para trabajar con clases abstractas.
from abc import ABC, abstractmethod


#  Creamos la clase Entidad, que será la clase base del sistema.
class Entidad(ABC):

    #  Inicializamos la clase y recibimos el identificador.
    def __init__(self, identificador):

        # Verificamos que el identificador tenga un valor válido.
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador no puede estar vacío.")

        # Guardamos el identificador para utilizarlo más adelante.
        self.__identificador = identificador.strip()

    #  Este método permite consultar el identificador.
    @property
    def identificador(self):
        return self.__identificador

    #  Este método deberá ser desarrollado por las clases que hereden de Entidad.
    @abstractmethod
    def obtener_tipo(self):
        pass

# Creamos la clase Cliente, que hereda de Entidad.
class Cliente(Entidad):

    # Inicializamos los datos personales del cliente.
    def __init__(self, identificacion, nombre, correo, telefono):

        # Llamamos al constructor de la clase Entidad.
        super().__init__(identificacion)

        # Verificamos que el nombre no esté vacío.
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")

        # Verificamos que el correo tenga un formato básico válido.
        if not isinstance(correo, str):
            raise ValueError("El correo debe ser un texto válido.")

        correo = correo.strip().lower()

        if correo.count("@") != 1 or " " in correo:
            raise ValueError("El correo electrónico no es válido.")

        if "." not in correo.split("@")[1]:
            raise ValueError("El correo electrónico no es válido.")

        # Verificamos que el teléfono tenga un formato correcto.
        if not isinstance(telefono, str):
            raise ValueError("El teléfono debe ser un texto.")

        telefono_limpio = telefono.strip().replace(" ", "").replace("-", "")

        if telefono_limpio.startswith("+"):
            telefono_limpio = telefono_limpio[1:]

        if not telefono_limpio.isdigit() or not 7 <= len(telefono_limpio) <= 15:
            raise ValueError("El número de teléfono no es válido.")

        # Guardamos los datos personales de forma privada.
        self.__nombre = nombre.strip()
        self.__correo = correo
        self.__telefono = telefono.strip()

    # Consultamos el nombre del cliente.
    @property
    def nombre(self):
        return self.__nombre

    # Consultamos el correo electrónico.
    @property
    def correo(self):
        return self.__correo

    # Consultamos el teléfono.
    @property
    def telefono(self):
        return self.__telefono

    # Indicamos el tipo de entidad.
    def obtener_tipo(self):
        return "Cliente"
