# R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R3 — Plan de materialización (enmienda de G5)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta documental**. No aprobada; pendiente de auditoría independiente y aprobación expresa.

```text
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
```

---

## 1. Versión anterior conservada

| Dato | Valor |
|---|---|
| Documento de origen | `docs/r13_oracle_artifacts_materialization_plan_r2.md` |
| SHA-256 de R2 | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| Git hash de R2 | `e37dfdae0663502e89cb522ca8605eb2791c828e` |
| Habilitación | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md`, SHA-256 `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |

R2 se conserva **íntegramente**. R3 modifica **exclusivamente** la fila G5 de la tabla de puertas (§8) y las consecuencias necesarias de los roles (§7). Las secciones 1–6, 9–11 y las filas G0–G4 y G6 permanecen con el contenido de R2.

---

## 2. Inventario, arquitectura y secuencia

Se mantienen sin cambios:

- los **siete artefactos** ORACLE-ART-01…07 y sus identidades;
- la arquitectura de generación de R2 §3;
- la secuencia de materialización de R2 §4;
- los criterios de verificación de ART-01/02/03/05/06/07;
- la integridad y el almacenamiento de R2 §6;
- la exigencia de auditoría independiente posterior;
- la aprobación expresa del propietario cuando corresponda;
- G6 como gate **separado** y Fase C bloqueada.

---

## 3. Roles y separación de responsabilidades (R3 §7)

Se añaden, sin eliminar los roles de R2:

| Rol | Responsabilidad | Prohibición |
|---|---|---|
| Generador | Producir artefactos y evidencia | No puede revisar ni auditar su propio trabajo |
| IA revisora | Emitir dictamen técnico bajo `INDEPENDENT_AI_REVIEW` | No aprueba, no firma, no modifica fuentes |
| Auditor posterior | Evaluar evidencia, confirmar severidades | Distinto del generador y de la IA; evaluación a ciegas |
| Propietario | Aceptación expresa | No delega su autoridad en la IA ni en el auditor |

---

## 4. Puertas de control (R3 §8)

| Puerta | Criterios de entrada | Criterios de salida | Rechazo |
|---|---|---|---|
| **G0** Especificación aprobada | R2 aprobada y auditada `ACCEPTED` | Registro de aprobación vigente | Hash R2 divergente o auditoría no favorable |
| **G1** Plan revisado | Plan documental completo y cotejado con R9/R2 | Revisión documental sin contradicciones | Convertir decisiones pendientes en aprobadas |
| **G2** Fuentes y herramientas verificadas | §9.2, schema y R2 disponibles; decisiones críticas registradas | Procedencia documentada | Fuente modificada o decisión crítica sin resolver |
| **G3** Autorización de materialización | Decisión expresa del propietario | Autorización registrada | Cualquier aprobación anterior interpretada como autorización |
| **G4** Artefactos generados | G3 concedido | 01–07 generados con sus estados | Artefacto incompleto o no reproducible |
| **G5 (R3)** Verificación independiente | G4 completo; **revisión independiente realizada** conforme a modalidad autorizada: `HUMAN_INDEPENDENT_REVIEW` o `INDEPENDENT_AI_REVIEW` para ART-04; autorización R3 en vigor si se usa IA | Evidencia de verificación y dictamen; **informe de auditoría separada**; aceptación expresa del propietario | Discrepancia no resuelta; revisión no independiente; `INCONCLUSIVE`/`REJECTED`; `ACCEPTED_WITH_FINDINGS` con hallazgos `BLOCKER`/`HIGH`; falta de auditoría separada |
| **G6 (sin cambios sustantivos)** Resolución de AUD-R8-02 | G5 favorable; siete artefactos materializados y estados verificados; informe de auditoría independiente favorable; sin hallazgos bloqueantes; aceptación expresa del propietario | Cierre documentado de AUD-R8-02 con evidencia trazable de los cinco requisitos | Artefacto ausente o no verificado; informe desfavorable; hallazgo bloqueante sin resolver; falta de aceptación expresa; evidencia incompleta |

La aprobación de G0 **no** implica aprobar G1–G6. G3 es obligatoria antes de cualquier generación.

### 4.1 Regla crítica de G5

**Un dictamen de IA no puede cerrar G5 automáticamente.** Para que G5 quede favorable con `INDEPENDENT_AI_REVIEW` deben concurrir conjuntamente:

1. autorización de materialización R3 **en vigor** (auditada y aprobada);
2. D3-R3, especificación R3 y plan R3 auditados y aprobados;
3. revisión ejecutada conforme al protocolo R2;
4. dictamen `ACCEPTED` o `ACCEPTED_WITH_FINDINGS` sin hallazgos `BLOCKER`/`HIGH`;
5. auditoría técnica separada del informe de IA, favorable;
6. ORACLE-ART-04 materializado y auditado;
7. aceptación expresa del propietario, independiente de la aceptación técnica;
8. siete artefactos en estado `VERIFIED`.

`INCONCLUSIVE` y `REJECTED` **nunca** desbloquean G5.

### 4.2 G6 permanece separado

Se conserva literalmente la condición de R2 §8: *«G5 favorable no equivale a superar G6. Solo puede considerarse superada cuando concurran conjuntamente: (1) los siete artefactos requeridos están materializados y sus estados individuales verificados; (2) existe un informe de auditoría independiente favorable que verifica los criterios correspondientes a AUD-R8-02; (3) no quedan hallazgos bloqueantes sin resolver; (4) el propietario ha emitido aceptación expresa del resultado de la auditoría, independiente de la aceptación técnica del auditor; y (5) existe evidencia documental trazable de cada requisito anterior. La superación de G6 no autoriza por sí misma la implementación de Fase C».*

---

## 5. Decisiones pendientes (R3 §10)

Se añaden a las pendientes de R2: aprobación de D3-R3, especificación R3, plan R3, autorización R3 y protocolo R2, cada una posterior a su auditoría independiente; aceptación del resultado de la revisión IA; aceptación de ART-04; aceptación del resultado de G5; y, separadamente, de G6.

---

## 6. Estado final y trazabilidad (R3 §11)

| Versión | Cambio | Estado |
|---|---|---|
| R1 | Plan inicial | Histórico |
| R2 (sha `d4d0c689…`) | Correcciones AUD-MAT-PLAN-R1-01…03 | Histórico, **no modificado** |
| **R3** | G5 admite modalidad IA autorizada; G6 intacto | **Propuesta pendiente de auditoría** |

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

Esta propuesta **no** ejecuta G5/G6, **no** crea ART-04, **no** altera los criterios de los otros seis artefactos y **no** autoriza Fase C.

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R3.**
