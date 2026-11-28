# R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R2 — Análisis y propuesta de resolución de decisiones pendientes

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Documento de origen:** `docs/r13_oracle_artifacts_decision_resolution_r1.md`, conservado íntegramente como registro histórico.
**Auditoría incorporada:** `R13-AUDIT-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R1 — ACCEPTED WITH FINDINGS` (AUD-DEC-RES-R1-01 a R1-04).
**Naturaleza:** análisis documental y propuesta técnica. **No** constituye aprobación del propietario, autorización de materialización ni autorización de implementación.
**Estado:** propuesta. Las seis decisiones analizadas permanecen pendientes.

---

## 1. Propósito y alcance

Analizar las seis decisiones pendientes registradas en `docs/r13_oracle_artifacts_materialization_plan_r2.md` §10 (plan R2, aprobado documentalmente, SHA-256 `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0`, Git `e37dfdae0663502e89cb522ca8605eb2791c828e`), y presentar alternativas, recomendación técnica razonada, consecuencias y prerrequisitos.

Se respeta íntegramente el plan R2, la especificación R2 aprobada, el diseño R9 aprobado y sus auditorías independientes `ACCEPTED`. No se materializa ningún artefacto, no se ejecuta el oracle y no se introducen dependencias.

Esta revisión R2 incorpora cuatro precisiones de auditoría, sin resolver ninguna decisión: ubicación del ejecutable ORACLE-ART-02 (AUD-DEC-RES-R1-01), separación entre preimagen normativa y evidencia derivada (R1-02), tratamiento de correcciones sin impacto normativo (R1-03) y secuencia explícita de resolución (R1-04).

### 1.1 Convención de calificación

Basada en `docs/r13_decision_resolution_r1.md` §Convención de calificación:

| Marca | Significado en este documento |
|---|---|
| **[RECOMENDACIÓN TÉCNICA]** | Propuesta del análisis; **no** es decisión aprobada |
| **[PENDIENTE DE APROBACIÓN]** | Requiere decisión o designación expresa del propietario |
| **[CONVENCIÓN EXISTENTE]** | Práctica verificable del repositorio, citada como evidencia |
| **[REQUISITO NORMATIVO]** | Contenido de R9, especificación R2 o plan R2 |

Ninguna decisión se marca `CLOSED` ni `APPROVED`.

---

## 2. Convenciones existentes del repositorio

| Convención | Evidencia | Uso en el análisis |
|---|---|---|
| Documentos `r13_*_rN.md` con sufijo de revisión | `docs/r13_phase_c_design_r*.md`, `docs/r13_oracle_artifacts_*_r*.md` | Numeración y conservación de revisiones históricas |
| Vocabulario `CLOSED / DEFERRED / PENDING APPROVAL / NOT IN SCOPE` | `docs/r13_decision_resolution_r1.md` §Convención de estado | Clasificación de las seis decisiones como `PENDING APPROVAL` o diferidas a decisión autorizada |
| Registro DEC con estado `APPROVED` y sección de origen | `docs/aud04b_model_provenance_v4_approval_r1.md` tabla DEC-01…09 | No reabrir decisiones aprobadas; toda resolución nueva debe registrarse por separado |
| Identidad del aprobador como «propietario del proyecto», sin nombre | `docs/r13_owner_design_approval_r1.md`, `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | No inventar nombres ni firmas |
| Schema v4 como recurso de paquete | `importlib.resources.read_text('tradingai.schemas', …)` en `provenance_v4.py`; `src/tradingai/schemas/manifest_v4.json` | Alternativa de ubicación para artefactos de solo lectura |
| JCS mediante `rfc8785.dumps` | `provenance.py::jcs_canonical` y `jcs_bytes`; `pyproject.toml` declara `rfc8785>=0.1.4` | Sin serializadores alternativos ni nuevas dependencias |
| SHA-256 hexadecimal minúsculo de 64 caracteres | `hashlib.sha256(...).hexdigest()` en `provenance.py`; patrón `^[0-9a-f]{64}$` en el schema | Formato del checksum de ORACLE-ART-03 |
| Pruebas `test_provenance_v4_*.py`, `pytest` con `pythonpath=["src"]` | `tests/`, `pyproject.toml` | Alternativa de verificación en CI sin tocar producción |
| Aislamiento de v3 y dispatch explícito | `provenance.py`, `provenance_v4.py::validate_manifest_v4`, DEC-05 | El verificador no debe convertirse en fuente normativa ni modificar v3 |

No se encontró convención existente que fije formato de `rule_id`, ubicación de artefactos, identidad de revisor, formato de evidencias ni convención de versiones del oracle: por eso se tratan como decisiones pendientes.

---

## 3. Análisis de las seis decisiones

### 3.1 Decisión 1 — Formato estable de identificadores `rule_id`

**Definición del problema.** R9 §5.8.1 exige que cada una de las diez campos del oracle incluya `rule_id`, que identifica la fila correspondiente de §9.2, pero no prescribe su sintaxis. Sin formato estable, la trazabilidad entre transcripción, revisión y evidencia puede divergir.

**Requisitos normativos.** R2 §4.1: `rule_id` referencia la fila de §9.2; §4.5: cada fila de cobertura lleva correspondencia con el oracle; §8.1: formato pendiente, a proponer en futura tarea autorizada y revisar con la transcripción. Plan R2 §10: bloquea la trazabilidad completa de ORACLE-ART-01.

**Alternativas.**

| Alternativa | Ventajas | Riesgos |
|---|---|---|
| A. Identificador secuencial por fila de §9.2, p. ej. `R9-9.2-NN` | Estable, legible, fácil de cotejar con el documento normativo; no depende de texto | Requiere asociar cada ruta expandida a la fila correcta; una reordenación normativa exige nueva versión |
| B. Identificador semántico derivado del contenido de la regla | Autoexplicativo | Fragilidad ante cambios de redacción; mayor riesgo de ambigüedad |
| C. Hash del texto normalizado de la regla | Determinista y sensible a cambios | Poco legible para revisión humana; podría confundirse con checksum |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA].** Alternativa A, con asignación explícita durante la transcripción, tabla de correspondencia `ruta expandida → rule_id → fila §9.2` y revisión semántica. El formato concreto debe aprobarse antes de ORACLE-ART-01.

**Compatibilidad.** Compatible con R9 §5.8.1 y R2 §4.1/§8.1; no amplía el vocabulario de condiciones ni cambia los siete artefactos.

**Impacto.** Reproducibilidad: alta si la tabla de correspondencia se conserva. Trazabilidad: directa a §9.2. Independencia: no depende del código productivo. Fail-closed: `rule_id` ausente o duplicado debe rechazar la transcripción.

**Criterio de aceptación verificable.** Cada una de las 139 rutas expandidas tiene exactamente un `rule_id`; cada `rule_id` referencia una fila existente de §9.2; la tabla de correspondencia está incluida en la evidencia de ORACLE-ART-01 y revisada en ORACLE-ART-04.

**Intervención humana.** Sí: **[PENDIENTE DE APROBACIÓN]**; el propietario o autoridad designada aprueba el formato antes de generar ORACLE-ART-01.

---

### 3.2 Decisión 2 — Ubicación física de artefactos ejecutables y evidencias

**Definición del problema.** R2 §8.2 deja abierta la ubicación física; el plan R2 §6.2 propone tres alternativas sin adoptar ninguna. La ubicación debe fijarse antes de G2/G4.

**Requisitos normativos.** Plan R2 §6.1: ninguna sobrescritura de versiones revisadas; conservar versiones anteriores; identificar artefactos incompletos o rechazados. R9 §5.8.5: el checksum se guarda «junto con el oracle en el módulo de pruebas», sin importarlo en producción.

**Convenciones existentes.** `manifest_v4.json` se distribuye como recurso de paquete; los tests viven en `tests/`; los registros de aprobación y decisiones viven en `docs/`.

**Alternativas.** Las tres del plan R2 §6.2:

1. Directorio de evidencias versionado en el repositorio.
2. Artefacto de Release con control de acceso.
3. Almacenamiento externo con referencia inmutable en el repositorio.

| Alternativa | Ventajas | Riesgos |
|---|---|---|
| 1 | Trazabilidad Git nativa; revisión por diff; sin nueva infraestructura | Aumenta tamaño del repositorio; exige política clara de inmutabilidad |
| 2 | Control de acceso y separación del código | Requiere proceso de Release; riesgo de dependencia de plataforma externa |
| 3 | Evidencia inmutable fuera del repositorio | Requiere disponibilidad a largo plazo; referencia debe verificarse |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA].** Alternativa 1 para evidencias documentales y transcripción; alternativa 3 solo si se requiere evidencia de gran tamaño, con referencia inmutable verificable. Cualquier elección debe registrarse formalmente antes de ORACLE-ART-01. No se adopta aquí ninguna.

**Compatibilidad.** Compatible con R9 y R2 siempre que se respeten inmutabilidad, procedencia y separación producción/CI. No se modifica dependencias.

**Impacto.** Reproducibilidad: depende de que la ubicación permita recuperar entradas exactas. Trazabilidad: requiere referencia del artefacto a la fuente. Independencia: la ubicación no debe permitir que producción importe el oracle. Fail-closed: ausencia de ubicación definida bloquea G2.

**Criterio de aceptación verificable.** Decisión registrada antes de ORACLE-ART-01; ruta o referencia inmutable documentada; política de no sobrescritura verificable; evidencia recuperable y con hash cuando corresponda.

**Intervención humana.** Sí: **[PENDIENTE DE APROBACIÓN]**; propietario o autoridad designada.

**Precisión AUD-DEC-RES-R1-01 — ORACLE-ART-02.** La recomendación de ubicación se completa para el ejecutable, sin seleccionar una ubicación definitiva ni modificar el plan R2. Se preserva la distinción entre **transcripción normativa** (ORACLE-ART-01), **ejecutable** (ORACLE-ART-02) y **evidencias** (ORACLE-ART-03…07):

| Criterio | Requisito propuesto para el ejecutable |
|---|---|
| Ubicación | Cuerpo separado de la transcripción y de las evidencias, dentro del ámbito de verificación de CI/auditoría; nunca en el camino productivo |
| Versionado | Identificador de versión propio, ligado a la versión de la transcripción que verifica y registrado en cada salida |
| Inmutabilidad | Ninguna versión revisada se sobrescribe; una corrección produce nueva versión o registro de procedencia conforme a D5 |
| Procedencia | Registro de entradas, generador funcional, fecha real, versión y checksum de la transcripción de origen; sin importaciones productivas |
| Referencias | Cada salida referencia al ejecutable por versión y a la transcripción por versión/checksum; la referencia debe ser verificable desde la matriz de aceptación |

Alternativas específicas para el ejecutable, con sus riesgos:

| Alternativa | Ventaja | Riesgo |
|---|---|---|
| i. Subárea diferenciada del directorio de evidencias versionado | Unifica procedencia e inmutabilidad | Mezcla artefactos de naturalezas distintas si no se separan claramente |
| ii. Módulo de verificación bajo `tests/` con recursos de solo lectura | Coincide con D6; evita importaciones productivas | Exige que CI lo ejecute fuera del camino productivo y que su salida se versione por separado |
| iii. Artefacto externo con referencia inmutable | Alta separación del repositorio | Dependencia de disponibilidad externa y verificación de la referencia |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA]:** alternativa ii para el verificador en CI, con la copia versionada de su salida en el directorio de evidencias (alternativa i) y conservación de procedencia. La decisión formal sobre la ubicación permanece **[PENDIENTE DE APROBACIÓN]**.

---

### 3.3 Decisión 3 — Identidad del revisor humano independiente

**Definición del problema.** R2 §4.4 exige revisión semántica real por revisor distinto del generador; §8.3 deja pendiente la identidad funcional. No se debe inventar persona, firma ni aprobación.

**Requisitos normativos.** R9 §5.8.1: la revisión humana no se sustituye por checksum. R2 §4.4: identidad funcional, independencia, versión y checksum revisados, alcance, casos, hallazgos, resolución, dictamen y fecha. Plan R2 §7: el revisor no es el generador.

**Alternativas.**

| Alternativa | Ventajas | Riesgos |
|---|---|---|
| A. Designación nominal por el propietario | Alta trazabilidad personal | Requiere dato real; no puede inventarse |
| B. Designación funcional por rol, con registro de la persona real al ejecutar | Compatible con el registro de aprobaciones existente; no inventa identidad | Requiere control de que el rol sea efectivamente independiente |
| C. Revisor externo | Mayor independencia | Requiere contratación/acceso; fuera de alcance documental |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA].** Alternativa B: el propietario designa un rol funcional independiente, y la identidad real se registra en ORACLE-ART-04 en el momento de la revisión. El generador del oracle no puede actuar como su propio revisor. No se propone nombre alguno.

**Compatibilidad.** Coherente con los registros de aprobación existentes, que identifican al aprobador como «propietario del proyecto» sin datos personales inventados.

**Impacto.** Reproducibilidad: la identidad funcional permite repetir la revisión. Trazabilidad: alta. Independencia: exigible y verificable. Fail-closed: revisión sin independencia declarada rechaza ORACLE-ART-04.

**Criterio de aceptación verificable.** ORACLE-ART-04 contiene rol funcional designado, identidad funcional verificable real, declaración de independencia, versión/checksum revisados, casos, hallazgos resueltos, dictamen y fecha; el revisor no es el generador.

**Intervención humana.** Sí: **[PENDIENTE DE APROBACIÓN]**; designación real del propietario.

---

### 3.4 Decisión 4 — Formato de las evidencias de ejecución

**Definición del problema.** R2 §8.4 no fija formato para las salidas de las verificaciones. Sin formato común, la evidencia puede no ser reproducible ni auditable.

**Requisitos normativos.** Plan R2 §5.1: evidencia por verificación; §5.2: distinción entre documental, automática, revisión humana y auditoría; R2 §4.5/§4.6: salidas deterministas, ordenadas y deduplicadas.

**Convenciones existentes.** JCS y SHA-256 hex para datos canónicos; archivos bajo `docs/` para registros; `tests/` para salidas de prueba; UTF-8; patrón hex minúsculo de 64 caracteres.

**Alternativas.**

| Alternativa | Ventajas | Riesgos |
|---|---|---|
| A. Texto UTF-8 determinista con encabezado de versión, entradas, salidas y fecha real | Legible, sin dependencias, fácil de auditar | Menos estructurado para procesamiento automático |
| B. JSON canónico JCS con esquema de evidencia | Machine-readable y reproducible | Requiere acuerdo de campos; rigidez ante cambios |
| C. Formato nativo del tool de CI | Integración sencilla | Dependencia de plataforma y posible pérdida de independencia |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA].** Alternativa A como formato base, con campos obligatorios: versión de la fuente, versión del artefacto, entradas, salida, código de error si aplica, fecha real y referencia al artefacto. Si se requiere procesamiento automático, derivar un JSON JCS desde el mismo contenido, sin introducir dependencias.

**Precisión AUD-DEC-RES-R1-02 — preimagen frente a evidencia derivada.** La preimagen de ORACLE-ART-03 sigue siendo **exclusivamente** la estructura normativa `{"version": ..., "entries": [...]}` canonicalizada conforme a R9 §5.8.5. El JSON JCS que pueda derivarse de las evidencias es una **representación auxiliar y no normativa**: no sustituye, amplía ni modifica la preimagen del SHA-256. No se exige un checksum adicional del JSON derivado ni del ejecutable ORACLE-ART-02. No se introduce un octavo artefacto; el conjunto permanece en siete.

**Compatibilidad.** Compatible con R9 §5.8.2 (errores `list[str]` ordenados y deduplicados) y con R2 §4.5/§4.6. No cambia los siete artefactos.

**Impacto.** Reproducibilidad: alta si se conservan entradas y versión. Trazabilidad: referencia explícita al artefacto. Independencia: el formato no debe depender del generador. Fail-closed: evidencia incompleta impide aceptación.

**Criterio de aceptación verificable.** Toda salida de verificación contiene los campos obligatorios, es reproducible con las mismas entradas y está referenciada desde la matriz de aceptación correspondiente.

**Intervención humana.** Parcial: **[PENDIENTE DE APROBACIÓN]** por autoridad técnica autorizada; si cambia el alcance, decisión del propietario.

---

### 3.5 Decisión 5 — Convención de versiones de los artefactos

**Definición del problema.** R9 §5.8.1 fija `ORACLE_NORMATIVE_V4_R5` mientras §9.2 no cambie, pero no define la convención para versiones futuras. R2 §8.5 la registra pendiente.

**Requisitos normativos.** R9 §5.8.1 procedimiento ante cambio normativo: aprobar cambio, transcribir nueva versión, revisar, recalcular checksum, actualizar `ALLOWLIST_V4`, verificar. Plan R2 §3.2: versión de fuente y de artefacto en entradas y salidas.

**Alternativas.**

| Alternativa | Ventajas | Riesgos |
|---|---|---|
| A. Mantener `ORACLE_NORMATIVE_V4_R5` hasta cambio aprobado de §9.2; nueva versión secuencial tras aprobación | Estabilidad, coherencia con R9 | Requiere disciplina de registro |
| B. Versión semántica `MAJOR.MINOR` | Expresa naturaleza del cambio | Requiere definir reglas de MAJOR/MINOR no aprobadas |
| C. Versión por fecha | Simple de datar | No expresa relación con el cambio normativo; colisiones |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA].** Alternativa A. Toda versión nueva debe surgir de un cambio normativo aprobado y auditado; debe incluirse en la preimagen del checksum y en la evidencia. No se cambia la versión actual.

**Precisión AUD-DEC-RES-R1-03 — correcciones sin impacto normativo.** Se propone el tratamiento siguiente, sin autorizarlo todavía:

- Son correcciones sin impacto normativo las erratas tipográficas, de formato o de presentación que **no** cambian el significado de una regla, su estructura normativa ni el comportamiento verificable.
- Toda corrección de este tipo se registra en la procedencia y en el historial del artefacto afectado, con versión normativa inalterada, fecha real y descripción del cambio.
- Debe revisarse para demostrar ausencia de impacto semántico; la revisión queda documentada con los casos examinados.
- La versión normativa se conserva: una corrección sin impacto no produce nueva versión ni nuevo checksum de la transcripción, salvo que la corrección altere bytes de la preimagen canonicalizada, en cuyo caso se trata como cambio normativo.
- Si la corrección altera significado, estructura normativa o comportamiento verificable, se escala a **nueva versión**, aprobación formal y auditoría conforme a R9 §5.8.1.

Esta propuesta no permite cambios silenciosos: toda corrección, con o sin cambio de versión, queda trazada y revisada.

**Compatibilidad.** Directamente conforme a R9 §5.8.1 y R2 §3.2/§8.5. No modifica el conjunto de siete artefactos.

**Impacto.** Reproducibilidad: la versión fija la fuente. Trazabilidad: vincula cambio normativo, transcripción y checksum. Independencia: no depende del productivo. Fail-closed: versión no declarada o desalineada activa `ORACLE_VERSION_MISMATCH`.

**Criterio de aceptación verificable.** Versión declarada en cada artefacto; coincide con la fuente normativa aprobada; cambio de versión solo tras documentación aprobada y auditoría; checksum recalculado.

**Intervención humana.** Sí: **[PENDIENTE DE APROBACIÓN]**; propietario para la convención y para cada cambio normativo.

---

### 3.6 Decisión 6 — Arquitectura de ORACLE-ART-02, versión ejecutable del oracle

**Definición del problema.** R2 §4.2 no prescribe lenguaje, biblioteca ni arquitectura; la decide una futura tarea autorizada. Debe garantizarse independencia, determinismo y ausencia de dependencias ocultas sin modificar `pyproject.toml`.

**Requisitos normativos.** R9 §5.8.5: el oracle es herramienta de CI/auditoría; el módulo productivo no importa la transcripción desde tests. R2 §4.2: fuente de verdad en la transcripción; errores explícitos; sin fallback. Plan R2 §3: separación fuentes/generadores/artefactos/verificadores.

**Convenciones existentes.** `tests/test_provenance_v4_*.py`, `pytest` con `pythonpath=["src"]`, `jsonschema` y `rfc8785` ya declarados, `importlib.resources` para recursos del schema, JCS con `rfc8785.dumps`.

**Alternativas.**

| Alternativa | Ventajas | Riesgos |
|---|---|---|
| A. Verificador en `tests/`, sin importar módulos productivos para obtener la transcripción | Alineado con R9; sin nuevas dependencias; independencia verificable por revisión de imports | Requiere que CI lo ejecute fuera del camino productivo |
| B. Módulo de verificación separado dentro de `src/tradingai/` con recursos de solo lectura | Reutilizable y empaquetable | Riesgo de que producción lo importe; exigiría control estricto de dependencias |
| C. Herramienta externa con dependencias nuevas | Flexibilidad | Requiere modificar dependencias y autorización del propietario; no recomendable |

**Recomendación técnica [RECOMENDACIÓN TÉCNICA].** Alternativa A: verificador de CI/auditoría ubicado con las pruebas, con entradas declaradas limitadas a la transcripción aprobada y a `ALLOWLIST_V4` como representación ejecutable sometida a comparación. Sin importaciones desde `provenance_v4.py` hacia el oracle y sin que producción importe el oracle. No se crea código en esta tarea.

**Garantías exigibles.**

- Correspondencia con la transcripción: cada entrada del oracle se coteja con ORACLE-ART-01 y con §9.2.
- Reproducibilidad: mismas entradas ⇒ misma salida; sin fecha ni aleatoriedad en la decisión.
- Separación: especificación, implementación del verificador y auditoría son funciones distintas.
- Verificación independiente: el generador no es el único verificador; ORACLE-ART-04 y la auditoría son independientes.
- Integridad y procedencia: versión y checksum de la transcripción registrados en la salida.
- Fail-closed: datos incompletos, versión/checksum divergentes o condición inválida producen error determinista.
- Ausencia de dependencias ocultas: lista declarada de entradas; sin archivos implícitos, variables de entorno no documentadas ni importaciones productivas.

**Compatibilidad.** Compatible con R9 §5.8.1/5.8.5, R2 §4.2 y DEC-05 (sin fallback). No modifica dependencias ni alcance.

**Impacto.** Reproducibilidad: alta si las entradas están cerradas. Trazabilidad: cada salida referencia versión y artefacto. Independencia: verificable por inspección de imports y roles. Fail-closed: explícito.

**Criterio de aceptación verificable.** Auditoría de independencia documentada; lista de entradas declarada y cerrada; sin importación productiva del oracle; salida determinista; códigos de error explícitos; ninguna dependencia nueva en `pyproject.toml`.

**Intervención humana.** Sí solo si la arquitectura elegida amplía alcance o dependencias: **[PENDIENTE DE APROBACIÓN]** del propietario. La alternativa recomendada no amplía alcance, pero requiere autorización para implementarla.

---

## 4. Matriz consolidada de propuesta

| # | Decisión | Recomendación técnica | Estado | Autoridad necesaria |
|---|---|---|---|---|
| 1 | Formato `rule_id` | Secuencial por fila de §9.2, con tabla de correspondencia revisada | Pendiente | Propietario / autoridad designada |
| 2 | Ubicación física | Evidencias versionadas en repositorio; externo solo con referencia inmutable | Pendiente | Propietario / autoridad designada |
| 3 | Revisor independiente | Rol funcional designado; identidad real registrada al ejecutar | Pendiente | Propietario |
| 4 | Formato de evidencias | Texto UTF-8 determinista con campos obligatorios; JCS opcional derivado | Pendiente | Autoridad técnica; propietario si amplía alcance |
| 5 | Convención de versiones | Mantener `ORACLE_NORMATIVE_V4_R5`; nueva versión solo tras cambio aprobado | Pendiente | Propietario |
| 6 | Arquitectura de ORACLE-ART-02 | Verificador en `tests/`, sin dependencias nuevas ni imports productivos | Pendiente | Propietario si amplía alcance; autoridad técnica para implementar |

Ninguna recomendación se presenta como decisión aprobada.

### 4.1 Secuencia propuesta de resolución (AUD-DEC-RES-R1-04)

| Orden | Decisión | Debe resolverse antes de | Razón de la dependencia |
|---|---|---|---|
| 1 | D1 formato `rule_id` | ORACLE-ART-01 | El identificador se asigna durante la transcripción y forma parte de sus diez campos |
| 2 | D2 ubicación física | ORACLE-ART-01 y G2/G4 | La transcripción y el ejecutable necesitan destino con procedencia e inmutabilidad |
| 3 | D5 convención de versiones | ORACLE-ART-01 | La versión se incluye en la preimagen de ORACLE-ART-03 y en la evidencia |
| 4 | D6 arquitectura de ORACLE-ART-02 | ORACLE-ART-02 | El verificador no puede construirse sin decidir su independencia y entradas |
| 5 | D4 formato de evidencias | ORACLE-ART-05 y ORACLE-ART-06 | Las salidas de comparación deben ser reproducibles y auditables |
| 6 | D3 identidad del revisor | ORACLE-ART-04 | La revisión humana requiere designación real e independiente |

D1, D2 y D5 son paralelas entre sí y previas al paso 1; D6 precede al paso 2; D4 precede a los pasos 5 y 6; D3 precede al paso 4. **No existe circularidad**: ninguna decisión depende de un artefacto posterior a ella, y las seis son prerrequisitos de decisión, no resultados de la materialización.

Esta secuencia es **planificación técnica propuesta**. No autoriza generar artefactos ni superar ninguna puerta G0–G6.

---

## 5. Riesgos e incompatibilidades detectados

| Riesgo | Descripción | Mitigación propuesta |
|---|---|---|
| Circularidad | El verificador podría derivar la transcripción del código productivo | Fuentes separadas y auditoría de imports |
| Identidad ficticia | Registrar revisor sin designación real | Designación funcional del propietario; identidad real al ejecutar |
| Falta de formato de `rule_id` | Trazabilidad incompleta | Aprobar formato antes de ORACLE-ART-01 |
| Ubicación no definida | G2/G4 no pueden superarse | Decisión registrada antes de ORACLE-ART-01 |
| Evidencia no reproducible | Salidas sin entradas/versión | Campos obligatorios de evidencia |
| Versión silenciosa | Cambio normativo sin nueva versión | Procedimiento R9 §5.8.1 y `ORACLE_VERSION_MISMATCH` |
| Dependencias nuevas | Arquitectura C modificaría `pyproject.toml` | Descartada; requiere decisión expresa si se reconsidera |

No se detectó incompatibilidad entre las recomendaciones y R9/R2. Las seis decisiones deben resolverse antes de G2/G4 según corresponda.

---

## 6. Decisiones que requieren intervención humana

Todas las seis requieren intervención humana en algún grado:

1. Formato `rule_id`: aprobación del formato.
2. Ubicación física: decisión del propietario.
3. Revisor independiente: designación real del propietario.
4. Formato de evidencias: autoridad técnica; propietario si amplía alcance.
5. Convención de versiones: aprobación del propietario.
6. Arquitectura de ORACLE-ART-02: autorización técnica; aprobación del propietario si amplía alcance o dependencias.

No se designa persona, no se inventa firma y no se concede autorización en este documento.

---

## 7. Trazabilidad y estados

| Decisión | Plan R2 | Especificación R2 | R9 | Convención / evidencia |
|---|---|---|---|---|
| `rule_id` | §10.1 | §4.1, §8.1 | §5.8.1 | `docs/r13_decision_resolution_r1.md` |
| Ubicación | §6.2, §10.2 | §8.2 | §5.8.5 | `importlib.resources`, `docs/` |
| Revisor | §7, §10.3 | §4.4, §8.3 | §5.8.1 | Registros de aprobación sin nombres |
| Evidencias | §5, §10.4 | §4.5–4.7, §8.4 | §5.8.2 | `tests/`, `pyproject.toml` |
| Versiones | §3.2, §10.5 | §8.5 | §5.8.1 | DEC-05, sin fallback |
| Arquitectura | §3, §10.6 | §4.2 | §5.8.5 | `tests/test_provenance_v4_*.py` |

Se declaran expresamente:

```text
DECISION_RESOLUTION_STATUS: PROPOSAL
MATERIALIZATION_PLAN_OWNER_APPROVAL: APPROVED
ORACLE_ARTIFACT_MATERIALIZATION_AUTHORIZATION: NOT_GRANTED
ORACLE_ARTIFACTS_STATUS: NOT_CREATED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La aprobación del plan no autoriza materialización; las recomendaciones técnicas no sustituyen decisiones formales; AUD-R8-02 permanece abierto.

**Fin de R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R2.**
