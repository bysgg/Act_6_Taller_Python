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

def menu_agregar(gestor: GestorTareas) -> None:
    print("\n  ¿Qué tipo de tarea?")
    print("  1. Simple")
    print("  2. Urgente")
    print("  3. Recurrente")
    tipo = input("  Opción: ").strip()

    datos = pedir_datos_base(gestor)

    if tipo == "1":
        tarea = TareaSimple(**datos)
    elif tipo == "2":
        motivo = input("  Motivo de urgencia: ").strip()
        tarea = TareaUrgente(**datos, motivo_urgencia=motivo)
    elif tipo == "3":
        frecuencia = input("  Frecuencia (Diaria/Semanal/Mensual): ").strip()
        tarea = TareaRecurrente(**datos, frecuencia=frecuencia)
    else:
        print("  ❌ Tipo inválido.")
        return

    gestor.agregar_tarea(tarea)
    print("  ✔ Tarea guardada.")