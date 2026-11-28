# R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R4 — Resolución de decisiones (corrección R4)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta de corrección**. No aprobada. Estado de los hallazgos: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

---

## 1. Versión anterior conservada

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_artifacts_decision_resolution_r3.md` |
| SHA-256 de R3 | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` |
| Git hash de R3 | `fbbb05f9529e59b92a44fe65fca540d39839ec00` |
| Base histórica | Resolución R2, SHA-256 `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |

R3 y R2 permanecen **íntegros** como registros históricos. R4 no los sobrescribe ni modifica retroactivamente.

---

## 2. Alcance de la corrección

Esta R4 corrige **exclusivamente** la referencia interna observada en AUD-ANT-04 (sección 5: `Especificación R3 §4.4`, sección inexistente). El contenido normativo de D3-R3 se conserva literalmente: modalidad `INDEPENDENT_AI_REVIEW` solo para ORACLE-ART-04, vía humana preferente, separación de roles y controles `DEC-OWNER-AI-04`/`DEC-OWNER-AI-05`.

D1, D2, D4, D5 y D6 permanecen con el contenido aprobado en R2.

---

## 3. D3-R4 — Decisión 3 (texto conservado)

### 3.1 Antecedentes y superación documentada

D3 en R2 §3.3 exige revisión semántica por persona funcionalmente independiente, distinta del generador, con identidad funcional designada por el propietario e identidad real registrada al ejecutar. D3-R3 citó literalmente la recomendación de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1 y declaró su superación **exclusiva** para ORACLE-ART-04 mediante la modalidad regulada, conservando el texto original y la vía humana para todo lo demás. Esa redacción se conserva en R4 sin cambios.

### 3.2 Modalidades

| Modalidad | Estado | Naturaleza |
|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | Vía preferente, vigente | Persona real funcionalmente independiente |
| `INDEPENDENT_AI_REVIEW` | Vía excepcional, solo ART-04 | Revisión técnica automatizada externa; **nunca** revisión humana |
| `AUTOMATED_INTERNAL_VERIFICATION` | Evidencia auxiliar | No sustenta ART-04 ni sustituye auditoría |

### 3.3 Separación de responsabilidades

Generador, IA revisora, auditor posterior y propietario permanecen como cuatro roles separados e inconfundibles. El propietario conserva exclusivamente la autoridad de aceptación.

### 3.4 Controles incorporados

Se conservan los controles de `DEC-OWNER-AI-04` (proveedor/modelo distinto, sesión limpia, fuentes originales, sin dictámenes previos, prompt y hashes, linaje, reconstrucción hashable, limitaciones declaradas) y de `DEC-OWNER-AI-05` (cuatro dictámenes, severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`, IA propone, auditor confirma, propietario acepta). Dos ejecuciones del mismo modelo no constituyen independencia. `INCONCLUSIVE`/`REJECTED` no desbloquean G5.

### 3.5 Criterio de aceptación verificable

ORACLE-ART-04 bajo `INDEPENDENT_AI_REVIEW` es aceptable solo si: modalidad autorizada y en vigor; controles cumplidos y registrados; dictamen no bloqueante; auditoría separada favorable; aceptación expresa del propietario; etiqueta `INDEPENDENT_AI_REVIEW`. Sin independencia demostrable o con `INCONCLUSIVE`, se rechaza (fail-closed).

---

## 4. Corrección aplicada — AUD-ANT-04

| Referencia | Antes (R3 §5) | Después (R4 §5) | Verificación |
|---|---|---|---|
| Especificación | `Especificación R3 §4.4 define el contenido de ART-04…` | `Especificación R4 §3 define el contenido de ART-04…` | R4 §3 existe y contiene ART-04 (§3.1–§3.8) |
| Plan | `Plan R3` | `Plan R4` | Documento R4 preparado en este paquete |
| Autorización | `Autorización R3` | `Autorización R4` | Documento R4 preparado en este paquete |
| Protocolo | `protocolo R2` | `Protocolo R3 (corrección R2)` | Documento R3 preparado en este paquete |

No se modifica ningún otro texto normativo. La tabla completa de referencias internas figura en el paquete de correcciones.

---

## 5. Compatibilidad con otros documentos

Especificación R4 §3, Plan R4 §4 y Autorización R4 §3 reflejan la misma modalidad y alcance. Protocolo R3 implementa los controles. Ninguno crea dependencia circular: las decisiones aprobadas → enmiendas corregidas → auditoría → aprobación → autorización → ejecución.

---

## 6. Estados y límites

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_ANT_01_STATUS: INCONCLUSIVE
```

Esta propuesta **no** declara resuelto AUD-ANT-04, **no** aprueba la modalidad, **no** crea ART-04, **no** ejecuta G5/G6 ni autoriza Fase C.

**Fin de R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R4.**
