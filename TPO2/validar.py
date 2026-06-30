from pyshacl import validate
import rdflib


# ──────────────────────────────────────────────────────────────────
#  Utilidad: convierte una URI completa en una forma corta legible
#  Ej: http://example.org/musica/c1  ->  mus:c1
# ──────────────────────────────────────────────────────────────────


def shorten(graph: rdflib.Graph, term) -> str:
    """Devuelve una representación corta y legible de un término RDF."""
    if term is None:
        return "(no especificado)"
    if isinstance(term, rdflib.Literal):
        return f'"{term}"'
    try:
        qname = graph.namespace_manager.normalizeUri(term)
        return qname
    except Exception:
        return str(term)
 
 
# ──────────────────────────────────────────────────────────────────
#  Reporte legible: recorre el results_graph con SPARQL y arma
#  una salida clara en lugar de usar results_text (formato Turtle).
# ──────────────────────────────────────────────────────────────────

def imprimir_reporte(titulo: str, conforms: bool, results_graph: rdflib.Graph):
    print("=" * 70)
    print(f" {titulo}")
    print("=" * 70)
 
    if conforms:
        print("✅ Conforms: True — no se encontraron violaciones.\n")
        return
 
    print(f"❌ Conforms: False\n")
 
    query = """
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?focusNode ?path ?message ?severity ?value ?component
    WHERE {
        ?result a sh:ValidationResult ;
                sh:focusNode ?focusNode .
        OPTIONAL { ?result sh:resultPath ?path . }
        OPTIONAL { ?result sh:resultMessage ?message . }
        OPTIONAL { ?result sh:resultSeverity ?severity . }
        OPTIONAL { ?result sh:value ?value . }
        OPTIONAL { ?result sh:sourceConstraintComponent ?component . }
    }
    ORDER BY ?focusNode ?path
    """
 
    rows = list(results_graph.query(query))
    print(f"Se encontraron {len(rows)} violación(es):\n")
 
    for i, row in enumerate(rows, start=1):
        focus_node = shorten(results_graph, row.focusNode)
        path = shorten(results_graph, row.path)
        severity = shorten(results_graph, row.severity).replace("sh:", "")
        component = shorten(results_graph, row.component).replace("sh:", "")
        value = shorten(results_graph, row.value) if row.value is not None else "(sin valor)"
        message = str(row.message) if row.message is not None else "(sin mensaje)"
 
        icono = "🟥" if severity == "Violation" else "🟨" if severity == "Warning" else "ℹ️"
 
        print(f"{icono} [{i}] Severidad: {severity}")
        print(f"     Nodo afectado : {focus_node}")
        print(f"     Propiedad     : {path}")
        print(f"     Valor actual  : {value}")
        print(f"     Tipo de error : {component}")
        print(f"     Mensaje       : {message}")
        print("-" * 70)
 
    print()


# Prueba 1: Validación de los datos de cada nodo. 

# cargar el grafo de datos
data_graph = rdflib.Graph()
data_graph.parse("musica.ttl", format="turtle")

# cargar el grafo de formas (shapes)
shapes_graph = rdflib.Graph()
shapes_graph.parse("data_shapes.ttl", format="turtle")

# luego, se ejecuta la validación
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    data_graph_format="turtle",
    shacl_graph_format="turtle",
    inference='rdfs', 
    debug=False
)

imprimir_reporte("PRUEBA 1: Validación de datos (musica.ttl)", conforms, results_graph)



# Prueba 2: Metadatos de la ontologia

#cargamos los metadatos de la ontologia musica
data_graph = rdflib.Graph()
data_graph.parse("musica_ontologia.ttl", format="turtle")
 
# cargamos shapes
shapes_graph = rdflib.Graph()
shapes_graph.parse("ontology_shapes.ttl", format="turtle")
 
# luego, se ejecuta la validación
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference="rdfs",
    abort_on_first=False,
    debug=False,
)

imprimir_reporte("PRUEBA 2: Validación de metadatos (musica_ontologia.ttl)", conforms, results_graph)

