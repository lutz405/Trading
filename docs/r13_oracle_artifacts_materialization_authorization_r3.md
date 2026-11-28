# R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R3 — Autorización de materialización (propuesta)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta documental**. **NO está en vigor.** No confiere autorización ejecutable hasta su propia auditoría independiente y aprobación expresa.

```text
MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
```

---

## 1. Preservación de la versión anterior

| Dato | Valor |
|---|---|
| Documento de origen | `docs/r13_oracle_artifacts_materialization_authorization_r2.md` |
| SHA-256 de R2 | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| Git hash de R2 | `33693367f38ca579864d5ea98ebb8aa63918011d` |
| Estado de R2 | `GRANTED`; **se conserva íntegramente como registro histórico** |
| Habilitación de esta propuesta | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md`, SHA-256 `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |

R3 **no modifica retroactivamente** R2. R2 sigue siendo la autorización vigente; esta propuesta solo describe la versión futura que el propietario podría aprobar.

---

## 2. Excepción propuesta (DEC-OWNER-AI-02)

> Se autoriza preparar y aprobar una **Autorización de Materialización R3**, documento nuevo que conserva íntegramente la R2 como registro histórico (SHA-256 `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9`). R3 levanta la prohibición de R2 §3 **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04, registra la decisión habilitante, mantiene todos los demás límites de R2, surte efecto solo tras aprobadas la enmienda de D3, la especificación R3 y el plan R3, y se somete a auditoría independiente antes de su aprobación definitiva.

### 2.1 Alcance exacto del levantamiento

| Elemento | Antes (R2 §3) | Después (R3 propuesto) |
|---|---|---|
| «Omitir revisión humana independiente» | Prohibido | **Permitido únicamente** mediante `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04 |
| Cualquier otro artefacto | Sin cambios | Sin cambios: sigue exigiéndose revisión humana independiente |
| Auditoría independiente de los siete artefactos | Obligatoria | Obligatoria, sin excepción |
| G6, AUD-R8-02, Fase C | Sin cambios | Sin cambios |

La excepción **no convierte** la revisión IA en revisión humana y **no crea** una excepción general a las auditorías independientes.

---

## 3. Condiciones previas a la entrada en vigor

R3 no surte efecto hasta que concurran **todas**:

1. D3-R3 (`docs/r13_oracle_artifacts_decision_resolution_r3.md`) auditado y aprobado;
2. Especificación R3 (`docs/r13_oracle_artifacts_specification_r3.md`) auditada y aprobada;
3. Plan R3 (`docs/r13_oracle_artifacts_materialization_plan_r3.md`) auditado y aprobado;
4. la propia autorización R3 auditada e independientemente favorable;
5. aprobación expresa del propietario del resultado de esa auditoría, en registro separado;
6. protocolo R2 operativo conforme a `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md`.

No se acepta aprobación implícita, presunta o derivada de la aprobación de las seis decisiones.

---

## 4. Alcance de la autorización futura

| Artefacto | Autorización | Modalidad de revisión |
|---|---|---|
| ORACLE-ART-01 | Según R2 | `HUMAN_INDEPENDENT_REVIEW` |
| ORACLE-ART-02 | Según R2 | Sin cambios |
| ORACLE-ART-03 | Según R2 | Sin cambios |
| **ORACLE-ART-04** | Según R3, solo cambio | `HUMAN_INDEPENDENT_REVIEW` (preferente) o `INDEPENDENT_AI_REVIEW` (excepcional) |
| ORACLE-ART-05/06/07 | Según R2 | Sin cambios |

El conjunto sigue siendo de siete artefactos. No se amplía la autorización a artefactos distintos de ORACLE-ART-04.

---

## 5. Límites explícitos (heredados y nuevos)

La futura R3 **NO** concede permiso para:

- implementar Fase C ni autorizar fases D, E, F, G o S2;
- cerrar automáticamente AUD-R8-02 ni declarar G6 superada sin sus cinco condiciones;
- omitir auditoría independiente de los siete artefactos;
- crear ORACLE-ART-04 sin revisión y auditoría favorables;
- modificar producción, schemas, dependencias, tests ni Parquet protegidos;
- modificar artefactos Oracle distintos de los permitidos por R2/R3;
- ejecutar G5/G6 automáticamente: un dictamen IA no cierra puertas;
- tratar `INCONCLUSIVE` o `REJECTED` como resultado habilitante;
- extenderse a otros artefactos ni convertir la IA en revisora humana;
- realizar commits o push por esta autorización.

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

## 6. Verificación de referencias

| Referencia | Valor verificado |
|---|---|
| R2 SHA-256 | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| Plan R2 SHA-256 | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| Diseño R9 SHA-256 | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| Registro de decisiones SHA-256 | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |
| HEAD / rama | `259ca6ee11878f114cdcab4cef500074b3bc1a48`, `main`, alineado |

---

## 7. Estado y cierre

Esta propuesta **no está en vigor**. No crea ART-04, no ejecuta G5/G6, no modifica R2 ni autoriza Fase C. Requiere auditoría independiente y aprobación expresa separada.

```text
MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R3.**
