import json
import os
import sys
import tempfile
import unittest

# Permite importar los módulos del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from tarea import TareaSimple, TareaUrgente, TareaRecurrente, tarea_desde_dict
from repositorio import RepositorioTareas
from gestor import GestorTareas


# ─────────────────────────────────────────────────────────────
#  TESTS: Herencia y Polimorfismo
# ─────────────────────────────────────────────────────────────
class TestHerenciaYPolimorfismo(unittest.TestCase):
    """Verifica que la herencia y el polimorfismo funcionan correctamente."""

    def setUp(self):
        self.simple = TareaSimple(1, "Comprar pan", "Ir al super", "Baja", "Hogar", "2025-12-01")
        self.urgente = TareaUrgente(2, "Pagar factura", "Vence hoy", "Alta", "Finanzas",
                                    "2025-06-01", motivo_urgencia="Multa por mora")
        self.recurrente = TareaRecurrente(3, "Reunión equipo", "Sync semanal", "Media",
                                          "Trabajo", "2025-12-31", frecuencia="Semanal")

    # ── Herencia: todas son instancias de Tarea ──────────────────────────────
    def test_herencia_tarea_simple(self):
        from tarea import Tarea
        self.assertIsInstance(self.simple, Tarea)

    def test_herencia_tarea_urgente(self):
        from tarea import Tarea
        self.assertIsInstance(self.urgente, Tarea)

    def test_herencia_tarea_recurrente(self):
        from tarea import Tarea
        self.assertIsInstance(self.recurrente, Tarea)

    # ── Atributos propios de cada subclase ───────────────────────────────────
    def test_urgente_tiene_motivo(self):
        self.assertEqual(self.urgente.motivo_urgencia, "Multa por mora")

    def test_recurrente_tiene_frecuencia(self):
        self.assertEqual(self.recurrente.frecuencia, "Semanal")

    # ── Polimorfismo: mostrar_detalle() diferente en cada subclase ───────────
    def test_polimorfismo_simple(self):
        detalle = self.simple.mostrar_detalle()
        self.assertIn("[SIMPLE]", detalle)
        self.assertIn("Comprar pan", detalle)

    def test_polimorfismo_urgente(self):
        detalle = self.urgente.mostrar_detalle()
        self.assertIn("[URGENTE", detalle)
        self.assertIn("Multa por mora", detalle)

    def test_polimorfismo_recurrente(self):
        detalle = self.recurrente.mostrar_detalle()
        self.assertIn("[RECURRENTE", detalle)
        self.assertIn("Semanal", detalle)

    def test_polimorfismo_mismo_metodo_diferente_resultado(self):
        """El mismo método retorna texto distinto según el tipo concreto."""
        detalles = [t.mostrar_detalle() for t in [self.simple, self.urgente, self.recurrente]]
        # Todos son strings distintos
        self.assertNotEqual(detalles[0], detalles[1])
        self.assertNotEqual(detalles[1], detalles[2])


# ─────────────────────────────────────────────────────────────
#  TESTS: Reutilización de código (método heredado)
# ─────────────────────────────────────────────────────────────
class TestReutilizacionCodigo(unittest.TestCase):
    """Verifica que los métodos heredados de Tarea funcionan en subclases."""

    def test_marcar_completada_en_simple(self):
        t = TareaSimple(1, "T1", "Desc", "Baja", "Cat", "2025-01-01")
        self.assertFalse(t.completada)
        t.marcar_completada()
        self.assertTrue(t.completada)

    def test_marcar_completada_en_urgente(self):
        t = TareaUrgente(2, "T2", "Desc", "Alta", "Cat", "2025-01-01", motivo_urgencia="X")
        t.marcar_completada()
        self.assertTrue(t.completada)

    def test_marcar_completada_en_recurrente(self):
        t = TareaRecurrente(3, "T3", "Desc", "Media", "Cat", "2025-01-01", frecuencia="Diaria")
        t.marcar_completada()
        self.assertTrue(t.completada)

    def test_to_dict_incluye_tipo(self):
        """to_dict hereda el campo 'tipo' del nombre de la clase."""
        t = TareaUrgente(4, "T4", "D", "Alta", "C", "2025-01-01", motivo_urgencia="M")
        d = t.to_dict()
        self.assertEqual(d["tipo"], "TareaUrgente")
        self.assertIn("motivo_urgencia", d)       # Campo extendido en subclase


# ─────────────────────────────────────────────────────────────
#  TESTS: Manejo de archivos (repositorio JSON)
# ─────────────────────────────────────────────────────────────
class TestRepositorio(unittest.TestCase):
    """Verifica la lectura y escritura en archivos JSON."""

    def setUp(self):
        # Usa un archivo temporal para no afectar datos reales
        self.tmpdir = tempfile.mkdtemp()
        self.ruta = os.path.join(self.tmpdir, "test_tareas.json")
        self.repo = RepositorioTareas(ruta=self.ruta)

    def tearDown(self):
        if os.path.exists(self.ruta):
            os.remove(self.ruta)

    def test_cargar_archivo_inexistente_retorna_lista_vacia(self):
        tareas = self.repo.cargar()
        self.assertEqual(tareas, [])

    def test_guardar_y_cargar_tarea_simple(self):
        t = TareaSimple(1, "Test", "Desc", "Baja", "Cat", "2025-01-01")
        self.repo.guardar([t])
        cargadas = self.repo.cargar()
        self.assertEqual(len(cargadas), 1)
        self.assertEqual(cargadas[0].titulo, "Test")
        self.assertIsInstance(cargadas[0], TareaSimple)

    def test_guardar_y_cargar_tarea_urgente(self):
        t = TareaUrgente(2, "Urgente", "Desc", "Alta", "Cat", "2025-01-01",
                         motivo_urgencia="Revisión")
        self.repo.guardar([t])
        cargadas = self.repo.cargar()
        self.assertIsInstance(cargadas[0], TareaUrgente)
        self.assertEqual(cargadas[0].motivo_urgencia, "Revisión")

    def test_guardar_y_cargar_tarea_recurrente(self):
        t = TareaRecurrente(3, "Rec", "Desc", "Media", "Cat", "2025-01-01",
                            frecuencia="Mensual")
        self.repo.guardar([t])
        cargadas = self.repo.cargar()
        self.assertIsInstance(cargadas[0], TareaRecurrente)
        self.assertEqual(cargadas[0].frecuencia, "Mensual")

    def test_archivo_json_es_valido(self):
        """El archivo guardado debe ser JSON válido."""
        t = TareaSimple(1, "JSON", "Desc", "Baja", "Cat", "2025-01-01")
        self.repo.guardar([t])
        with open(self.ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["titulo"], "JSON")

    def test_persistencia_completada(self):
        """El estado 'completada' se persiste correctamente."""
        t = TareaSimple(1, "Test", "Desc", "Baja", "Cat", "2025-01-01")
        t.marcar_completada()
        self.repo.guardar([t])
        cargadas = self.repo.cargar()
        self.assertTrue(cargadas[0].completada)


# ─────────────────────────────────────────────────────────────
#  TESTS: GestorTareas (lógica de negocio)
# ─────────────────────────────────────────────────────────────
class TestGestorTareas(unittest.TestCase):
    """Pruebas de la lógica de negocio del gestor."""

    def setUp(self):
        tmpdir = tempfile.mkdtemp()
        ruta = os.path.join(tmpdir, "gestor_test.json")
        repo = RepositorioTareas(ruta=ruta)
        self.gestor = GestorTareas(repositorio=repo)

        # Datos de prueba con distintos tipos
        self.gestor.agregar_tarea(
            TareaSimple(1, "Comprar leche", "Super", "Baja", "Hogar", "2025-12-01"))
        self.gestor.agregar_tarea(
            TareaUrgente(2, "Pagar arriendo", "Banco", "Alta", "Finanzas", "2025-06-15",
                         motivo_urgencia="Fecha máxima"))
        self.gestor.agregar_tarea(
            TareaRecurrente(3, "Gym", "Ejercicio", "Media", "Salud", "2025-12-31",
                            frecuencia="Diaria"))

    def test_agregar_tarea(self):
        self.assertEqual(len(self.gestor.tareas), 3)

    def test_proximo_id(self):
        self.assertEqual(self.gestor.proximo_id(), 4)

    def test_eliminar_tarea_existente(self):
        resultado = self.gestor.eliminar_tarea(1)
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.tareas), 2)

    def test_eliminar_tarea_inexistente(self):
        resultado = self.gestor.eliminar_tarea(999)
        self.assertFalse(resultado)

    def test_marcar_completada(self):
        resultado = self.gestor.marcar_completada(2)
        self.assertTrue(resultado)
        tarea = self.gestor.buscar_por_id(2)
        self.assertTrue(tarea.completada)

    def test_marcar_completada_inexistente(self):
        self.assertFalse(self.gestor.marcar_completada(999))

    def test_buscar_por_texto(self):
        resultados = self.gestor.buscar_por_texto("arriendo")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].id, 2)

    def test_buscar_por_texto_insensible_mayusculas(self):
        resultados = self.gestor.buscar_por_texto("GYM")
        self.assertEqual(len(resultados), 1)

    def test_filtrar_por_prioridad(self):
        altas = self.gestor.filtrar_por_prioridad("Alta")
        self.assertEqual(len(altas), 1)
        self.assertEqual(altas[0].id, 2)

    def test_filtrar_por_categoria(self):
        salud = self.gestor.filtrar_por_categoria("Salud")
        self.assertEqual(len(salud), 1)
        self.assertIsInstance(salud[0], TareaRecurrente)

    def test_filtrar_pendientes(self):
        self.gestor.marcar_completada(1)
        pendientes = self.gestor.filtrar_pendientes()
        self.assertEqual(len(pendientes), 2)

    def test_buscar_por_id(self):
        t = self.gestor.buscar_por_id(3)
        self.assertIsNotNone(t)
        self.assertEqual(t.titulo, "Gym")

    def test_buscar_por_id_inexistente(self):
        self.assertIsNone(self.gestor.buscar_por_id(999))


# ─────────────────────────────────────────────────────────────
#  TESTS: Fábrica tarea_desde_dict
# ─────────────────────────────────────────────────────────────
class TestFabricaTareas(unittest.TestCase):

    def _base(self, tipo: str) -> dict:
        return {"tipo": tipo, "id": 1, "titulo": "T", "descripcion": "D",
                "prioridad": "Baja", "categoria": "C", "fecha_limite": "2025-01-01",
                "completada": False}

    def test_fabrica_simple(self):
        d = self._base("TareaSimple")
        self.assertIsInstance(tarea_desde_dict(d), TareaSimple)

    def test_fabrica_urgente(self):
        d = self._base("TareaUrgente")
        d["motivo_urgencia"] = "Prueba"
        t = tarea_desde_dict(d)
        self.assertIsInstance(t, TareaUrgente)
        self.assertEqual(t.motivo_urgencia, "Prueba")

    def test_fabrica_recurrente(self):
        d = self._base("TareaRecurrente")
        d["frecuencia"] = "Diaria"
        t = tarea_desde_dict(d)
        self.assertIsInstance(t, TareaRecurrente)
        self.assertEqual(t.frecuencia, "Diaria")

    def test_fabrica_tipo_desconocido_retorna_simple(self):
        d = self._base("TipoInexistente")
        self.assertIsInstance(tarea_desde_dict(d), TareaSimple)


if __name__ == "__main__":
    unittest.main(verbosity=2)
