# R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R2 — Plan operativo de materialización del oracle

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Documento de origen:** `docs/r13_oracle_artifacts_materialization_plan_r1.md`, conservado íntegramente como registro histórico.
**Auditoría incorporada:** `R13-AUDIT-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R1 — ACCEPTED WITH FINDINGS` (AUD-MAT-PLAN-R1-01, R1-02 y R1-03).
**Naturaleza:** plan documental preparatorio. No materializa artefactos, no ejecuta el oracle, no genera fingerprints ni checksums de artefactos inexistentes, y no autoriza implementación.

---

## 1. Propósito y límites

### 1.1 Propósito

Transformar los requisitos de `docs/r13_oracle_artifacts_specification_r2.md` (R2), aprobada documentalmente por el propietario, en un procedimiento técnico concreto, reproducible y auditable para la futura materialización de ORACLE-ART-01…07.

Esta segunda revisión del plan corrige exclusivamente los tres hallazgos de `R13-AUDIT-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R1`: condiciones de la puerta G6 (AUD-MAT-PLAN-R1-01), evidencia de ORACLE-ART-04 (R1-02) y nota de procedencia de ORACLE-ART-03 (R1-03). No cambia artefactos, dependencias, riesgos, decisiones pendientes ni estados de autorización.

### 1.2 Base normativa

| Elemento | Referencia |
|---|---|
| Diseño Fase C aprobado | `docs/r13_phase_c_design_r9.md` — Git `d21de0f112329ad9a9c30f167189a1f81ecef685`; SHA-256 `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| Registro de aprobación del diseño | `docs/r13_owner_design_approval_r1.md` — Git `6ecdf341fba3e2324505dd546cc1b792f20a6ad5` |
| Especificación aprobada | `docs/r13_oracle_artifacts_specification_r2.md` — Git `5179cad31e0a640837c785a8516bc46b126e4ea3`; SHA-256 `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| Registro de aprobación de la especificación | `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` — Git `22052a44e2f090fea294a7a51c676507bcaeefab` |
| Auditoría de la especificación | `R13-AUDIT-ORACLE-ARTIFACTS-SPECIFICATION-R2 — ACCEPTED`, sin hallazgos nuevos |
| Auditoría del registro de aprobación | `R13-AUDIT-ORACLE-ARTIFACTS-OWNER-APPROVAL-R1 — ACCEPTED` |
| HEAD de referencia | `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main` |
| Limitación pendiente | `AUD-R8-02: OPEN` |

### 1.3 Alcance

Incluye únicamente: procedimiento, dependencias, puertas de control, protocolo de verificación, requisitos de almacenamiento, roles, riesgos y decisiones pendientes.

**Excluido expresamente:** generar ORACLE-ART-01…07; crear el ejecutable del oracle; calcular checksums de artefactos inexistentes; ejecutar el oracle; ejecutar pruebas o la mutación; modificar código, tests, schemas, dependencias, datasets ni registros anteriores; acceder a Parquet protegidos; conceder autorizaciones.

Ninguna aprobación anterior se interpreta como autorización de ejecución. La aprobación del diseño R9 y de la especificación R2 habilita solo la planificación documental.

---

## 2. Inventario de artefactos

| ID | Nombre (R2) | Objetivo | Fuente normativa | Formato esperado | Dependencias | Procedimiento futuro | Verificación independiente | Evidencia de aceptación | Criterios de rechazo | Estado |
|---|---|---|---|---|---|---|---|---|---|---|
| ORACLE-ART-01 | Transcripción normativa completa e independiente | Fijar §9.2/DEC-06 como datos comparables | R2 §4.1; R9 §5.8.1/5.8.5 | Objeto `{"version":…,"entries":[…]}`; diez campos por entrada; entradas ordenadas por `path` | Ninguna | Transcribir desde §9.2; expandir `{partition}`; asignar `rule_id` pendiente de formato | Revisión semántica fila por fila por revisor distinto del generador | Transcripción revisada; 139 rutas; P1–P5; I1–I12; separación texto/datos/auxiliar | Campo ausente; ruta duplicada/omitida; condición fuera de vocabulario; copia desde código productivo | `NOT_CREATED` |
| ORACLE-ART-02 | Versión ejecutable del oracle | Verificar la representación ejecutable en CI/auditoría | R2 §4.2; R9 §5.8.5 | **A decidir en futura tarea autorizada** (R2 no prescribe lenguaje, biblioteca ni arquitectura) | 01 | Implementar desde la transcripción; registrar decisión de arquitectura | Auditoría de independencia y ejecución aislada | Resultados deterministas; sin importaciones productivas; errores explícitos; sin fallback | Resultados no deterministas; dependencia de producción o tests; silencio ante datos incompletos | `NOT_CREATED` |
| ORACLE-ART-03 | SHA-256 de la transcripción canonicalizada | Fijar integridad de la transcripción | R2 §4.3 (título corregido); R9 §5.8.1/5.8.5 | Hex minúsculo de 64 caracteres | 01, 02 | JCS de `{version, entries}`; SHA-256; sin auxiliares ni propio checksum en la preimagen | Recálculo por verificador distinto | Preimagen documentada; valor reproducible | Bytes sin canonicalizar; auxiliares incluidos; checksum como prueba semántica | `NOT_CREATED` |
| ORACLE-ART-04 | Registro de revisión humana independiente | Evidenciar revisión semántica real | R2 §4.4; R9 §5.8.1/5.8.5 | Registro documental estructurado | 01, 03 | Revisión efectiva por persona independiente | Auditoría del registro y de los casos examinados | Identidad funcional; alcance; casos; hallazgos resueltos; dictamen; fecha real | Plantilla vacía; revisor no independiente; versión/checksum distintos | `NOT_CREATED` |
| ORACLE-ART-05 | Evidencia de cobertura de 139 rutas | Verificar semántica por ruta | R2 §4.5; R9 §5.8.2/5.8.5 | Matriz: ruta, aplicabilidad, comportamiento esperado, resultado observado, caso, evidencia, `rule_id` | 01, 02 | Comparar conjuntos en ambos sentidos | Revisión de la matriz y de las salidas | 139 filas únicas con semántica y caso asociado | Contar filas sin semántica; duplicados; `shared_with` fuera de calibration | `NOT_CREATED` |
| ORACLE-ART-06 | Evidencia de comprobación de nueve metadatos | Comparar los nueve campos de `AllowlistEntry` | R2 §4.6; R9 §5.1/5.8.2/5.8.5 | Fila por ruta y campo con valores y resultado | 01, 02, 05 | Comparación campo por campo | Verificación de la salida determinista | Nueve campos comparados por ruta; divergencia con campo indicado | Campo omitido; comparación solo de conjuntos; divergencia silenciada | `NOT_CREATED` |
| ORACLE-ART-07 | Evidencia de la mutación `external_run_only` | Demostrar detección de cambio normativo | R2 §4.7; R9 §5.8.2/5.8.5 | Salida determinista antes/después sobre copia aislada | 01, 02, 06 | Mutar copia aislada de `base_*` a `always` | Revisión de antes/después y aislamiento | `ALLOWLIST_ORACLE_METADATA_DIVERGENCE` en tres rutas | Mutación en producción; detección solo interna; no reversible | `NOT_CREATED` |

El décimo campo del oracle, `rule_id`, es de trazabilidad y **no** se cuenta entre los nueve metadatos comparados (R2 §4.6).

---

## 3. Arquitectura de generación

### 3.1 Separación de funciones

| Capa | Contenido | Regla |
|---|---|---|
| Fuentes normativas | DEC-06, diseño v4 §9.2, `manifest_v4.json`, R9, R2 | Solo fuentes aprobadas; ninguna se modifica durante la materialización |
| Generadores | Futuros procedimientos para ORACLE-ART-01/02/03/05/06/07 | No se implementan en este plan; se registran cuando se autoricen |
| Artefactos | ORACLE-ART-01…07 | Cada uno con versión, procedencia y estado |
| Verificadores | ORACLE-ART-04 y auditoría independiente | Distintos del generador; sin circularidad |

### 3.2 Versiones

Toda entrada y salida deberá identificar la versión de la fuente normativa consultada y la versión del artefacto. Se conserva `ORACLE_NORMATIVE_V4_R5` mientras §9.2 no cambie; un cambio normativo exige nueva versión aprobada (R9 §5.8.1). El formato de `rule_id` y la convención de versiones futuras están pendientes (§10).

### 3.3 Reproducibilidad y procedencia

Registrar para cada artefacto: entradas exactas, procedimiento seguido, fecha real, identidad funcional de quien generó, versión de la fuente, salida y calculación SHA-256 cuando corresponda. La reproducibilidad se demuestra repitiendo el procedimiento con las mismas entradas y obteniendo la misma salida.

### 3.4 Integridad

Solo ORACLE-ART-03 exige SHA-256 conforme a R2 §4.3. No se calcula checksum de artefactos inexistentes ni se inventa valor alguno. Un checksum válido **no** sustituye la revisión semántica (ORACLE-ART-04).

### 3.5 Prevención de modificaciones accidentales

Las fuentes normativas se tratan como solo lectura. La mutación de ORACLE-ART-07 se aplica únicamente a una copia aislada. La producción no importa el oracle ni artefactos de tests.

### 3.6 Errores y fail-closed

Cualquier dato incompleto, discrepancia de versión/checksum, condición fuera de vocabulario o ausencia de evidencia produce error determinista e interrumpe la secuencia. No se aplican aproximaciones, coerciones ni fallbacks silenciosos.

---

## 4. Secuencia de materialización

Orden justificado por dependencias reales de R2: la transcripción es origen de todo; el ejecutable depende de ella; el checksum se calcula sobre la transcripción; la revisión depende de transcripción y checksum; la cobertura depende de transcripción y ejecutable; los metadatos dependen además de la cobertura; la mutación depende de los metadatos.

| Paso | Artefacto | Precondiciones | Entradas | Operación futura | Salida esperada | Comprobaciones posteriores | Evidencia a conservar | Condiciones de interrupción |
|---|---|---|---|---|---|---|---|---|
| 0 | Puertas G0–G3 | Especificación y plan revisados; autorización expresa de materialización | R9, R2, registro de aprobación | Confirmar puertas y decisiones pendientes críticas | Autorización registrada | Cotejo de hashes y estados | Registro de puertas | Falta G3; hash divergente; decisión crítica sin resolver |
| 1 | ORACLE-ART-01 | G3 concedido; §9.2 disponible | Diseño v4 §9.2, DEC-06 | Transcribir y expandir 139 rutas; asignar `rule_id` | Objeto `version`/`entries` | 139 rutas; diez campos; P1–P5; I1–I12 | Entradas, notas de transcripción, salida | Ruta repetida/omitida; condición inválida; copia desde productivo |
| 2 | ORACLE-ART-02 | Paso 1 completo | ORACLE-ART-01 | Implementar verificador independiente | Ejecutable con formato decidido | Determinismo; independencia; errores explícitos | Decisión de arquitectura y salidas aisladas | Importación productiva; resultados no deterministas |
| 3 | ORACLE-ART-03 | Pasos 1–2 completos | ORACLE-ART-01 | JCS + SHA-256 | Hex minúsculo de 64 | Recálculo independiente | Preimagen y valor | Auxiliares en preimagen; checksum no reproducible |
| 4 | ORACLE-ART-04 | Pasos 1 y 3 completos | 01, 03 | Revisión semántica real | Registro con dictamen | Casos examinados; hallazgos resueltos | Identidad funcional verificable del revisor; evidencia documental de su revisión y aprobación; fecha y referencia del registro; no se exige firma criptográfica salvo decisión aprobada futura | Revisor no independiente; versión/checksum distintos |
| 5 | ORACLE-ART-05 | Pasos 1–2 completos | 01, 02 | Comparación de conjuntos de rutas | Matriz de 139 filas | Semántica por fila | Salidas antes/después | Filas sin semántica; `shared_with` mal clasificado |
| 6 | ORACLE-ART-06 | Pasos 1, 2 y 5 completos | 01, 02, 05 | Comparación de nueve metadatos | Matriz por ruta y campo | Divergencias con campo indicado | Salida ordenada y deduplicada | Campo omitido; divergencia silenciada |
| 7 | ORACLE-ART-07 | Pasos 1, 2 y 6 completos | 01, 02, 06 | Mutar copia aislada de `base_*` | Salida antes/después | Detección en tres rutas | Copia original, copia mutada, salidas | Mutación en producción; no reversible |

**Nota ORACLE-ART-03 (AUD-MAT-PLAN-R1-03):** mantiene la dependencia declarada de ORACLE-ART-01 y ORACLE-ART-02 conforme a R2. Los bytes utilizados para calcular el SHA-256 proceden exclusivamente de la transcripción canonicalizada definida por R9 §5.8.5. ORACLE-ART-02 participa en la cadena de procedencia y verificación, pero sus bytes ejecutables **no** forman parte de la preimagen del checksum. No se exige un checksum adicional del ejecutable. La definición normativa del checksum y las dependencias de R2 no se modifican.

La secuencia no asume generación automática total: ORACLE-ART-04 exige revisión humana independiente y ORACLE-ART-02 requiere una decisión de arquitectura pendiente.

---

## 5. Verificación independiente

### 5.1 Protocolo

| Verificación | Método | Evidencia | Criterio |
|---|---|---|---|
| Integridad | Recalcular SHA-256 de ORACLE-ART-03 desde la transcripción | Preimagen y valor | Reproducible por verificador distinto |
| Correspondencia R2 | Cotejar cada artefacto con §4.1–4.7 de R2 | Matriz de cotejo | Sin campo omitido ni añadido |
| 139 rutas | Igualdad de conjuntos en ambos sentidos | Matriz ORACLE-ART-05 | 139 rutas únicas con semántica |
| Nueve metadatos | Comparación campo por campo | Matriz ORACLE-ART-06 | Nueve nombres exactos de R2 §4.6 |
| `rule_id` | Comprobar que es décimo campo de trazabilidad | Entradas de ORACLE-ART-01 | No contado entre los nueve |
| P1–P5 e I1–I12 | Revisión semántica de la transcripción | Salida ORACLE-ART-01 | Coherencia con R9 §5.8.3 y §5.7 |
| Revisión humana | Auditoría de ORACLE-ART-04 | Registro de revisión | Real, con hallazgos resueltos |
| Mutación | Comparar salida antes/después de la copia aislada | Salida ORACLE-ART-07 | Detección por oracle en tres rutas |

### 5.2 Clases de evidencia

| Clase | Ejemplo | No equivale a |
|---|---|---|
| Documental | Transcripción revisada, registro de revisión | Ejecución real |
| Generada automáticamente | Salidas de comparación de rutas y metadatos | Revisión semántica humana |
| Revisión humana | Dictamen de ORACLE-ART-04 | Aprobación del propietario |
| Auditoría | Informe independiente posterior | Autorización de materialización |

La prueba de mutación queda **diseñada pero no ejecutada**.

---

## 6. Integridad y almacenamiento

### 6.1 Requisitos futuros

- Ubicación futura de cada artefacto: **decisión pendiente**; R2 no la fija.
- Convenciones de nombres y versiones: derivadas de los ID ORACLE-ART-01…07 y de la versión de la fuente; el formato definitivo de `rule_id` y la convención de versiones futuras están pendientes.
- Hashes: solo el de ORACLE-ART-03, con preimagen documentada.
- Procedencia: conservar entradas, fecha, generador, versión y salida.
- Protección contra sobrescritura: versiones inmutables; nunca sobrescribir una versión revisada.
- Versiones anteriores: conservarlas para auditoría.
- Artefactos incompletos o rechazados: marcar con su estado y conservar la evidencia que motivó el rechazo.

### 6.2 Alternativas para ubicación (sin decidir)

1. Directorio de evidencias versionado dentro del repositorio, sujeto a aprobación de ubicación.
2. Artefacto de Release con control de acceso, sujeto a aprobación de ubicación.
3. Almacenamiento externo con referencia inmutable en el repositorio, sujeto a aprobación de ubicación.

Ninguna alternativa se adopta aquí. La decisión corresponde al propietario o a la autoridad que este designe, y debe registrarse antes de ORACLE-ART-01.

---

## 7. Roles y separación de responsabilidades

| Función | Responsabilidad | Independencia exigible |
|---|---|---|
| Generación | Producir 01, 02, 03, 05, 06, 07 | No puede ser único verificador de su resultado |
| Revisión técnica | Comprobar requisitos R2 y R9 | Distinta de la generación |
| Revisión humana independiente | Emitir ORACLE-ART-04 | No es el generador del artefacto revisado |
| Auditoría independiente | Auditar evidencia y proceso | No genera ni aprueba artefactos |
| Propietario | Aprobar especificación y conceder autorizaciones | No se inventa identidad personal |

No se atribuye a una misma función una independencia que no pueda demostrarse. El checksum no sustituye la revisión humana; esta no sustituye la aprobación del propietario.

---

## 8. Puertas de control

| Puerta | Criterios de entrada | Criterios de salida | Rechazo |
|---|---|---|---|
| **G0** Especificación aprobada | R2 aprobada y auditada `ACCEPTED` | Registro de aprobación vigente | Hash R2 divergente o auditoría no favorable |
| **G1** Plan revisado | Plan documental completo y cotejado con R9/R2 | Revisión documental sin contradicciones | Convertir decisiones pendientes en aprobadas |
| **G2** Fuentes y herramientas verificadas | §9.2, schema y R2 disponibles; decisiones críticas registradas | Procedencia documentada | Fuente modificada o decisión crítica sin resolver |
| **G3** Autorización de materialización | Decisión expresa del propietario | Autorización registrada | Cualquier aprobación anterior interpretada como autorización |
| **G4** Artefactos generados | G3 concedido | 01–07 generados con sus estados | Artefacto incompleto o no reproducible |
| **G5** Verificación independiente | G4 completo; revisión humana realizada | Evidencia de verificación y dictamen | Discrepancia no resuelta; revisión no independiente |
| **G6** Resolución de AUD-R8-02 | G5 favorable; siete artefactos materializados y estados verificados; informe de auditoría independiente favorable; sin hallazgos bloqueantes; aceptación expresa del propietario | Cierre documentado de AUD-R8-02 con evidencia trazable de los cinco requisitos | Artefacto ausente o no verificado; informe desfavorable; hallazgo bloqueante sin resolver; falta de aceptación expresa del propietario; evidencia incompleta |

La aprobación de G0 **no** implica aprobar G1–G6. G3 es obligatoria antes de cualquier generación.

**G6 (AUD-MAT-PLAN-R1-01):** G5 favorable **no** equivale a superar G6. Solo puede considerarse superada cuando concurran conjuntamente: (1) los siete artefactos requeridos están materializados y sus estados individuales verificados; (2) existe un informe de auditoría independiente favorable que verifica los criterios correspondientes a AUD-R8-02; (3) no quedan hallazgos bloqueantes sin resolver; (4) el propietario ha emitido aceptación expresa del resultado de la auditoría, independiente de la aceptación técnica del auditor; y (5) existe evidencia documental trazable de cada requisito anterior. La superación de G6 **no** autoriza por sí misma la implementación de Fase C: esa autorización continúa siendo una decisión separada y explícita.

---

## 9. Riesgos y contingencias

| Riesgo | Medida preventiva | Criterio de interrupción |
|---|---|---|
| Divergencia normativa | Cotejar §9.2 y R2 antes de generar; conservar fuente exacta | Cambio no aprobado de §9.2 o de R2 |
| Generación no reproducible | Registrar entradas, versión y procedimiento; repetir con mismas entradas | Salida distinta al repetir |
| Hash incorrecto | Preimagen documentada y recálculo independiente | Preimagen con auxiliares o valor no reproducible |
| Cobertura incompleta | Matriz de 139 rutas con semántica por fila | Ruta duplicada, omitida o sin caso |
| Dependencias no fijadas | Respetar grafo de dependencias de R2 | Generar un artefacto antes de sus dependencias |
| Contaminación de independencia | Separar generador, revisor y auditor | Revisor igual al generador |
| Evidencia incompleta | Lista de evidencia por artefacto y por puerta | Falta de fecha real, dictamen o salida |
| Modificación accidental de fuentes | Fuentes en solo lectura; mutación solo en copia aislada | Cualquier cambio en §9.2, R2, schema o registros |

---

## 10. Decisiones pendientes

| Decisión | Impacto | Opciones | Recomendación técnica | Autoridad | Estado |
|---|---|---|---|---|---|
| Formato de `rule_id` (R2 §8.1) | Bloquea trazabilidad completa de ORACLE-ART-01 | Definir esquema estable por fila de §9.2 | Proponer esquema en la tarea autorizada y revisarlo con la transcripción | Propietario o autoridad designada | **Pendiente, no aprobada** |
| Ubicación física de artefactos y ejecutable (R2 §8.2) | Bloquea G2/G4 | Tres alternativas de §6.2 | Registrar decisión antes de ORACLE-ART-01 | Propietario | **Pendiente, no aprobada** |
| Identidad funcional del revisor humano (R2 §8.3) | Bloquea ORACLE-ART-04 | Rol funcional independiente, sin nombre inventado | Registrar rol real en el momento de la revisión | Propietario o autoridad designada | **Pendiente, no aprobada** |
| Formato de evidencias de ejecución (R2 §8.4) | Afecta reproducibilidad | Salida determinista documentada | Elegir formato verificable sin ampliar alcance | Autoridad técnica autorizada | **Pendiente, no aprobada** |
| Convención de versiones futuras (R2 §8.5) | Afecta cambios normativos | Versión nueva por cambio aprobado de §9.2 | Mantener `ORACLE_NORMATIVE_V4_R5` hasta cambio aprobado | Propietario | **Pendiente, no aprobada** |
| Decisión de arquitectura de ORACLE-ART-02 (R2 §4.2) | Afecta método de verificación | No prescrita por R2 | Registrar decisión antes de generar el ejecutable | Autoridad técnica autorizada, con aprobación del propietario si amplía alcance | **Pendiente, no aprobada** |

Ninguna se marca aprobada. Ninguna se resuelve unilateralmente en este plan.

---

## 11. Estado final y trazabilidad

| Etapa del plan | R9 | R2 | Norma / decisión | CP-C |
|---|---|---|---|---|
| §1 Propósito y límites | §§5.8.5, 12 | §§1, 9 | Aprobación R9 y de la especificación | — |
| §2 Inventario | §5.8.1–5.8.5 | §§4.1–4.7 | DEC-06, §9.2 | 05, 07, 08, 13 |
| §3 Arquitectura | §5.8.1–5.8.5 | §§4.2, 6 | DEC-05 (sin fallback) | 05, 13 |
| §4 Secuencia | §5.8.1–5.8.5 | §5 | DEC-06, V4-U10/U11 | 05, 13 |
| §5 Verificación | §5.8.2, §5.8.4, §5.8.5 | §§4.4–4.7, 5 | DEC-01…09 | 05, 07, 08, 13 |
| §6 Almacenamiento | §5.8.1 | §§4.3, 8 | Decisiones pendientes | 05, 13 |
| §7 Roles | §5.8.5 | §3, §4.4 | Aislamiento de aprobaciones | 05, 13 |
| §8 Puertas | §5.6, §5.8.2, §5.8.5 | §5 | AUD-R8-02 | 05, 13 |
| §9 Riesgos | §11 | §6 | Fail-closed | 13, 18 |
| §10 Decisiones pendientes | §5.8.1, §5.8.5 | §8 | Reservadas al propietario | — |

Se declaran expresamente:

```text
MATERIALIZATION_PLAN_STATUS: DOCUMENTARY_DRAFT
ORACLE_ARTIFACT_MATERIALIZATION_AUTHORIZATION: NOT_GRANTED
ORACLE_ARTIFACTS_STATUS: NOT_CREATED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R2.**
