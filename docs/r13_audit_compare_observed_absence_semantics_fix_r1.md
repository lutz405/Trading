# R13-AUDIT-COMPARE-OBSERVED-ABSENCE-SEMANTICS-FIX-R1 — Informe de auditoría independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto auditado:** corrección de `AUD-IMP-REP-R1-01` en `tests/oracle_verification_representation_v4_r5.py` y sus pruebas.
**Restricción:** solo lectura, salvo este informe. No se corrigió código durante la auditoría.

---

## 1. Dictamen

**ACCEPTED WITH FINDINGS.** El defecto MEDIUM original está resuelto: `compare_observed()` distingue ausencia de `None` y reporta cada categoría por ruta y metadato. Se detectó un hallazgo LOW adicional en `_flatten()` para el formato nativo con `metadata`, donde una ausencia de `rule_id` se reporta como divergencia con valor `None` en lugar de `RULE_MISSING`. No produce falso PASS, pero debe corregirse antes de declarar plenamente cerrada la semántica de ausencia.

---

## 2. Resolución del hallazgo MEDIUM original

| Caso | Antes (auditoría previa) | Después (auditoría actual) |
|---|---|---|
| `manifest_required_when` ausente, esperado `None` | `ERRORS []`, `COUNT 0` | `METADATA_MISSING:calibration.base_artifact_sha256.rf:manifest_required_when` |
| Clave presente con `None`, esperado `None` | No cubierto | Sin errores; `None` legítimo conservado |
| Clave presente con valor concreto distinto | No cubierto | `METADATA_DIVERGENCE:…:type:expected='string':observed='number'` |
| Campo desconocido | No cubierto | `UNKNOWN_FIELD:…:campo_desconocido` |
| Metadato ausente (`manifest_required=True`) | No cubierto | `METADATA_MISSING:…:manifest_required` |
| `rule_id` ausente en forma plana | No cubierto | `RULE_MISSING:…` |
| `rule_id` divergente | No cubierto | `RULE_DIVERGENCE:…` |
| Determinismo | No cubierto | Salidas idénticas en ejecuciones repetidas |

**AUD-IMP-REP-R1-01: RESOLVED** para la ruta plana.

---

## 3. Matriz de pruebas

| Comando | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **12 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed**, 1 warning anyio |
| Script de auditoría con ocho casos reproducidos | Categorías verificadas; ver §2 y §4 |
| `git diff --check` | exit 0 |

El warning de `anyio` (`CallSpec2`) no afecta los resultados. No se añadieron pruebas de auditoría al repositorio; se usó un script temporal eliminado.

---

## 4. Hallazgo adicional

| ID | Severidad | Ubicación | Evidencia | Consecuencia | Corrección requerida | Bloquea |
|---|---|---|---|---|---|---|
| **AUD-ABS-FIX-R1-01** | **LOW** | `_flatten()` líneas 206–211 de `tests/oracle_verification_representation_v4_r5.py` | Entrada nativa `{"path":…, "metadata":{…}}` sin clave `rule_id` outer produce `observed='None'` y `RULE_DIVERGENCE`, no `RULE_MISSING`. Reproducido: `RULE_DIVERGENCE:calibration.base_artifact_sha256.rf:R9-9.2-20:None` | Confusión residual entre ausencia y `null` para `rule_id` en formato nativo; **no** falso PASS | No sintetizar `rule_id=None` en `_flatten()`; conservar ausencia con centinela | Aceptación plena; no bloquea ART-06 con observaciones planas |

No se encontraron otras rutas que confundan ausencia con `null` en los nueve metadatos. `observed_paths` usa `.get("path")`, pero una ruta ausente se reporta como `EXTRA_PATH:None`, no como PASS.

---

## 5. Revisión de implementación

- `_MISSING = object()` se usa correctamente en la comparación de metadatos y `rule_id` en `compare_observed()`.
- No se usa `.get()` para comparar valores de metadatos dentro de `compare_observed()`.
- Fail-closed: campos desconocidos, rutas duplicadas/ausentes/extra y errores de regla generan entradas deterministas y ordenadas.
- Trazabilidad: todos los errores relevantes incluyen `ruta` y `campo` o `rule_id`.
- No se introdujeron falsos PASS en los casos reproducidos.
- No se alteraron las 139 rutas, los nueve metadatos, las 24 filas normativas ni D1–D6.

---

## 6. Hashes

| Archivo | SHA-256 | Git hash |
|---|---|---|
| Informe de corrección | `3d1aa7429356ea4742e885c979c06c3aaf50ac67dbff94d14992a1cc87555eb1` | `de3e180e06d6cfd1ba26a38b4166113076e8d0dd` |
| `tests/oracle_verification_representation_v4_r5.py` | `548da2fc507b38c5fe764050581a7ba4528cbfa1b31d788f98b3a8390d2e1cc6` | `88b565aef8bfbfa19e3d7ec2cd7a100a4a328032` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `80dc8ea2076c2c4f863992c12dd5f242b59306508ebac2225100e1935801f164` | `d697516e9bbd46f3b62581f898458442c217ab4b` |
| Auditoría previa de implementación | `241107f5e5df165153ef8fc275faf42993984d3e5e3c7d967440f44e32cf25ed` | `595672caae04807966c7c83e7e608d670e607b05` |
| `provenance_v4.py` | `3216d8919a82e61ff4c1fba238f130ce2283e2c363e46c315114042c002c8a6b` | `9b4c16ea08591d649bbdc6e4641eca62fa25e8f7` |
| `manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |
| `pyproject.toml` | `0d127c0b39ddafabd2aa8f890b3ea847f731b402f2a41ba948e9b2005fb5c12a` | `ff15764bf9907c0a0b3d2f43ad26b49ce4049715` |

Artefactos Oracle 01/03/05 y verificador sin cambios.

---

## 7. Estado Git y límites

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin staged ni diff. `git diff --check`: exit 0. Sin commits ni push; sin acceso a Parquet. Único archivo creado por esta auditoría: este informe. No se crearon ORACLE-ART-04/06/07 ni se ejecutaron G5/G6 o Fase C.

**Limitación:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen.

---

## 8. Conclusión sobre ART-06

El hallazgo MEDIUM original está corregido y la semántica de ausencia es correcta para observaciones en forma plana, que es el contrato previsto para ORACLE-ART-06. **Puede prepararse ORACLE-ART-06** con la condición de usar observaciones planas o corregir primero el hallazgo LOW de `_flatten()` si se va a aceptar el formato nativo. No se ejecutó G5 ni se creó el artefacto.

```text
AUD-IMP-REP-R1-01: RESOLVED
AUD-ABS-FIX-R1-01: LOW (pendiente)
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

**Fin de R13-AUDIT-COMPARE-OBSERVED-ABSENCE-SEMANTICS-FIX-R1.**
