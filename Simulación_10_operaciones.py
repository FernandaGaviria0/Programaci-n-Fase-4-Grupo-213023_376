import importlib.util
import sys
from pathlib import Path


def localizar_carpeta_proyecto():
    base = Path(__file__).resolve().parent
    objetivo = base / "excepciones_modulo_4.py"
    if objetivo.exists():
        return base
    for encontrado in base.rglob("excepciones_modulo_4.py"):
        return encontrado.parent
    raise FileNotFoundError("No se encontró excepciones_modulo_4.py en el proyecto.")


CARPETA_PROYECTO = localizar_carpeta_proyecto()
if str(CARPETA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(CARPETA_PROYECTO))

ruta_servicios = CARPETA_PROYECTO / "Clase abstracta y especializaciones.py"
spec = importlib.util.spec_from_file_location("servicios_mod", ruta_servicios)
servicios_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(servicios_mod)

ReservaSalas = servicios_mod.ReservaSalas
AlquilerEquipos = servicios_mod.AlquilerEquipos
AsesoriaEspecializada = servicios_mod.AsesoriaEspecializada

from FASE4 import Cliente, GestorClientes
from reservas_modulo_3 import Reserva, GestorReservas
from excepciones_modulo_4 import (
    ErrorSistema,
    DatosInvalidosError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    validar_parametros_obligatorios,
    validar_servicio_disponible,
    validar_operacion_permitida,
    validar_estado_reserva,
    ejecutar_operacion,
    registrar_evento,
    registrar_error,
)


def correr_prueba(numero, descripcion, accion, razon_fallo):
    print(f"--- Prueba {numero}: {descripcion} ---")
    try:
        resultado = ejecutar_operacion(accion)
        print(f"Resultado: {resultado}\n")
        return resultado
    except Exception as exc:
        detalle = str(exc).strip()
        if detalle:
            mensaje_error = f"Prueba {numero} falló ({razon_fallo}) -> Detalle: {detalle}"
        else:
            mensaje_error = f"Prueba {numero} falló ({razon_fallo})"

        try:
            raise ErrorSistema(mensaje_error) from exc
        except ErrorSistema as encadenado:
            registrar_error(str(encadenado))
            print(f"Error: {encadenado}\n")
            return None


def simular_sistema():
    registrar_evento("=== INICIO DE SIMULACIÓN (PRUEBAS 1 A 10 - SOFTWARE FJ) ===")
    gestor_clientes = GestorClientes()
    gestor_reservas = GestorReservas()
    servicios_creados = []

    cliente_valido = [None]
    sala_valida = [None]
    reserva_activa = [None]

    # Prueba 1: Registro válido de cliente
    def p1():
        c = Cliente("CC-1001", "Laura Gaviria", "laura@softwarefj.com", "+57 3001234567")
        msg = gestor_clientes.registrar_cliente(c)
        cliente_valido[0] = c
        return f"{msg} Total clientes: {gestor_clientes.total_clientes}"

    correr_prueba(
        1,
        "Registro válido de cliente",
        p1,
        "no se pudo registrar el cliente válido",
    )

    # Prueba 2: Registro inválido de cliente (correo inválido)
    def p2():
        validar_parametros_obligatorios(
            identificacion="CC-1002", nombre="Carlos", correo="correo_invalido"
        )
        c_malo = Cliente("CC-1002", "Carlos", "correo_invalido", "3009876543")
        return gestor_clientes.registrar_cliente(c_malo)

    correr_prueba(
        2,
        "Registro inválido de cliente por correo",
        p2,
        "el correo electrónico no tiene un formato válido (falta '@' o dominio)",
    )

    # Prueba 3: Registro de segundo cliente válido
    def p3():
        c2 = Cliente("CC-1003", "Andrés Pérez", "andres@softwarefj.com", "3105551234")
        return gestor_clientes.registrar_cliente(c2)

    correr_prueba(
        3,
        "Registro válido de segundo cliente",
        p3,
        "no se pudo registrar el segundo cliente",
    )

    # Prueba 4: Creación correcta de servicio de Reserva de Salas y cálculo de costo
    def p4():
        sala = ReservaSalas("SAL-01", "Sala Conferencias A", 60000, 20)
        validar_servicio_disponible(True)
        servicios_creados.append(sala)
        sala_valida[0] = sala
        costo = sala.calcular_costo(horas=3, aplica_descuento=True, impuesto=0.19)
        return f"{sala.describir_servicio()} | Costo (3h, desc 10%, IVA 19%): ${costo}"

    correr_prueba(
        4,
        "Creación correcta de ReservaSalas y cálculo de costo",
        p4,
        "no se pudo crear la sala o calcular su costo",
    )

    # Prueba 5: Creación incorrecta de servicio (precio base inválido)
    def p5():
        equipo_malo = AlquilerEquipos("EQ-01", "Proyector", -5000, "Epson")
        servicios_creados.append(equipo_malo)
        return equipo_malo.describir_servicio()

    correr_prueba(
        5,
        "Creación incorrecta de servicio con precio negativo",
        p5,
        "ingrese un valor mayor a 0 para el precio base del servicio",
    )

    # Prueba 6: Creación correcta de AlquilerEquipos y AsesoriaEspecializada
    def p6():
        equipo = AlquilerEquipos("EQ-02", "Cámara Full HD", 40000, "Sony")
        asesoria = AsesoriaEspecializada(
            "ASE-01", "Auditoría de Código", 90000, "Calidad de Software"
        )
        servicios_creados.extend([equipo, asesoria])
        c_eq = equipo.calcular_costo(dias=2, seguro_adicional=10000)
        c_as = asesoria.calcular_costo(sesiones=2, nivel_complejidad=1.2)
        return (
            f"Servicios activos: {len(servicios_creados)} | "
            f"Equipo: ${c_eq} | Asesoría: ${c_as}"
        )

    correr_prueba(
        6,
        "Creación de AlquilerEquipos y AsesoriaEspecializada",
        p6,
        "no se pudieron crear los servicios adicionales o calcular sus costos",
    )

    # Prueba 7: Reserva exitosa (registrar, confirmar y procesar)
    def p7():
        if cliente_valido[0] is None or sala_valida[0] is None:
            raise ReservaIncorrectaError(
                "debe existir un cliente y un servicio válidos antes de crear la reserva"
            )
        res = Reserva("RES-001", cliente_valido[0], sala_valida[0], 3)
        msg_reg = gestor_reservas.registrar_reserva(res)
        msg_conf = res.confirmar()
        msg_proc = res.procesar()
        reserva_activa[0] = res
        return f"{msg_reg} -> {msg_conf} -> {msg_proc} (Estado final: {res.estado})"

    correr_prueba(
        7,
        "Reserva exitosa (registrar, confirmar y procesar)",
        p7,
        "no se pudo completar el registro, confirmación o procesamiento de la reserva",
    )

    # Prueba 8: Intento de reserva fallido por duración inválida
    def p8():
        if cliente_valido[0] is None or sala_valida[0] is None:
            raise ReservaIncorrectaError(
                "falta un cliente o servicio válido para probar la reserva"
            )
        res_invalida = Reserva("RES-002", cliente_valido[0], sala_valida[0], 0)
        return gestor_reservas.registrar_reserva(res_invalida)

    correr_prueba(
        8,
        "Intento de reserva fallido por duración inválida",
        p8,
        "ingrese una duración mayor a 0 para la reserva",
    )

    # Prueba 9: Intento de operación no permitida
    def p9():
        validar_operacion_permitida(False)
        return "No debería ejecutarse"

    correr_prueba(
        9,
        "Intento de operación no permitida",
        p9,
        "la operación solicitada no está permitida en el estado actual del sistema",
    )

    # Prueba 10: Intento de cancelar una reserva ya procesada
    def p10():
        if reserva_activa[0] is None:
            raise ReservaIncorrectaError("no hay una reserva registrada para validar")
        validar_estado_reserva(reserva_activa[0].estado, ("Pendiente", "Confirmada"))
        return reserva_activa[0].cancelar()

    correr_prueba(
        10,
        "Intento de cancelar una reserva ya procesada",
        p10,
        "no se puede cancelar una reserva que ya fue procesada",
    )

    registrar_evento("=== FIN DE SIMULACIÓN (PRUEBAS 1 A 10 - SOFTWARE FJ) ===")
    print(f"Simulación completada. Revisa el registro en: {CARPETA_PROYECTO / 'eventos_errores.log'}")


if __name__ == "__main__":
    simular_sistema()