# R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R5 — Resolución de decisiones (corrección R5)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** revisión documental R5. **No aprobada ni auditada.** Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

---

## 1. Versión anterior conservada

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_artifacts_decision_resolution_r4.md` |
| SHA-256 de R4 | `a95f6af90b212d8539e1818ad3680a51762504fc9025cc1ae7d2436311b66ea5` |
| Git hash de R4 | `310915829fc90b04c3808c39092f0f58ef31e13c` |
| Base histórica | R3 `25ab2032…`, R2 `6f408724…` |

R4, R3, R2 y R1 permanecen **íntegros**.

---

## 2. Alcance de la corrección

R5 corrige **exclusivamente** `AUD-ANT-NEW-01`: imprecisión entre la tabla de §4 y la redacción efectiva de §5 de R4. No se modifica D3-R4, D1, D2, D4, D5 ni D6; no se cambia el alcance de `DEC-OWNER-AI-01…06`.

---

## 3. D3-R5 — Decisión 3 (texto conservado)

### 3.1 Antecedentes y superación documentada

D3 en R2 §3.3 exige revisión semántica por persona funcionalmente independiente, distinta del generador, con identidad funcional designada por el propietario e identidad real registrada al ejecutar. D3-R3/R4 citaron literalmente la recomendación de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1 y declararon su superación **exclusiva** para ORACLE-ART-04 mediante la modalidad regulada, conservando el texto original y la vía humana para todo lo demás. Esa redacción se conserva.

### 3.2 Modalidades

| Modalidad | Estado | Naturaleza |
|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | Vía preferente, vigente | Persona real funcionalmente independiente |
| `INDEPENDENT_AI_REVIEW` | Vía excepcional, solo ART-04 | Revisión técnica automatizada externa; **nunca** revisión humana |
| `AUTOMATED_INTERNAL_VERIFICATION` | Evidencia auxiliar | No sustenta ART-04 ni sustituye auditoría |

### 3.3 Separación de responsabilidades

Generador, IA revisora, auditor posterior y propietario permanecen como cuatro roles separados. El propietario conserva la autoridad de aceptación.

### 3.4 Controles incorporados

Se conservan los controles de `DEC-OWNER-AI-04` y `DEC-OWNER-AI-05` en los términos de R4 §3.4.

### 3.5 Criterio de aceptación verificable

Sin cambios respecto de R4 §3.5: modalidad autorizada y en vigor, controles cumplidos, dictamen no bloqueante, auditoría separada favorable, aceptación expresa del propietario y etiqueta `INDEPENDENT_AI_REVIEW`. Sin independencia demostrable o con `INCONCLUSIVE`, se rechaza (fail-closed).

---

## 4. Corrección aplicada — AUD-ANT-NEW-01

| Elemento | R4 (antes) | R5 (después) |
|---|---|---|
| Resumen de la tabla §4 | «`Especificación R4 §3 define el contenido de ART-04…`» | «`Especificación R5 §3, Plan R5 §4 y Autorización R5 §§2–4 reflejan la misma modalidad y alcance`» (texto literal de §5) |
| Destino de modalidad y alcance | Remisión genérica a `Autorización R4 §3` | Precisión: `Autorización R5 §2 (excepción y alcance), §4 (por artefacto) y §3 (condiciones de entrada en vigor)` |
| Referencias cruzadas | Plan R4, Autorización R4, Protocolo R3 | Plan R5, Autorización R5, Protocolo R4 |

La tabla de §4 reproducirá **literalmente** el texto de §5, de modo que resumen y redacción efectiva coincidan. Todas las secciones citadas existen en los documentos R5.

---

## 5. Compatibilidad con otros documentos

Especificación R5 §3, Plan R5 §4 y Autorización R5 §§2–4 reflejan la misma modalidad y alcance; el Protocolo R4 implementa los controles. No se crea dependencia circular: decisiones aprobadas → versiones corregidas → auditoría → aprobación → autorización → ejecución.

---

## 6. Estados y límites

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUDIT_VERDICT_R4: INCONCLUSIVE
AUD_ANT_01_STATUS: HIGH / INCONCLUSIVE
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

R5 **no** está aprobado ni auditado; la aprobación del propietario **no se presume**. Ningún hallazgo se declara cerrado.

**Fin de R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R5.**
