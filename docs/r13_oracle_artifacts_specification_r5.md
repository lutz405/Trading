# R13-ORACLE-ARTIFACTS-SPECIFICATION-R5 — Especificación Oracle (corrección R5)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** revisión documental R5. **No aprobada ni auditada.** Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

---

## 1. Versión anterior conservada

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_artifacts_specification_r4.md` |
| SHA-256 de R4 | `ff722887189e6e5ca223e3699fae34b870c09d36810f81680b26689d978c1ba5` |
| Git hash de R4 | `2bdae65282062979a49191970640de123a52dfce` |
| Base histórica | R3 `d627f236…`, R2 `0ede7956…` |

R4 y sus predecesores permanecen intactos.

---

## 2. Alcance de la corrección

R5 **no introduce cambios normativos** respecto de R4. Actualiza únicamente las referencias de versión (R4 → R5, Protocolo R3 → R4) para mantener la coherencia del paquete. Se preservan íntegramente la jerarquía normativa, los siete artefactos, las 139 rutas, los nueve metadatos, los 24 `rule_id`, los 15 campos de R1 §9, las dependencias y los estados.

La autoridad normativa es DEC-06, diseño v4 §9.2 y `manifest_v4.json`. La IA revisora no es fuente normativa.

---

## 3. ORACLE-ART-04-R5

### 3.1 Identidad y naturaleza

| Campo | Especificación R5 |
|---|---|
| Identificador estable | `ORACLE-ART-04` |
| Propósito | Evidenciar revisión independiente de la transcripción contra §9.2 por agente distinto del generador |
| Modalidades | `HUMAN_INDEPENDENT_REVIEW` (preferente) e `INDEPENDENT_AI_REVIEW` (excepcional, solo ART-04) |
| Dependencias | **`ORACLE-ART-01`, `ORACLE-ART-03`** (según R2 §4.4) |
| Estado propuesto | `NOT_CREATED` |

ART-02 se verifica dentro del **alcance** de la revisión (§3.6), sin ser dependencia formal. No se crea dependencia sobre ART-05/06/07 ni octavo artefacto.

### 3.2 Diferencia entre modalidades

La revisión por IA nunca se denomina revisión humana. Ambas se registran con su etiqueta literal; el dictamen IA es técnico y la aceptación corresponde al propietario. La auditoría posterior es obligatoria.

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

Los 15 campos mínimos del registro se conservan en Protocolo R4 §9.6.

### 3.4 Evidencias obligatorias de la revisión IA

Proveedor y modelo distintos con linaje declarado; sesión limpia; fuentes originales; sin dictámenes previos en contexto; prompt íntegro y hashes de entradas; registro de respuestas y parámetros; reconstrucción hashable anterior a la comparación; matriz **139 rutas × 9 metadatos** —`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`, con `rule_id` separado—; tabla de discrepancias; auditoría separada. Dos ejecuciones del mismo modelo no bastan.

### 3.5 Dictámenes y severidades

Solo `ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED` e `INCONCLUSIVE`. Escala `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

`ACCEPTED_WITH_FINDINGS`: solo `MEDIUM` con resolución documentada y `LOW`/`INFO` **registrados y trazables**; sin `BLOCKER`/`HIGH`. **`INCONCLUSIVE` de forma incondicional** ante versión del modelo no disponible, evidencia insuficiente, contradicción no resuelta o independencia no demostrable. `INCONCLUSIVE`/`REJECTED` no sustentan ART-04 ni desbloquean G5.

### 3.6 Relación con ART-01, ART-02 y ART-03

ART-01 es el objeto revisado, no fuente de los esperados. ART-02 se verifica contra la reconstrucción independiente de §9.2/R9 §5.4/schema; su comparación con ART-01 es secundaria. ART-03 se verifica por recálculo JCS/SHA-256. **Dependencias declaradas: ART-01, ART-03.** ART-02 es alcance, no dependencia; no hay dependencia sobre ART-05/06/07.

### 3.7 Criterios de aceptación

Revisión ejecutada y documentada; modalidad etiquetada; independencia demostrada (limitación no demostrable ⇒ `INCONCLUSIVE`); hashes coincidentes; matriz y tabla de discrepancias completas; sin `BLOCKER`/`HIGH` abiertos; auditoría separada favorable; dictamen conforme a §3.5; fecha real; aprobación expresa.

### 3.8 Condiciones de rechazo

Registro vacío; revisor que es el generador; auditor que es la IA; falsa revisión humana; ausencia de evidencia hashable; `INCONCLUSIVE`/`REJECTED`; `BLOCKER`/`HIGH` sin resolver; fuentes modificadas.

---

## 4. Matriz consolidada de aceptación

Línea base histórica de R2 §5; los estados son los declarados en R2, no los corrientes.

| Artefacto | Requisitos clave | Criterio de aceptación | Verificación independiente | CP-C | Dependencias | Estado actual (R2) |
|---|---|---|---|---|---|---|
| ORACLE-ART-01 | 139 rutas, diez campos, P1–P5, I1–I12 | Revisión semántica contra §9.2 | Revisor distinto del generador | 05, 13 | — | `NOT_CREATED` |
| ORACLE-ART-02 | Independiente, determinista, reproducible | Auditoría de independencia y resultados | Ejecución aislada | 05, 13 | 01 | `NOT_CREATED` |
| ORACLE-ART-03 | JCS y SHA-256 | Recálculo independiente | Verificador distinto | 05, 13 | 01, 02 | `NOT_CREATED` |
| **ORACLE-ART-04 (R5)** | Registro de revisión independiente, modalidad explícita, 24 `rule_id`, 15 campos, auditoría separada | Revisión real y documentada; §3.7 | Auditoría del registro y del informe IA si aplica | 05, 13 | **01, 03** | `NOT_CREATED` |
| ORACLE-ART-05 | 139 filas con semántica por ruta | Cobertura completa y correcta | Comparación de conjuntos | 05, 08 | 01, 02 | `NOT_CREATED` |
| ORACLE-ART-06 | Nueve metadatos por ruta | Sin divergencia no reportada | Comparación campo por campo | 05, 07, 13 | 01, 02, 05 | `NOT_CREATED` |
| ORACLE-ART-07 | Mutación aislada de `external_run_only` | Detección por oracle en tres rutas | Revisión de antes/después | 05, 08, 13 | 01, 02, 06 | `NOT_CREATED` |

---

## 5. Independencia y circularidad

Se mantienen los controles de R2 §6 y de R4 §5: sesión limpia, sin resúmenes del generador, reconstrucción hashable, autoridad de aceptación del propietario, auditor distinto y alcance confinado a ART-04. Sin fallback; verificación fuera del camino productivo.

---

## 6. Trazabilidad y versiones

R1 → R2 (`0ede7956…`) → R3 (`d627f236…`) → R4 (`ff722887…`) → **R5 (propuesta)**. Versiones anteriores conservadas. La adopción de R5 exige auditoría independiente y aprobación expresa.

---

## 7. Estados y límites

```text
NORMATIVE_AMENDMENTS: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUDIT_VERDICT_R4: INCONCLUSIVE
AUD_ANT_01_STATUS: HIGH / INCONCLUSIVE
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

**Fin de R13-ORACLE-ARTIFACTS-SPECIFICATION-R5.**
