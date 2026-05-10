from gestor import GestorTareas
from tarea import TareaSimple, TareaUrgente, TareaRecurrente
from typing import Any


def pedir_datos_base(gestor: GestorTareas) -> dict[str, Any]:
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


def menu() -> None:
    gestor = GestorTareas()

    opciones = {
        "1": "Agregar tarea",
        "2": "Mostrar todas las tareas",
        "3": "Buscar por texto",
        "4": "Filtrar por prioridad",
        "5": "Filtrar por categoría",
        "6": "Mostrar tareas pendientes",
        "7": "Marcar como completada",
        "8": "Eliminar tarea",
        "9": "Salir",
    }

    while True:
        print("\n╔══════════════════════════════╗")
        print("║    GESTOR DE TAREAS  v2.0    ║")
        print("╚══════════════════════════════╝")
        for k, v in opciones.items():
            print(f"  {k}. {v}")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            menu_agregar(gestor)

        elif opcion == "2":
            print()
            gestor.mostrar_tareas()

        elif opcion == "3":
            texto = input("  Texto a buscar: ").strip()
            resultados = gestor.buscar_por_texto(texto)
            print(f"\n  {len(resultados)} resultado(s):")
            for t in resultados:
                print(f"  {t}")

        elif opcion == "4":
            prioridad = input("  Prioridad (Alta/Media/Baja): ").strip()
            for t in gestor.filtrar_por_prioridad(prioridad):
                print(f"  {t}")

        elif opcion == "5":
            categoria = input("  Categoría: ").strip()
            for t in gestor.filtrar_por_categoria(categoria):
                print(f"  {t}")

        elif opcion == "6":
            pendientes = gestor.filtrar_pendientes()
            print(f"\n  Tareas pendientes: {len(pendientes)}")
            for t in pendientes:
                print(f"  {t}")

        elif opcion == "7":
            try:
                id_ = int(input("  ID de la tarea: "))
                if gestor.marcar_completada(id_):
                    print("  ✔ Tarea marcada como completada.")
                else:
                    print("  ❌ No se encontró la tarea.")
            except ValueError:
                print("  ❌ ID inválido.")

        elif opcion == "8":
            try:
                id_ = int(input("  ID de la tarea a eliminar: "))
                if gestor.eliminar_tarea(id_):
                    print("  🗑 Tarea eliminada.")
                else:
                    print("  ❌ No se encontró la tarea.")
            except ValueError:
                print("  ❌ ID inválido.")

        elif opcion == "9":
            print("  👋 ¡Hasta luego!")
            break

        else:
            print("  ❌ Opción inválida.")


if __name__ == "__main__":
    menu()
