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


# Creamos una clase para gestionar los clientes del sistema.
class GestorClientes:

    # Inicializamos una lista para guardar los clientes.
    def __init__(self):
        self.__clientes = []

    # Registramos un nuevo cliente en la lista.
    def registrar_cliente(self, cliente):

        # Verificamos que el objeto sea de tipo Cliente.
        if not isinstance(cliente, Cliente):
            raise TypeError("El registro debe ser un objeto de tipo Cliente.")

        # Comprobamos que no exista otro cliente con la misma identificación.
        for cliente_registrado in self.__clientes:
            if cliente_registrado.identificador == cliente.identificador:
                raise ValueError("Ya existe un cliente con esa identificación.")

        # Agregamos el cliente a la lista.
        self.__clientes.append(cliente)

        return "Cliente registrado correctamente."

    # Buscamos un cliente por su identificación.
    def buscar_cliente(self, identificacion):

        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ValueError("Debe ingresar una identificación válida.")

        for cliente in self.__clientes:
            if cliente.identificador == identificacion.strip():
                return cliente

        return None

    # Consultamos todos los clientes registrados.
    def listar_clientes(self):
        return tuple(self.__clientes)

    # Consultamos la cantidad de clientes registrados.
    @property
    def total_clientes(self):
        return len(self.__clientes)
