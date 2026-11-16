from abc import ABC, abstractmethod
from FASE4 import Entidad

# Creamos la clase abstracta Servicio, que hereda de Entidad y ABC.
class Servicio(Entidad, ABC):

    # Inicializamos los datos comunes de cualquier servicio.
    def __init__(self, identificador, nombre_servicio, precio_base):
        
        # Validamos el identificador llamando al constructor padre.
        super().__init__(identificador)

        # Verificamos que el nombre del servicio sea válido.
        if not isinstance(nombre_servicio, str) or not nombre_servicio.strip():
            raise ValueError("El nombre del servicio no puede estar vacío.")

        # Verificamos que el precio base sea un número positivo.
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ValueError("El precio base debe ser un valor numérico mayor a cero.")

        # Guardamos los atributos de forma privada.
        self.__nombre_servicio = nombre_servicio.strip()
        self.__precio_base = float(precio_base)

    # Consultamos el nombre del servicio.
    @property
    def nombre_servicio(self):
        return self.__nombre_servicio

    # Consultamos el precio base.
    @property
    def precio_base(self):
        return self.__precio_base

    # Indicamos el tipo de entidad.
    def obtener_tipo(self):
        return "Servicio"

    # Método abstracto obligatorio para calcular costos (aplicando polimorfismo).
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    # Método abstracto obligatorio para describir el servicio.
    @abstractmethod
    def describir_servicio(self):
        pass


# Servicio Especializado 1: Reserva de Salas
class ReservaSalas(Servicio):
    def __init__(self, identificador, nombre_servicio, precio_base, capacidad_personas):
        super().__init__(identificador, nombre_servicio, precio_base)
        
        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise ValueError("La capacidad de personas debe ser un entero positivo.")
        
        self.__capacidad_personas = capacidad_personas

    # Método sobrecargado para calcular costos (admite horas, descuentos e impuestos).
    def calcular_costo(self, horas=1, aplica_descuento=False, impuesto=0.19):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas de reserva deben ser mayores a cero.")
        
        costo_total = self.precio_base * horas
        if aplica_descuento:
            costo_total *= 0.90  # 10% de descuento
            
        costo_total += costo_total * impuesto
        return round(costo_total, 2)

    def describir_servicio(self):
        return f"Reserva de Sala: {self.nombre_servicio} (Capacidad: {self.__capacidad_personas} personas)"


# Servicio Especializado 2: Alquiler de Equipos
class AlquilerEquipos(Servicio):
    def __init__(self, identificador, nombre_servicio, precio_base, marca):
        super().__init__(identificador, nombre_servicio, precio_base)
        
        if not isinstance(marca, str) or not marca.strip():
            raise ValueError("La marca del equipo es obligatoria.")
        
        self.__marca = marca.strip()

    def calcular_costo(self, dias=1, seguro_adicional=0.0):
        if not isinstance(dias, int) or dias <= 0:
            raise ValueError("Los días de alquiler deben ser un entero positivo.")
        if not isinstance(seguro_adicional, (int, float)) or seguro_adicional < 0:
            raise ValueError("El seguro adicional no puede ser negativo.")
        
        costo_total = (self.precio_base * dias) + seguro_adicional
        return round(costo_total, 2)

    def describir_servicio(self):
        return f"Alquiler de Equipo: {self.nombre_servicio} - Marca: {self.__marca}"


# Servicio Especializado 3: Asesorías Especializadas
class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador, nombre_servicio, precio_base, area_especialidad):
        super().__init__(identificador, nombre_servicio, precio_base)
        
        if not isinstance(area_especialidad, str) or not area_especialidad.strip():
            raise ValueError("El área de especialidad es obligatoria.")
        
        self.__area_especialidad = area_especialidad.strip()

    def calcular_costo(self, sesiones=1, nivel_complejidad=1.0):
        if not isinstance(sesiones, int) or sesiones <= 0:
            raise ValueError("El número de sesiones debe ser un entero positivo.")
        if not isinstance(nivel_complejidad, (int, float)) or nivel_complejidad <= 0:
            raise ValueError("El nivel de complejidad debe ser mayor a cero.")
        
        costo_total = self.precio_base * sesiones * nivel_complejidad
        return round(costo_total, 2)

    def describir_servicio(self):
        return f"Asesoría Especializada en {self.__area_especialidad}: {self.nombre_servicio}"
