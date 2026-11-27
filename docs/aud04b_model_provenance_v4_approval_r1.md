# R13-APPROVAL-4.0.0-R1 — Registro formal de decisiones normativas

**Estado del registro:** propuesta documental para decisión humana. No aprueba la especificación 4.0.0, no implementa R13 y no modifica el comportamiento de S1.

**Base conocida:** commit remoto **764f11dea72c862a33e27a3019b426e0ecc8bb21**.

**Continuación documental inspeccionada:** **cb436b51b7038039d4f1f72e0d5fec899aa9ef0f**, descendiente de la base conocida.
**Fuentes normativas:**

- **docs/aud04b_model_provenance_v3_design.md**, contrato histórico 3.0.0 congelado.
- **docs/aud04b_model_provenance_v4_design.md**, especificación propuesta de 4.0.0.
- R13-DESIGN-R3.2, R13-DOCUMENTATION-R1 y R13-DOCUMENTATION-R1.1.

## 1. Propósito y reglas de estado

Este registro hace explícitas las decisiones que la especificación 4.0.0 deja pendientes. Es una fuente de trazabilidad del proceso de aprobación; no sustituye a la especificación técnica ni cambia el contrato 3.0.0.

| Estado | Significado |
|---|---|
| **PROPUESTA PARA APROBACIÓN** | La decisión está definida para revisión humana, pero no está aprobada ni implementada. |
| **APROBADA** | Estado reservado para una decisión humana posterior y explícita. |
| **RECHAZADA** | Estado reservado para una decisión humana posterior y explícita. |
| **APLAZADA** | Tema fuera de 4.0.0 inicial que no puede implementarse ni aceptarse sin un cambio de contrato posterior. |

En este registro no hay decisiones **APROBADAS** ni **RECHAZADAS**. Ninguna mención de una propuesta se interpreta como autorización para modificar schema, código, tests, fixtures, loaders, registry, writer, inferencia o S2.

## 2. Matriz de decisiones

| ID | Decisión | Estado | Especificación 4.0.0 | Impacto en schema futuro | Impacto en implementación futura | Pruebas futuras |
|---|---|---|---|---|---|---|
| DEC-01 | reason_code sin catálogo cerrado inicial | PROPUESTA PARA APROBACIÓN | §7.3 | Patrón ASCII y campos de evidence por evento | Validación sintáctica; sin enum implícito | V4-U08 y casos de patrón válido/inválido |
| DEC-02 | actor con namespace explícito | PROPUESTA PARA APROBACIÓN | §7.2 | Patrón de identificador; no proveedor de identidad | Validación de formato solamente | V4-U08 y casos de namespace |
| DEC-03 | extensions vacío en 4.0.0 inicial | PROPUESTA PARA APROBACIÓN | §§9.2–9.3 | extensions constante como objeto vacío | Rechazo de extensiones no vacías | V4-U13 |
| DEC-04 | calibration únicamente compartida con validation | PROPUESTA PARA APROBACIÓN | §6 | shared_with y fit_partition restringidos | Validación de equivalencia; sin frontera artificial | V4-U04 |
| DEC-05 | contratos 3.0.0 y 4.0.0 separados | PROPUESTA PARA APROBACIÓN | §3 | Esquema 4.0.0 independiente | Dispatch explícito por schema_version | V4-U01 |
| DEC-06 | run_fingerprint con allowlist normativa | PROPUESTA PARA APROBACIÓN | §9 | Rutas incluidas, opcionales y anulables definidas | Construcción de preimagen reproducible | V4-U10, V4-U11 y vectores dorados completos |
| DEC-07 | eventos de nueve campos y sidecar Ed25519 | PROPUESTA PARA APROBACIÓN | §§7–8 | Contratos de evento, evidence y sidecar | Cadena estructural; asociación de sidecar; sin confianza criptográfica S1 | V4-U07, V4-U08, V4-U09 y V4-U11 |
| DEC-08 | posiciones fuente y purga por fuente | PROPUESTA PARA APROBACIÓN | §§4–5 | Límites fuente y reglas de partición | Validación estructural; verificador de datos posterior separado | V4-U02, V4-U03, V4-U14 y V4-U15 |

## 3. Decisiones propuestas

### DEC-01 — reason_code

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** reason_code es una cadena ASCII que cumple el patrón **^[a-z][a-z0-9_]{0,63}$**. La primera versión 4.0.0 no define un catálogo cerrado. Un catálogo versionado futuro requerirá un cambio explícito de contrato.

**Justificación:** la especificación propuesta necesita distinguir la validez sintáctica de la política semántica. Un enum no documentado convertiría una decisión pendiente en una restricción implícita.

**Impacto futuro:** el schema de evidence debe aplicar el patrón a los eventos deprecated, revoked y rejected. La implementación solo valida sintaxis y campos obligatorios; no asigna significado, permisos ni efectos al texto. Las pruebas deben cubrir valores válidos, cadenas con mayúsculas, espacios, caracteres no ASCII, longitud límite y longitud excesiva.

**Relación con la especificación:** coincide con §7.3 y conserva como pendiente el catálogo de valores.

### DEC-02 — actor

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** actor usa exactamente uno de los prefijos **human:** o **service:** seguido de un identificador ASCII local. El patrón propuesto es **^(human|service):[A-Za-z0-9][A-Za-z0-9._-]{0,119}$**. Los prefijos distinguen el tipo declarado de actor, sin elegir un proveedor de identidad ni un sistema de autenticación.

**Justificación:** el texto de actor debe ser trazable y no ambiguo, sin confundir una etiqueta declarada con una identidad autenticada.

**Impacto futuro:** el schema debe restringir el formato del identificador y documentar namespaces permitidos. La implementación solo comprueba formato y conserva el valor canónico. La autenticación, autorización, pertenencia a un rol y confianza del emisor requieren evidencia externa; S1 no las infiere de actor. Las pruebas deben cubrir namespaces humano y servicio válidos, formato inválido y ausencia de inferencia de autoridad.

**Compatibilidad y límites:** el patrón propuesto es una restricción más específica compatible con el patrón general de actor de §7.2. No se propone proveedor, directorio de usuarios ni protocolo de autenticación.

### DEC-03 — extensions

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** 4.0.0 inicial exige **extensions = {}**. No se aceptan extensiones no vacías hasta definir namespaces registrados, schemas, límites de tamaño y una política de estabilidad y sensibilidad. Las extensiones futuras requieren cambio explícito de contrato.

**Justificación:** el objeto abierto genérico no permite demostrar que los valores sean no sensibles, estables y no conductuales. Aceptarlo debilitaría la reproducibilidad y permitiría configuración relevante fuera de las rutas tipadas.

**Impacto futuro:** el schema 4.0.0 debe restringir extensions al objeto vacío. La implementación rechaza cualquier namespace no vacío. El run_fingerprint continúa excluyendo extensions porque la única forma permitida inicial es vacía. Las pruebas deben cubrir objeto vacío aceptado y objeto no vacío rechazado.

**Relación con la especificación:** coincide con §§9.2–9.3 y V4-U13.

### DEC-04 — calibración compartida

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** 4.0.0 inicial admite únicamente calibration compartida exactamente con validation. calibration.fit_partition vale **validation** y validation.partitions.calibration.shared_with vale **validation**. Calibration independiente queda aplazada.

**Justificación:** la modalidad compartida tiene una representación completa y evita crear una frontera cronológica ficticia entre validation y calibration. La modalidad independiente necesita una definición aprobada de partición, fit_partition, orden temporal, purga, embargo y relaciones de hash.

**Impacto futuro:** el schema debe restringir shared_with y fit_partition. La implementación valida que calibration y validation tengan los mismos límites, límites fuente, conteos, timestamps normalizados e index_sha256. Solo existen las fronteras train a validation y validation a test. Las pruebas deben cubrir equivalencia completa, divergencias y la ausencia de una frontera validation a calibration.

**Elemento aplazado:** calibration independiente. No forma parte de 4.0.0 inicial ni de R13-IMPLEMENTATION mientras no exista un cambio de contrato aprobado.

### DEC-05 — versionado

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** 3.0.0 permanece congelado; 4.0.0 es un contrato y schema independientes. El validador público conserva su interfaz y selecciona reglas mediante schema_version. No hay conversión implícita ni aplicación de defaults para migrar manifiestos.

**Justificación:** los nuevos límites de posición fuente, reglas de calibration, evidence y fingerprint son incompatibles con la validez histórica de 3.0.0. Reinterpretar manifiestos existentes rompería su reproducibilidad.

**Impacto futuro:** se requiere un schema 4.0.0 separado y dispatch explícito. La implementación mantiene el retorno público list[str], sin afirmar que esa implementación exista hoy. Las pruebas deben aceptar cada versión solo bajo su propio contrato y rechazar versiones ausentes o desconocidas.

**Relación con la especificación:** coincide con §3 y V4-U01.

### DEC-06 — run_fingerprint

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** run_fingerprint se calcula sobre la allowlist normativa de §9.2. La preimagen conserva presencia frente a null, incluye configuración efectiva y excluye identificadores de salida, timestamps, artefactos, métricas y hashes derivados. Se canonicaliza con JCS y se hashea con SHA-256.

**Justificación:** una proyección explícita evita que cambios incidentales o resultados derivados modifiquen la identidad de intención del run, y evita omitir configuración semánticamente relevante.

**Impacto futuro:** el schema debe incorporar los campos 4.0.0 requeridos por la allowlist. La implementación construye una preimagen nueva solo con rutas permitidas; no copia el manifiesto completo. Las pruebas deben demostrar que cambiar cada ruta incluida altera el fingerprint y que cambiar una ruta excluida no lo altera. Deben verificarse independientemente index_sha256, partition_manifest_sha256, calibration_input_sha256 y event_sha256.

**Elemento aplazado:** los vectores dorados completos de manifiesto y fingerprint. La especificación conserva el vector JCS reducido; los vectores completos se producen y verifican durante la implementación, sin que ello autorice cambios silenciosos de proyección.

### DEC-07 — eventos y firmas

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** el payload canónico contiene nueve campos: sequence_number, event_id, model_id, event, at, actor, evidence, manifest_sha256 y previous_event_sha256. El evento almacenado añade event_sha256 como décimo campo. El sidecar es un objeto independiente. Ed25519 firma los bytes JCS UTF-8, sin BOM ni salto final, del payload de nueve campos.

**Justificación:** esta separación elimina la circularidad entre firma y event_sha256 y diferencia la cadena de integridad de la autenticidad criptográfica.

**Impacto futuro:** el schema debe cerrar los objetos de evento, evidence y sidecar, y exigir sus campos según el tipo de evento. La implementación valida estructura, secuencia, hashes, transiciones permitidas y asociación sidecar-evento. S1 no verifica firmas, claves, roles, revocaciones ni anclajes externos, y no concede autorización de inferencia. Las pruebas deben cubrir primera entrada, sentinel de génesis, continuidad, transiciones inválidas, sidecars ausentes/duplicados/mal asociados y preimágenes de hash.

**Relación con la especificación:** coincide con §§7–8 y V4-U07 a V4-U09.

### DEC-08 — posiciones fuente y purga

**Estado:** PROPUESTA PARA APROBACIÓN.

**Decisión propuesta:** source_position es el ordinal de la fila en la serie OHLCV original antes del filtrado. Las posiciones por secuencia son enteros no negativos, estrictamente crecientes y únicos. Los límites son semiabiertos; source_position_start coincide con la primera posición conservada y source_position_end con la última más uno. La purga se comprueba con **gap_source(A,B) >= max(H,E)**.

**Justificación:** las filas filtradas y las posiciones de la serie fuente son coordenadas distintas. La condición usa la coordenada en la que se mide horizon_bars y evita sumar dos veces embargo y horizonte.

**Impacto futuro:** el schema debe añadir los límites fuente a cada partición y documentar que embargo_rows cuenta posiciones de la serie fuente en 4.0.0. La implementación S1 valida estructura, aritmética y relaciones declaradas. Un verificador posterior, con dataset original y reglas de filtrado, reconstruye la secuencia, comprueba las invariantes y recalcula límites e index_sha256. Las pruebas deben separar los casos estructurales de las comprobaciones que requieren datos originales.

**Relación con la especificación:** coincide con §§4–5, V4-U02, V4-U03, V4-U14 y V4-U15.

## 4. Registro de aprobaciones, rechazos y aplazamientos

### Aprobadas

Ninguna. Este documento no registra aprobación humana de DEC-01 a DEC-08.

### Rechazadas

Ninguna. No se ha presentado una decisión humana de rechazo.

### Aplazadas

| Tema | Motivo | Condición para reabrir |
|---|---|---|
| Calibration independiente | Carece de contrato completo de partición, fit_partition, purga, embargo y hashes. | Cambio de contrato documentado y aprobado. |
| Catálogo cerrado de reason_code | La primera versión solo propone formato sintáctico. | Catálogo versionado con semántica, compatibilidad y pruebas. |
| Extensiones no vacías | Faltan namespaces registrados, schemas, límites y política de sensibilidad. | Cambio de contrato con validación explícita. |
| Vectores dorados completos de fingerprint | Requieren la implementación independiente de preimágenes y canonicalización. | Implementación posterior y pruebas reproducibles. |
| Autenticación, confianza de claves y autorización | Están fuera de la validación estructural S1. | Diseño e implementación de verificador criptográfico y política de autorización fuera de S1. |

## 5. Conflictos y consistencia

No se detectó un conflicto normativo entre DEC-01 a DEC-08 y la especificación propuesta 4.0.0. Las decisiones concretan los puntos que la especificación marca como pendientes, sin alterar el contrato histórico 3.0.0.

Hay dos límites deliberados que deben mantenerse visibles:

- DEC-02 propone una sintaxis de namespace, pero no una identidad verificada ni un proveedor; no se debe implementar autenticación por inferencia.
- DEC-08 permite validación estructural en S1, pero no afirma validación efectiva contra datos originales sin que un verificador posterior recalcule la secuencia y sus hashes.

## 6. Criterios para una aprobación humana posterior

Una aprobación válida de cada DEC debe identificar el ID, el texto de la decisión aceptada, la versión documental resultante y cualquier excepción. La aprobación no autoriza por sí sola R13-IMPLEMENTATION, modificaciones de schema o código, ni el inicio de S2; dichas acciones requieren autorización separada.

Antes de implementar, la especificación aprobada debe mantener:

- Un ID estable y una fuente normativa para cada decisión.
- El impacto declarado sobre schema, implementación y pruebas.
- Ausencia de decisiones implícitas o defaults de migración.
- La separación entre integridad estructural, autenticidad criptográfica, confianza y autorización.
- La congelación íntegra del contrato 3.0.0.

## 7. Límites de alcance preservados

Este registro es solo documentación. No modifica código Python, JSON Schema, fixtures, tests, dependencias, modelos, datasets, cuarentena ni archivos Parquet. No implementa R13, no cambia el comportamiento de S1, no inicia S2, no habilita inferencia ni autoriza modelos.
