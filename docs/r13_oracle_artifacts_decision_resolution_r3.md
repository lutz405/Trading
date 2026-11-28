# R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R3 — Resolución de decisiones (enmienda de D3)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta documental** preparada con autorización expresa de las decisiones `DEC-OWNER-AI-01…06`. **No aprobada.** Sometida a auditoría independiente antes de cualquier aprobación.

```text
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
```

---

## 1. Versión anterior conservada

| Dato | Valor |
|---|---|
| Documento de origen | `docs/r13_oracle_artifacts_decision_resolution_r2.md` |
| SHA-256 de R2 | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| Git hash de R2 | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| Registro de aprobación de D1–D6 | `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` |
| Habilitación de esta enmienda | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md`, SHA-256 `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |

R2 se conserva **íntegramente** como registro histórico. Esta R3 **no modifica retroactivamente** ningún contenido aprobado: solo incorpora una versión nueva de la Decisión 3 (D3-R3).

---

## 2. Alcance de la modificación

| Decisión | Estado en R3 |
|---|---|
| D1 — Formato de `rule_id` | **Sin cambios**; se rige por R2 §3.1 |
| D2 — Ubicación física de artefactos | **Sin cambios**; se rige por R2 §3.2 |
| **D3 — Identidad del revisor** | **Única decisión enmendada**: se sustituye por D3-R3 (§3) |
| D4 — Formato de evidencias | **Sin cambios**; se rige por R2 §3.4 |
| D5 — Convención de versiones | **Sin cambios**; se rige por R2 §3.5 |
| D6 — Arquitectura de ART-02 | **Sin cambios**; se rige por R2 §3.6 |

No se introducen decisiones nuevas D7–D9 ni se reabre ninguna decisión DEC-01…DEC-09 del diseño R9.

---

## 3. D3-R3 — Identidad e independencia del revisor de ORACLE-ART-04

### 3.1 Antecedentes

D3 en R2 §3.3 exige revisión semántica por persona funcionalmente independiente, distinta del generador, con identidad funcional designada por el propietario e identidad real registrada al ejecutar. La auditoría del protocolo R1 clasificó como HIGH (AUD-AI-REV-R1-02) la omisión de la recomendación de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1, que exige revisor humano real. El propietario aprobó las decisiones `DEC-OWNER-AI-01`, `03`, `04` y `05` para superar esa recomendación exclusivamente mediante la modalidad regulada, conservando la recomendación original.

### 3.2 Decisión aprobada (texto)

> El propietario, habiendo examinado la recomendación literal de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1, autoriza **superarla exclusivamente** en el sentido de admitir la revisión automatizada regulada como sustituto de la revisión humana para ORACLE-ART-04, motivándolo en la indisponibilidad de revisor humano real. La recomendación original **se conserva íntegramente** en su documento y **no se borra ni se reinterpretan sus términos**; la superación se registra en una decisión versionada nueva con fecha real y referencia verificable. La vía humana sigue vigente para cualquier artefacto o revisión futura no cubierta por esta excepción.

> Se autoriza admitir la modalidad `INDEPENDENT_AI_REVIEW` **exclusivamente** para la revisión de ORACLE-ART-04, bajo los controles del protocolo R2 y previa resolución de DEC-OWNER-AI-02 a DEC-OWNER-AI-06. Esta modalidad **no equivale a revisión humana**, **no modifica** los requisitos de los artefactos ORACLE-ART-01/02/03/05/06/07, **no crea** una excepción general a las auditorías independientes y **no autoriza** la implementación de Fase C. La vía `HUMAN_INDEPENDENT_REVIEW` permanece válida y preferente.

### 3.3 Modalidades reconocidas

| Modalidad | Estado | Naturaleza |
|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | **Vía preferente**, vigente | Revisión semántica por persona real independiente, distinta del generador |
| `INDEPENDENT_AI_REVIEW` | **Vía excepcional**, solo ART-04 | Revisión técnica automatizada externa; **nunca** revisión humana |
| `AUTOMATED_INTERNAL_VERIFICATION` | Evidencia auxiliar | No sustenta ORACLE-ART-04 ni sustituye auditoría independiente |

### 3.4 Separación de responsabilidades

D3-R3 mantiene cuatro roles **inconfundibles y separados**:

1. **Generador** de ORACLE-ART-01/03 y de la evidencia: no puede actuar como revisor ni como auditor posterior.
2. **IA revisora**: emite dictamen técnico; no aprueba, no firma, no modifica fuentes.
3. **Auditor posterior**: distinto del generador y de la IA revisora; evalúa evidencia y confirma severidades con evaluación a ciegas.
4. **Propietario**: conserva exclusivamente la autoridad de aceptación mediante registro expreso.

### 3.5 Controles de independencia incorporados (DEC-OWNER-AI-04)

Proveedor y modelo distintos del generador con declaración de linaje; sesión limpia sin historial previo; fuentes normativas originales sin resúmenes derivados del generador; ausencia de dictámenes o conclusiones previos en el contexto inicial; prompt íntegro y hashes de todas las entradas; linaje y contexto registrados con inventario de herramientas y parámetros; reconstrucción independiente de las reglas en artefacto hashable anterior a la comparación; limitaciones expresamente declaradas. El mismo proveedor o una limitación no demostrable obliga a `INCONCLUSIVE`. Dos ejecuciones del mismo modelo **no** constituyen independencia suficiente.

### 3.6 Autoridad y aceptación incorporadas (DEC-OWNER-AI-05)

La IA revisora emite únicamente un dictamen técnico (`ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED`, `INCONCLUSIVE`) con severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`. El auditor posterior confirma severidades. El propietario decide la aceptación. `INCONCLUSIVE` y `REJECTED` no desbloquean G5; tampoco `ACCEPTED_WITH_FINDINGS` con hallazgos `BLOCKER`/`HIGH` sin resolver.

### 3.7 Criterio de aceptación verificable

ORACLE-ART-04 bajo `INDEPENDENT_AI_REVIEW` es aceptable solo si: modalidad autorizada y en vigor; controles de §3.5 cumplidos y registrados; dictamen no bloqueante; auditoría separada favorable; aceptación expresa del propietario; etiqueta `INDEPENDENT_AI_REVIEW` en todo registro. Sin independencia demostrable o con `INCONCLUSIVE`, se rechaza (fail-closed).

### 3.8 Intervención del propietario

**Sí.** Habilitación ya registrada en `R13-ORACLE-ART-04-AI-REVIEW-OWNER-DECISION-REGISTRATION-R1` (fecha `2026-11-27`, identidad funcional `Project Owner — TradingAI_BTC`). **La aprobación de esta R3 es un acto separado y pendiente**, posterior a su auditoría independiente.

---

## 4. Historial y trazabilidad de D3

| Versión | Contenido | Estado |
|---|---|---|
| R1 | Revisor humano; identidad funcional pendiente | Histórico |
| R2 (sha `6f408724…`) | Alternativa B: rol funcional e identidad real al ejecutar | Histórico, aprobado, **no modificado** |
| **R3 (este documento)** | D3-R3: excepción regulada para ART-04; vía humana preferente | **Propuesta pendiente de auditoría y aprobación** |

---

## 5. Compatibilidad con otros documentos

- Plan R3 §8 ajusta G5 exclusivamente para reflejar la modalidad autorizada.
- Especificación R3 §4.4 define el contenido de ART-04 bajo la modalidad.
- Autorización R3 levanta la prohibición de R2 §3 solo para esta modalidad y artefacto.
- Protocolo R2 implementa los controles operativos y resuelve los ocho hallazgos de auditoría.
- Diseño R9 permanece intacto (SHA-256 `884ee501…`).

Ninguno de estos documentos crea dependencia circular de aprobación: la autorización R3 depende de la aprobación de D3-R3, especificación R3 y plan R3; el protocolo R2 depende de las decisiones aprobadas para su contenido, pero **no condiciona** la aprobación de las enmiendas.

---

## 6. Estados y límites

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

Esta propuesta **no** aprueba la modalidad operativa, **no** crea ART-04, **no** ejecuta G5/G6, **no** autoriza Fase C y **no** modifica R2.

**Fin de R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R3.**
