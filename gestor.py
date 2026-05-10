from typing import List, Optional
from tarea import Tarea
from repositorio import RepositorioTareas


class GestorTareas:
    """
    Orquesta las operaciones sobre tareas.
    Depende de la abstracción RepositorioTareas, no de una implementación concreta.
    """

    def __init__(self, repositorio: Optional[RepositorioTareas] = None):
        self._repo = repositorio or RepositorioTareas()
        self.tareas: List[Tarea] = self._repo.cargar()

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def agregar_tarea(self, tarea: Tarea) -> None:
        """Agrega una nueva tarea y la persiste."""
        self.tareas.append(tarea)
        self._repo.guardar(self.tareas)

    def eliminar_tarea(self, id: int) -> bool:
        """Elimina la tarea con el id dado. Retorna True si existía."""
        antes = len(self.tareas)
        self.tareas = [t for t in self.tareas if t.id != id]
        if len(self.tareas) < antes:
            self._repo.guardar(self.tareas)
            return True
        return False

    def marcar_completada(self, id: int) -> bool:
        """Marca la tarea como completada. Retorna True si se encontró."""
        for t in self.tareas:
            if t.id == id:
                t.marcar_completada()          # Método heredado de Tarea (reutilización)
                self._repo.guardar(self.tareas)
                return True
        return False

    def buscar_por_id(self, id: int) -> Optional[Tarea]:
        return next((t for t in self.tareas if t.id == id), None)

    # ── FILTROS ───────────────────────────────────────────────────────────────

    def buscar_por_texto(self, texto: str) -> List[Tarea]:
        return [t for t in self.tareas if texto.lower() in t.titulo.lower()]

    def filtrar_por_prioridad(self, prioridad: str) -> List[Tarea]:
        return [t for t in self.tareas if t.prioridad.lower() == prioridad.lower()]

    def filtrar_por_categoria(self, categoria: str) -> List[Tarea]:
        return [t for t in self.tareas if t.categoria.lower() == categoria.lower()]

    def filtrar_pendientes(self) -> List[Tarea]:
        return [t for t in self.tareas if not t.completada]