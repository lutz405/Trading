# R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R4 — Autorización de materialización (corrección R4)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta de corrección**. **NO está en vigor.** Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

```text
MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE
```

---

## 1. Versiones anteriores conservadas

| Documento | SHA-256 |
|---|---|
| Autorización R2 (histórica, `GRANTED`) | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| Autorización R3 (corregida) | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` |

R2 y R3 permanecen **íntegros**; R4 no los modifica retroactivamente.

---

## 2. Excepción propuesta (DEC-OWNER-AI-02, texto literal conservado)

> Se autoriza preparar y aprobar una **Autorización de Materialización R3**, documento nuevo que conserva íntegramente la R2 como registro histórico (SHA-256 `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9`). R3 levanta la prohibición de R2 §3 **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04, registra la decisión habilitante, mantiene todos los demás límites de R2, surte efecto solo tras aprobadas la enmienda de D3, la especificación R3 y el plan R3, y se somete a auditoría independiente antes de su aprobación definitiva.

**Nota de versión (AUD-ANT-04):** las referencias a R3 en el texto aprobado se conservan literalmente. En este paquete R4 se entienden referidas a sus versiones corregidas —D3-R4, especificación R4 y plan R4— una vez auditadas y aprobadas. Esta nota **no modifica** la decisión aprobada ni amplía su alcance.

### 2.1 Alcance del levantamiento

La prohibición de R2 §3 de omitir revisión humana queda superada **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04. Los siete artefactos, la auditoría independiente y todos los demás límites de R2 se conservan. La IA no se denomina revisora humana.

---

## 3. Condiciones previas a la entrada en vigor (corregido AUD-ANT-02)

R4 no surte efecto hasta que concurran:

1. D3-R4 auditado y aprobado;
2. Especificación R4 auditada y aprobada;
3. Plan R4 auditado y aprobado;
4. la propia autorización R4 auditada e independientemente favorable;
5. aprobación expresa del propietario del resultado de esa auditoría, en registro separado.

**Se elimina la condición 6 de R3** («protocolo R2 operativo»), que no figuraba en DEC-OWNER-AI-02 y era ambigua. La aprobación y ejecución del Protocolo R3 es un **prerrequisito operativo para ejecutar una revisión**, regulado en el Protocolo R3 §3, **no** una condición de entrada en vigor de esta autorización. Esta distinción preserva la autoridad del propietario y evita dependencias circulares.

No se acepta aprobación implícita, presunta o derivada de las seis decisiones aprobadas.

---

## 4. Alcance por artefacto (corregido AUD-ANT-03)

| Artefacto | Autorización | Modalidad de revisión |
|---|---|---|
| ORACLE-ART-01 | Según R2/D3-R4 | Según D3-R4; la modalidad se registra en **ORACLE-ART-04**, pudiendo ser `INDEPENDENT_AI_REVIEW` |
| ORACLE-ART-02 | Según R2 | Sin cambios |
| ORACLE-ART-03 | Según R2 | Sin cambios |
| **ORACLE-ART-04** | Único cambio respecto de R2 | `HUMAN_INDEPENDENT_REVIEW` (preferente) o `INDEPENDENT_AI_REVIEW` (excepcional) |
| ORACLE-ART-05/06/07 | Según R2 | Sin cambios |

Se retira la asignación `HUMAN_INDEPENDENT_REVIEW` a ORACLE-ART-01 que figuraba en R3 §4, pues ORACLE-ART-04 es el registro de revisión de ART-01 y la excepción regulada permite modalidad IA para ese registro. No se amplía la autorización a artefactos distintos de ART-04.

---

## 5. Límites explícitos (heredados de R2 y DEC-OWNER-AI-06)

No autoriza: Fase C ni fases D–G/S2; cierre automático de AUD-R8-02 ni G6 sin sus cinco condiciones; omisión de auditoría independiente; creación de ART-04 sin revisión y auditoría favorables; cambios en producción, schemas, dependencias, tests ni Parquet; modificación de artefactos no permitidos; ejecución automática de G5/G6; uso de `INCONCLUSIVE`/`REJECTED` como habilitante; extensión de la excepción; commits o push.

```text
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_D_AUTHORIZATION: NOT_GRANTED
PHASE_E_AUTHORIZATION: NOT_GRANTED
PHASE_F_AUTHORIZATION: NOT_GRANTED
PHASE_G_AUTHORIZATION: NOT_GRANTED
S2_AUTHORIZATION: NOT_GRANTED
```

---

## 6. Verificación de referencias y estado

R2 SHA-256 `d692e49e…`; plan R2 `d4d0c689…`; diseño R9 `884ee501…`; registro de decisiones `3b6c946e…`; HEAD `259ca6ee…`, rama `main`.

```text
MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_ANT_01_STATUS: INCONCLUSIVE
```

Esta propuesta no está en vigor, no crea ART-04, no ejecuta G5/G6 ni autoriza Fase C. Ningún hallazgo se declara cerrado.

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R4.**
