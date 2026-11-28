# R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R4 — Plan de materialización (corrección R4)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta de corrección**. No aprobada. Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

---

## 1. Versión anterior conservada y alcance real

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_artifacts_materialization_plan_r3.md` |
| SHA-256 de R3 | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` |
| Git hash de R3 | `10d7f4be8b36849916d26f87c4baf3457538bc54` |
| Base histórica | Plan R2, SHA-256 `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |

**Alcance real de la corrección (AUD-ANT-07):** respecto de R2 se modifica la fila **G5** de §8, los roles de §7, las decisiones pendientes de §10 y el estado final de §11. Las secciones §1–§6 y §9 y las filas **G0–G4 y G6** conservan su contenido normativo; solo se actualizan sus **referencias documentales** a las versiones corregidas, sin alterar historial ni resultados. R3 y R2 permanecen intactos.

---

## 2. Inventario de artefactos

Los siete artefactos conservan identidad, responsabilidades y dependencias originales:

| Artefacto | Dependencias originales |
|---|---|
| ORACLE-ART-01 | — |
| ORACLE-ART-02 | 01 |
| ORACLE-ART-03 | 01, 02 |
| **ORACLE-ART-04** | **01, 03** (según R2 §4.4 y especificación R4 §3.6) |
| ORACLE-ART-05 | 01, 02 |
| ORACLE-ART-06 | 01, 02, 05 |
| ORACLE-ART-07 | 01, 02, 06 |

No se añade ART-02 como dependencia formal de ART-04: su verificación es parte del alcance de la revisión, no una dependencia (AUD-ANT-03). No se crea octavo artefacto.

---

## 3. Roles y separación

Generador, IA revisora, auditor posterior y propietario permanecen separados. La IA no aprueba ni firma; el auditor es distinto del generador y de la IA; el propietario conserva la aceptación expresa.

---

## 4. Puertas de control

| Puerta | Criterios de entrada (referencias actualizadas) | Criterios de salida | Rechazo |
|---|---|---|---|
| **G0** Especificación aprobada | Especificación R4 aprobada y auditada `ACCEPTED`; registro vigente (línea base: R2 aprobada en A-03) | Registro de aprobación vigente | Hash divergente o auditoría no favorable |
| **G1** Plan revisado | Plan R4 documentalmente completo y cotejado con R9/R4 (línea base: R2 en A-04) | Revisión sin contradicciones | Convertir decisiones pendientes en aprobadas |
| **G2** Fuentes y herramientas verificadas | §9.2, schema y especificación aprobada disponibles; decisiones críticas registradas (línea base: R2) | Procedencia documentada | Fuente modificada o decisión crítica sin resolver |
| **G3** Autorización de materialización | Decisión expresa del propietario | Autorización registrada | Aprobación anterior interpretada como autorización |
| **G4** Artefactos generados | G3 concedido | 01–07 generados con sus estados | Artefacto incompleto o no reproducible |
| **G5 (R4)** Verificación independiente | G4 completo; revisión independiente realizada conforme a modalidad autorizada (`HUMAN_INDEPENDENT_REVIEW` o `INDEPENDENT_AI_REVIEW` solo para ART-04); autorización R4 en vigor si se usa IA | Evidencia de verificación y dictamen; auditoría separada; aceptación expresa | Discrepancia no resuelta; revisión no independiente; `INCONCLUSIVE`/`REJECTED`; `ACCEPTED_WITH_FINDINGS` con `BLOCKER`/`HIGH`; falta de auditoría separada |
| **G6 (sin cambios sustantivos)** Resolución de AUD-R8-02 | G5 favorable; siete artefactos materializados y verificados; informe de auditoría independiente favorable; sin hallazgos bloqueantes; aceptación expresa del propietario | Cierre documentado con evidencia trazable de los cinco requisitos | Artefacto ausente; informe desfavorable; hallazgo bloqueante; falta de aceptación; evidencia incompleta |

La aprobación de G0 no implica aprobar G1–G6. G3 es obligatoria antes de cualquier generación. Las referencias a R2 se conservan como **línea base histórica**; no se alteran sus resultados.

### 4.1 Regla crítica de G5

Un dictamen IA **no cierra G5 automáticamente**. Deben concurrir: autorización R4 en vigor; D3-R4, especificación R4 y plan R4 auditados y aprobados; protocolo R3 aprobado y auditado antes de ejecutar la revisión; dictamen no bloqueante; auditoría separada favorable; ART-04 materializado y auditado; aceptación expresa; siete artefactos `VERIFIED`. `INCONCLUSIVE`/`REJECTED` nunca desbloquean G5.

### 4.2 G6 permanece separado

Se conservan literalmente las cinco condiciones de R2 §8: siete artefactos verificados; informe de auditoría independiente favorable; sin hallazgos bloqueantes; aceptación expresa del propietario independiente de la aceptación técnica; evidencia documental trazable. Superar G6 no autoriza Fase C.

---

## 5. Verificación independiente

Se mantienen las ocho verificaciones de R2 §5.1: integridad de ART-03; correspondencia con R2 §4.1–4.7; 139 rutas; nueve metadatos; `rule_id` como décimo campo; P1–P5 e I1–I12; revisión de ART-04; mutación aislada de `external_run_only`. La modalidad de ART-04 no reduce ninguna verificación.

---

## 6. Integridad, decisiones pendientes y estado

Se conservan §6 (integridad), §7 (roles, con la adición ya descrita), §9 (riesgos) y se actualizan §10 (decisiones pendientes: aprobación de D3-R4, especificación R4, plan R4, autorización R4 y protocolo R3, cada una tras auditoría) y §11 (trazabilidad de versiones).

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

Esta propuesta no ejecuta G5/G6, no crea ART-04, no altera los otros artefactos y no autoriza Fase C.

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R4.**
