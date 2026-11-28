# R13-ORACLE-ARTIFACTS-SPECIFICATION-R4 — Especificación Oracle (corrección R4)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta de corrección**. No aprobada. Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

---

## 1. Versión anterior conservada

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_artifacts_specification_r3.md` |
| SHA-256 de R3 | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` |
| Git hash de R3 | `6167d76a89a6bf4e37c1978c8357d732d7d4b7c9` |
| Base histórica | Especificación R2, SHA-256 `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |

R3 y R2 permanecen intactos.

---

## 2. Alcance de la corrección

R4 corrige AUD-ANT-03 (dependencias de ART-04), AUD-ANT-05 (preservación de 24 `rule_id` y 15 campos), AUD-ANT-06 (severidades y versión no disponible) y AUD-ANT-07 (columnas de la tabla heredada). No altera la jerarquía normativa ni los requisitos de los otros seis artefactos. El conjunto sigue siendo de **siete artefactos**.

La autoridad normativa es DEC-06, diseño v4 §9.2 y `manifest_v4.json`. La IA revisora **no** es fuente normativa.

---

## 3. ORACLE-ART-04-R4

### 3.1 Identidad y naturaleza

| Campo | Especificación R4 |
|---|---|
| Identificador estable | `ORACLE-ART-04` |
| Propósito | Evidenciar revisión independiente de la transcripción contra §9.2 por agente distinto del generador |
| Modalidades | `HUMAN_INDEPENDENT_REVIEW` (preferente) e `INDEPENDENT_AI_REVIEW` (excepcional, solo ART-04) |
| Dependencias | **`ORACLE-ART-01`, `ORACLE-ART-03`** (según R2 §4.4) |
| Estado propuesto | `NOT_CREATED` |

ART-02 se verifica **dentro del alcance de la revisión**, conforme a §3.6, pero **no** se declara dependencia formal de ART-04. No se crea dependencia sobre ART-05/06/07.

### 3.2 Diferencia entre modalidades

La revisión por IA nunca se denomina revisión humana. Ambas modalidades se registran con su etiqueta literal. El dictamen IA es técnico; la aceptación corresponde al propietario. La auditoría posterior es obligatoria en ambos casos y, para IA, incluye auditoría separada del informe.

### 3.3 Contenido mínimo obligatorio

1. identificador de revisión y modalidad;
2. identidad funcional del revisor (proveedor/modelo/versión cuando sea IA, sin nombre inventado);
3. declaración de independencia y limitaciones;
4. versión revisada (`ORACLE_NORMATIVE_V4_R5`) y hashes de las fuentes;
5. alcance: 139 rutas, **24 `rule_id`** (13 en allowlist + 11 de exclusión), nueve metadatos, ART-02, tipos, condiciones, nulabilidad y normalización;
6. casos examinados con matriz verificable y resultados positivos/negativos;
7. hallazgos con ID, severidad, fuente normativa, comprobación, resultado y resolución;
8. dictamen y confirmación de severidades por el auditor posterior;
9. fecha real y referencia a la evidencia original;
10. evidencia de aprobación del propietario, registrada por separado.

### 3.4 Evidencias obligatorias de la revisión IA

Proveedor y modelo distintos con linaje declarado; sesión limpia; fuentes originales; sin dictámenes previos en contexto; prompt íntegro y hashes de entradas; registro de respuestas y parámetros; reconstrucción hashable anterior a la comparación; matriz **139 rutas × 9 metadatos**; tabla de discrepancias; auditoría separada. Dos ejecuciones del mismo modelo no bastan.

### 3.5 Dictámenes y severidades (armonizado AUD-ANT-06)

Solo `ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED` e `INCONCLUSIVE`. Escala: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

- `ACCEPTED`: comprobaciones reproducidas sin discrepancias, sin limitaciones de independencia/reproducibilidad y sin hallazgos abiertos.
- `ACCEPTED_WITH_FINDINGS`: solo `MEDIUM` con resolución documentada y `LOW`/`INFO` **registrados y trazables**; sin `BLOCKER`/`HIGH`; sin contradicción normativa.
- `REJECTED`: contradicción normativa, discrepancia bloqueante o dependencia circular demostrada.
- `INCONCLUSIVE`: evidencia insuficiente, versión del modelo no disponible, contradicción no resuelta o independencia no demostrable.

`INCONCLUSIVE` y `REJECTED` no sustentan ART-04 ni desbloquean G5. `ACCEPTED_WITH_FINDINGS` no desbloquea G5 con `BLOCKER`/`HIGH` abiertos.

### 3.6 Relación con ART-01, ART-02 y ART-03 (corregido AUD-ANT-03)

- ART-01 es el objeto revisado, no fuente de los esperados.
- ART-02 se verifica contra la reconstrucción independiente de §9.2/R9 §5.4/schema; la comparación ART-01 ↔ ART-02 es secundaria y nunca prueba de corrección mutua. Su verificación forma parte del **alcance**, no de las dependencias de ART-04.
- ART-03 se verifica por recálculo JCS/SHA-256; el hash no demuestra corrección semántica.
- **Dependencias declaradas: ART-01, ART-03.** No se declara dependencia de ART-04 sobre ART-02, ART-05, ART-06 ni ART-07.

### 3.7 Criterios de aceptación (armonizado)

Revisión ejecutada y documentada; modalidad etiquetada; **independencia demostrada —una limitación no demostrable obliga a `INCONCLUSIVE`—**; hashes coincidentes; matriz y tabla de discrepancias completas; sin `BLOCKER`/`HIGH` abiertos; auditoría separada favorable; dictamen conforme a §3.5; fecha real; aprobación expresa.

### 3.8 Condiciones de rechazo

Registro vacío; revisor que es el generador; auditor que es la IA revisora; afirmación de revisión humana cuando se usó IA; ausencia de evidencia hashable; `INCONCLUSIVE`/`REJECTED`; `BLOCKER`/`HIGH` sin resolver; fuentes modificadas.

---

## 4. Matriz consolidada de aceptación (restaurada AUD-ANT-07)

Línea base histórica de R2 §5: los estados mostrados son los **declarados en R2**, no los corrientes, que se rigen por sus registros de verificación.

| Artefacto | Requisitos clave | Criterio de aceptación | Verificación independiente | CP-C | Dependencias | Estado actual (R2) |
|---|---|---|---|---|---|---|
| ORACLE-ART-01 | 139 rutas, diez campos, P1–P5, I1–I12 | Revisión semántica contra §9.2 | Revisor distinto del generador | 05, 13 | — | `NOT_CREATED` |
| ORACLE-ART-02 | Independiente, determinista, reproducible | Auditoría de independencia y resultados | Ejecución aislada | 05, 13 | 01 | `NOT_CREATED` |
| ORACLE-ART-03 | JCS y SHA-256 | Recálculo independiente | Verificador distinto | 05, 13 | 01, 02 | `NOT_CREATED` |
| **ORACLE-ART-04 (R4)** | Registro de revisión independiente, modalidad explícita, 24 `rule_id`, 15 campos, auditoría separada | Revisión real y documentada; §3.7 | Auditoría del registro y del informe IA si aplica | 05, 13 | **01, 03** | `NOT_CREATED` |
| ORACLE-ART-05 | 139 filas con semántica por ruta | Cobertura completa y correcta | Comparación de conjuntos | 05, 08 | 01, 02 | `NOT_CREATED` |
| ORACLE-ART-06 | Nueve metadatos por ruta | Sin divergencia no reportada | Comparación campo por campo | 05, 07, 13 | 01, 02, 05 | `NOT_CREATED` |
| ORACLE-ART-07 | Mutación aislada de `external_run_only` | Detección por oracle en tres rutas | Revisión de antes/después | 05, 08, 13 | 01, 02, 06 | `NOT_CREATED` |

---

## 5. Independencia y circularidad

Se mantienen los controles de R2 §6 y se añade: sesión limpia, sin resúmenes del generador, artefacto de reconstrucción hashable, autoridad de aceptación del propietario, auditor distinto y alcance confinado a ART-04. La verificación de consistencia se ejecuta fuera del camino productivo, sin fallback.

---

## 6. Trazabilidad y versiones

R1 → R2 (`0ede7956…`) → R3 (`d627f236…`) → **R4 (propuesta)**. Versiones anteriores conservadas. La adopción de R4 exige auditoría independiente y aprobación expresa; ningún hallazgo se declara cerrado en este documento.

---

## 7. Estados y límites

```text
NORMATIVE_AMENDMENTS: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_ANT_01_STATUS: INCONCLUSIVE
```

**Fin de R13-ORACLE-ARTIFACTS-SPECIFICATION-R4.**
