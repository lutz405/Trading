# R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R5 — Plan de materialización (corrección R5)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** revisión documental R5. **No aprobada ni auditada.** Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

---

## 1. Versión anterior conservada y alcance real

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_artifacts_materialization_plan_r4.md` |
| SHA-256 de R4 | `226c51d08a3171232098f40d4e22cf0d2d1487a1c373aa480e69d5651da63e71` |
| Git hash de R4 | `aa8c03700edf5c78b1a7602ce92e9f900c7924a8` |
| Base histórica | R3 `2f6f48a2…`, R2 `d4d0c689…` |

R5 corrige **exclusivamente** `AUD-ANT-NEW-02`: define sin abreviaturas los registros de aprobación citados en G0/G1 y sustituye `R9/R4` por `R9 y Especificación R5`.

**Alcance real respecto de R2:** se modifica la fila **G5** de §8, los roles de §7, las decisiones pendientes de §10 y el estado de §11. §1–§6, §9 y las filas G0–G4 y G6 conservan su contenido normativo; solo se actualizan sus referencias documentales, sin alterar historial ni resultados.

### 1.1 Definición de registros de aprobación citados

| Código del manifiesto de transferencia | Ruta completa |
|---|---|
| `A-03` | `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` |
| `A-04` | `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` |

Estos códigos provienen del inventario del manifiesto de transferencia y **no se usan como abreviaturas** en este documento: G0 y G1 citan las rutas completas. También puede consultarse Plan R2 §1.2.

---

## 2. Inventario de artefactos

Los siete artefactos conservan identidad, responsabilidades y dependencias originales:

| Artefacto | Dependencias originales |
|---|---|
| ORACLE-ART-01 | — |
| ORACLE-ART-02 | 01 |
| ORACLE-ART-03 | 01, 02 |
| **ORACLE-ART-04** | **01, 03** (R2 §4.4; Especificación R5 §3.6) |
| ORACLE-ART-05 | 01, 02 |
| ORACLE-ART-06 | 01, 02, 05 |
| ORACLE-ART-07 | 01, 02, 06 |

ART-02 se verifica dentro del alcance de la revisión, no como dependencia formal de ART-04. No se crea octavo artefacto.

---

## 3. Roles y separación

Generador, IA revisora, auditor posterior y propietario permanecen separados. La IA no aprueba ni firma; el auditor es distinto del generador y de la IA; el propietario conserva la aceptación expresa.

---

## 4. Puertas de control

| Puerta | Criterios de entrada (referencias explícitas) | Criterios de salida | Rechazo |
|---|---|---|---|
| **G0** Especificación aprobada | Especificación R5 aprobada y auditada `ACCEPTED`. Línea base: R2 aprobada en `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | Registro de aprobación vigente | Hash divergente o auditoría no favorable |
| **G1** Plan revisado | Plan R5 documentalmente completo y cotejado con **R9 y la Especificación R5**. Línea base: R2 aprobada en `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` | Revisión sin contradicciones | Convertir decisiones pendientes en aprobadas |
| **G2** Fuentes y herramientas verificadas | §9.2, schema y Especificación R5 disponibles; decisiones críticas registradas (línea base: R2) | Procedencia documentada | Fuente modificada o decisión crítica sin resolver |
| **G3** Autorización de materialización | Decisión expresa del propietario | Autorización registrada | Aprobación anterior interpretada como autorización |
| **G4** Artefactos generados | G3 concedido | 01–07 generados con sus estados | Artefacto incompleto o no reproducible |
| **G5 (R5)** Verificación independiente | G4 completo; revisión independiente conforme a modalidad autorizada (`HUMAN_INDEPENDENT_REVIEW` o `INDEPENDENT_AI_REVIEW` solo para ART-04); Autorización R5 en vigor si se usa IA | Evidencia y dictamen; auditoría separada; aceptación expresa | Discrepancia no resuelta; revisión no independiente; `INCONCLUSIVE`/`REJECTED`; `ACCEPTED_WITH_FINDINGS` con `BLOCKER`/`HIGH`; falta de auditoría separada |
| **G6 (sin cambios sustantivos)** Resolución de AUD-R8-02 | G5 favorable; siete artefactos verificados; informe de auditoría independiente favorable; sin hallazgos bloqueantes; aceptación expresa | Cierre documentado con evidencia trazable de los cinco requisitos | Artefacto ausente; informe desfavorable; hallazgo bloqueante; falta de aceptación; evidencia incompleta |

La aprobación de G0 no implica aprobar G1–G6. Las referencias a R2 se conservan como línea base histórica.

### 4.1 Regla crítica de G5

Un dictamen IA **no cierra G5 automáticamente**. Deben concurrir: Autorización R5 en vigor; D3-R5, Especificación R5 y Plan R5 auditados y aprobados; Protocolo R4 aprobado y auditado antes de ejecutar la revisión; dictamen no bloqueante; auditoría separada favorable; ART-04 materializado y auditado; aceptación expresa; siete artefactos `VERIFIED`. `INCONCLUSIVE`/`REJECTED` nunca desbloquean G5.

### 4.2 G6 permanece separado

Se conservan las cinco condiciones de R2 §8: siete artefactos verificados; informe de auditoría favorable; sin hallazgos bloqueantes; aceptación expresa independiente de la técnica; evidencia documental trazable. Superar G6 no autoriza Fase C.

---

## 5. Verificación independiente

Se mantienen las ocho verificaciones de R2 §5.1: integridad de ART-03; correspondencia con R2 §4.1–4.7; 139 rutas; nueve metadatos; `rule_id` como décimo campo; P1–P5 e I1–I12; revisión de ART-04; mutación aislada de `external_run_only`.

---

## 6. Integridad, decisiones pendientes y estado

Se conservan §6 (integridad), §7 (roles), §9 (riesgos) y se actualizan §10 (decisiones pendientes: aprobación de D3-R5, Especificación R5, Plan R5, Autorización R5 y Protocolo R4, cada una tras auditoría) y §11 (trazabilidad de versiones).

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

R5 no ejecuta G5/G6, no crea ART-04 y no autoriza Fase C.

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R5.**
