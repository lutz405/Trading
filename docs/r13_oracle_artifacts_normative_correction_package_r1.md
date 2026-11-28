# R13-ORACLE-ARTIFACTS-NORMATIVE-CORRECTION-PACKAGE-R1 — Paquete de correcciones R4

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** paquete documental de propuestas. **No** aprueba versiones, **no** declara cerrados hallazgos, **no** sustituye auditoría independiente.

---

## 1. Versiones nuevas identificadas

| ID | Documento nuevo | Documento corregido | SHA-256 nuevo | Git hash |
|---|---|---|---|---|
| N-01 | `docs/r13_oracle_artifacts_decision_resolution_r4.md` | Decisión R3 (`25ab2032…`) | `a95f6af90b212d8539e1818ad3680a51762504fc9025cc1ae7d2436311b66ea5` | `310915829fc90b04c3808c39092f0f58ef31e13c` |
| N-02 | `docs/r13_oracle_artifacts_specification_r4.md` | Especificación R3 (`d627f236…`) | `ff722887189e6e5ca223e3699fae34b870c09d36810f81680b26689d978c1ba5` | `2bdae65282062979a49191970640de123a52dfce` |
| N-03 | `docs/r13_oracle_artifacts_materialization_plan_r4.md` | Plan R3 (`2f6f48a2…`) | `226c51d08a3171232098f40d4e22cf0d2d1487a1c373aa480e69d5651da63e71` | `aa8c03700edf5c78b1a7602ce92e9f900c7924a8` |
| N-04 | `docs/r13_oracle_artifacts_materialization_authorization_r4.md` | Autorización R3 (`7571faf5…`) | `2db94133ef1f01b9f8ef6884efac95243c95b69b2fff489aac64f83bab55b2ec` | `75c0790733930e9a6b4514c32afe42810a7728f6` |
| N-05 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r3.md` | Protocolo R2 (`6a095901…`) | `e538b144b575843ad528faf9220e1f6bffbf2f4a90710539b87032101d1e3f75` | `6c972eedfbb747c00da50d28d6ef078bf57238e9` |

Las cinco versiones R3/R2 precedentes permanecen intactas; sus hashes se verificaron antes y después de la preparación.

---

## 2. Hallazgos abordados y estado

| Hallazgo | Documento(s) que lo abordan | Estado |
|---|---|---|
| AUD-ANT-02 | N-04 §3, N-05 §3 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-ANT-03 | N-02 §3.1/§3.6/§4, N-03 §2, N-04 §4, N-05 §13 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-ANT-04 | N-01 §4, N-05 §5, §14 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-ANT-05 | N-02 §3.3, N-05 §9.6 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-ANT-06 | N-02 §3.5/§3.7, N-05 §5, §7, §8 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-ANT-07 | N-02 §4, N-03 §1/§4 | `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| AUD-ANT-01 | No se modifica | `INCONCLUSIVE` (sin cambios) |

---

## 3. Tabla de cambios exactos

| ID | Ubicación | Antes | Después |
|---|---|---|---|
| C-02-01 | Autorización R3 §3.6 | «6. protocolo R2 operativo…» como condición de entrada en vigor | Condición eliminada; prerrequisito operativo trasladado a Protocolo R3 §3 |
| C-03-01 | Especificación R3 §3.6 | «Dependencias declaradas: ART-01, ART-02, ART-03» | «Dependencias declaradas: ART-01, ART-03»; ART-02 como alcance, no dependencia |
| C-03-02 | Protocolo R2 §13 Etapa D | «ART-01/02/03/04/05/06/07» como objetos de comparación | ART-01/02/03 y fuentes; ART-05/06/07 como alcance auxiliar; ART-04 no se compara contra sí mismo |
| C-03-03 | Autorización R3 §4 | ART-01 → `HUMAN_INDEPENDENT_REVIEW` | ART-01 → modalidad según D3-R4, registrada en ART-04 (puede ser IA) |
| C-04-01 | Decisión R3 §5 | «Especificación R3 §4.4» | «Especificación R4 §3» |
| C-04-02 | Protocolo R2 §5 y §14 | `§5.01`, `§5.02`, `§6.1`, remisión a `§13` | Encabezados reales: `§5 (AUD-AI-REV-R1-01/02)`, `§6`, `§12`; remisión a Resolución R4 §3.1 |
| C-05-01 | Protocolo R2 §9 | Sin listas explícitas de 24 `rule_id` ni 15 campos | §9.6 con 13 usados + 11 exclusión y 15 campos de R1 §9 |
| C-06-01 | Protocolo R2 §5 | Ocho etiquetas `RESUELTO` | Ocho etiquetas `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT` |
| C-06-02 | Especificación R3 §3.5 / Protocolo R2 §8 | `LOW`/`INFO` «resueltos» frente a «no bloqueantes» | Regla única: `BLOCKER`/`HIGH` bloquean, `MEDIUM` requiere resolución, `LOW`/`INFO` se registran |
| C-06-03 | Protocolo R2 §7 | Versión no disponible ⇒ `INCONCLUSIVE` «para lo que dependa de él» | `INCONCLUSIVE` para la revisión cuando una conclusión dependa de la identidad del modelo |
| C-07-01 | Especificación R3 §4 | Tabla sin `CP-C` ni `Estado actual` | Columnas restauradas con nota de línea base histórica |
| C-07-02 | Plan R3 §1 | «modifica exclusivamente §7 y §8» | «modifica G5/§8, roles §7, decisiones §10 y estado §11; G0–G4 y G6 conservan contenido» |
| C-07-03 | Plan R3 §4 G0–G2 | Referencias solo a R2 | Referencias a R4 con línea base R2 conservada |

---

## 4. Matriz de trazabilidad

| Decisión / hallazgo | Documento | Cláusula | Cambio |
|---|---|---|---|
| DEC-OWNER-AI-01 | N-01, N-02, N-03, N-05 | §3.2 / §3.2 / §4 / §4 | Sin cambio de alcance |
| DEC-OWNER-AI-02 | N-04, N-05 | §1–3 / §3 | C-02-01 |
| DEC-OWNER-AI-03 | N-01, N-05 | §3.1 / §5 | Sin cambio |
| DEC-OWNER-AI-04 | N-01, N-02, N-05 | §3.4 / §3.4 / §6, §10 | Sin cambio |
| DEC-OWNER-AI-05 | N-01, N-02, N-05 | §3.4 / §3.5 / §8 | C-06-02, C-06-03 |
| DEC-OWNER-AI-06 | N-04, N-03, N-05 | §5 / §4.1 / §12 | Sin cambio |
| AUD-ANT-02 | N-04, N-05 | §3 / §3 | C-02-01 |
| AUD-ANT-03 | N-02, N-03, N-04, N-05 | §3.6/§4 / §2 / §4 / §13 | C-03-01, C-03-02, C-03-03 |
| AUD-ANT-04 | N-01, N-05 | §4 / §5, §14 | C-04-01, C-04-02 |
| AUD-ANT-05 | N-02, N-05 | §3.3 / §9.6 | C-05-01 |
| AUD-ANT-06 | N-02, N-05 | §3.5/§3.7 / §5, §7, §8 | C-06-01, C-06-02, C-06-03 |
| AUD-ANT-07 | N-02, N-03 | §4 / §1, §4 | C-07-01, C-07-02, C-07-03 |

---

## 5. Matriz de referencias internas (antes/después)

| Documento | Referencia anterior | ¿Existía? | Referencia nueva | Verificación |
|---|---|---|---|---|
| Decisión R3 §5 | Especificación `§4.4` | No (ART-04 estaba en §3) | Especificación R4 `§3` | Existe §3.1–§3.8 |
| Protocolo R2 §5 | `§5.01` | No | `§5 (AUD-AI-REV-R1-01)` | Encabezado real |
| Protocolo R2 §5 | `§5.02` | No | `§5 (AUD-AI-REV-R1-02)` | Encabezado real |
| Protocolo R2 §5 | `§6.1` | No (§6 es lista 1–9) | `§6` | Sección real |
| Protocolo R2 §5 | `§13` para R1-02 | No trataba ese hallazgo | Resolución R4 `§3.1` | Sección real |
| Protocolo R2 §14 | `§5.01`, `§5.02`, `§6.1` | No | Encabezados reales | Matriz N-05 §14 |
| Autorización R3 §3.6 | «protocolo R2 operativo» | Condición ambigua | Eliminada; N-05 §3 | Ambas secciones verificadas |

---

## 6. Matriz de preservación de 24 `rule_id`

| Categoría | Identificadores exactos | Cantidad | Ubicación |
|---|---|---|---|
| Usados por la allowlist | `R9-9.2-01`, `R9-9.2-03`, `R9-9.2-05`, `R9-9.2-07`, `R9-9.2-09`, `R9-9.2-10`, `R9-9.2-11`, `R9-9.2-12`, `R9-9.2-13`, `R9-9.2-14`, `R9-9.2-15`, `R9-9.2-19`, `R9-9.2-20` | 13 | N-05 §9.6 |
| Reglas de exclusión | `R9-9.2-02`, `R9-9.2-04`, `R9-9.2-06`, `R9-9.2-08`, `R9-9.2-16`, `R9-9.2-17`, `R9-9.2-18`, `R9-9.2-21`, `R9-9.2-22`, `R9-9.2-23`, `R9-9.2-24` | 11 | N-05 §9.6 |
| **Total** | `R9-9.2-01…24` | **24** | D1; R1 §6; ORACLE-ART-01 |

Ningún identificador se inventa, omite o cambia de significado. Los 13 usados se verificaron contra ORACLE-ART-01 (139 entradas, 13 distintos).

---

## 7. Matriz de preservación de 15 campos

| # | Campo (R1 §9) | Ubicación en N-05 §9.6 | Cambio de significado |
|---|---|---|---|
| 1 | Identificador de revisión | Lista numerada | No |
| 2 | Modalidad (`INDEPENDENT_AI_REVIEW`) | Lista numerada | No |
| 3 | Proveedor y modelo de IA | Lista numerada | No |
| 4 | Fecha real y versión del modelo, si está disponible | Lista numerada | No |
| 5 | Identidad funcional del sistema revisor | Lista numerada | No |
| 6 | Hashes de todas las fuentes revisadas | Lista numerada | No |
| 7 | Fuentes normativas utilizadas | Lista numerada | No |
| 8 | Alcance y cobertura (139 rutas, 24 `rule_id`, nueve metadatos) | Lista numerada | No |
| 9 | Método de reconstrucción independiente | Lista numerada | No |
| 10 | Pruebas realizadas | Lista numerada | No |
| 11 | Resultados reproducibles | Lista numerada | No |
| 12 | Hallazgos y severidad | Lista numerada | No |
| 13 | Limitaciones | Lista numerada | No |
| 14 | Dictamen | Lista numerada | No |
| 15 | Referencia a la evidencia original de la revisión | Lista numerada | No |

---

## 8. Dependencias entre correcciones

1. **AUD-ANT-04 y AUD-ANT-07** son correcciones documentales independientes; pueden aprobarse primero.
2. **AUD-ANT-03** debe preceder a cualquier auditoría porque afecta dependencias y circularidad.
3. **AUD-ANT-02** depende de la redacción final del protocolo (N-05 §3).
4. **AUD-ANT-05 y AUD-ANT-06** requieren coherencia entre N-02 y N-05.
5. **AUD-ANT-01** permanece `INCONCLUSIVE` y exige auditor con proveedor acreditado.
6. No hay ciclo: decisiones → versiones corregidas → auditoría → aprobación → autorización → ejecución.

---

## 9. Comprobación interna de consistencia

Realizada por el generador de las propuestas. **No es auditoría independiente** y no declara hallazgos cerrados.

| # | Comprobación | Resultado |
|---|---|---|
| 1 | Consistencia entre los cinco documentos nuevos | Sin contradicción detectada |
| 2 | Correspondencia con D1–D6 | Confirmada; solo D3 corregida |
| 3 | Jerarquía normativa | DEC-06 / §9.2 / schema conservada; IA no es fuente |
| 4 | 24 `rule_id` | 13 + 11 presentes en N-05 §9.6 |
| 5 | 15 campos de registro | Presentes en N-05 §9.6 |
| 6 | Dependencias de siete artefactos | ART-04 = `01, 03`; ART-02 como alcance |
| 7 | Referencias internas válidas | Matriz §5; todas existen en los documentos nuevos |
| 8 | Autorización implícita de Fase C | Ausente; `NOT_GRANTED` en los cinco |
| 9 | Cambios de alcance | Ninguno; ART-04 sigue siendo el único artefacto afectado |
| 10 | Correspondencia corrección-hallazgo | Matriz §4 |

---

## 10. Riesgos y limitaciones

- Este paquete y su comprobación interna provienen del **generador** de las propuestas; requieren auditoría independiente.
- AUD-ANT-01 sigue `INCONCLUSIVE`: no se acredita proveedor distinto del generador.
- Las versiones nuevas **no** están aprobadas; su entrada en vigor exige auditoría y aprobación expresa.
- Si se aprueban las correcciones sin reauditoría, podrían cerrarse hallazgos sin evidencia de ejecución.
- La deliberada conservación del texto literal de DEC-OWNER-AI-02 (que menciona R3) exige la nota de versión de N-04 §2 para evitar confusión con R4.
- No se han ejecutado pruebas de la revisión IA ni se ha materializado ART-04.

---

## 11. Estados finales

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_PROTOCOL_R3: PREPARED_PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_ANT_01_STATUS: INCONCLUSIVE
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin commits ni push. No se modificaron R3, fuentes originales, manifiesto, artefactos, producción, tests, schemas, dependencias ni Parquet. No se creó ART-04 ni se ejecutaron G5/G6.

**Fin de R13-ORACLE-ARTIFACTS-NORMATIVE-CORRECTION-PACKAGE-R1.**
