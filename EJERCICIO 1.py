"""
=======================================================================
SISTEMA SOFTWARE FJ - ARCHIVO ÚNICO COMPLETO Y EJECUTABLE
=======================================================================
Módulos incluidos:
  1. Excepciones personalizadas
  2. Sistema de logs
  3. Entidades (clase abstracta base y Cliente)
  4. Servicios (abstracto + 3 especializados)
  5. Reservas
  6. Main con 20 operaciones de demostración
=======================================================================
Ejecución: python software_fj_completo.py
=======================================================================
"""


# =======================================================================
# SECCIÓN 1: EXCEPCIONES PERSONALIZADAS
# =======================================================================

class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""
    # Todos los errores del sistema heredan de esta clase,
    # lo que permite capturarlos todos con un solo except SoftwareFJError

    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        # Guarda el mensaje legible del error como atributo accesible externamente
        self.mensaje = mensaje
        # Guarda el código único del error para identificación programática
        self.codigo = codigo
        # Llama al constructor de Exception con el mensaje formateado [CODIGO] mensaje
        super().__init__(f"[{codigo}] {mensaje}")


# ── Excepciones de Cliente ─────────────────────────────────────────────

class ClienteError(SoftwareFJError):
    """Excepción base para errores relacionados con clientes."""
    # Agrupa todos los errores de cliente bajo un tipo común

    def __init__(self, mensaje: str, codigo: str = "ERR_CLIENTE"):
        # Delega al constructor de SoftwareFJError con el código de cliente por defecto
        super().__init__(mensaje, codigo)


class ClienteYaExisteError(ClienteError):
    # Se lanza cuando se intenta registrar un cliente cuya identificación ya existe

    def __init__(self, identificacion: str):
        # Incluye la identificación duplicada en el mensaje para facilitar el diagnóstico
        super().__init__(
            f"El cliente con identificación '{identificacion}' ya está registrado.",
            "ERR_CLIENTE_DUPLICADO"
        )


class ClienteNoEncontradoError(ClienteError):
    # Se lanza cuando se busca un cliente por ID y no existe ningún registro con ese valor

    def __init__(self, identificacion: str):
        # Incluye el ID buscado para que el desarrollador sepa qué valor falló
        super().__init__(
            f"No se encontró ningún cliente con identificación '{identificacion}'.",
            "ERR_CLIENTE_NO_ENCONTRADO"
        )


class DatosClienteInvalidosError(ClienteError):
    # Se lanza cuando un campo del cliente no supera las validaciones de formato

    def __init__(self, campo: str, valor):
        # Incluye el nombre del campo y el valor recibido para diagnóstico claro
        super().__init__(
            f"El campo '{campo}' tiene un valor inválido: '{valor}'.",
            "ERR_CLIENTE_DATOS_INVALIDOS"
        )


# ── Excepciones de Servicio ────────────────────────────────────────────

class ServicioError(SoftwareFJError):
    """Excepción base para errores relacionados con servicios."""
    # Agrupa todos los errores de servicio bajo un tipo común

    def __init__(self, mensaje: str, codigo: str = "ERR_SERVICIO"):
        # Delega al constructor base con el código de servicio por defecto
        super().__init__(mensaje, codigo)


class ServicioNoDisponibleError(ServicioError):
    # Se lanza cuando se intenta usar un servicio que está deshabilitado

    def __init__(self, nombre_servicio: str):
        # Usa el nombre del servicio para que el mensaje sea comprensible al usuario
        super().__init__(
            f"El servicio '{nombre_servicio}' no está disponible actualmente.",
            "ERR_SERVICIO_NO_DISPONIBLE"
        )


class ServicioNoEncontradoError(ServicioError):
    # Se lanza cuando se busca un servicio por ID y no existe ningún registro

    def __init__(self, id_servicio: str):
        # Incluye el ID buscado para identificar cuál servicio no existe
        super().__init__(
            f"No se encontró el servicio con ID '{id_servicio}'.",
            "ERR_SERVICIO_NO_ENCONTRADO"
        )


class ParametroServicioInvalidoError(ServicioError):
    # Se lanza cuando un parámetro no cumple las reglas del negocio
    # (horas fuera de rango, capacidad excedida, tipo de equipo inválido, etc.)

    def __init__(self, parametro: str, razon: str):
        # Incluye el nombre del parámetro y la razón específica del rechazo
        super().__init__(
            f"Parámetro inválido '{parametro}': {razon}.",
            "ERR_SERVICIO_PARAMETRO"
        )


class CostoInconsistenteError(ServicioError):
    # Se lanza cuando el cálculo de costo produce un valor incoherente (negativo, etc.)

    def __init__(self, detalle: str):
        # Incluye el detalle técnico del cálculo fallido para facilitar la depuración
        super().__init__(
            f"Cálculo de costo inconsistente: {detalle}.",
            "ERR_SERVICIO_COSTO"
        )


# ── Excepciones de Reserva ─────────────────────────────────────────────

class ReservaError(SoftwareFJError):
    """Excepción base para errores relacionados con reservas."""
    # Agrupa todos los errores del ciclo de vida de una reserva

    def __init__(self, mensaje: str, codigo: str = "ERR_RESERVA"):
        # Delega al constructor base con el código de reserva por defecto
        super().__init__(mensaje, codigo)


class ReservaNoEncontradaError(ReservaError):
    # Se lanza cuando se busca una reserva por ID y no existe en el sistema

    def __init__(self, id_reserva: str):
        # Incluye el ID buscado para identificar exactamente qué reserva no se encontró
        super().__init__(
            f"No se encontró la reserva con ID '{id_reserva}'.",
            "ERR_RESERVA_NO_ENCONTRADA"
        )


class ReservaOperacionInvalidaError(ReservaError):
    # Se lanza cuando se intenta una transición de estado no permitida
    # (confirmar una reserva cancelada, procesar sin haber confirmado, etc.)

    def __init__(self, operacion: str, estado_actual: str):
        # Incluye la operación intentada y el estado actual de la reserva
        super().__init__(
            f"Operación '{operacion}' no permitida en estado '{estado_actual}'.",
            "ERR_RESERVA_OPERACION"
        )


class DuracionInvalidaError(ReservaError):
    # Se lanza cuando las horas solicitadas están fuera del rango permitido por el servicio

    def __init__(self, duracion, minimo: float, maximo: float):
        # Muestra la duración recibida y el rango válido para que el error sea autoexplicativo
        super().__init__(
            f"Duración '{duracion}h' fuera del rango permitido [{minimo}h – {maximo}h].",
            "ERR_RESERVA_DURACION"
        )


class ReservaConflictoError(ReservaError):
    # Se lanza cuando ocurre un problema lógico en el procesamiento que no encaja en otras categorías

    def __init__(self, detalle: str):
        # Incluye el detalle del conflicto para facilitar el diagnóstico
        super().__init__(
            f"Conflicto en la reserva: {detalle}.",
            "ERR_RESERVA_CONFLICTO"
        )


# =======================================================================
# SECCIÓN 2: SISTEMA DE LOGS
# =======================================================================

# Módulo para interactuar con el sistema operativo (rutas, directorios)
import os
# Módulo para capturar y formatear trazas de error (stack trace)
import traceback
# Clase para obtener la fecha y hora actual
from datetime import datetime

# Define la ruta absoluta del archivo de logs en una subcarpeta "logs/"
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def _asegurar_directorio():
    # Extrae solo la parte del directorio de la ruta completa del log
    directorio = os.path.dirname(LOG_PATH)
    # Si la carpeta "logs/" no existe, la crea incluyendo subcarpetas si fuera necesario
    if not os.path.exists(directorio):
        os.makedirs(directorio)


def _escribir(nivel: str, mensaje: str, excepcion: Exception = None):
    # Garantiza que la carpeta de logs exista antes de escribir
    _asegurar_directorio()
    # Captura la fecha y hora actual con formato legible para el log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Construye la primera línea del registro con timestamp, nivel y mensaje
    lineas = [f"[{timestamp}] [{nivel}] {mensaje}"]
    # Si se pasó una excepción, intenta incluir la traza completa del error
    if excepcion:
        # Obtiene la traza del error activo en el contexto actual de ejecución
        tb = traceback.format_exc()
        # Solo agrega la traza si tiene contenido real (no es una traza vacía)
        if tb.strip() != "NoneType: None":
            lineas.append(f"  TRAZA: {tb.strip()}")
    # Une todas las líneas con salto de línea y agrega uno al final del bloque
    entrada = "\n".join(lineas) + "\n"
    # Abre el archivo en modo "append" para no sobreescribir registros anteriores
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        # Escribe la entrada completa en el archivo de logs
        f.write(entrada)
    # Imprime en consola un resumen visible para facilitar el seguimiento en la demo
    print(f"  📋 LOG [{nivel}]: {mensaje}")


def log_info(mensaje: str):
    # Registra un mensaje informativo de bajo impacto (operación exitosa, estado normal)
    _escribir("INFO", mensaje)


def log_advertencia(mensaje: str, excepcion: Exception = None):
    # Registra una situación anormal pero no crítica; el sistema puede continuar
    _escribir("ADVERTENCIA", mensaje, excepcion)


def log_error(mensaje: str, excepcion: Exception = None):
    # Registra un error que impidió completar una operación; requiere atención
    _escribir("ERROR", mensaje, excepcion)


def log_evento(mensaje: str):
    # Registra un evento relevante del negocio (registro de cliente, creación de reserva, etc.)
    _escribir("EVENTO", mensaje)


def leer_logs() -> str:
    """Retorna el contenido completo del archivo de logs."""
    try:
        # Intenta abrir y leer el archivo de logs existente
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            # Devuelve todo el contenido como una sola cadena de texto
            return f.read()
    except FileNotFoundError:
        # Si el archivo no existe aún (ningún log generado), retorna mensaje por defecto
        return "(Sin registros aún)"


# =======================================================================
# SECCIÓN 3: ENTIDADES (CLASE ABSTRACTA BASE Y CLIENTE)
# =======================================================================

# Módulo para trabajar con expresiones regulares (validación de correo, teléfono, etc.)
import re
# ABC: clase base para crear clases abstractas; abstractmethod: decorador para métodos obligatorios
from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════
# CLASE ABSTRACTA BASE
# ══════════════════════════════════════════════════════
class EntidadBase(ABC):
    """
    Clase abstracta que representa cualquier entidad registrable en el sistema.
    Principios aplicados: Abstracción, Encapsulación.
    """

    def __init__(self, id_entidad: str, nombre: str):
        # Atributo protegido: identificador único de la entidad (accesible en subclases)
        self._id = id_entidad
        # Atributo protegido: nombre legible de la entidad
        self._nombre = nombre
        # Toda entidad comienza como activa al momento de su creación
        self._activo = True

    @property
    def id(self) -> str:
        # Propiedad de solo lectura que expone el ID sin permitir modificación externa
        return self._id

    @property
    def nombre(self) -> str:
        # Propiedad de solo lectura que expone el nombre sin permitir modificación externa
        return self._nombre

    @property
    def activo(self) -> bool:
        # Propiedad de solo lectura que indica si la entidad está habilitada en el sistema
        return self._activo

    def desactivar(self):
        # Cambia el estado de la entidad a inactivo (baja lógica, no se elimina del sistema)
        self._activo = False

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción textual de la entidad."""
        # Método abstracto: cada subclase DEBE implementar su propia versión de describir()
        ...

    @abstractmethod
    def validar(self) -> bool:
        """Valida que los datos de la entidad sean correctos."""
        # Método abstracto: cada subclase DEBE definir sus propias reglas de validación
        ...

    def __str__(self) -> str:
        # Cuando se imprime el objeto con print(), llama automáticamente a describir()
        return self.describir()

    def __repr__(self) -> str:
        # Representación técnica del objeto, útil para depuración en consola o logs
        return f"{self.__class__.__name__}(id='{self._id}', nombre='{self._nombre}')"


# ══════════════════════════════════════════════════════
# CLASE CLIENTE
# ══════════════════════════════════════════════════════
class Cliente(EntidadBase):
    """
    Representa un cliente de Software FJ.
    Aplica encapsulación estricta y validación de datos personales.
    """

    def __init__(
        self,
        identificacion: str,    # Cédula, NIT u otro documento único del cliente
        nombre: str,            # Nombre completo o razón social
        correo: str,            # Correo electrónico de contacto
        telefono: str,          # Número telefónico con o sin indicativo internacional
        tipo: str = "natural",  # Tipo de cliente: persona "natural" o "empresa"
    ):
        # Se validan todos los campos ANTES de inicializar el objeto padre
        # para evitar crear un objeto en estado inválido
        self._validar_identificacion(identificacion)
        self._validar_nombre(nombre)
        self._validar_correo(correo)
        self._validar_telefono(telefono)
        self._validar_tipo(tipo)

        # Una vez validados los datos, se inicializa la clase padre con ID y nombre
        super().__init__(identificacion, nombre)
        # Doble guion bajo aplica name-mangling: almacenado como _Cliente__correo,
        # impidiendo acceso directo desde fuera de la clase
        self.__correo = correo
        # Mismo mecanismo de privacidad estricta para el teléfono
        self.__telefono = telefono
        # Tipo de cliente: protegido (accesible en subclases)
        self._tipo = tipo
        # Lista interna que almacena los IDs de las reservas asociadas a este cliente
        self._reservas: list = []

    # ── Propiedades de acceso ──────────────────────────
    @property
    def correo(self) -> str:
        # Permite leer el correo desde fuera de la clase de forma controlada
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        # Valida el nuevo correo antes de permitir su modificación
        self._validar_correo(valor)
        # Solo asigna el nuevo valor si pasó la validación
        self.__correo = valor

    @property
    def telefono(self) -> str:
        # Permite leer el teléfono desde fuera de la clase de forma controlada
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Valida el nuevo teléfono antes de permitir su modificación
        self._validar_telefono(valor)
        # Solo asigna si el valor es válido
        self.__telefono = valor

    @property
    def tipo(self) -> str:
        # Expone el tipo de cliente como solo lectura (no debe cambiar tras el registro)
        return self._tipo

    @property
    def num_reservas(self) -> int:
        # Calcula en tiempo real cuántas reservas tiene el cliente contando la lista interna
        return len(self._reservas)

    # ── Métodos de validación internos ────────────────
    @staticmethod
    def _validar_identificacion(valor: str):
        # Verifica que el valor exista, sea texto y no esté vacío
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise DatosClienteInvalidosError("identificacion", valor)
        # Aplica expresión regular: solo letras, números y guiones, entre 3 y 20 caracteres
        if not re.match(r"^[A-Za-z0-9\-]{3,20}$", valor.strip()):
            raise DatosClienteInvalidosError(
                "identificacion",
                f"'{valor}' — debe tener 3-20 caracteres alfanuméricos o guiones"
            )

    @staticmethod
    def _validar_nombre(valor: str):
        # El nombre debe ser texto no vacío con al menos 2 caracteres significativos
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosClienteInvalidosError("nombre", valor)

    @staticmethod
    def _validar_correo(valor: str):
        # Patrón de expresión regular para validar formato básico de correo electrónico
        patron = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
        # Si el valor está vacío o no coincide con el patrón, se lanza la excepción
        if not valor or not re.match(patron, valor.strip()):
            raise DatosClienteInvalidosError("correo", valor)

    @staticmethod
    def _validar_telefono(valor: str):
        # Acepta números con o sin "+" al inicio, entre 7 y 15 dígitos (estándar E.164)
        if not valor or not re.match(r"^\+?[0-9]{7,15}$", valor.strip()):
            raise DatosClienteInvalidosError("telefono", valor)

    @staticmethod
    def _validar_tipo(valor: str):
        # Solo se aceptan exactamente los dos tipos definidos en el sistema
        if valor not in ("natural", "empresa"):
            raise DatosClienteInvalidosError("tipo", valor)

    # ── Métodos abstractos implementados ──────────────
    def describir(self) -> str:
        # Determina el texto del estado según el atributo heredado de EntidadBase
        estado = "Activo" if self._activo else "Inactivo"
        # Construye y retorna una cadena con todos los datos visibles del cliente
        return (
            f"Cliente [{self._tipo.upper()}] | ID: {self._id} | "
            f"Nombre: {self._nombre} | Correo: {self.__correo} | "
            f"Tel: {self.__telefono} | Reservas: {self.num_reservas} | {estado}"
        )

    def validar(self) -> bool:
        try:
            # Vuelve a ejecutar todas las validaciones sobre los datos actuales del objeto
            self._validar_identificacion(self._id)
            self._validar_nombre(self._nombre)
            self._validar_correo(self.__correo)
            self._validar_telefono(self.__telefono)
            # Si ninguna validación lanza excepción, el objeto es consistente
            return True
        except DatosClienteInvalidosError:
            # Si alguna validación falla, retorna False sin propagar la excepción
            return False

    # ── Gestión de reservas del cliente ───────────────
    def agregar_reserva(self, id_reserva: str):
        # Solo agrega el ID si no está ya en la lista (evita duplicados)
        if id_reserva not in self._reservas:
            self._reservas.append(id_reserva)

    def eliminar_reserva(self, id_reserva: str):
        # Solo elimina si el ID existe en la lista (evita errores por elemento inexistente)
        if id_reserva in self._reservas:
            self._reservas.remove(id_reserva)

    def obtener_reservas(self) -> list:
        # Retorna una COPIA de la lista para proteger la lista interna de modificaciones externas
        return list(self._reservas)


# ══════════════════════════════════════════════════════
# REPOSITORIO DE CLIENTES
# ══════════════════════════════════════════════════════
class RepositorioClientes:
    """
    Gestiona el almacenamiento en memoria de todos los clientes.
    Aplica el patrón Repository para desacoplar la lógica de acceso.
    """

    def __init__(self):
        # Diccionario que actúa como base de datos en memoria: clave=ID, valor=objeto Cliente
        self._clientes: dict = {}

    def registrar(self, cliente: Cliente) -> Cliente:
        try:
            # Verifica si ya existe un cliente con el mismo ID antes de registrar
            if cliente.id in self._clientes:
                raise ClienteYaExisteError(cliente.id)
            # Segunda verificación: confirma que el objeto mismo sea internamente válido
            if not cliente.validar():
                raise DatosClienteInvalidosError("general", "datos inconsistentes")
            # Si pasó todas las validaciones, almacena el cliente en el diccionario
            self._clientes[cliente.id] = cliente
            # Registra el evento exitoso en el archivo de logs
            log_evento(f"Cliente registrado: {cliente.id} - {cliente.nombre}")
            # Retorna el cliente recién registrado para uso del llamador
            return cliente
        except ClienteYaExisteError:
            # Registra el intento de duplicado en logs y relanza la excepción hacia arriba
            log_error(f"Intento de registro duplicado: {cliente.id}")
            raise
        except DatosClienteInvalidosError as e:
            # Registra el error de datos en logs y relanza para que el llamador lo maneje
            log_error(f"Datos inválidos al registrar cliente: {e}")
            raise

    def buscar(self, identificacion: str) -> Cliente:
        # Busca el cliente en el diccionario por su ID
        cliente = self._clientes.get(identificacion)
        # Si no existe (get retorna None), lanza excepción específica
        if not cliente:
            raise ClienteNoEncontradoError(identificacion)
        # Si existe, retorna el objeto Cliente encontrado
        return cliente

    def listar_todos(self) -> list:
        # Retorna una lista con todos los objetos Cliente registrados en el sistema
        return list(self._clientes.values())

    def total(self) -> int:
        # Retorna el número total de clientes almacenados contando las claves del diccionario
        return len(self._clientes)


# =======================================================================
# SECCIÓN 4: SERVICIOS
# =======================================================================

# ══════════════════════════════════════════════════════
# CLASE ABSTRACTA SERVICIO
# ══════════════════════════════════════════════════════
class Servicio(EntidadBase):
    """
    Clase abstracta base para todos los servicios de Software FJ.
    Define la interfaz común que deben implementar los servicios especializados.
    """

    # Porcentaje de IVA aplicado en Colombia
    IMPUESTO_BASE = 0.19

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        # Verifica que la tarifa sea un valor positivo antes de crear el objeto
        if tarifa_hora <= 0:
            raise ParametroServicioInvalidoError("tarifa_hora", "debe ser mayor a 0")
        # Inicializa la clase padre con el ID y nombre del servicio
        super().__init__(id_servicio, nombre)
        # Almacena la tarifa por hora como atributo protegido
        self._tarifa_hora = tarifa_hora
        # Indica si el servicio está habilitado para ser reservado
        self._disponible = disponible

    @property
    def tarifa_hora(self) -> float:
        # Expone la tarifa por hora como solo lectura
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        # Expone el estado de disponibilidad del servicio como solo lectura
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool):
        # Actualiza la disponibilidad y registra el cambio en los logs
        self._disponible = estado
        log_info(f"Servicio '{self._nombre}' disponibilidad → {estado}")

    @abstractmethod
    def calcular_costo(self, horas: float, **kwargs) -> float:
        # Método abstracto: cada servicio define su propia lógica de cálculo de costo base
        ...

    @abstractmethod
    def validar_parametros(self, horas: float, **kwargs) -> bool:
        # Método abstracto: cada servicio define qué parámetros son válidos para él
        ...

    @abstractmethod
    def descripcion_detallada(self) -> str:
        # Método abstracto: cada servicio genera su propia descripción extendida
        ...

    def describir(self) -> str:
        # Construye la descripción básica del servicio con su estado de disponibilidad
        estado = "✅ Disponible" if self._disponible else "❌ No disponible"
        return (
            f"[{self.__class__.__name__}] {self._nombre} | "
            f"ID: {self._id} | Tarifa: ${self._tarifa_hora:,.0f}/h | {estado}"
        )

    def validar(self) -> bool:
        # Un servicio es válido si tiene tarifa positiva y nombre no vacío
        return self._tarifa_hora > 0 and bool(self._nombre)

    def calcular_costo_con_impuesto(self, horas: float, incluir_iva: bool = True,
                                     descuento: float = 0.0, **kwargs) -> dict:
        """Versión sobrecargada: calcula costo con IVA y descuento opcionales."""
        try:
            # Verifica que el servicio esté disponible antes de calcular
            if not self._disponible:
                raise ServicioNoDisponibleError(self._nombre)
            # Valida los parámetros específicos del servicio (horas, capacidad, etc.)
            self.validar_parametros(horas, **kwargs)
            # Verifica que el descuento esté en un rango porcentual válido (0% a 99%)
            if not (0.0 <= descuento < 1.0):
                raise ParametroServicioInvalidoError(
                    "descuento", f"debe estar entre 0.0 y 0.99, recibido {descuento}"
                )
            # Calcula el costo base usando la implementación del servicio específico
            base = self.calcular_costo(horas, **kwargs)
            # Verifica que el costo base no sea negativo (indicaría un error de lógica)
            if base < 0:
                raise CostoInconsistenteError(f"el costo base es negativo: {base}")
            # Aplica el porcentaje de descuento sobre el costo base
            valor_descuento = base * descuento
            # Subtotal es el costo base menos el descuento aplicado
            subtotal = base - valor_descuento
            # Calcula el IVA solo si se solicitó incluirlo
            iva = subtotal * self.IMPUESTO_BASE if incluir_iva else 0.0
            # El total es la suma del subtotal más el IVA
            total = subtotal + iva
            # Retorna un diccionario con el desglose completo de la factura
            return {
                "base": round(base, 2),
                "descuento_aplicado": round(valor_descuento, 2),
                "subtotal": round(subtotal, 2),
                "iva": round(iva, 2),
                "total": round(total, 2),
                "incluye_iva": incluir_iva,
                "horas": horas,
            }
        except (ServicioNoDisponibleError, ParametroServicioInvalidoError,
                CostoInconsistenteError):
            # Relanza excepciones conocidas sin modificarlas
            raise
        except Exception as e:
            # Cualquier error inesperado se convierte en CostoInconsistenteError
            raise CostoInconsistenteError(str(e)) from e

    def calcular_costo_simple(self, horas: float) -> float:
        """Sobrecarga simplificada: retorna solo el costo base sin IVA ni descuentos."""
        # Valida parámetros antes de calcular
        self.validar_parametros(horas)
        # Retorna directamente el costo base sin ningún extra
        return self.calcular_costo(horas)

    def calcular_costo_corporativo(self, horas: float, num_personas: int,
                                    descuento_vol: float = 0.10) -> dict:
        """Sobrecarga corporativa: aplica descuento automático según número de personas."""
        # Verifica que el número de personas sea al menos 1
        if num_personas < 1:
            raise ParametroServicioInvalidoError("num_personas", "debe ser ≥ 1")
        # Calcula el descuento total según grupos de 5 personas, con tope del 40%
        descuento_total = min(descuento_vol * (num_personas // 5), 0.40)
        # Reutiliza el método con impuesto aplicando el descuento corporativo calculado
        return self.calcular_costo_con_impuesto(horas, descuento=descuento_total)


# ══════════════════════════════════════════════════════
# SERVICIO 1: RESERVA DE SALA
# ══════════════════════════════════════════════════════
class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    # Duración mínima y máxima permitida para reservar una sala (en horas)
    DURACION_MIN = 1.0
    DURACION_MAX = 8.0

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float,
                 capacidad_max: int, tiene_proyector: bool = False,
                 tiene_videoconferencia: bool = False):
        # Verifica que la capacidad sea al menos de 1 persona
        if capacidad_max < 1:
            raise ParametroServicioInvalidoError("capacidad_max", "debe ser ≥ 1")
        # Inicializa la clase padre Servicio con los datos básicos
        super().__init__(id_servicio, nombre, tarifa_hora)
        # Número máximo de personas que pueden ocupar la sala
        self._capacidad_max = capacidad_max
        # Indica si la sala cuenta con proyector disponible
        self._tiene_proyector = tiene_proyector
        # Indica si la sala cuenta con sistema de videoconferencia
        self._tiene_videoconferencia = tiene_videoconferencia

    @property
    def capacidad_max(self) -> int:
        # Expone la capacidad máxima como solo lectura
        return self._capacidad_max

    def calcular_costo(self, horas: float, num_asistentes: int = 1, **kwargs) -> float:
        # Costo base: tarifa por hora multiplicada por las horas reservadas
        base = self._tarifa_hora * horas
        # Si más del 50% de la capacidad está ocupada, se aplica un recargo del 10%
        if num_asistentes > self._capacidad_max * 0.5:
            base *= 1.10
        # Retorna el costo final con o sin recargo según la ocupación
        return base

    def validar_parametros(self, horas: float, num_asistentes: int = 1, **kwargs) -> bool:
        # Verifica que las horas estén dentro del rango permitido para salas
        if not (self.DURACION_MIN <= horas <= self.DURACION_MAX):
            raise ParametroServicioInvalidoError(
                "horas",
                f"para sala debe estar entre {self.DURACION_MIN}h y {self.DURACION_MAX}h"
            )
        # Verifica que el número de asistentes sea al menos 1
        if num_asistentes < 1:
            raise ParametroServicioInvalidoError("num_asistentes", "debe ser ≥ 1")
        # Verifica que los asistentes no superen la capacidad máxima de la sala
        if num_asistentes > self._capacidad_max:
            raise ParametroServicioInvalidoError(
                "num_asistentes",
                f"excede la capacidad máxima de {self._capacidad_max} personas"
            )
        # Si todas las validaciones pasaron, retorna True
        return True

    def descripcion_detallada(self) -> str:
        # Construye la lista de equipamiento disponible en la sala
        extras = []
        if self._tiene_proyector:
            extras.append("Proyector")
        if self._tiene_videoconferencia:
            extras.append("Videoconferencia")
        # Si no hay extras, muestra un mensaje indicándolo
        extras_str = ", ".join(extras) if extras else "Sin extras"
        # Retorna la descripción completa con todos los atributos de la sala
        return (
            f"SALA DE REUNIONES: {self._nombre}\n"
            f"  Capacidad máx.: {self._capacidad_max} personas\n"
            f"  Equipamiento:   {extras_str}\n"
            f"  Tarifa:         ${self._tarifa_hora:,.0f}/hora\n"
            f"  Duración:       {self.DURACION_MIN}h – {self.DURACION_MAX}h"
        )


# ══════════════════════════════════════════════════════
# SERVICIO 2: ALQUILER DE EQUIPO
# ══════════════════════════════════════════════════════
class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    # Duración mínima y máxima permitida para alquilar un equipo (en horas)
    DURACION_MIN = 2.0
    DURACION_MAX = 72.0
    # A partir de estas horas se aplica el recargo por uso extendido
    HORAS_RECARGO = 8.0
    # Porcentaje de recargo sobre las horas adicionales al límite base
    PORCENTAJE_RECARGO = 0.15
    # Monto fijo del depósito de garantía en pesos colombianos
    DEPOSITO_BASE = 50_000

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float,
                 tipo_equipo: str, requiere_deposito: bool = True):
        # Lista de tipos de equipo aceptados por el sistema
        tipos_validos = ("laptop", "camara", "drone", "proyector", "servidor", "otro")
        # Verifica que el tipo de equipo sea uno de los permitidos
        if tipo_equipo not in tipos_validos:
            raise ParametroServicioInvalidoError(
                "tipo_equipo", f"debe ser uno de: {tipos_validos}"
            )
        # Inicializa la clase padre Servicio con los datos básicos
        super().__init__(id_servicio, nombre, tarifa_hora)
        # Categoría del equipo (laptop, cámara, drone, etc.)
        self._tipo_equipo = tipo_equipo
        # Indica si el alquiler exige un depósito de garantía al cliente
        self._requiere_deposito = requiere_deposito

    @property
    def tipo_equipo(self) -> str:
        # Expone el tipo de equipo como solo lectura
        return self._tipo_equipo

    def calcular_costo(self, horas: float, **kwargs) -> float:
        # Si las horas están dentro del límite base, el costo es directo
        if horas <= self.HORAS_RECARGO:
            return self._tarifa_hora * horas
        # Para las primeras HORAS_RECARGO horas se aplica tarifa normal
        costo_normal = self._tarifa_hora * self.HORAS_RECARGO
        # Las horas adicionales tienen un recargo porcentual sobre la tarifa
        horas_extra = horas - self.HORAS_RECARGO
        costo_extra = self._tarifa_hora * horas_extra * (1 + self.PORCENTAJE_RECARGO)
        # El costo total es la suma del bloque normal más el bloque con recargo
        return costo_normal + costo_extra

    def calcular_deposito(self) -> float:
        # Retorna el monto del depósito si aplica, o cero si no se requiere
        return self.DEPOSITO_BASE if self._requiere_deposito else 0.0

    def validar_parametros(self, horas: float, **kwargs) -> bool:
        # Verifica que las horas estén dentro del rango permitido para equipos
        if not (self.DURACION_MIN <= horas <= self.DURACION_MAX):
            raise ParametroServicioInvalidoError(
                "horas",
                f"para equipo debe estar entre {self.DURACION_MIN}h y {self.DURACION_MAX}h"
            )
        # Si la validación pasó, retorna True
        return True

    def descripcion_detallada(self) -> str:
        # Formatea el depósito o indica que no es requerido
        deposito_info = f"${self.DEPOSITO_BASE:,.0f}" if self._requiere_deposito else "No requerido"
        # Retorna la descripción completa con todos los atributos del equipo
        return (
            f"ALQUILER DE EQUIPO: {self._nombre}\n"
            f"  Tipo:           {self._tipo_equipo.upper()}\n"
            f"  Tarifa base:    ${self._tarifa_hora:,.0f}/hora\n"
            f"  Recargo +{self.HORAS_RECARGO}h: {int(self.PORCENTAJE_RECARGO*100)}%\n"
            f"  Depósito:       {deposito_info}\n"
            f"  Duración:       {self.DURACION_MIN}h – {self.DURACION_MAX}h"
        )


# ══════════════════════════════════════════════════════
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# ══════════════════════════════════════════════════════
class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría y consultoría profesional."""

    # Duración mínima y máxima para una sesión de asesoría (en horas)
    DURACION_MIN = 0.5
    DURACION_MAX = 4.0

    # Multiplicadores de costo según el nivel de experiencia del asesor
    MULTIPLICADORES_NIVEL = {
        "junior": 1.0,   # Tarifa base sin ajuste
        "senior": 1.5,   # 50% más que la tarifa base
        "experto": 2.0,  # El doble de la tarifa base
    }

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float,
                 area: str, nivel_asesor: str = "senior"):
        # Verifica que el nivel del asesor sea uno de los tres definidos
        if nivel_asesor not in self.MULTIPLICADORES_NIVEL:
            raise ParametroServicioInvalidoError(
                "nivel_asesor",
                f"debe ser uno de: {list(self.MULTIPLICADORES_NIVEL.keys())}"
            )
        # Inicializa la clase padre Servicio con los datos básicos
        super().__init__(id_servicio, nombre, tarifa_hora)
        # Área temática de la asesoría (Tecnología, Legal, Financiero, etc.)
        self._area = area
        # Nivel de experiencia del asesor asignado
        self._nivel_asesor = nivel_asesor

    @property
    def area(self) -> str:
        # Expone el área temática como solo lectura
        return self._area

    @property
    def nivel_asesor(self) -> str:
        # Expone el nivel del asesor como solo lectura
        return self._nivel_asesor

    def calcular_costo(self, horas: float, **kwargs) -> float:
        # Obtiene el multiplicador correspondiente al nivel del asesor
        multiplicador = self.MULTIPLICADORES_NIVEL[self._nivel_asesor]
        # El costo es tarifa base × horas × multiplicador del nivel
        return self._tarifa_hora * horas * multiplicador

    def validar_parametros(self, horas: float, **kwargs) -> bool:
        # Verifica que las horas estén dentro del rango permitido para asesorías
        if not (self.DURACION_MIN <= horas <= self.DURACION_MAX):
            raise ParametroServicioInvalidoError(
                "horas",
                f"para asesoría debe estar entre {self.DURACION_MIN}h y {self.DURACION_MAX}h"
            )
        # Si la validación pasó, retorna True
        return True

    def descripcion_detallada(self) -> str:
        # Obtiene el multiplicador para mostrar la tarifa real al cliente
        mult = self.MULTIPLICADORES_NIVEL[self._nivel_asesor]
        # Calcula la tarifa efectiva que pagará el cliente por hora
        tarifa_real = self._tarifa_hora * mult
        # Retorna la descripción completa con nivel, área y tarifa efectiva
        return (
            f"ASESORÍA ESPECIALIZADA: {self._nombre}\n"
            f"  Área:           {self._area}\n"
            f"  Nivel asesor:   {self._nivel_asesor.upper()} (×{mult})\n"
            f"  Tarifa efectiva:${tarifa_real:,.0f}/hora\n"
            f"  Duración:       {self.DURACION_MIN}h – {self.DURACION_MAX}h"
        )


# ══════════════════════════════════════════════════════
# REPOSITORIO DE SERVICIOS
# ══════════════════════════════════════════════════════
class RepositorioServicios:
    """Gestiona el catálogo de servicios disponibles en memoria."""

    def __init__(self):
        # Diccionario en memoria: clave=ID del servicio, valor=objeto Servicio
        self._servicios: dict = {}

    def agregar(self, servicio: Servicio) -> Servicio:
        try:
            # Verifica que el servicio tenga datos internamente válidos
            if not servicio.validar():
                raise ParametroServicioInvalidoError("servicio", "datos inválidos")
            # Almacena el servicio en el diccionario usando su ID como clave
            self._servicios[servicio.id] = servicio
            # Registra el evento en los logs
            log_evento(f"Servicio agregado: {servicio.id} - {servicio.nombre}")
            # Retorna el servicio recién agregado
            return servicio
        except ParametroServicioInvalidoError:
            # Registra el error en logs y relanza la excepción
            log_error(f"Error al agregar servicio {servicio.id}")
            raise

    def buscar(self, id_servicio: str) -> Servicio:
        # Busca el servicio en el diccionario por su ID
        svc = self._servicios.get(id_servicio)
        # Si no existe, lanza excepción específica de servicio no encontrado
        if not svc:
            raise ServicioNoEncontradoError(id_servicio)
        # Si existe, retorna el objeto Servicio encontrado
        return svc

    def listar_disponibles(self) -> list:
        # Filtra y retorna solo los servicios cuya disponibilidad es True
        return [s for s in self._servicios.values() if s.disponible]

    def listar_todos(self) -> list:
        # Retorna todos los servicios sin importar su disponibilidad
        return list(self._servicios.values())

    def total(self) -> int:
        # Retorna el número total de servicios registrados en el catálogo
        return len(self._servicios)


# =======================================================================
# SECCIÓN 5: RESERVAS
# =======================================================================

# Módulo para generar identificadores únicos para cada reserva
import uuid

# ══════════════════════════════════════════════════════
# CLASE RESERVA
# ══════════════════════════════════════════════════════
class Reserva:
    """
    Representa una reserva que integra un Cliente, un Servicio,
    una duración y un estado. Implementa el ciclo de vida completo.

    Estados válidos:  PENDIENTE → CONFIRMADA → PROCESADA
                      PENDIENTE → CANCELADA
                      CONFIRMADA → CANCELADA
    """

    # Conjunto de estados válidos que puede tener una reserva
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    # Diccionario que define qué transiciones de estado están permitidas
    TRANSICIONES = {
        "PENDIENTE":  {"CONFIRMADA", "CANCELADA"},  # Desde pendiente se puede confirmar o cancelar
        "CONFIRMADA": {"PROCESADA", "CANCELADA"},   # Desde confirmada se puede procesar o cancelar
        "PROCESADA":  set(),                         # Una reserva procesada no puede cambiar
        "CANCELADA":  set(),                         # Una reserva cancelada no puede cambiar
    }

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: float,
                 notas: str = "", **parametros_servicio):
        # Verifica que el servicio esté disponible antes de crear la reserva
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre)
        # Valida los parámetros específicos del servicio (horas, capacidad, etc.)
        try:
            servicio.validar_parametros(horas, **parametros_servicio)
        except ParametroServicioInvalidoError as e:
            # Convierte el error de parámetro en error de duración encadenando la causa
            raise DuracionInvalidaError(horas, 0, 99) from e

        # Genera un ID único de 8 caracteres en mayúsculas para identificar la reserva
        self._id = str(uuid.uuid4())[:8].upper()
        # Guarda la referencia al objeto Cliente asociado a esta reserva
        self._cliente = cliente
        # Guarda la referencia al objeto Servicio reservado
        self._servicio = servicio
        # Duración de la reserva en horas
        self._horas = horas
        # Parámetros adicionales específicos del servicio (num_asistentes, etc.)
        self._parametros = parametros_servicio
        # Notas o comentarios opcionales sobre la reserva
        self._notas = notas
        # Toda reserva inicia en estado PENDIENTE
        self._estado = "PENDIENTE"
        # Marca temporal de creación de la reserva
        self._fecha_creacion = datetime.now()
        # Marca temporal de la última actualización del estado
        self._fecha_actualizacion = datetime.now()
        # Diccionario donde se guardará el desglose del costo al confirmar
        self._costo_calculado: dict = {}
        # Lista que registra el historial de cambios de estado de la reserva
        self._historial: list = [
            f"{self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')} — Reserva creada (PENDIENTE)"
        ]

        # Vincula esta reserva al cliente para mantener el conteo actualizado
        cliente.agregar_reserva(self._id)
        # Registra la creación de la reserva en los logs del sistema
        log_evento(
            f"Reserva {self._id} creada | Cliente: {cliente.id} | "
            f"Servicio: {servicio.id} | Horas: {horas}"
        )

    # ── Propiedades ───────────────────────────────────
    @property
    def id(self) -> str:
        # Expone el ID único de la reserva como solo lectura
        return self._id

    @property
    def cliente(self) -> Cliente:
        # Expone el objeto Cliente asociado como solo lectura
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        # Expone el objeto Servicio reservado como solo lectura
        return self._servicio

    @property
    def horas(self) -> float:
        # Expone la duración de la reserva en horas como solo lectura
        return self._horas

    @property
    def estado(self) -> str:
        # Expone el estado actual de la reserva como solo lectura
        return self._estado

    @property
    def costo(self) -> dict:
        # Expone el desglose de costo calculado como solo lectura
        return self._costo_calculado

    @property
    def fecha_creacion(self) -> datetime:
        # Expone la fecha y hora de creación como solo lectura
        return self._fecha_creacion

    # ── Transiciones de estado ────────────────────────
    def _cambiar_estado(self, nuevo_estado: str, motivo: str = ""):
        # Verifica que la transición solicitada esté permitida desde el estado actual
        if nuevo_estado not in self.TRANSICIONES[self._estado]:
            raise ReservaOperacionInvalidaError(nuevo_estado, self._estado)
        # Guarda el estado anterior para el historial
        estado_anterior = self._estado
        # Aplica la transición al nuevo estado
        self._estado = nuevo_estado
        # Actualiza la marca temporal de la última modificación
        self._fecha_actualizacion = datetime.now()
        # Construye la entrada del historial con timestamp, estados y motivo
        entrada = (
            f"{self._fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S')} — "
            f"{estado_anterior} → {nuevo_estado}"
            + (f" ({motivo})" if motivo else "")
        )
        # Agrega la entrada al historial de la reserva
        self._historial.append(entrada)
        # Registra el cambio de estado en los logs del sistema
        log_evento(
            f"Reserva {self._id}: {estado_anterior} → {nuevo_estado}"
            + (f" | {motivo}" if motivo else "")
        )

    def confirmar(self, incluir_iva: bool = True, descuento: float = 0.0) -> dict:
        """Confirma la reserva y calcula el costo definitivo. Usa try/except/else/finally."""
        try:
            # Intenta cambiar el estado a CONFIRMADA (falla si no es una transición válida)
            self._cambiar_estado("CONFIRMADA", "confirmación manual")
            # Calcula el costo con todos los parámetros del servicio
            costo = self._servicio.calcular_costo_con_impuesto(
                self._horas, incluir_iva=incluir_iva,
                descuento=descuento, **self._parametros,
            )
        except ReservaOperacionInvalidaError as e:
            # Si la transición no es válida, registra el error y relanza
            log_error(f"No se pudo confirmar reserva {self._id}: {e}")
            raise
        except Exception as e:
            # Cualquier otro error se convierte en ReservaConflictoError encadenado
            log_error(f"Error inesperado al confirmar reserva {self._id}: {e}")
            raise ReservaConflictoError(str(e)) from e
        else:
            # El bloque else solo se ejecuta si NO hubo ninguna excepción
            self._costo_calculado = costo
            log_info(f"Reserva {self._id} confirmada | Total: ${costo['total']:,.2f}")
            return costo
        finally:
            # El bloque finally siempre se ejecuta, haya o no excepción
            log_info(f"Proceso de confirmación de reserva {self._id} finalizado")

    def procesar(self) -> bool:
        """Marca la reserva como ejecutada (servicio entregado). Usa try/except/finally."""
        try:
            # Verifica que el costo ya fue calculado (requiere haber confirmado antes)
            if not self._costo_calculado:
                raise ReservaConflictoError(
                    "se intentó procesar sin haber calculado el costo (confirmar primero)"
                )
            # Intenta cambiar el estado a PROCESADA
            self._cambiar_estado("PROCESADA", "servicio entregado")
            return True
        except (ReservaOperacionInvalidaError, ReservaConflictoError) as e:
            # Registra el error y relanza la excepción hacia el llamador
            log_error(f"Error al procesar reserva {self._id}: {e}")
            raise
        finally:
            # Siempre registra que se intentó el procesamiento, haya fallado o no
            log_info(f"Intento de procesamiento de reserva {self._id} completado")

    def cancelar(self, motivo: str = "sin motivo especificado") -> bool:
        """Cancela la reserva y la desvincula del cliente. Usa try/except/else."""
        try:
            # Intenta cambiar el estado a CANCELADA con el motivo indicado
            self._cambiar_estado("CANCELADA", motivo)
        except ReservaOperacionInvalidaError as e:
            # Si la transición no es válida, registra el error y relanza
            log_error(f"No se pudo cancelar reserva {self._id}: {e}")
            raise
        else:
            # Solo si la cancelación fue exitosa, desvincula la reserva del cliente
            self._cliente.eliminar_reserva(self._id)
            # Registra el evento de cancelación exitosa en los logs
            log_evento(f"Reserva {self._id} cancelada: {motivo}")
            return True

    def describir(self) -> str:
        # Formatea el costo total o indica que aún no fue calculado
        costo_str = (
            f"${self._costo_calculado.get('total', 0):,.2f}"
            if self._costo_calculado else "Por calcular"
        )
        # Retorna una cadena con los datos principales de la reserva
        return (
            f"RESERVA {self._id}\n"
            f"  Cliente:  {self._cliente.nombre} ({self._cliente.id})\n"
            f"  Servicio: {self._servicio.nombre}\n"
            f"  Horas:    {self._horas}h\n"
            f"  Estado:   {self._estado}\n"
            f"  Costo:    {costo_str}\n"
            f"  Creada:   {self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def historial_estados(self) -> str:
        # Une todas las entradas del historial con viñetas para facilitar la lectura
        return "\n".join(f"  • {h}" for h in self._historial)

    def __str__(self) -> str:
        # Al imprimir la reserva con print() retorna la descripción completa
        return self.describir()


# ══════════════════════════════════════════════════════
# REPOSITORIO DE RESERVAS
# ══════════════════════════════════════════════════════
class RepositorioReservas:
    """Gestiona todas las reservas del sistema en memoria."""

    def __init__(self):
        # Diccionario en memoria: clave=ID de reserva, valor=objeto Reserva
        self._reservas: dict = {}

    def crear(self, cliente: Cliente, servicio: Servicio, horas: float,
              notas: str = "", **params) -> Reserva:
        try:
            # Crea el objeto Reserva con todos los parámetros recibidos
            reserva = Reserva(cliente, servicio, horas, notas, **params)
            # Almacena la reserva en el diccionario usando su ID como clave
            self._reservas[reserva.id] = reserva
            # Retorna la reserva recién creada
            return reserva
        except Exception as e:
            # Registra cualquier error durante la creación y relanza
            log_error(f"Error al crear reserva: {e}", e)
            raise

    def buscar(self, id_reserva: str) -> Reserva:
        # Busca la reserva en el diccionario por su ID
        r = self._reservas.get(id_reserva)
        # Si no existe, lanza excepción específica de reserva no encontrada
        if not r:
            raise ReservaNoEncontradaError(id_reserva)
        # Si existe, retorna el objeto Reserva encontrado
        return r

    def listar_por_cliente(self, id_cliente: str) -> list:
        # Filtra las reservas que pertenecen al cliente con el ID indicado
        return [r for r in self._reservas.values() if r.cliente.id == id_cliente]

    def listar_por_estado(self, estado: str) -> list:
        # Filtra las reservas que se encuentran en el estado indicado
        return [r for r in self._reservas.values() if r.estado == estado]

    def listar_todas(self) -> list:
        # Retorna todas las reservas sin importar su estado
        return list(self._reservas.values())

    def total(self) -> int:
        # Retorna el número total de reservas registradas en el sistema
        return len(self._reservas)


# =======================================================================
# SECCIÓN 6: PROGRAMA PRINCIPAL CON 20 OPERACIONES DE DEMOSTRACIÓN
# =======================================================================

import sys

# ── Utilidades de presentación ────────────────────────────────────────

# Separador mayor para títulos de bloque
SEP_MAYOR = "═" * 65
# Separador menor para subtítulos de operación
SEP_MENOR = "─" * 65

def titulo(texto: str):
    # Imprime un encabezado de bloque con doble línea decorativa
    print(f"\n{SEP_MAYOR}\n  {texto}\n{SEP_MAYOR}")

def subtitulo(texto: str):
    # Imprime un encabezado de operación con línea simple decorativa
    print(f"\n{SEP_MENOR}\n  {texto}\n{SEP_MENOR}")

def ok(texto: str):
    # Imprime un mensaje de operación exitosa con ícono verde
    print(f"  ✅ {texto}")

def fallo(texto: str):
    # Imprime un mensaje de operación fallida con ícono rojo
    print(f"  ❌ {texto}")

def info(texto: str):
    # Imprime un mensaje informativo con ícono azul
    print(f"  ℹ️  {texto}")

def mostrar_costo(desglose: dict):
    # Imprime el desglose completo de una factura línea por línea
    print(f"     Base:      ${desglose['base']:>12,.2f}")
    if desglose['descuento_aplicado']:
        print(f"     Descuento: ${desglose['descuento_aplicado']:>12,.2f}")
    print(f"     Subtotal:  ${desglose['subtotal']:>12,.2f}")
    if desglose['incluye_iva']:
        print(f"     IVA (19%): ${desglose['iva']:>12,.2f}")
    print(f"     TOTAL:     ${desglose['total']:>12,.2f}")


# ── Bloque 1: Clientes ────────────────────────────────────────────────

def bloque_clientes(repo_clientes: RepositorioClientes):
    titulo("BLOQUE 1 — REGISTRO DE CLIENTES")

    # Operación 1: cliente persona natural con datos válidos
    subtitulo("Operación 1 — Cliente válido (persona natural)")
    try:
        # Crea un objeto Cliente con datos correctos
        c1 = Cliente("CC-1001", "Ana Martínez", "ana@correo.com", "3001234567", "natural")
        # Lo registra en el repositorio en memoria
        repo_clientes.registrar(c1)
        ok(f"Cliente registrado: {c1.nombre}")
    except SoftwareFJError as e:
        fallo(f"Error inesperado: {e}")

    # Operación 2: cliente empresa con datos válidos
    subtitulo("Operación 2 — Cliente válido (empresa)")
    try:
        c2 = Cliente("NIT-9002", "TechCorp SAS", "contacto@techcorp.co", "6013456789", "empresa")
        repo_clientes.registrar(c2)
        ok(f"Empresa registrada: {c2.nombre}")
    except SoftwareFJError as e:
        fallo(f"Error: {e}")

    # Operación 3: correo sin arroba (debe fallar y ser capturado)
    subtitulo("Operación 3 — Correo inválido (debe fallar)")
    try:
        c_malo = Cliente("CC-1002", "Pedro Rojas", "correo-sin-arroba", "3009876543")
        repo_clientes.registrar(c_malo)
        fallo("No se detectó el error de correo")
    except SoftwareFJError as e:
        ok(f"Error capturado correctamente → {e}")

    # Operación 4: mismo ID de Ana (debe fallar por duplicado)
    subtitulo("Operación 4 — Registro duplicado (debe fallar)")
    try:
        c_dup = Cliente("CC-1001", "Copia Ana", "copia@correo.com", "3001111111")
        repo_clientes.registrar(c_dup)
        fallo("No se detectó el duplicado")
    except SoftwareFJError as e:
        ok(f"Duplicado rechazado correctamente → {e}")

    # Operación 5: teléfono con letras (debe fallar)
    subtitulo("Operación 5 — Teléfono inválido (debe fallar)")
    try:
        c_tel = Cliente("CC-1003", "Luis García", "luis@ok.com", "abc-no-es-tel")
        repo_clientes.registrar(c_tel)
        fallo("No se detectó el teléfono inválido")
    except SoftwareFJError as e:
        ok(f"Teléfono inválido rechazado → {e}")

    # Cliente adicional válido necesario para las reservas del bloque 3
    try:
        c3 = Cliente("CC-2050", "Carlos Ruiz", "carlos@empresa.org", "3157890123", "natural")
        repo_clientes.registrar(c3)
        ok(f"Cliente adicional registrado: {c3.nombre}")
    except SoftwareFJError as e:
        fallo(str(e))

    info(f"Total clientes registrados: {repo_clientes.total()}")
    return repo_clientes


# ── Bloque 2: Servicios ───────────────────────────────────────────────

def bloque_servicios(repo_servicios: RepositorioServicios):
    titulo("BLOQUE 2 — CREACIÓN DE SERVICIOS")

    # Operación 6: sala de reuniones con todos los atributos válidos
    subtitulo("Operación 6 — Sala de reuniones válida")
    try:
        sala1 = ReservaSala(
            "SALA-A1", "Sala Ejecutiva A",
            tarifa_hora=80_000, capacidad_max=10,
            tiene_proyector=True, tiene_videoconferencia=True,
        )
        repo_servicios.agregar(sala1)
        ok(f"Servicio creado: {sala1.nombre}")
        # Muestra la descripción detallada generada por el método sobrescrito
        print(f"\n{sala1.descripcion_detallada()}\n")
    except SoftwareFJError as e:
        fallo(str(e))

    # Operación 7: equipo tipo laptop con depósito requerido
    subtitulo("Operación 7 — Alquiler de equipo (laptop)")
    try:
        laptop = AlquilerEquipo(
            "EQ-L01", "Laptop HP ProBook",
            tarifa_hora=25_000, tipo_equipo="laptop", requiere_deposito=True,
        )
        repo_servicios.agregar(laptop)
        ok(f"Servicio creado: {laptop.nombre}")
        print(f"\n{laptop.descripcion_detallada()}\n")
    except SoftwareFJError as e:
        fallo(str(e))

    # Operación 8: asesoría de nivel experto en tecnología
    subtitulo("Operación 8 — Asesoría especializada")
    try:
        asesoria = AsesoriaEspecializada(
            "ASE-001", "Consultoría en Ciberseguridad",
            tarifa_hora=150_000, area="Tecnología", nivel_asesor="experto",
        )
        repo_servicios.agregar(asesoria)
        ok(f"Servicio creado: {asesoria.nombre}")
        print(f"\n{asesoria.descripcion_detallada()}\n")
    except SoftwareFJError as e:
        fallo(str(e))

    # Operación 9: tipo de equipo "ovni" no existe en el sistema (debe fallar)
    subtitulo("Operación 9 — Equipo con tipo inválido (debe fallar)")
    try:
        equipo_malo = AlquilerEquipo(
            "EQ-X99", "Máquina misteriosa",
            tarifa_hora=10_000, tipo_equipo="ovni",
        )
        repo_servicios.agregar(equipo_malo)
        fallo("No se detectó el tipo inválido")
    except SoftwareFJError as e:
        ok(f"Tipo de equipo inválido rechazado → {e}")

    # Operación 10: nivel "semidios" no está en los niveles definidos (debe fallar)
    subtitulo("Operación 10 — Asesoría con nivel inválido (debe fallar)")
    try:
        ase_mala = AsesoriaEspecializada(
            "ASE-999", "Gurú misterioso",
            tarifa_hora=200_000, area="Magia", nivel_asesor="semidios",
        )
        repo_servicios.agregar(ase_mala)
        fallo("No se detectó el nivel inválido")
    except SoftwareFJError as e:
        ok(f"Nivel inválido rechazado → {e}")

    info(f"Total servicios registrados: {repo_servicios.total()}")
    return repo_servicios


# ── Bloque 3: Reservas ────────────────────────────────────────────────

def bloque_reservas(repo_clientes, repo_servicios, repo_reservas):
    titulo("BLOQUE 3 — GESTIÓN DE RESERVAS")

    # Recupera los objetos necesarios desde los repositorios
    ana    = repo_clientes.buscar("CC-1001")
    corp   = repo_clientes.buscar("NIT-9002")
    carlos = repo_clientes.buscar("CC-2050")
    sala   = repo_servicios.buscar("SALA-A1")
    laptop = repo_servicios.buscar("EQ-L01")
    ase    = repo_servicios.buscar("ASE-001")

    # Variable para reutilizar la reserva de Ana en operaciones posteriores
    reserva1 = None

    # Operación 11: reserva de sala con 6 asistentes, 3 horas, 5% descuento, con IVA
    subtitulo("Operación 11 — Reserva de sala válida (Ana, 3 horas)")
    try:
        reserva1 = repo_reservas.crear(ana, sala, horas=3.0, num_asistentes=6)
        ok(f"Reserva creada: {reserva1.id}")
        costo = reserva1.confirmar(incluir_iva=True, descuento=0.05)
        ok("Reserva confirmada")
        mostrar_costo(costo)
    except SoftwareFJError as e:
        fallo(f"Error: {e}")

    # Operación 12: reserva de laptop por 10 horas, ciclo completo hasta PROCESADA
    subtitulo("Operación 12 — Reserva de laptop (TechCorp, 10 horas)")
    try:
        reserva2 = repo_reservas.crear(corp, laptop, horas=10.0)
        ok(f"Reserva creada: {reserva2.id}")
        costo = reserva2.confirmar(incluir_iva=True)
        ok("Reserva confirmada")
        mostrar_costo(costo)
        # Procesa la reserva para marcarla como servicio entregado
        reserva2.procesar()
        ok("Reserva procesada (servicio entregado)")
    except SoftwareFJError as e:
        fallo(f"Error: {e}")

    # Operación 13: asesoría usando sobrecarga corporativa con 10 personas
    subtitulo("Operación 13 — Asesoría (Carlos, 2h, tarifa corporativa)")
    try:
        reserva3 = repo_reservas.crear(carlos, ase, horas=2.0)
        ok(f"Reserva creada: {reserva3.id}")
        # Usa el método sobrecargado calcular_costo_corporativo
        costo = reserva3.servicio.calcular_costo_corporativo(2.0, num_personas=10)
        ok("Costo corporativo calculado (sobrecarga de método)")
        mostrar_costo(costo)
        reserva3.confirmar(incluir_iva=True)
        ok("Reserva confirmada")
    except SoftwareFJError as e:
        fallo(f"Error: {e}")

    # Operación 14: 15 horas excede el máximo de 8h para salas (debe fallar)
    subtitulo("Operación 14 — Sala con 15h (excede límite, debe fallar)")
    try:
        r_mala = repo_reservas.crear(ana, sala, horas=15.0, num_asistentes=2)
        fallo("No se detectó la duración inválida")
    except SoftwareFJError as e:
        ok(f"Duración inválida rechazada → {e}")

    # Operación 15: deshabilita la sala temporalmente y verifica el rechazo
    subtitulo("Operación 15 — Servicio deshabilitado (debe fallar)")
    try:
        # Deshabilita el servicio para simular mantenimiento o baja temporal
        sala.cambiar_disponibilidad(False)
        r_no_disp = repo_reservas.crear(ana, sala, horas=2.0, num_asistentes=3)
        fallo("No se detectó el servicio no disponible")
    except SoftwareFJError as e:
        ok(f"Servicio no disponible rechazado → {e}")
    finally:
        # Restaura la disponibilidad sin importar si hubo error o no
        sala.cambiar_disponibilidad(True)

    # Operación 16: cancela la reserva de Ana con motivo explicado
    subtitulo("Operación 16 — Cancelar reserva de Ana")
    try:
        if reserva1:
            reserva1.cancelar("Cliente solicitó reprogramación")
            ok(f"Reserva {reserva1.id} cancelada exitosamente")
            # Muestra el historial completo de transiciones de la reserva
            info(f"Historial:\n{reserva1.historial_estados()}")
    except SoftwareFJError as e:
        fallo(f"Error al cancelar: {e}")

    # Operación 17: intenta confirmar una reserva ya cancelada (debe fallar)
    subtitulo("Operación 17 — Confirmar reserva cancelada (debe fallar)")
    try:
        if reserva1:
            # CANCELADA → CONFIRMADA no está permitido por la máquina de estados
            reserva1.confirmar()
            fallo("No se detectó la operación inválida")
    except SoftwareFJError as e:
        ok(f"Operación inválida rechazada → {e}")

    # Operación 18: 50 asistentes exceden la capacidad máxima de 10 (encadenamiento)
    subtitulo("Operación 18 — Exceso de asistentes en sala (encadenamiento)")
    try:
        r_cap = repo_reservas.crear(corp, sala, horas=2.0, num_asistentes=50)
        fallo("No se detectó el exceso de capacidad")
    except SoftwareFJError as e:
        ok(f"Exceso de capacidad rechazado → {e}")
        # Muestra la causa original encadenada con from
        if e.__cause__:
            ok(f"  Causa original (encadenada): {e.__cause__}")

    # Operación 19: cálculo simple de costo sin IVA usando la sobrecarga básica
    subtitulo("Operación 19 — Cálculo simple de asesoría (sin IVA)")
    try:
        # Usa el método sobrecargado calcular_costo_simple
        costo_simple = ase.calcular_costo_simple(1.5)
        ok(f"Costo simple de asesoría por 1.5h: ${costo_simple:,.2f}")
    except SoftwareFJError as e:
        fallo(str(e))

    # Operación 20: descuento de 150% es inválido, el sistema debe rechazarlo
    subtitulo("Operación 20 — Descuento inválido > 100% (debe fallar)")
    try:
        r_desc = repo_reservas.crear(carlos, ase, horas=1.0)
        # Un descuento de 1.5 equivale al 150%, lo que no tiene sentido de negocio
        r_desc.confirmar(incluir_iva=True, descuento=1.5)
        fallo("No se detectó el descuento inválido")
    except SoftwareFJError as e:
        ok(f"Descuento inválido rechazado → {e}")

    info(f"Total reservas creadas en el sistema: {repo_reservas.total()}")


# ── Bloque 4: Resumen final ───────────────────────────────────────────

def bloque_resumen(repo_clientes, repo_servicios, repo_reservas):
    titulo("BLOQUE 4 — RESUMEN FINAL DEL SISTEMA")

    # Lista todos los clientes con su descripción completa
    subtitulo("Clientes registrados")
    for c in repo_clientes.listar_todos():
        print(f"  • {c.describir()}")

    # Lista todos los servicios con su estado de disponibilidad
    subtitulo("Servicios disponibles")
    for s in repo_servicios.listar_todos():
        print(f"  • {s.describir()}")

    # Muestra cada reserva con su descripción y su historial de estados
    subtitulo("Todas las reservas")
    for r in repo_reservas.listar_todas():
        print(f"\n{r.describir()}")
        print(f"  Historial:\n{r.historial_estados()}")

    # Cuenta cuántas reservas hay en cada estado
    subtitulo("Estadísticas")
    estados = {}
    for r in repo_reservas.listar_todas():
        # Incrementa el contador del estado correspondiente
        estados[r.estado] = estados.get(r.estado, 0) + 1
    for estado, cnt in estados.items():
        print(f"  {estado}: {cnt} reserva(s)")

    # Muestra los totales generales del sistema
    print(f"\n  Clientes:  {repo_clientes.total()}")
    print(f"  Servicios: {repo_servicios.total()}")
    print(f"  Reservas:  {repo_reservas.total()}")


# ── Punto de entrada principal ────────────────────────────────────────

def main():
    # Imprime el encabezado visual del sistema al iniciar
    print("\n" + "█" * 65)
    print("█" + " " * 15 + "SOFTWARE FJ — SISTEMA INTEGRAL" + " " * 18 + "█")
    print("█" + " " * 10 + "Gestión de Clientes, Servicios y Reservas" + " " * 11 + "█")
    print("█" * 65)

    try:
        # Registra el inicio del sistema en los logs
        log_evento("=== INICIO DEL SISTEMA SOFTWARE FJ ===")

        # Crea los tres repositorios centrales en memoria
        repo_clientes  = RepositorioClientes()
        repo_servicios = RepositorioServicios()
        repo_reservas  = RepositorioReservas()

        # Ejecuta los cuatro bloques de demostración en orden
        bloque_clientes(repo_clientes)
        bloque_servicios(repo_servicios)
        bloque_reservas(repo_clientes, repo_servicios, repo_reservas)
        bloque_resumen(repo_clientes, repo_servicios, repo_reservas)

        # Mensaje de cierre exitoso del sistema
        titulo("SISTEMA FINALIZADO CORRECTAMENTE")
        print("  Todos los errores fueron capturados y el sistema")
        print("  se mantuvo estable en todo momento.\n")
        print(f"  📄 Logs guardados en: logs/software_fj.log\n")
        log_evento("=== SISTEMA FINALIZADO SIN INTERRUPCIONES ===")

    except Exception as e:
        # Captura de último recurso: errores no controlados que no debería haber
        log_error(f"ERROR CATASTRÓFICO NO CONTROLADO: {e}", e)
        print(f"\n  🔴 Error crítico no controlado: {e}")
        # Termina el proceso con código de error 1 para indicar fallo al sistema operativo
        sys.exit(1)


# Punto de entrada: solo ejecuta main() si el archivo se corre directamente
# (no cuando se importa como módulo desde otro archivo)
if __name__ == "__main__":
    main()