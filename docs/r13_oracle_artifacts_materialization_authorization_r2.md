# R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R2 — Autorización de materialización de los artefactos del oracle

**Proyecto:** `TradingAI_BTC`.
**Documento de origen:** `docs/r13_oracle_artifacts_materialization_authorization_r1.md`, conservado íntegramente como registro histórico.
**Auditoría incorporada:** `R13-AUDIT-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R1 — ACCEPTED WITH FINDINGS` (AUD-MAT-AUTH-R1-01).
**Tipo:** autorización expresa del propietario para la materialización controlada de ORACLE-ART-01 a ORACLE-ART-07. No autoriza implementación de Fase C ni cierre automático de AUD-R8-02.

---

## 1. Declaración de autorización

```text
MATERIALIZATION_AUTHORIZATION_STATUS: GRANTED
AUTHORIZATION_DATE: 2026-11-27
AUTHORIZATION_SCOPE: ORACLE-ART-01 through ORACLE-ART-07
APPROVED_MATERIALIZATION_PLAN: R2
MATERIALIZATION_PLAN_SHA256: d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0
MATERIALIZATION_PLAN_GIT_HASH: e37dfdae0663502e89cb522ca8605eb2791c828e
PLAN_OWNER_APPROVAL_GIT_HASH: 4cd2d20f92b161217ab6334d10039e6b17172e3a
PLAN_INDEPENDENT_AUDIT_STATUS: ACCEPTED
DECISIONS_D1_D6_STATUS: APPROVED
DECISION_APPROVAL_AUDIT_STATUS: ACCEPTED
```

El propietario del proyecto `TradingAI_BTC` autoriza expresamente la materialización controlada de los siete artefactos, conforme al plan R2 aprobado, a las decisiones D1–D6 aprobadas y a las auditorías independientes favorables. No se inventa nombre personal del aprobador.

---

## 2. Alcance autorizado

| ID | Artefacto |
|---|---|
| ORACLE-ART-01 | Transcripción normativa completa e independiente |
| ORACLE-ART-02 | Versión ejecutable del oracle |
| ORACLE-ART-03 | SHA-256 de la transcripción canonicalizada |
| ORACLE-ART-04 | Registro de revisión humana independiente |
| ORACLE-ART-05 | Evidencia de cobertura de 139 rutas |
| ORACLE-ART-06 | Evidencia de comprobación de nueve metadatos |
| ORACLE-ART-07 | Evidencia de mutación `external_run_only` |

La ejecución deberá respetar íntegramente:

- `docs/r13_oracle_artifacts_materialization_plan_r2.md` (plan R2), incluidas las puertas G0–G6.
- Las decisiones D1–D6 aprobadas en `docs/r13_oracle_artifacts_decision_resolution_r2.md` y su registro de aprobación.
- `docs/r13_phase_c_design_r9.md` (diseño R9 aprobado).
- `docs/r13_oracle_artifacts_specification_r2.md` (especificación R2 aprobada).
- Las convenciones y límites de las auditorías independientes `ACCEPTED`.

---

## 3. Límites explícitos

Esta autorización **NO** concede permiso para:

- Implementar Fase C.
- Cerrar automáticamente AUD-R8-02.
- Omitir revisión humana independiente.
- Omitir auditoría independiente de los siete artefactos.
- Declarar G6 superada sin satisfacer todos sus criterios.
- Iniciar fases D, E, F, G o S2.
- Modificar los Parquet protegidos.
- Cambiar código de producción, esquemas o dependencias fuera del alcance aprobado.
- Realizar commits o push por esta autorización.

```text
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED_PENDING_ORACLE_ARTIFACT_VERIFICATION_AND_G6
PHASE_D_AUTHORIZATION: NOT_GRANTED
PHASE_E_AUTHORIZATION: NOT_GRANTED
PHASE_F_AUTHORIZATION: NOT_GRANTED
PHASE_G_AUTHORIZATION: NOT_GRANTED
S2_AUTHORIZATION: NOT_GRANTED
```

La autorización de materialización no equivale a verificación: los siete artefactos deberán generarse, revisarse y auditarse conforme a G4–G6 antes de cualquier cambio de estado.

---

## 4. Verificación de referencias

| Referencia | Valor verificado |
|---|---|
| Plan R2 SHA-256 | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` ✅ |
| Plan R2 Git hash | `e37dfdae0663502e89cb522ca8605eb2791c828e` ✅ |
| Aprobación del plan Git hash | `4cd2d20f92b161217ab6334d10039e6b17172e3a` ✅ |
| Auditoría del plan | `R13-AUDIT-ORACLE-ARTIFACTS-MATERIALIZATION-PLAN-R2 — ACCEPTED` ✅ |
| Resolución D1–D6 Git hash | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` ✅ |
| Aprobación D1–D6 Git hash | `432084a4baead2a5ad84d4d43c158f8bc3dc7731` ✅ |
| Auditoría de la aprobación D1–D6 | `R13-AUDIT-ORACLE-ARTIFACTS-DECISION-OWNER-APPROVAL-R1 — ACCEPTED` ✅ |
| HEAD / rama | `259ca6ee11878f114cdcab4cef500074b3bc1a48`, `main`, alineado ✅ |

---

## 5. Condición de ejecución futura

La materialización solo podrá ejecutarse en una tarea posterior, con:

1. Cumplimiento de G0–G3 según plan R2.
2. Generación de ORACLE-ART-01…07 conforme a D1–D6.
3. Revisión humana independiente (ORACLE-ART-04) y auditoría independiente de los siete artefactos.
4. Verificación de 139 rutas, nueve metadatos, `rule_id` separado, P1–P5 e I1–I12.
5. Evidencia de la mutación `external_run_only` en entorno aislado.
6. Aceptación expresa del propietario del resultado de la auditoría antes de declarar G6 superada y AUD-R8-02 resuelta.

Este registro **no** ejecuta ninguno de esos pasos.

---

## 6. Estado Git y cierre

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni unstaged. `git diff --check`: exit 0. Índice Git sin modificaciones; sin commits ni push.

No se materializaron artefactos, no se ejecutó el oracle, fingerprints, pruebas ni mutaciones, no se modificaron código, tests, schemas, dependencias ni datasets, y no se accedió a Parquet protegidos.

La autorización cubre exclusivamente ORACLE-ART-01…07. **AUD-R8-02 permanece OPEN**; Fase C continúa `BLOCKED_PENDING_ORACLE_ARTIFACT_VERIFICATION_AND_G6`; D, E, F, G y S2 permanecen sin autorización.

**Fin de R13-ORACLE-ARTIFACTS-MATERIALIZATION-AUTHORIZATION-R2.**
