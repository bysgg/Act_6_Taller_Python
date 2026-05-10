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
