# R13-ORACLE-ARTIFACTS-DECISION-OWNER-APPROVAL-R1 — Registro de aprobación del propietario de las decisiones D1–D6

**Proyecto:** `TradingAI_BTC`.
**Tipo:** aprobación expresa del propietario de las seis decisiones técnicas contenidas en una resolución documental. No autoriza materialización ni implementación.

---

## 1. Base verificada

| Dato | Valor |
|---|---|
| Documento aprobado | `docs/r13_oracle_artifacts_decision_resolution_r2.md` |
| Revisión | `R2` |
| SHA-256 verificado | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| Hash Git verificado | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| Auditoría independiente | `R13-AUDIT-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R2` |
| Dictamen de auditoría | `ACCEPTED` |
| Hallazgos nuevos | Ninguno |
| HEAD de referencia | `259ca6ee11878f114cdcab4cef500074b3bc1a48` |
| Rama | `main`, `origin/main` alineada |
| Identidad del aprobador | Propietario del proyecto `TradingAI_BTC`; no se inventa nombre personal |

La auditoría de R1 tuvo dictamen `ACCEPTED WITH FINDINGS`; R2 incorporó las cuatro correcciones y la auditoría de R2 emitió dictamen `ACCEPTED` sin hallazgos nuevos. Las seis recomendaciones registradas en R2 §4 coinciden con las decisiones aprobadas en §2.

---

## 2. Declaración expresa del propietario

```text
DECISION_RESOLUTION_OWNER_APPROVAL: APPROVED
APPROVAL_DATE: 2026-11-27
APPROVED_DECISION_RESOLUTION: R2
APPROVED_DECISION_RESOLUTION_SHA256: 6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5
APPROVED_DECISION_RESOLUTION_GIT_HASH: cccbe4dfa6531f1cce0d3014e46eedf7d36fb265
INDEPENDENT_AUDIT_STATUS: ACCEPTED
```

### 2.1 Decisiones aprobadas individualmente

| ID | Decisión aprobada | Estado |
|---|---|---|
| **D1** | Identificadores `rule_id` secuenciales por fila de §9.2, con tabla de correspondencia revisada | `APPROVED` |
| **D2** | Ubicación versionada de artefactos en el repositorio; referencias externas únicamente para recursos inmutables | `APPROVED` |
| **D3** | Revisor independiente designado por función, con identidad funcional real y evidencia documentada de independencia | `APPROVED` |
| **D4** | Evidencias deterministas UTF-8 y JSON JCS derivado exclusivamente auxiliar, sin modificar la preimagen de ORACLE-ART-03 | `APPROVED` |
| **D5** | Correcciones no semánticas documentadas sin incrementar versión; cambios semánticos sujetos a nueva versión | `APPROVED` |
| **D6** | Verificador ORACLE-ART-02 ubicado en `tests/`, sin importaciones de producción ni dependencias nuevas, con entradas declaradas y cerradas | `APPROVED` |

La aprobación se limita a D1–D6 y a su alcance documental. No certifica que los artefactos existan, estén verificados o hayan sido materializados.

---

## 3. Límites obligatorios

```text
ORACLE_ARTIFACT_MATERIALIZATION_AUTHORIZATION: NOT_GRANTED
ORACLE_ARTIFACTS_STATUS: NOT_CREATED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
PHASE_D_AUTHORIZATION: NOT_GRANTED
PHASE_E_AUTHORIZATION: NOT_GRANTED
PHASE_F_AUTHORIZATION: NOT_GRANTED
PHASE_G_AUTHORIZATION: NOT_GRANTED
S2_AUTHORIZATION: NOT_GRANTED
```

La aprobación de D1–D6 **no** autoriza crear, ejecutar, verificar ni materializar ORACLE-ART-01…07, ni implementar Fase C. Las puertas G0–G6 del plan R2 deben cumplirse íntegramente. La eventual autorización de materialización y la autorización técnica de Fase C requieren decisiones separadas y expresas del propietario. Las aprobaciones previas del diseño R9, la especificación R2 y el plan R2 conservan su alcance original.

---

## 4. Conservación normativa

Este registro no modifica los siete artefactos ni sus dependencias, las 139 rutas, los nueve metadatos, `rule_id` como campo separado, P1–P5, I1–I12, las puertas G0–G6 ni la secuencia de resolución de R2 §4.1. No introduce requisitos normativos nuevos ni cambia el estado de AUD-R8-02.

---

## 5. Verificación final

| Comprobación | Resultado |
|---|---|
| R2 SHA-256 / hash Git | idénticos a los declarados |
| Auditoría R2 | `ACCEPTED`, sin hallazgos nuevos |
| D1–D6 | coinciden con la matriz de recomendaciones de R2 §4 |
| R1 y documentos previos | intactos |
| Único archivo nuevo | este registro |
| staged / diff | ninguno |
| `git diff --check` | exit 0 |
| Índice Git | sin modificaciones |
| Commits / push | ninguno |

No se materializaron artefactos, no se ejecutó el oracle, fingerprints, pruebas ni mutaciones, no se modificaron código, tests, schemas, dependencias ni datasets, y no se accedió a Parquet protegidos.

---

## 6. Conclusión

Quedan aprobadas expresamente las decisiones D1–D6 de `R13-ORACLE-ARTIFACTS-DECISION-RESOLUTION-R2`. La autorización de materialización y la autorización de implementación de Fase C **no** están concedidas. **AUD-R8-02 continúa OPEN**; Fase C continúa **BLOCKED**; D, E, F, G y S2 permanecen sin autorización.

**Fin de R13-ORACLE-ARTIFACTS-DECISION-OWNER-APPROVAL-R1.**
