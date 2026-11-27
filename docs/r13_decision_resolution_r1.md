# R13-DECISION-RESOLUTION-R1 — Resolución documental de hallazgos de Fase B

**Estado del documento:** resolución documental. No modifica código, schemas, tests, dependencias, decisiones normativas ni el plan R1.1.
**Revisión:** R1.1 (correcciones derivadas de `R13-AUDIT-DECISION-RESOLUTION-R1`, dictamen `ACCEPTED WITH FINDINGS`).
**Fecha:** 2026-11-27.
**Base:** el presente documento fue publicado por el propietario en el commit `53cfd6f28a169f2e71edf557e66b7c4f5ea17a1d`, hijo de `f17246e0abf5878f3ad6f2df84d30bb76a351542` (Fase B). La auditoría verificó HEAD local y remoto alineados en `53cfd6f…` y árbol de trabajo limpio.

**Convención de estado:**

| Estado | Significado |
|---|---|
| **CLOSED** | Asunto resuelto documentalmente; no requiere acción adicional. |
| **DEFERRED** | Asunto diferido a una fase posterior ya prevista o a una capacidad posterior. |
| **PENDING APPROVAL** | Requiere decisión o autorización explícita del propietario antes de cualquier cambio. |
| **NOT IN SCOPE** | Problema preexistente o ajeno al alcance de Fase B; no se corrige aquí. |

**Convención de calificación:**

| Marca | Significado |
|---|---|
| **[APROBADO]** | **Exclusivamente** DEC-01 a DEC-08, aprobadas normativamente con anterioridad. No se reabren. |
| **[REQUISITO DE DISEÑO / CRITERIO DE PLAN]** | Contenido del diseño v4 o del plan R1.1. No constituye una DEC aprobada ni autoriza implementación por sí mismo. |
| **[ACEPTADO POR AUDITORÍA]** | Resultado de la auditoría independiente `R13-AUDIT-IMPLEMENTATION-B-CP-B-R1`. No equivale a autorización de la siguiente fase. |
| **[RECOMENDACIÓN TÉCNICA]** | Propuesta del responsable de trazabilidad; **no** es una decisión aprobada. |
| **[PENDIENTE DE APROBACIÓN]** | Acción que requiere autorización explícita del propietario. |

---

## 1. Resumen ejecutivo

1. **[ACEPTADO POR AUDITORÍA] — R1:** Fase B fue auditada con dictamen **ACCEPTED WITH FINDINGS**; CP-B-01 a CP-B-10 resultaron **PASS**; no hay hallazgos Critical, High ni Medium. La aceptación de CP-B **no autoriza** Fase C, que permanece **BLOQUEADA**.
2. **[CLOSED] — R2:** la diferencia entre el informe inicial de implementación y el estado auditado se debe a que el propietario realizó personalmente el commit y push. Se registra como aclaración documental cerrada, sin calificarla como incidencia de autorización ni atribuir acciones a terceros.
3. **[PENDING APPROVAL] — R3:** la permutación exacta entre `class_order` y `classes` aparece en el diseño v4 §5.3 (propuesta no aprobada) y el plan R1.1 la contempla como V4-U06 en Fase B, pero no se implementó. Se recomienda incorporarla al validador semántico v4; el cambio requiere autorización del propietario porque Fase B ya fue auditada y aceptada.
4. **[DEFERRED] — R4:** los tres flags son resultados derivados o evidencia de ejecución. Su tipo/estructura se validó en B; su veracidad debe demostrarse en Fase D o en el verificador posterior (S6). No se convierten automáticamente en `true`.
5. **[DEFERRED / NOT IN SCOPE] — R5:** F-4 y F-5 quedan diferidos sin bloquear CP-B; F-6 es un conjunto de problemas históricos fuera del alcance de B.
6. **[REVISIÓN R1.1]:** se corrigen AUD-F-1 (etiquetas normativas), AUD-F-2 (estado Git autorreferenciado), AUD-F-3 (autoridad de V4-U06) y AUD-F-4 (distinción entre los flags de purga). Las correcciones son documentales; no cierran las cuestiones técnicas pendientes.

---

## 2. Base y estado verificado

| Ítem | Valor |
|---|---|
| Repositorio | `lutz405/Trading` |
| Rama | `main` |
| HEAD del documento R1 | `53cfd6f28a169f2e71edf557e66b7c4f5ea17a1d` |
| Padre de R1 | `f17246e0abf5878f3ad6f2df84d30bb76a351542` (Fase B) |
| Abuelo de R1 | `e83ad182483c9ec2eb446b757ee53ea8496d31a2` (Fase A) |
| Remoto | `origin/main` = `53cfd6f…`, alineado con el HEAD local (verificado por la auditoría) |
| Árbol de trabajo | Limpio (`git status --porcelain` sin salida) durante la auditoría |
| Publicación de R1 | El propietario realizó personalmente el commit y push del documento; no se atribuye la operación a terceros |
| DEC-01 a DEC-08 | **APPROVED**, sin modificaciones; no se reabren ni reinterpretan |

---

## 3. R1 — Estado formal de Fase B

### 3.1 Registro de aceptación

| Elemento | Registro |
|---|---|
| Commit auditado | `f17246e0…`, hijo directo de `e83ad182…` |
| Alcance | 6 archivos: `pyproject.toml`, `src/tradingai/ml/provenance.py`, `tests/test_provenance_v4_dispatch.py` (modificados); `src/tradingai/ml/provenance_v4.py`, `src/tradingai/schemas/manifest_v4.json`, `tests/test_provenance_v4_schema.py` (nuevos) |
| Dictamen | **ACCEPTED WITH FINDINGS** |
| CP-B | CP-B-01 a CP-B-10: **PASS** |
| Hallazgos Critical / High / Medium | **Ninguno** |
| Hallazgos restantes | F-1 a F-6: informativos, LOW o fuera de alcance; ninguno bloquea CP-B |

### 3.2 Pruebas reproducidas por la auditoría

| Comando | Resultado |
|---|---|
| `python -m pytest tests/test_provenance_v4_schema.py -q` | `25 passed, 1 warning in 4.13s` |
| `python -m pytest tests/test_provenance_v4_dispatch.py -q` | `29 passed, 1 warning in 4.73s` |
| `python -m pytest tests/test_provenance.py -q` | `116 passed, 1 warning in 4.41s` |
| `python -m pytest -q` | `495 passed, 1 warning in 11.29s` |
| `python -m ruff check <4 archivos>` | 5 `SIM102` preexistentes en el validador v3; 0 diagnósticos nuevos |
| `git diff --check` | exit `0` |
| Wheel en copia temporal | contiene `manifest_v3.json`, `manifest_v4.json` y `provenance_v4.py` |

### 3.3 Distinción esencial

| Concepto | Estado |
|---|---|
| Aceptación de CP-B | **[ACEPTADO POR AUDITORÍA]**: sí, con hallazgos no bloqueantes. |
| Autorización para Fase C | **NO concedida**. Fase C permanece **BLOQUEADA** hasta autorización explícita del propietario. |
| Implementación de JCS/fingerprint, gaps/purga, eventos o sidecars | No realizada; pertenece a Fases C–F. |

**Estado R1: CLOSED.**

---

## 4. R2 — Discrepancia temporal del estado Git

### 4.1 Hechos registrados

1. El informe inicial de implementación describía el estado previo al commit: cambios locales, HEAD en `e83ad182…`, sin commit ni push.
2. Con posterioridad, el propietario del proyecto realizó personalmente el commit y push, generando `f17246e0…`.
3. La auditoría independiente verificó el commit publicado, su padre (`e83ad182…`) y el contenido exacto de los seis archivos del alcance.
4. El contenido publicado coincide con el alcance auditado; no hay cambios adicionales ocultos y el árbol está limpio.
5. Posteriormente, el propietario publicó el presente documento R1 mediante el commit `53cfd6f…`, hijo de `f17246e…`. La auditoría de R1 verificó HEAD local y remoto alineados en `53cfd6f…` y árbol limpio. Este hecho se registra como continuación de la misma secuencia temporal, no como una operación ajena.

### 4.2 Resolución

**[HECHO VERIFICADO]** No existe incidencia de autorización: el commit y push de Fase B y la publicación posterior de R1 fueron realizados por el propietario del proyecto. No se atribuye la operación a terceros ni se especula sobre su ejecución. La diferencia es únicamente temporal entre el informe y el estado final.

**Clasificación: aclaración documental cerrada. Estado R2: CLOSED.**

---

## 5. R3 — V4-U06: correspondencia entre `class_order` y `classes`

### 5.1 Normativa aplicable

| Fuente | Texto relevante |
|---|---|
| `docs/aud04b_model_provenance_v4_design.md` §5.3 | "`target.classes` y `target.class_order` son arrays no vacíos de enteros JSON, sin duplicados" y "**`class_order` debe ser una permutación exacta de `classes`**". También fija la normalización de `1.0` a `1` y la exclusión de booleanos. |
| §9.2 | Incluye `target.classes` y `target.class_order` en la allowlist del fingerprint; la identidad del run depende de ambos. |
| §6.1 | La preimagen de `calibration_input_sha256` usa las columnas en `class_order`. |
| `docs/aud04b_model_provenance_v3_design.md` §5.6 | `class_counts` se declara "en el orden de `class_order`". |
| v3 §6.1 / I14 y §13.4 / V06 | "El orden de clases es único y consistente"; `class_order` consistente en target, modelos, calibrador y métricas. |
| `docs/aud04b_model_provenance_v4_implementation_plan_r1.md` §6.1 | V4-U06 aparece con fase **B** y estado "Parcial: ... sin permutación ni normalización explícita". |

### 5.2 Interpretación normativa

La correspondencia exacta **no es opcional** ni puede sustituirse por la unicidad individual de cada array. Es una relación semántica entre dos campos:

- `classes` define el conjunto de etiquetas permitidas.
- `class_order` define el orden posicional de columnas de probabilidad y de conteos.
- Ambos intervienen en `run_fingerprint`, en `calibration_input_sha256` y en la alineación de `class_counts`, por lo que una discrepancia cambia la identidad del run y la interpretación de las probabilidades.

JSON Schema 2020-12 puede exigir tipo, `minItems` y `uniqueItems` (ya implementado), pero **no puede expresar la permutación entre dos arrays**. Por tanto, la comprobación debe residir en el validador semántico, no en el schema.

### 5.3 Decisión recomendada (no aprobada)

**Autoridad normativa (AUD-F-3):** la regla de permutación exacta aparece en `docs/aud04b_model_provenance_v4_design.md` §5.3, documento que se identifica a sí mismo como "propuesta documental para revisión humana; no implementada ni aprobada". La regla **no forma parte de DEC-01 a DEC-08**: el registro de aprobación R2 limita el estado `APPROVED` a esas ocho decisiones y conserva las etiquetas de propuesta del diseño como historial documental. El plan R1.1 contempla V4-U06 en su §6.1 con fase B, pero el propio plan declara que no autoriza implementación. En consecuencia, la corrección en `validate_manifest_v4` **requiere autorización explícita del propietario**, porque Fase B ya fue auditada y aceptada. No se afirma que la regla tenga estatus de DEC aprobada.

**[RECOMENDACIÓN TÉCNICA]**

1. **Schema:** mantener `minItems: 1` y `uniqueItems: true` en `classes` y `class_order`. No inventar restricciones adicionales en el schema.
2. **Validador semántico v4:** incorporar en `validate_manifest_v4` la comprobación de que, tras la normalización documentada en §5.3, `class_order` es una permutación exacta de `classes`. Rechazar booleanos, `null`, strings, números fraccionarios, NaN/infinitos y duplicados; `1.0` y `1` se tratan como el mismo valor.
3. **Fase responsable:** Fase B (es donde el plan sitúa V4-U06). Como Fase B ya fue aceptada, cualquier cambio requiere **[PENDIENTE DE APROBACIÓN]** del propietario.
4. **No se requiere una DEC nueva**: la regla ya está en el diseño v4 §5.3 y en V4-U06 del plan; no por ello tiene estatus de DEC aprobada. La autorización exigida es la del propietario para modificar una fase cerrada y ajustar el plan R1.1.

### 5.4 Criterio de aceptación verificable

- `validate_manifest_v4` acepta `classes=[0,1,2]`, `class_order=[2,0,1]`.
- Rechaza `classes=[0,1,2]`, `class_order=[0,1,9]` y `class_order=[0,0,2]`.
- Rechaza tipos no enteros y valores fuera del rango seguro de JCS.
- El error identifica la ruta `$.target.class_order` y no depende del orden de iteración de los diccionarios.
- Prueba asociada: extensión de V4-U06 con casos válidos, inválidos y límite `1.0` vs `1`.

**Estado R3: PENDING APPROVAL.**

---

## 6. R4 — Flags derivados

### 6.1 Principio general

**[REQUISITO DE DISEÑO / CRITERIO DE PLAN]** La spec v4 §9.2 declara `label_purge_satisfied`, los tres `leakage_checks` y `test_evaluated_once` como resultados derivados o de evaluación, **excluidos del fingerprint** y que **deben ser `true`** para admitir el manifiesto. Este contenido procede de un documento de diseño rotulado como propuesta no aprobada y del plan R1.1; **no ha sido aprobado mediante DEC-01 a DEC-08**. La exclusión de resultados derivados del fingerprint es coherente con DEC-06 (allowlist y exclusión de resultados derivados), y la condición de purga por fuente que puede respaldar `label_purge_satisfied`/`purge_satisfied` está amparada por DEC-08; ninguna de esas DEC aprueba por sí sola el valor `true` de los tres flags. Validar el tipo booleano (Fase B) **no demuestra** que el hecho ocurrió. La demostración pertenece a la verificación de relaciones con datos declarados (Fase D) o a la verificación de ejecución (S6).

No se debe convertir automáticamente ningún flag en `true` ni aceptar una afirmación sin evidencia.

### 6.2 `validation.purge.label_purge_satisfied`

| Aspecto | Resolución |
|---|---|
| Naturaleza | **Derivado**. v3 §5.6: "Calculado, no declarado a mano". |
| Componente que lo determina | Cálculo de purga de Fase D sobre límites declarados: `gap_source >= max(H,E)` en todas las fronteras reales, con `H = target.horizon_bars` y `E = validation.purge.embargo_rows` interpretado como barras de fuente. |
| Evidencia que lo hace verdadero | Recálculo determinista de gaps y coherencia con `label_horizon_bars`; no basta el digest ni la declaración. |
| Cuándo rechazar | Valor `false`; valor `true` con límites que violen la fórmula, gap negativo o frontera omitida. |
| Fase responsable | D (estructura/relaciones declaradas). Evidencia efectiva sobre datos originales: verificador posterior, fuera de S1. |
| Pruebas | Casos límite `gap_source == max(H,E)`, mayor y menor; ejemplo con filas descartadas; bandera `false`. |

**Nota AUD-F-4 — distinción pendiente:** `label_purge_satisfied` y `leakage_checks.purge_satisfied` se relacionan con la condición de purga, pero el diseño v3 §5.6 les asigna naturaleza distinta: el primero está "calculado, no declarado a mano" y el segundo es "verificado por el validador". Este documento **no asume que sean intercambiables ni que tengan necesariamente idéntico alcance**. Fase D deberá determinar: (1) si ambos campos son verificaciones redundantes; (2) si uno es un resultado agregado y el otro una comprobación específica; (3) qué componente calcula cada uno; (4) cómo se evita una contradicción entre ambos; y (5) qué pruebas demostrarán su consistencia. Si esa distinción exige cambiar el contrato normativo, queda pendiente de una decisión aprobada; no se inventa aquí una interpretación definitiva.

### 6.3 `validation.leakage_checks.disjoint` y `.purge_satisfied`

| Aspecto | Resolución |
|---|---|
| Naturaleza | **Derivados / verificados por el validador** (v3 §5.6) y resultados derivados en v4 §9.2. |
| Componente que los determina | Fase D: orden y no solapamiento de intervalos declarados para `disjoint`; comprobación de purga para `purge_satisfied`, sin presumir que sea idéntica a `label_purge_satisfied` (véase la nota AUD-F-4 en §6.2). |
| Evidencia | Límites `row_start/row_end` y `source_position_start/end` declarados, con aritmética reproducible. |
| Cuándo rechazar | Valor `false`; valor `true` con solapamiento declarado, orden invertido o purga insuficiente. |
| Fase responsable | D. La correspondencia con el dataset original queda para el verificador posterior (R1.2 del plan). |
| Pruebas | Particiones solapadas, desordenadas, purga suficiente/insuficiente, banderas incoherentes. |

### 6.4 `validation.leakage_checks.labels_within_partition`

| Aspecto | Resolución |
|---|---|
| Naturaleza | **Derivado con evidencia de datos**: afirma que las etiquetas pertenecen a su partición. S1, con solo límites e `index_sha256`, **no puede demostrarlo** (v4 §4.3 y plan §3.11). |
| Componente que lo determina | Verificación estructural de la declaración en Fase D; demostración efectiva únicamente con dataset/labels y reglas de filtrado, en verificador posterior. |
| Evidencia | Preimagen de `index_sha256` reconstruida desde los datos originales; no basta el digest bien formado. |
| Cuándo rechazar | Valor `false`; o valor `true` presentado como "verificado por S1" sin la entrada de datos necesaria. |
| Fase responsable | D para la declaración; fuera de A–G para la demostración efectiva. |
| Pruebas | Caso con secuencia entregada vs caso sin secuencia; assertions de que ningún mensaje afirme verificación de datos. |

### 6.5 `validation.evaluation.test_evaluated_once`

| Aspecto | Resolución |
|---|---|
| Naturaleza | **Evidencia de ejecución del protocolo**, no un valor puramente derivado de los límites. v3 §5.6: "Debe ser `true` para sellar"; I13 exige "`test_evaluated_once` + revisión del verificador"; V04 exige que el informe de selección no use test. v4 §9.2: "debe ser `true` para admitir el manifiesto". |
| Componente que lo determina | Protocolo de evaluación y verificador independiente (S6 en el diseño v3, fuera de A–G). S1 puede exigir el valor `true`, pero no puede certificar por sí solo que la evaluación ocurrió una sola vez. |
| Evidencia | Informe que contenga `model_id`, `manifest_sha256`, métricas y la afirmación de evaluación de test única, con firma/revisión externa (v3 §8.6). |
| Cuándo rechazar | Valor `false`; valor `true` sin informe cuando el contexto lo exige; uso de test en selección de hiperparámetros o calibración. |
| Fase responsable | Admisión estructural en B/D; verificación de evidencia en S6, que requiere autorización separada. |
| Pruebas | Informe ausente/alterado, bandera `false`, reutilización de test, coherencia `model_id`/`manifest_sha256`. |

### 6.6 Resumen de responsabilidades

| Flag | Tipo | Fase estructural | Demostración efectiva |
|---|---|---|---|
| `label_purge_satisfied` | Derivado | D | Verificador de purga con datos |
| `leakage_checks.disjoint` | Derivado | D | Verificador de datos |
| `leakage_checks.purge_satisfied` | Derivado | D | Verificador de datos |
| `leakage_checks.labels_within_partition` | Derivado con datos | D (solo declaración) | Verificador con labels/dataset |
| `test_evaluated_once` | Evidencia de ejecución | B/D (valor `true`) | S6 / verificador independiente |

Nota: la distinción entre `label_purge_satisfied` y `leakage_checks.purge_satisfied` permanece pendiente de resolución técnica en Fase D (AUD-F-4).

**Estado R4: DEFERRED.** La parte de evidencia de ejecución queda fuera de A–G y no se activa sin autorización.

---

## 7. R5 — Otros hallazgos informativos

| Hallazgo | Clasificación | Resolución documental |
|---|---|---|
| **F-4** — `source_position_start < source_position_end` no comprobado en B | **DEFERRED** | El plan R1.1 Fase B ítem 5 asigna explícitamente la semiabertura y el orden a Fase D. No es un defecto de B. Criterio: rechazar límites invertidos/negativos/solapados cuando se validen las relaciones declaradas. |
| **F-5** — mensaje de error para entradas no-dict sin prefijo de ruta | **DEFERRED** (mejora no bloqueante) | Afecta a `validate_manifest_v4` y al wrapper de Fase A. Requiere autorización para cambiar una fase ya aceptada. Criterio: todo error de validación de manifiesto incluya prefijo de ruta `$`, conservando los mensajes históricos de v3. |
| **F-6a** — `KeyError: 'role'` con `artifacts:[{}]` | **NOT IN SCOPE** | Problema histórico del validador v3, preexistente a Fase B y reproducido en la auditoría. No se corrige aquí; requiere autorización separada. |
| **F-6b** — cinco `SIM102` en `provenance.py` | **NOT IN SCOPE** | Preexistentes, confirmados contra el commit base. No se modifica el validador histórico. |
| **F-6c** — warning `anyio CallSpec2` | **NOT IN SCOPE** | Originado en `site-packages`, ajeno al código del proyecto. |

No se introducen correcciones de código.

---

## 8. Matriz de trazabilidad

| Hallazgo | Decisión | Fase responsable | Criterio de aceptación | Estado |
|---|---|---|---|---|
| R1 — Estado de Fase B | Registrar `ACCEPTED WITH FINDINGS`, CP-B-01…10 PASS, sin Critical/High/Medium; separar aceptación de autorización | Cierre de B (auditoría) | Dictamen e evidencia reproducida en §3 | **CLOSED** |
| R2 — Discrepancia Git | Aclaración documental: commit/push del propietario; contenido coincide con el alcance | Cierre de B (auditoría) | §4; sin incidencia de autorización | **CLOSED** |
| R3 — V4-U06 | Exigir permutación exacta en el validador semántico v4; mantener límites en schema | B (modificación de fase ya aceptada) | §5.4: permutación válida/inválida, tipos y rango | **PENDING APPROVAL** |
| R4a — `label_purge_satisfied`, `disjoint`, `purge_satisfied` | Veracidad derivada de relaciones declaradas; no forzar `true` | D | §6.2–6.3: gaps, solapamiento, banderas coherentes | **DEFERRED** |
| R4b — `labels_within_partition` | Declaración en D; evidencia efectiva solo con datos | D + verificador posterior | §6.4: sin afirmación de S1 sobre datos no entregados | **DEFERRED** |
| R4c — `test_evaluated_once` | Valor `true` para admisión; evidencia de ejecución en S6 | B/D + S6 | §6.5: informe con `model_id`, `manifest_sha256`, métricas y evaluación única | **DEFERRED** |
| F-4 — semiabertura de posiciones | Ya asignada por el plan | D | Rechazo de límites invertidos/negativos/solapados | **DEFERRED** |
| F-5 — prefijo de ruta en errores no-dict | Mejora no bloqueante | B/G (tras autorización) | Todos los errores con prefijo `$`; mensajes v3 intactos | **DEFERRED** |
| F-6 — históricos | No corregir en B | Fuera de A–G | Sin cambios en el validador histórico | **NOT IN SCOPE** |
| AUD-F-1 | Etiquetas normativas corregidas: `[APROBADO]` restringido a DEC-01…08; requisitos de diseño rotulados por separado | Corrección documental R1.1 | §6.1 y convención de calificación | **CLOSED** |
| AUD-F-2 | Estado Git actualizado: R1 publicado en `53cfd6f…`; HEAD/remoto alineados; sin atribución a terceros | Corrección documental R1.1 | §2, §4.1 y §11.8 | **CLOSED** |
| AUD-F-3 | Autoridad normativa de V4-U06 aclarada: diseño no aprobado, no es DEC; requiere autorización del propietario | Corrección documental R1.1 | §5.3 y §5.4; V4-U06 sigue `PENDING APPROVAL` | **CLOSED** |
| AUD-F-4 | Distinción documentada entre los dos flags de purga; resolución semántica diferida a D | D | §6.2/§6.3 y nota en §6.6; definir redundancia, alcance, componente y pruebas | **DEFERRED** |

`CLOSED` se refiere únicamente a la corrección documental. No cierra la implementación de V4-U06 ni la resolución técnica de la duplicidad de flags.

---

## 9. Posibles modificaciones futuras al plan R1.1 (no aplicadas)

**[RECOMENDACIÓN TÉCNICA — PENDIENTE DE APROBACIÓN]**

1. **§5 Fase B, ítems 2 y 5:** añadir explícitamente la comprobación semántica de permutación `class_order` ↔ `classes` y su prueba negativa. Hoy el ítem 2 enumera patrones y tipos, no relaciones entre arrays.
2. **§6.1 fila V4-U06:** sustituir "Parcial: ... sin permutación" por un criterio verificable de permutación con fase B, o reasignar explícitamente a D. Requiere decisión del propietario porque V4-U06 figura hoy como B.
3. **§5 Fase B / Fase D:** precisar que los flags derivados se comprueban en D y que `test_evaluated_once` requiere evidencia de S6, fuera de A–G.
4. **§9 Aplazamientos:** registrar la verificación de evidencia de `test_evaluated_once` y de `labels_within_partition` como capacidades posteriores con interfaz y criterios propios.

**No se modifica el plan en esta tarea.** Cualquier cambio debe ser autorizado por el propietario.

---

## 10. Verificación de coherencia

| Comprobación | Resultado |
|---|---|
| DEC-01 a DEC-08 no reabiertas ni modificadas | Confirmado: siguen `APPROVED` en el documento de aprobación |
| Decisiones propuestas sin contradecir DEC aprobadas | Confirmado: R3/R4 desarrollan requisitos ya presentes en la spec; no crean DEC nuevas |
| Aceptación de CP-B no presentada como autorización de Fase C | Confirmado: Fase C sigue BLOQUEADA |
| Recomendaciones no presentadas como decisiones aprobadas | Confirmado: marcadas `[RECOMENDACIÓN TÉCNICA]` / `[PENDIENTE DE APROBACIÓN]` |
| Nombres de fases y V4-Uxx correctos | Confirmado contra plan R1.1 y diseño v4 |
| Archivos modificados | Solo el presente documento; el commit de publicación `53cfd6f…` contiene únicamente `docs/r13_decision_resolution_r1.md` |

---

## 11. Informe final — R13-DECISION-RESOLUTION-R1

1. **Archivo creado:** `docs/r13_decision_resolution_r1.md`.
2. **Hallazgos resueltos y pendientes:** R1 y R2 **CLOSED**; R3 **PENDING APPROVAL**; R4 **DEFERRED**; F-4 y F-5 **DEFERRED**; F-6 **NOT IN SCOPE**.
3. **Decisión recomendada para V4-U06:** exigir la permutación exacta en el validador semántico v4, manteniendo `minItems`/`uniqueItems` en el schema; fase B, con autorización previa por tratarse de una fase ya aceptada. No requiere una DEC nueva.
4. **Tratamiento recomendado de los flags:** ninguno se fuerza a `true`; veracidad derivada en Fase D para purga/leakage; `labels_within_partition` solo afirmable con datos por verificador posterior; `test_evaluated_once` exige informe de evaluación única verificado en S6.
5. **Matriz de trazabilidad:** sección 8.
6. **Modificaciones futuras al plan R1.1:** sección 9, todas pendientes de autorización.
7. **Confirmación:** no se modificó código, schema, tests, fixtures, dependencias, modelos ni datasets; no se leyeron ni procesaron los Parquet protegidos.
8. **Confirmación Git:** el propietario publicó el documento R1 mediante el commit `53cfd6f28a169f2e71edf557e66b7c4f5ea17a1d` y el correspondiente push; la auditoría verificó HEAD local y remoto alineados en `53cfd6f…` y árbol limpio. La redacción original de este apartado describía el estado anterior a esa publicación y ha sido corregida en R1.1.

**Clasificación: COMPLETADO.** La resolución distingue lo aprobado, lo aceptado por auditoría, lo recomendado técnicamente y lo que requiere aprobación del propietario. **Fase C permanece BLOQUEADA hasta autorización explícita.**

**Fin de R13-DECISION-RESOLUTION-R1.**
