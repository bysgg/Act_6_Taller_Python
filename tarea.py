from abc import ABC, abstractmethod
from typing import Dict, Any


# ─────────────────────────────────────────────
#  CLASE BASE ABSTRACTA
# ─────────────────────────────────────────────
class Tarea(ABC):
    """Clase base abstracta que representa una tarea genérica."""

    def __init__(
        self,
        id: int,
        titulo: str,
        descripcion: str,
        prioridad: str,
        categoria: str,
        fecha_limite: str,
        completada: bool = False,
    ):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.categoria = categoria
        self.fecha_limite = fecha_limite
        self.completada = completada

    # ── Método concreto reutilizable en todas las subclases ──
    def marcar_completada(self) -> None:
        """Marca la tarea como completada (reutilización de código)."""
        self.completada = True

    def to_dict(self) -> Dict[str, Any]:
        """Serializa la tarea a un diccionario (reutilización de código)."""
        return {
            "tipo": self.__class__.__name__,
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "categoria": self.categoria,
            "fecha_limite": self.fecha_limite,
            "completada": self.completada,
        }

    # ── Método abstracto: cada subclase lo implementa diferente (polimorfismo) ──
    @abstractmethod
    def mostrar_detalle(self) -> str:
        """Retorna un resumen con detalle propio de cada tipo de tarea."""
        pass

    def __repr__(self) -> str:
        estado = "✔" if self.completada else "⏳"
        return f"[{self.id}] {estado} {self.titulo} ({self.prioridad}) — {self.categoria}"

# ─────────────────────────────────────────────
#  SUBCLASE 1: Tarea Simple
# ─────────────────────────────────────────────
class TareaSimple(Tarea):
    """Tarea básica sin atributos extra. Hereda todo de Tarea."""

    def mostrar_detalle(self) -> str:
        """Polimorfismo: detalle de tarea simple."""
        return (
            f"[SIMPLE] {self.titulo}\n"
            f"  Descripción : {self.descripcion}\n"
            f"  Prioridad   : {self.prioridad}\n"
            f"  Categoría   : {self.categoria}\n"
            f"  Fecha límite: {self.fecha_limite}\n"
            f"  Estado      : {'Completada' if self.completada else 'Pendiente'}"
        )

# ─────────────────────────────────────────────
#  SUBCLASE 2: Tarea Urgente
# ─────────────────────────────────────────────
class TareaUrgente(Tarea):
    """Tarea con nivel de alerta adicional. Hereda de Tarea."""

    def __init__(self, *args: Any, motivo_urgencia: str = "Sin especificar", **kwargs: Any):
        super().__init__(*args, **kwargs)           # Reutilización: llama al __init__ padre
        self.motivo_urgencia = motivo_urgencia

    def mostrar_detalle(self) -> str:
        """Polimorfismo: detalle de tarea urgente con su motivo."""
        return (
            f"[URGENTE 🚨] {self.titulo}\n"
            f"  Descripción    : {self.descripcion}\n"
            f"  Motivo urgencia: {self.motivo_urgencia}\n"
            f"  Prioridad      : {self.prioridad}\n"
            f"  Categoría      : {self.categoria}\n"
            f"  Fecha límite   : {self.fecha_limite}\n"
            f"  Estado         : {'Completada' if self.completada else 'Pendiente'}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Reutilización: extiende to_dict del padre con campo extra."""
        data = super().to_dict()
        data["motivo_urgencia"] = self.motivo_urgencia
        return data


# ─────────────────────────────────────────────
#  SUBCLASE 3: Tarea Recurrente
# ─────────────────────────────────────────────
class TareaRecurrente(Tarea):
    """Tarea que se repite en un intervalo dado. Hereda de Tarea."""

    def __init__(self, *args: Any, frecuencia: str = "Semanal", **kwargs: Any):
        super().__init__(*args, **kwargs)           # Reutilización: llama al __init__ padre
        self.frecuencia = frecuencia

    def mostrar_detalle(self) -> str:
        """Polimorfismo: detalle de tarea recurrente con su frecuencia."""
        return (
            f"[RECURRENTE 🔄] {self.titulo}\n"
            f"  Descripción : {self.descripcion}\n"
            f"  Frecuencia  : {self.frecuencia}\n"
            f"  Prioridad   : {self.prioridad}\n"
            f"  Categoría   : {self.categoria}\n"
            f"  Fecha límite: {self.fecha_limite}\n"
            f"  Estado      : {'Completada' if self.completada else 'Pendiente'}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Reutilización: extiende to_dict del padre con campo extra."""
        data = super().to_dict()
        data["frecuencia"] = self.frecuencia
        return data

# ─────────────────────────────────────────────
#  FÁBRICA: reconstruye el tipo correcto desde JSON
# ─────────────────────────────────────────────
def tarea_desde_dict(data: Dict[str, Any]) -> Tarea:
    """Fábrica que reconstruye el tipo concreto de Tarea desde un diccionario."""
    tipo = data.get("tipo", "TareaSimple")
    base = {
        "id": data["id"],
        "titulo": data["titulo"],
        "descripcion": data["descripcion"],
        "prioridad": data["prioridad"],
        "categoria": data["categoria"],
        "fecha_limite": data["fecha_limite"],
        "completada": data.get("completada", False),
    }
    if tipo == "TareaUrgente":
        return TareaUrgente(**base, motivo_urgencia=data.get("motivo_urgencia", ""))
    if tipo == "TareaRecurrente":
        return TareaRecurrente(**base, frecuencia=data.get("frecuencia", "Semanal"))
    return TareaSimple(**base)