# R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R2 — Protocolo de revisión IA independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta documental**. No aprobada; pendiente de auditoría independiente.

```text
AI_REVIEW_PROTOCOL_R2: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
```

---

## 1. Propósito y estado

Definir la modalidad `INDEPENDENT_AI_REVIEW` para sustentar **exclusivamente** ORACLE-ART-04, resolviendo individualmente los ocho hallazgos de la auditoría del protocolo R1. Esta revisión **nunca** se denomina revisión humana. El protocolo no ejecuta revisión alguna ni crea artefactos.

---

## 2. Fuentes verificadas

| Fuente | SHA-256 |
|---|---|
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` |
| `docs/r13_audit_oracle_art_04_ai_independent_review_protocol_r1.md` | `146274794b1b2453c04e936e892a6fa39d6e15c3cafde80fe191650d73330693` |
| `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |
| `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| `docs/r13_oracle_g5_blocker_resolution_analysis_r1.md` | `00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` |

Todas las fuentes se conservan sin modificar. Las versiones R3 correspondientes son propuestas simultáneas (§3).

---

## 3. Fundamento normativo

| Documento | Función | Estado |
|---|---|---|
| Decisiones `DEC-OWNER-AI-01…06` | Habilitación expresa | **Aprobadas** |
| Resolución de decisiones R3 (§3 de ese documento) | D3-R3: excepción regulada | Propuesta pendiente de auditoría |
| Especificación R3 §3 | Contenido de ART-04 | Propuesta pendiente de auditoría |
| Plan R3 §4 | Criterio de G5 | Propuesta pendiente de auditoría |
| Autorización R3 | Levantamiento de la prohibición | **Propuesta sin efecto** hasta su auditoría y aprobación |
| Diseño R9 §5.4/§5.8 | Autoridad normativa técnica | Aprobado, sin cambios |

---

## 4. Modalidades

| Modalidad | Naturaleza | ¿Sustenta ART-04? |
|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | Persona real independiente, distinta del generador | Sí, vía preferente |
| `INDEPENDENT_AI_REVIEW` | IA de terceros, distinta del generador | Sí, solo ART-04 y solo bajo este protocolo |
| `AUTOMATED_INTERNAL_VERIFICATION` | Verificadores internos | No; evidencia auxiliar |

Está prohibido denominar «revisión humana» a `INDEPENDENT_AI_REVIEW` o presentarla como cumplimiento directo de D3 en su versión R2.

---

## 5. Resolución individual de los ocho hallazgos

### AUD-AI-REV-R1-01 — HIGH — Autorización versionada — **RESUELTO**

**Problema.** La autorización R2 §3 prohíbe omitir revisión humana y el protocolo R1 no la consideró.
**Resolución.** Este protocolo condiciona su ejecución a la autorización R3 (§3), que conserva R2 íntegramente y levanta la prohibición solo para `INDEPENDENT_AI_REVIEW`/ART-04. R2 no se modifica retroactivamente; la excepción se registra con fecha, hash y referencia. Sin R3 **en vigor**, ninguna revisión puede ejecutarse.
**Cláusulas:** §3, §6.1, §12.

### AUD-AI-REV-R1-02 — HIGH — Recomendación del análisis G5 R1 — **RESUELTO**

**Problema.** El análisis R1 §8.1 exige revisor humano real; el protocolo R1 no la superó documentadamente.
**Resolución.** D3-R3 cita literalmente la recomendación y declara su superación exclusiva mediante la modalidad regulada, conservando el texto original y la vía humana. Véase §3.2 de la resolución R3. No se reinterpretan sus términos.
**Cláusulas:** §3, §5.02, §13.

### AUD-AI-REV-R1-03 — MEDIUM — Independencia verificable — **RESUELTO**

**Control objective:** proveedor y modelo distintos con linaje declarado; sesión limpia; fuentes originales; sin dictámenes previos en el contexto inicial; prompt íntegro y hashes de entrada; linaje y contexto registrados; reconstrucción hashable anterior a la comparación; limitaciones declaradas. El mismo proveedor o limitación no demostrable obliga a `INCONCLUSIVE`. Dos ejecuciones del mismo modelo no bastan.
**Cláusulas:** §6.

### AUD-AI-REV-R1-04 — MEDIUM — Reproducibilidad — **RESUELTO**

**Control:** identificador y versión exacta del modelo (o `NO_DISPONIBLE` con consecuencia); parámetros de generación; prompt verbatim con hash; hashes de todas las entradas; respuestas íntegras; repetición independiente cuando proceda; bases deterministas como autoridad y criterio de discrepancia. Véase §7.
**Cláusulas:** §7.

### AUD-AI-REV-R1-05 — MEDIUM — Dictamen, severidades y autoridad — **RESUELTO**

**Control:** cuatro dictámenes definidos, escala `BLOCKER/HIGH/MEDIUM/LOW/INFO`, IA propone, auditor confirma, propietario acepta; reglas prohibitivas para G5. Véase §8.
**Cláusulas:** §8.

### AUD-AI-REV-R1-06 — MEDIUM — Evidencia verificable — **RESUELTO**

**Control:** matriz 139 × 9, reconstrucción hashable, tabla de discrepancias, positivos/negativos y vinculación fuente→comprobación→resultado. Véase §9.
**Cláusulas:** §9.

### AUD-AI-REV-R1-07 — LOW — Auditor posterior — **RESUELTO**

**Control:** auditor distinto del generador y de la IA revisora, con evaluación a ciegas; herramientas deterministas frente a juicio humano. Véase §10.
**Cláusulas:** §10.

### AUD-AI-REV-R1-08 — LOW — ART-02 — **RESUELTO**

**Control:** ART-02 se incorpora al alcance y se verifica contra la reconstrucción independiente de §9.2/R9 §5.4/schema, sin usar ART-01 como fuente del esperado. Véase §11.
**Cláusulas:** §11.

---

## 6. Controles de independencia (DEC-OWNER-AI-04)

1. **Proveedor y modelo** distintos del generador, con declaración de linaje. Si no es viable o el linaje no puede declararse, la revisión concluye `INCONCLUSIVE`.
2. **Sesión limpia**: contexto nuevo, sin historial de revisiones previas; se conserva hash del manifiesto de apertura.
3. **Fuentes originales**: R9 §5.4, diseño §9.2, `manifest_v4.json`, R2/R3 y artefactos. Quedan prohibidos resúmenes o notas producidas por el generador como entrada.
4. **Sin dictámenes previos** en el contexto inicial: se registra el prompt completo y su hash; no se entregan las conclusiones de OpenCode ni de auditorías previas.
5. **Prompt íntegro y hashes** de todos los archivos de entrada, conservados sin recorte.
6. **Linaje y contexto** registrados: herramientas, parámetros, archivos leídos y transcripción completa de la sesión.
7. **Reconstrucción independiente** de las reglas en artefacto hashable, generada **antes** de la comparación (etapa C antes de D).
8. **Limitaciones** expresamente declaradas; cualquier limitación que afecte independencia impide `ACCEPTED`.
9. **Dos ejecuciones del mismo modelo no constituyen independencia.** La independencia se demuestra por procedimiento y trazabilidad.

La identidad funcional del sistema revisor se designa por el propietario; no se inventa nombre humano ni firma.

---

## 7. Reproducibilidad

| Elemento | Requisito |
|---|---|
| Modelo | Identificador y versión exacta; si no está disponible: `NO_DISPONIBLE` y conclusión `INCONCLUSIVE` para lo que dependa de él |
| Parámetros | Temperatura, `seed`, `top_p`, límites y herramientas, registrados |
| Prompt | Completo, verbatim, con hash |
| Entradas | Hash de **todos** los archivos leídos |
| Respuestas | Registro íntegro, sin recorte ni resumen |
| Repetición | Sesión nueva y mismo manifiesto cuando sea viable |
| Discrepancias | Las comprobaciones deterministas (hash, JCS, cobertura, metadatos) prevalecen; la parte estocástica exige concordancia; divergencia ⇒ `INCONCLUSIVE`; resuelve el auditor posterior, nunca la IA |

---

## 8. Dictamen, severidades y autoridad (DEC-OWNER-AI-05)

### 8.1 Dictámenes permitidos

| Dictamen | Criterio inequívoco |
|---|---|
| `ACCEPTED` | Todas las comprobaciones de §9 y §11 reproducidas; sin discrepancias; sin limitaciones de independencia/reproducibilidad; sin hallazgos abiertos |
| `ACCEPTED_WITH_FINDINGS` | Solo hallazgos `MEDIUM`/`LOW`/`INFO` con resolución verificable; sin contradicción normativa; sin limitación bloqueante |
| `REJECTED` | Contradicción normativa, discrepancia bloqueante, dependencia circular o artefacto alterado |
| `INCONCLUSIVE` | Evidencia insuficiente, versión no disponible, contradicción no resuelta o independencia no demostrable |

### 8.2 Severidades

`BLOCKER` (impide cualquier accepted), `HIGH` (bloquea G5), `MEDIUM` (requiere resolución documentada), `LOW` e `INFO` (registrados, no bloqueantes). Cualquier limitación de independencia o reproducibilidad se clasifica al menos `HIGH`.

### 8.3 Autoridad

La **IA revisora propone** el dictamen y la severidad. El **auditor posterior evalúa** la evidencia y confirma o corrige la severidad. El **propietario conserva la autoridad de aceptación** mediante registro expreso. El dictamen IA **no** es aprobación del propietario ni sustituye a la auditoría independiente.

### 8.4 Regla G5

`INCONCLUSIVE` y `REJECTED` **nunca** desbloquean G5. `ACCEPTED_WITH_FINDINGS` **tampoco** mientras existan hallazgos `BLOCKER` o `HIGH` sin resolver. Solo `ACCEPTED` —o `ACCEPTED_WITH_FINDINGS` plenamente resuelto— con auditoría separada favorable, ART-04 verificado y aceptación expresa puede sustentar la reevaluación de G5 (plan R3 §4.1).

---

## 9. Evidencia verificable (hallazgo AUD-AI-REV-R1-06)

### 9.1 Matriz

Una matriz de **139 rutas × 9 metadatos** (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`) con valor esperado reconstruido, valor observado y resultado por celda. `rule_id` se mantiene separado como campo de trazabilidad.

### 9.2 Reconstrucción

Artefacto hashable e inmutable con las reglas derivadas de §9.2/R9 §5.4/schema, con sello anterior a la comparación. No se deriva de ART-01 ni de ART-02.

### 9.3 Casos

Por cada ruta: caso positivo y cuatro negativos — ausencia, duplicación, ruta desconocida y divergencia—. Se registran error esperado y resultado `DETECTED`/`NOT_DETECTED`.

### 9.4 Tabla de discrepancias

| ID | Ruta/campo | Severidad | Fuente normativa | Comprobación reproducible | Resultado | Resolución |
|---|---|---|---|---|---|---|

### 9.5 Vinculación

Cada conclusión debe vincularse a: fuente normativa → comprobación reproducible → resultado verificable → entrada en la tabla de discrepancias. Un contador declarado sin esta vinculación **no** constituye evidencia.

---

## 10. Auditoría posterior (finding 07)

- El auditor es un rol **distinto** del generador y de la IA revisora, designado funcionalmente por el propietario.
- **Evaluación a ciegas**: ejecuta sus comprobaciones antes de leer el dictamen de la IA.
- Herramientas **deterministas** para hashes, JCS, cobertura de 139 rutas y comparaciones.
- **Juicio humano** para veracidad de identidad, versión, fecha y aceptabilidad de limitaciones.
- Se conservan registros separados: informe de la IA e informe de auditoría.
- Verifica además: reconstrucción previa a la comparación, ausencia de filtración de dictámenes, etiqueta de modalidad y cumplimiento de §8.4.

---

## 11. ART-02 sin circularidad (finding 08)

1. Reconstruir reglas desde R9 §5.4, diseño §9.2 y `manifest_v4.json`, **sin usar ART-01 ni ART-02** como fuente esperada.
2. Comparar ART-01 contra la reconstrucción (transcripción normativa).
3. Comparar ART-02 contra la reconstrucción (versión ejecutable), sin que sus constantes sean la fuente del esperado.
4. Comparar ART-01 ↔ ART-02 solo como comprobación secundaria: la coincidencia mutua no prueba corrección semántica.
5. Registrar los tres hashes y toda divergencia en la tabla de §9.4. Si ART-02 comparte generador con ART-01, declarar la limitación.

---

## 12. Controles contra falsos positivos

- No aceptar coincidencias superficiales ni un hash correcto como prueba de corrección semántica.
- No considerar pruebas internas (`tests/`) como evidencia independiente suficiente.
- No aceptar conclusiones sin trazabilidad normativa.
- Ante contradicción normativa: `INCONCLUSIVE` o `REJECTED`.
- La IA no modifica las fuentes que revisa: acceso de solo lectura.
- Sin autorización R3 en vigor, la revisión no produce efecto normativo.

---

## 13. Procedimiento A–H

| Etapa | Acción | Salida |
|---|---|---|
| A | Preparación de fuentes originales, sin inclusiones tutoras | Manifiesto de fuentes |
| B | Verificación de hashes | Tabla de hashes |
| C | Reconstrucción independiente (antes de D) | Artefacto hashable |
| D | Comparación contra ART-01/02/03/04/05/06/07 | Matriz y resultados |
| E | Análisis de discrepancias con severidades | Tabla de discrepancias |
| F | Integridad JCS/SHA-256 y reproducibilidad | Evidencia |
| G | Dictamen técnico propuesto | Dictamen |
| H | Limitaciones, trazabilidad y auditoría posterior | Registro completo |

---

## 14. Matriz de trazabilidad

| Decisión aprobada | Hallazgo | Documento nuevo | Cláusula |
|---|---|---|---|
| DEC-OWNER-AI-01 | — | Resolución R3 §3; Especificación R3 §3.1–3.2; Plan R3 §4; Protocolo R2 §4 | Modalidad y alcance |
| DEC-OWNER-AI-02 | AUD-AI-REV-R1-01 | Autorización R3 §1–2; Protocolo R2 §5.01, §6.1, §12 | Excepción versionada |
| DEC-OWNER-AI-03 | AUD-AI-REV-R1-02 | Resolución R3 §3.1–3.2, §4; Protocolo R2 §5.02 | Superación documentada |
| DEC-OWNER-AI-04 | AUD-AI-REV-R1-03, -07 | Resolución R3 §3.5; Especificación R3 §3.4; Protocolo R2 §6, §10 | Independencia y auditor |
| DEC-OWNER-AI-05 | AUD-AI-REV-R1-05 | Resolución R3 §3.6; Especificación R3 §3.5; Protocolo R2 §8 | Dictamen y autoridad |
| DEC-OWNER-AI-06 | — | Autorización R3 §5; Plan R3 §4.1; Protocolo R2 §12 | Límites |
| — | AUD-AI-REV-R1-04 | Protocolo R2 §7 | Reproducibilidad |
| — | AUD-AI-REV-R1-06 | Especificación R3 §3.3–3.4; Protocolo R2 §9 | Evidencia verificable |
| — | AUD-AI-REV-R1-08 | Especificación R3 §3.6; Protocolo R2 §11 | ART-02 |

---

## 15. Revisión de consistencia documental

Realizada sobre los cinco documentos propuestos. **No es una auditoría independiente externa.**

| Comprobación | Resultado |
|---|---|
| Coincidencia con las seis decisiones aprobadas | Sin contradicción; DEC-OWNER-AI-01…06 se respetan literalmente |
| Versiones anteriores preservadas | R2 de decisiones, especificación, plan y autorización citados con hashes y no modificados |
| Separación de responsabilidades | Generador, IA revisora, auditor posterior y propietario distintos en los cinco documentos |
| Alcance limitado a ART-04 | Confirmado en los cinco documentos; los otros seis artefactos conservan sus criterios |
| No conversión IA en revisión humana | Confirmado; etiqueta obligatoria en todos los documentos |
| G5 y G6 | G5 condicionado; G6 intacto con sus cinco condiciones; dictamen IA no cierra puertas |
| Fase C | `NOT_GRANTED` en los cinco documentos |
| Ausencia de ciclos de aprobación | Confirmado: las decisiones aprobadas → enmiendas (D3-R3, spec R3, plan R3) → auditoría → aprobación → autorización R3 → ejecución. El protocolo R2 depende de las decisiones para su contenido, pero **no condiciona** la aprobación de las enmiendas; la autorización R3 **no depende** de la aprobación del protocolo. No hay ciclo. |
| Hallazgos de auditoría | Ocho resueltos individualmente en §5 |
| Contradicciones normativas detectadas | **Ninguna** |

No se detectaron contradicciones que obligaran a detener la preparación. Los cinco documentos requieren auditoría independiente antes de cualquier aprobación.

---

## 16. Estados y límites

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_PROTOCOL_R2: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

Este protocolo **no** aprueba las propuestas, **no** ejecuta revisión IA, **no** crea ART-04, **no** ejecuta G5/G6, **no** modifica R2 ni el diseño R9, **no** toca producción, tests, schemas, dependencias ni Parquet, y **no** realiza commits o push.

**Fin de R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R2.**
