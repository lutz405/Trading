# R13-AUDIT-NATIVE-RULE-ID-ABSENCE-FIX-R1 — Informe de auditoría técnica independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto:** verificación independiente de `R13-ORACLE-G5-NATIVE-RULE-ID-ABSENCE-FIX-R1` y de los dos hallazgos previos.
**Restricción:** auditoría de solo lectura, salvo este informe.

---

## 1. Dictamen

**ACCEPTED.** Ambos hallazgos están resueltos:

- `AUD-IMP-REP-R1-01: RESOLVED` — `compare_observed()` distingue ausencia, `None` y valores concretos en los nueve metadatos.
- `AUD-ABS-FIX-R1-01: RESOLVED` — `_flatten()` no sintetiza `rule_id=None`; la ausencia en formato nativo produce `RULE_MISSING`.

No se detectaron hallazgos nuevos. La representación es técnicamente apta para preparar ORACLE-ART-06 y ORACLE-ART-07, sin ejecutar G5/G6 ni crear los artefactos.

---

## 2. Evidencia examinada y hashes

| Archivo | SHA-256 | Git hash |
|---|---|---|
| `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` | `8f3f066fd4712f2752a8ca06bbbd198b9bb3b527` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `132bad37b05960e828e8271b7b3cfeaebe220df7506d0af8a1fa0d9367649058` | `730f29877f540d1383381aab07eec4197755e336` |
| Informe de corrección | `b0895b55df59c4dc0824df2a2d3eeca14c7386d3e87e1db3a3d4b7eaeb007e93` | `9095e599b23e83c6d7c73300ba4bd2b72bbb6c83` |
| Auditoría previa de ausencia | `91ba9f578709652bb4eca9e5a9fc2dd490765116304f0f55e0bedb8bfcdfddc1` | `814a08077cfbc6436dc67df66d767979ba3f6706` |
| Auditoría de implementación | `241107f5e5df165153ef8fc275faf42993984d3e5e3c7d967440f44e32cf25ed` | `595672caae04807966c7c83e7e608d670e607b05` |
| R9 | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| Especificación R2 | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| Schema v4 | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |

Artefactos Oracle 01/03/05 y verificador sin cambios. `provenance_v4.py` sin cambios.

---

## 3. Reproducción de casos críticos

Script temporal de auditoría, ejecutado y eliminado; salidas exactas:

| Caso | Salida observada | Categoría correcta |
|---|---|---|
| Entrada nativa sin `rule_id` | `NATIVE_ABSENT_SYNTH False`; `RULE_MISSING:calibration.base_artifact_sha256.rf` | ✅ ausencia detectada |
| `rule_id=None` presente | `RULE_DIVERGENCE:…:expected R9-9.2-20, observed None` | ✅ divergencia, no ausencia |
| `rule_id` correcto | `NATIVE_CORRECT_ERRORS 0` | ✅ aceptación |
| `rule_id` divergente | `RULE_DIVERGENCE:…:R9-9.2-99` | ✅ divergencia |
| Metadato ausente con esperado `None` | `METADATA_MISSING:…:manifest_required_when` | ✅ ausencia detectada |
| Metadato presente con `None` | `META_NONE_ERRORS 0` | ✅ `None` legítimo conservado |
| Metadato con valor divergente | `METADATA_DIVERGENCE:…:type` | ✅ divergencia |
| Campo desconocido | `UNKNOWN_FIELD:…:extra_campo` | ✅ fail-closed |
| `rule_id` ausente/divergente en forma plana | `RULE_MISSING` / `RULE_DIVERGENCE` | ✅ distinguidos |
| Determinismo | `DETERMINISTIC True` | ✅ |
| Estructura | `ENTRIES 139`, `UNIQUE 139`, `FIELDS 9`, `RULE_SEPARATE True`, `SCHEMA_ERRORS []` | ✅ |
| Independencia | `FORBIDDEN []` | ✅ sin artefactos, producción ni dependencias nuevas |

No se encontró otra ruta de ejecución que confunda ausencia con `null`.

---

## 4. Revisión de implementación

- `_flatten()` inserta `rule_id` solo si la clave existe; no usa `.get()` para sintetizarlo.
- `compare_observed()` usa `_MISSING` para distinguished ausencia de metadatos y de `rule_id`.
- Errores deterministas, ordenados y con trazabilidad por ruta y campo/regla.
- Fail-closed: campo desconocido, metadato ausente, regla ausente y divergencia producen errores.
- No se introdujeron falsos PASS.
- La representación sigue derivada de R9 §5.4, diseño v4 §9.2 y schema v4; no lee ORACLE-ART-01/02/03/05 ni importa producción.

---

## 5. Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **17 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed**, 1 warning anyio |
| `git diff --check` | exit 0 |

El warning de `anyio` (`CallSpec2`) no afecta los resultados. Las pruebas anteriores no se debilitaron: el número de pruebas de representación pasó de 12 a 17.

---

## 6. Hallazgos nuevos

Ninguno. No hay severidades CRITICAL, HIGH, MEDIUM, LOW ni INFO pendientes.

---

## 7. Habilitación de artefactos

La representación es técnicamente apta para:

- **ORACLE-ART-06:** comparación determinista y trazable de los nueve metadatos y `rule_id`.
- **ORACLE-ART-07:** mutación aislada y reversible de `external_run_only` con detección verificada.

Esto **no** declara los artefactos materializados ni verificados: no se crearon ORACLE-ART-06 ni ORACLE-ART-07, no se ejecutó G5 ni G6 y no se autorizó Fase C. Falta además la revisión humana real para ORACLE-ART-04, por lo que G5 continúa bloqueada.

---

## 8. Limitaciones y estado Git

**Limitación:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen.

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin staged ni diff. `git diff --check`: exit 0. Sin commits ni push. No se accedió a Parquet protegidos. Único archivo creado: este informe.

```text
AUD-IMP-REP-R1-01: RESOLVED
AUD-ABS-FIX-R1-01: RESOLVED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

**Fin de R13-AUDIT-NATIVE-RULE-ID-ABSENCE-FIX-R1.**
