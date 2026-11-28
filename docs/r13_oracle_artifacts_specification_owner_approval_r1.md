# R13-ORACLE-ARTIFACTS-SPECIFICATION-OWNER-APPROVAL-R1 — Registro de aprobación del propietario de la especificación del oracle

**Proyecto:** `TradingAI_BTC`.
**Identificador del registro:** `R13-ORACLE-ARTIFACTS-SPECIFICATION-OWNER-APPROVAL-R1`.
**Naturaleza:** registro documental de una decisión del propietario. Aprueba **únicamente la especificación documental**. No autoriza materializar artefactos ni implementar Fase C.

---

## 1. Base verificada

| Dato | Valor |
|---|---|
| Documento aprobado | `docs/r13_oracle_artifacts_specification_r2.md` |
| SHA-256 de R2 | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| Hash Git de R2 | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| Auditoría independiente | `R13-AUDIT-ORACLE-ARTIFACTS-SPECIFICATION-R2` |
| Dictamen | `ACCEPTED` |
| Hallazgos nuevos | Ninguno |
| HEAD de referencia | `259ca6ee11878f114cdcab4cef500074b3bc1a48` |
| Rama | `main`, `origin/main` alineada |
| Estado de los siete artefactos | `NOT_CREATED` |
| AUD-R8-02 | `OPEN` |

La auditoría `R13-AUDIT-ORACLE-ARTIFACTS-SPECIFICATION-R1` tuvo dictamen `ACCEPTED WITH FINDINGS` (AUD-ORACLE-SPEC-R1-01 y R1-02); R2 corrigió ambos hallazgos y la auditoría de R2 emitió dictamen `ACCEPTED` sin hallazgos nuevos.

---

## 2. Decisión del propietario

La presente instrucción constituye la confirmación expresa del propietario en este flujo de trabajo. Se registra:

```text
ORACLE_SPECIFICATION_OWNER_APPROVAL: APPROVED
```

- **Aprobador:** propietario del proyecto `TradingAI_BTC`; no se inventa nombre ni identidad personal adicional.
- **Fecha:** 2026-11-27, fecha verificable del entorno de trabajo en que se emite esta instrucción.
- **Alcance exacto:** se aprueba la **especificación documental** de ORACLE-ART-01 a ORACLE-ART-07 contenida en `docs/r13_oracle_artifacts_specification_r2.md`: requisitos, estructura, contenido mínimo, fuentes normativas, métodos futuros de generación y verificación, criterios de aceptación y rechazo, dependencias, reproducibilidad, reglas de independencia y no circularidad, matriz de estados y trazabilidad.

La aprobación se refiere exclusivamente al documento. No modifica ni interpreta las decisiones DEC-01 a DEC-09, la aprobación del diseño R9 registrada en `docs/r13_owner_design_approval_r1.md`, ni los límites allí establecidos.

---

## 3. Límites explícitos

Se registran los estados siguientes, que esta aprobación **no** altera:

```text
ORACLE_ARTIFACT_MATERIALIZATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_R8_02: OPEN
PHASE_C_STATUS: BLOCKED_PENDING_ORACLE_ARTIFACTS_AND_TECHNICAL_AUTHORIZATION
```

La aprobación **no** debe:

- Autorizar la generación o materialización de ORACLE-ART-01…07.
- Cambiar ningún artefacto de `NOT_CREATED`.
- Declarar satisfecho AUD-R8-02.
- Autorizar la ejecución del oracle, fingerprints o pruebas.
- Aprobar la implementación de Fase C.
- Autorizar fases D, E, F, G o S2.
- Alterar las aprobaciones anteriores de R9 ni las decisiones DEC-01…DEC-09.

Ninguno de los siete artefactos existe materialmente; este registro no crea transcripción, versión ejecutable, checksum, revisión humana ni evidencia de comparación o mutación.

---

## 4. Trazabilidad

| Elemento | Referencia |
|---|---|
| Diseño aprobado | `docs/r13_phase_c_design_r9.md` (`d21de0f1…685`; SHA-256 `884ee501…5ead`) |
| Aprobación del diseño | `docs/r13_owner_design_approval_r1.md` (`6ecdf341…6ad5`) |
| Autoridad normativa | DEC-01…DEC-09, en especial DEC-03, DEC-04, DEC-05 y DEC-06; diseño v4 §9.2 |
| Contrato estructural | `src/tradingai/schemas/manifest_v4.json` |
| Contrato productivo | `src/tradingai/ml/provenance_v4.py`, Fase A/B aceptada |
| Criterios vinculados | CP-C-05, CP-C-07, CP-C-08, CP-C-13 |
| Limitación pendiente | AUD-R8-02 `OPEN` |

---

## 5. Restricciones aplicadas

- Solo se crea este documento; no se modifica R1, R2, R9 ni registros anteriores.
- No se modificaron código, tests, schemas, dependencias ni datasets.
- No se accedió a los Parquet protegidos.
- No se ejecutaron pruebas ni fingerprints.
- No se modificó el índice Git; no se crearon commits ni push.

---

## 6. Verificación final

| Comprobación | Resultado |
|---|---|
| HEAD | `259ca6ee11878f114cdcab4cef500074b3bc1a48` |
| Rama / remoto | `main`, `origin/main` alineados |
| R2 | SHA-256 y hash Git idénticos a la base de aprobación |
| R1 y registros históricos | intactos |
| Siete artefactos | `NOT_CREATED` |
| AUD-R8-02 | `OPEN` |
| `git diff --check` | sin errores |

---

## 7. Conclusión

Queda registrada la aprobación expresa del propietario de la **especificación documental** `R13-ORACLE-ARTIFACTS-SPECIFICATION-R2`. La autorización para materializar los siete artefactos y la autorización técnica de implementación de Fase C **no** están concedidas. Fase C permanece `BLOCKED_PENDING_ORACLE_ARTIFACTS_AND_TECHNICAL_AUTHORIZATION`; D, E, F, G y S2 permanecen sin autorización.

**Fin de R13-ORACLE-ARTIFACTS-SPECIFICATION-OWNER-APPROVAL-R1.**
