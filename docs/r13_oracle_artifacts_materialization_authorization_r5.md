# R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R5 — Autorización de materialización (corrección R5)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** revisión documental R5. **NO está en vigor.** Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

```text
MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE
```

---

## 1. Versiones anteriores conservadas

| Documento | SHA-256 |
|---|---|
| Autorización R2 (histórica, `GRANTED`) | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| Autorización R3 | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` |
| Autorización R4 (corregida) | `2db94133ef1f01b9f8ef6884efac95243c95b69b2fff489aac64f83bab55b2ec` |

R2, R3 y R4 permanecen **íntegros**; R5 no los modifica retroactivamente.

---

## 2. Alcance de la corrección

R5 **no introduce cambios normativos** respecto de R4. Actualiza las referencias de versión a D3-R5, Especificación R5, Plan R5 y Protocolo R4, preservando literalmente la excepción aprobada y sus límites.

---

## 3. Excepción propuesta (DEC-OWNER-AI-02, texto literal conservado)

> Se autoriza preparar y aprobar una **Autorización de Materialización R3**, documento nuevo que conserva íntegramente la R2 como registro histórico (SHA-256 `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9`). R3 levanta la prohibición de R2 §3 **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04, registra la decisión habilitante, mantiene todos los demás límites de R2, surte efecto solo tras aprobadas la enmienda de D3, la especificación R3 y el plan R3, y se somete a auditoría independiente antes de su aprobación definitiva.

**Nota de versión:** el texto aprobado se conserva literalmente. En este paquete R5, las referencias a R3 se entienden referidas a D3-R5, Especificación R5 y Plan R5 una vez auditados y aprobados. La nota **no modifica** la decisión ni amplía su alcance.

### 3.1 Alcance del levantamiento

La prohibición de R2 §3 de omitir revisión humana queda superada **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04. Los siete artefactos, la auditoría independiente y los demás límites de R2 se conservan. La IA no se denomina revisora humana.

---

## 4. Condiciones previas a la entrada en vigor

R5 no surte efecto hasta que concurran:

1. D3-R5 auditado y aprobado;
2. Especificación R5 auditada y aprobada;
3. Plan R5 auditado y aprobado;
4. la propia autorización R5 auditada e independientemente favorable;
5. aprobación expresa del propietario del resultado de esa auditoría, en registro separado.

No se incluye la condición ambigua eliminada en R4 («protocolo R2 operativo»). La aprobación del Protocolo R4 es un **prerrequisito operativo de ejecución** (Protocolo R4 §3), no una condición de entrada en vigor de esta autorización. No se acepta aprobación implícita.

---

## 5. Alcance por artefacto

| Artefacto | Autorización | Modalidad de revisión |
|---|---|---|
| ORACLE-ART-01 | Según R2/D3-R5 | Según D3-R5; la modalidad se registra en **ORACLE-ART-04**, pudiendo ser `INDEPENDENT_AI_REVIEW` |
| ORACLE-ART-02 | Según R2 | Sin cambios |
| ORACLE-ART-03 | Según R2 | Sin cambios |
| **ORACLE-ART-04** | Único cambio respecto de R2 | `HUMAN_INDEPENDENT_REVIEW` (preferente) o `INDEPENDENT_AI_REVIEW` (excepcional) |
| ORACLE-ART-05/06/07 | Según R2 | Sin cambios |

No se amplía la autorización a artefactos distintos de ART-04.

---

## 6. Límites explícitos

No autoriza: Fase C ni fases D–G/S2; cierre automático de AUD-R8-02 ni G6 sin sus cinco condiciones; omisión de auditoría independiente; creación de ART-04 sin revisión y auditoría favorables; cambios en producción, schemas, dependencias, tests ni Parquet protegidos; modificación de artefactos no permitidos; ejecución automática de G5/G6; uso de `INCONCLUSIVE`/`REJECTED` como habilitante; extensión de la excepción; commits o push.

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

## 7. Verificación y estado

R2 SHA-256 `d692e49e…`; plan R2 `d4d0c689…`; diseño R9 `884ee501…`; registro de decisiones `3b6c946e…`; HEAD `259ca6ee…`, rama `main`.

```text
MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE
NORMATIVE_AMENDMENTS: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUDIT_VERDICT_R4: INCONCLUSIVE
AUD_ANT_01_STATUS: HIGH / INCONCLUSIVE
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

R5 no está en vigor, no crea ART-04, no ejecuta G5/G6 ni autoriza Fase C.

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R5.**
