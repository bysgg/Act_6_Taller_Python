from gestor import GestorTareas


def pedir_datos_base(gestor: GestorTareas) -> dict:
    """Solicita los campos comunes a cualquier tipo de tarea."""
    return {
        "id": gestor.proximo_id(),
        "titulo": input("  Título        : ").strip(),
        "descripcion": input("  Descripción   : ").strip(),
        "prioridad": input("  Prioridad (Alta/Media/Baja): ").strip(),
        "categoria": input("  Categoría     : ").strip(),
        "fecha_limite": input("  Fecha límite (AAAA-MM-DD): ").strip(),
    }