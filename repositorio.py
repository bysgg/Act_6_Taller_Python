import json
import os
from typing import List

from tarea import Tarea, tarea_desde_dict

RUTA_ARCHIVO = os.path.join("data", "tareas.json")


class RepositorioTareas:
    """Responsable única de leer y escribir tareas en disco (JSON)."""

    def __init__(self, ruta: str = RUTA_ARCHIVO):
        self._ruta = ruta
        os.makedirs(os.path.dirname(self._ruta), exist_ok=True)

    def cargar(self) -> List[Tarea]:
        """Lee las tareas desde el archivo JSON. Retorna lista vacía si no existe."""
        try:
            with open(self._ruta, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                return [tarea_desde_dict(d) for d in json.loads(contenido)]
        except FileNotFoundError:
            return []

    def guardar(self, tareas: List[Tarea]) -> None:
        """Escribe la lista completa de tareas en el archivo JSON."""
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(
                [t.to_dict() for t in tareas],
                f,
                indent=4,
                ensure_ascii=False,
            )