# Agentes Inteligentes para la Web - SHACL

Este repositorio contiene la investigación, documentación y ejemplos prácticos desarrollados para el Trabajo Obligatorio N°2 de la asignatura Agentes Inteligentes para la Web (UNCo). El proyecto se centra en el estudio del estándar SHACL (Shapes Constraint Language), su sintaxis, marco teórico y sus aplicaciones en la Web Semántica.

## Equipo
* Paula Coronel
* Antonio Sarmiento
* Sthefany Cedeño

---

## Introducción a SHACL
La Web Semántica permite representar información estructurada mediante RDF y OWL. Sin embargo, a medida que los grafos de conocimiento crecen, surgen inconsistencias y problemas de calidad de datos. 

SHACL es la respuesta estandarizada por la W3C para resolver este problema. A diferencia de las ontologías tradicionales (que asumen un "Mundo Abierto" para inferir conocimiento), SHACL opera con un enfoque más cercano al "Mundo Cerrado", evaluando las restricciones (Shapes) directamente sobre el grafo de datos para validar su estructura y tipos, reportando violaciones sin asumir hechos no declarados.

## Componentes de SHACL
SHACL se basa en grafos de formas (shapes graphs) que validan grafos de datos (data graphs). Una forma o shape se compone de:
1.  **Name (s):** Nombre de la shape.
2.  **Target (t):** Define qué nodos serán evaluados (focus nodes). Puede apuntar a un nodo específico, a instancias de una clase (targetClass), o a sujetos/objetos de un predicado.
3.  **Constraint (d):** Las restricciones que debe cumplir el nodo, agrupadas en estructurales (cardinalidad, tipos), de filtro (expresiones regulares, datatypes) y lógicas (negación, conjunción).

## Ejemplos de Implementación
El repositorio documenta casos de uso progresivos para comprender el alcance de SHACL:

### 1. Restricción Básica (sh:minCount)
Define que todo empleado (targetClass: Employee) debe tener asignado al menos un número de oficina.
```turtle
:EmployeeShape a sh:PropertyShape ;
    sh:targetClass :Employee ;
    sh:path :hasOfficeNumber ;
    sh:minCount 1 .

```

### 2. Restricción Calificada (sh:qualifiedMinCount)

Extiende el caso anterior. No solo exige la existencia de la oficina, sino que el valor del número de oficina debe cumplir con otra shape anidada (ej. tener una longitud mínima de 3 caracteres).

```turtle
:EmployeeShapeB a sh:PropertyShape ;
    sh:targetClass :Employee ;
    sh:path :hasOfficeNumber ;
    sh:qualifiedMinCount 1 ;
    sh:qualifiedValueShape :OfficeNumberShape .

:OfficeNumberShape a sh:NodeShape ;
    sh:minLength 3 .

```

## Aplicaciones en el Mundo Real

SHACL ha superado la etapa de investigación y actualmente se utiliza en entornos productivos:

* **Bases de Datos (Triplestores):** Integración nativa en motores como GraphDB, Apache Jena y Stardog, actuando de forma análoga a las restricciones CHECK en SQL.
* **Cumplimiento Normativo (GDPR):** Validación de metadatos clínicos y auditoría de privacidad sobre knowledge graphs corporativos.
* **Sector Público:** Utilizado por la Comisión Europea para validar metadatos y garantizar el intercambio consistente de datos abiertos.
* **Ingeniería Ontológica:** Herramientas como Astrea permiten generar automáticamente restricciones SHACL a partir de ontologías OWL.

## Limitaciones y Desafíos

Aunque SHACL es robusto para validación sintáctica, presenta ciertas limitaciones:

* No puede acceder a recursos externos en la web de forma dinámica.
* La validación oficial carece de semántica formal estandarizada para manejar la recursión profunda.
* Su alcance de evaluación es local al focus node, por lo que no puede calcular métricas a nivel de red (ej. Interlinking).

## Referencias

* Cortés, C., et al. (2020). Is shacl suitable for data quality assessment?.
* Pareti, P., & Konstantinidis, G. (2021). A review of shacl: From data validation to schema reasoning for rdf graphs.

```

```
