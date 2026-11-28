# R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R3 — Protocolo de revisión IA (corrección R3)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta de corrección**. No aprobada. Estado de los hallazgos: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

```text
AI_REVIEW_PROTOCOL_R3: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
```

---

## 1. Propósito y estado

Definir `INDEPENDENT_AI_REVIEW` exclusivamente para ORACLE-ART-04, incorporando las correcciones derivadas de AUD-ANT-02…07. **La revisión por IA nunca se denomina revisión humana.** Este protocolo no ejecuta revisión, no crea artefactos y no declara cerrados hallazgos.

---

## 2. Fuentes verificadas

| Fuente | SHA-256 |
|---|---|
| `r13_oracle_art_04_ai_independent_review_protocol_r2.md` (corregido) | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` |
| `r13_oracle_art_04_ai_independent_review_protocol_r1.md` (original) | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` |
| `r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| `r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| `r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| `r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| `r13_oracle_art_04_ai_review_owner_decision_package_r1.md` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` |
| `r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |
| `r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| `aud04b_model_provenance_v4_design.md` (§9.2) | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` |

---

## 3. Fundamento normativo y prerrequisitos operativos (AUD-ANT-02)

Decisiones `DEC-OWNER-AI-01…06` aprobadas; D3-R4, especificación R4, plan R4 y autorización R4 como versiones corregidas pendientes de auditoría y aprobación; diseño R9 como autoridad técnica.

**Distinción normativa:** la aprobación del protocolo **no** es condición de entrada en vigor de la autorización R4. Es un **prerrequisito operativo**: antes de ejecutar cualquier revisión bajo este protocolo deben concurrir, simultáneamente:

1. autorización R4 en vigor;
2. D3-R4, especificación R4 y plan R4 auditados y aprobados;
3. este protocolo aprobado y auditado;
4. fuentes originales y hashes verificados.

Esta redacción retira la condición ambigua de R2/R3 y preserva la autoridad del propietario.

---

## 4. Modalidades

| Modalidad | Naturaleza | ¿Sustenta ART-04? |
|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | Persona real independiente | Sí, vía preferente |
| `INDEPENDENT_AI_REVIEW` | IA de terceros | Sí, solo ART-04 y bajo este protocolo |
| `AUTOMATED_INTERNAL_VERIFICATION` | Verificadores internos | No; evidencia auxiliar |

---

## 5. Estado de los hallazgos anteriores (corregido AUD-ANT-06)

Los ocho hallazgos de la auditoría del protocolo R1 tienen una propuesta de cierre en este documento. Su estado es **`PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`** en todos los casos. Solo una auditoría independiente posterior puede confirmar el cierre técnico; la aceptación final corresponde al propietario.

| Hallazgo | Propuesta de cierre | Cláusula que la contiene | Estado |
|---|---|---|---|
| AUD-AI-REV-R1-01 | Autorización R4 sin condición ambigua; R2 preservado | §3, §6, §12 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-02 | D3-R4 cita y supera la recomendación sin borrarla | Resolución R4 §3.1; este §5 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-03 | Nueve controles de independencia | §6 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-04 | Reproducibilidad armonizada | §7 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-05 | Dictámenes, severidades y autoridad | §8 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-06 | Evidencia verificable, 24 `rule_id`, 15 campos | §9 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-07 | Auditor posterior distinto y a ciegas | §10 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-AI-REV-R1-08 | ART-02 sin circularidad | §11 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |

Las referencias internas antes rotas (`§5.01`, `§5.02`, `§6.1`, `§13`) se sustituyen por los encabezados reales de este documento (AUD-ANT-04).

---

## 6. Controles de independencia (DEC-OWNER-AI-04)

1. Proveedor y modelo distintos del generador, con linaje declarado.
2. Sesión limpia, sin historial previo; hash del manifiesto de apertura.
3. Fuentes normativas originales; prohibidos resúmenes del generador.
4. Sin dictámenes ni conclusiones previos en el contexto inicial; prompt íntegro con hash.
5. Hashes de todas las entradas y registro íntegro de respuestas.
6. Linaje y contexto: herramientas, parámetros y archivos leídos.
7. Reconstrucción independiente en artefacto hashable, anterior a la comparación.
8. Auditor posterior distinto del generador y de la IA, con evaluación a ciegas.
9. Limitaciones expresamente declaradas; limitación no demostrable ⇒ `INCONCLUSIVE`.

El mismo proveedor o dos ejecuciones del mismo modelo **no** constituyen independencia suficiente.

---

## 7. Reproducibilidad (armonizado AUD-ANT-06)

Modelo con identificador y versión exacta; si no está disponible: `NO_DISPONIBLE` y **`INCONCLUSIVE` para la revisión completa cuando una conclusión dependa de la identidad del modelo**. Parámetros de generación, prompt verbatim con hash, hashes de entradas, respuestas íntegras, repetición independiente cuando proceda. Las comprobaciones deterministas (hash, JCS, cobertura, metadatos) prevalecen; divergencia en la parte estocástica ⇒ `INCONCLUSIVE`. La discrepancia la resuelve el auditor posterior, nunca la IA.

---

## 8. Dictámenes, severidades y autoridad (armonizado AUD-ANT-06)

### 8.1 Dictámenes permitidos

| Dictamen | Criterio |
|---|---|
| `ACCEPTED` | Comprobaciones reproducidas sin discrepancias ni limitaciones de independencia/reproducibilidad; sin hallazgos abiertos |
| `ACCEPTED_WITH_FINDINGS` | Solo `MEDIUM` con resolución documentada y `LOW`/`INFO` **registrados y trazables**; sin `BLOCKER`/`HIGH`; sin contradicción normativa |
| `REJECTED` | Contradicción normativa, discrepancia bloqueante o dependencia circular |
| `INCONCLUSIVE` | Evidencia insuficiente, versión no disponible, contradicción no resuelta o independencia no demostrable |

### 8.2 Severidades

`BLOCKER` y `HIGH` bloquean; `MEDIUM` exige resolución documentada; `LOW` e `INFO` se registran y son trazables sin bloquear. Cualquier limitación de independencia o reproducibilidad se clasifica al menos `HIGH`.

### 8.3 Autoridad

La IA **propone** el dictamen y la severidad; el auditor posterior **evalúa y confirma**; el propietario **acepta** mediante registro expreso. El dictamen IA no equivale a aprobación. `INCONCLUSIVE` y `REJECTED` nunca desbloquean G5; `ACCEPTED_WITH_FINDINGS` tampoco con `BLOCKER`/`HIGH` abiertos.

---

## 9. Evidencia verificable (AUD-ANT-05)

### 9.1 Matriz

139 rutas × 9 metadatos (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`) con esperado, observado y resultado por celda. `rule_id` se mantiene separado.

### 9.2 Reconstrucción

Artefacto hashable e inmutable con reglas derivadas de §9.2/R9 §5.4/schema, anterior a la comparación; no derivado de ART-01 ni ART-02.

### 9.3 Casos

Por ruta: un positivo y cuatro negativos (ausencia, duplicación, ruta desconocida, divergencia), con error esperado y resultado.

### 9.4 Tabla de discrepancias

| ID | Ruta/campo | Severidad | Fuente normativa | Comprobación reproducible | Resultado | Resolución |
|---|---|---|---|---|---|---|

### 9.5 Vinculación

Cada conclusión se vincula a fuente normativa → comprobación → resultado verificable → entrada en la tabla.

### 9.6 Preservación de R1: 24 `rule_id` y 15 campos

**24 `rule_id` normativos** (D1, `R9-9.2-01…24`):

| Categoría | Identificadores |
|---|---|
| 13 usados por la allowlist | `R9-9.2-01`, `R9-9.2-03`, `R9-9.2-05`, `R9-9.2-07`, `R9-9.2-09`, `R9-9.2-10`, `R9-9.2-11`, `R9-9.2-12`, `R9-9.2-13`, `R9-9.2-14`, `R9-9.2-15`, `R9-9.2-19`, `R9-9.2-20` |
| 11 reglas de exclusión | `R9-9.2-02`, `R9-9.2-04`, `R9-9.2-06`, `R9-9.2-08`, `R9-9.2-16`, `R9-9.2-17`, `R9-9.2-18`, `R9-9.2-21`, `R9-9.2-22`, `R9-9.2-23`, `R9-9.2-24` |

**15 campos mínimos del registro de evidencia** (R1 §9, conservados en orden y significado):

1. Identificador de revisión.
2. Modalidad (`INDEPENDENT_AI_REVIEW`).
3. Proveedor y modelo de IA.
4. Fecha real y versión del modelo, si está disponible.
5. Identidad funcional del sistema revisor.
6. Hashes de todas las fuentes revisadas.
7. Fuentes normativas utilizadas.
8. Alcance y cobertura (139 rutas, 24 `rule_id`, nueve metadatos).
9. Método de reconstrucción independiente.
10. Pruebas realizadas.
11. Resultados reproducibles.
12. Hallazgos y severidad.
13. Limitaciones.
14. Dictamen.
15. Referencia a la evidencia original de la revisión (transcripción de la sesión, salida íntegra o artefacto equivalente).

No se inventan identificadores ni campos; no se cambia su significado. Los campos no disponibles se marcan `NO_DISPONIBLE` con explicación.

---

## 10. Auditoría posterior

Auditor distinto del generador y de la IA, designado funcionalmente, con evaluación a ciegas. Herramientas deterministas para hashes, JCS, cobertura y comparaciones; juicio humano para identidad, versión, fecha y aceptabilidad de limitaciones. Registros separados para el informe IA y la auditoría.

---

## 11. ART-02 sin circularidad

Reconstruir desde §9.2/R9 §5.4/schema sin usar ART-01 ni ART-02 como esperado; comparar ART-01 y ART-02 contra la reconstrucción; la comparación ART-01 ↔ ART-02 es secundaria; registrar hashes y divergencias. ART-02 se verifica como **alcance**, no como dependencia de ART-04.

---

## 12. Controles contra falsos positivos

Sin coincidencias superficiales; hash correcto ≠ corrección semántica; pruebas internas no son auditoría; sin trazabilidad normativa no se acepta conclusión; contradicción ⇒ `INCONCLUSIVE`/`REJECTED`; la IA no modifica fuentes; sin autorización R4 en vigor la revisión no produce efecto normativo.

---

## 13. Procedimiento A–H

| Etapa | Acción | Salida |
|---|---|---|
| A | Preparación de fuentes originales | Manifiesto de fuentes |
| B | Verificación de hashes | Tabla de hashes |
| C | Reconstrucción independiente, antes de D | Artefacto hashable |
| D | Comparación de reglas reconstruidas contra **ART-01/ART-02/ART-03 y fuentes normativas**; ART-05/06/07 como alcance auxiliar de correspondencia, **no como entrada ni dependencia de ART-04**; ART-04 es resultado de la revisión y **no se compara contra sí mismo** | Matriz y resultados |
| E | Análisis de discrepancias con severidades | Tabla de discrepancias |
| F | Integridad JCS/SHA-256 y reproducibilidad | Evidencia |
| G | Dictamen técnico propuesto | Dictamen |
| H | Limitaciones, trazabilidad y auditoría posterior | Registro completo |

El orden C antes de D es obligatorio.

---

## 14. Matriz de trazabilidad

| Decisión / hallazgo | Documento | Cláusula real |
|---|---|---|
| DEC-OWNER-AI-01 | Resolución R4, Especificación R4, Plan R4, este protocolo | §3.2 / §3.2 / §4 / §4 |
| DEC-OWNER-AI-02 | Autorización R4, este protocolo | §1–§3 / §3 |
| DEC-OWNER-AI-03 | Resolución R4, este protocolo | §3.1 / §5 (AUD-AI-REV-R1-02) |
| DEC-OWNER-AI-04 | Resolución R4, Especificación R4, este protocolo | §3.4 / §3.4 / §6, §10 |
| DEC-OWNER-AI-05 | Resolución R4, Especificación R4, este protocolo | §3.4 / §3.5 / §8 |
| DEC-OWNER-AI-06 | Autorización R4, Plan R4, este protocolo | §5 / §4.1 / §12 |
| AUD-AI-REV-R1-01 | Autorización R4, este protocolo | §3 / §3, §6, §12 |
| AUD-AI-REV-R1-02 | Resolución R4, este protocolo | §3.1 / §5 (AUD-AI-REV-R1-02) |
| AUD-AI-REV-R1-03 | este protocolo | §6 |
| AUD-AI-REV-R1-04 | este protocolo | §7 |
| AUD-AI-REV-R1-05 | este protocolo | §8 |
| AUD-AI-REV-R1-06 | Especificación R4, este protocolo | §3.3, §3.6 / §9 |
| AUD-AI-REV-R1-07 | este protocolo | §10 |
| AUD-AI-REV-R1-08 | Especificación R4, este protocolo | §3.6 / §11 |

---

## 15. Comprobación interna de consistencia

Realizada por el generador de las propuestas. **No es una auditoría independiente** y no declara hallazgos cerrados. Se verificó: coherencia entre los cinco documentos R4/R3; D1–D6 preservadas; jerarquía normativa intacta; 24 `rule_id` y 15 campos presentes; dependencias de ART-04 `01, 03`; referencias internas válidas; sin autorización implícita de Fase C; sin ampliación de alcance; correspondencia de cada corrección con su hallazgo. Resultado: propuesta coherente, pendiente de auditoría independiente.

---

## 16. Estados y límites

```text
AI_REVIEW_PROTOCOL_R3: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_ANT_01_STATUS: INCONCLUSIVE
```

Este protocolo no aprueba las versiones, no ejecuta revisión IA, no crea ART-04, no ejecuta G5/G6, no modifica R2/R3 ni fuentes, no toca producción, tests, schemas, dependencias ni Parquet, y no realiza commits o push.

**Fin de R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R3.**
