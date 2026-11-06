# Fase 4 - Programación
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Grupo: 213023_376


# 1. Importamos lo necesario para trabajar con clases abstractas.
from abc import ABC, abstractmethod


# 2. Creamos la clase Entidad, que será la clase base del sistema.
class Entidad(ABC):

    # 3. Inicializamos la clase y recibimos el identificador.
    def __init__(self, identificador):

        # Verificamos que el identificador tenga un valor válido.
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador no puede estar vacío.")

        # Guardamos el identificador para utilizarlo más adelante.
        self.__identificador = identificador.strip()

    # 4. Este método permite consultar el identificador.
    @property
    def identificador(self):
        return self.__identificador

    # 5. Este método deberá ser desarrollado por las clases que hereden de Entidad.
    @abstractmethod
    def obtener_tipo(self):
        pass
