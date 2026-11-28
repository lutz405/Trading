# R13-ORACLE-G5-INDEPENDENT-VERIFICATION-REPRESENTATION-IMPLEMENTATION-R1 — Implementación de la representación independiente de verificación

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Alcance:** implementación en `tests/` autorizada por `docs/r13_oracle_g5_verification_representation_owner_approval_r1.md`. No ejecuta G5 ni G6; no crea ORACLE-ART-04, 06 ni 07.

---

## 1. Gates previos verificados

| Elemento | Evidencia | Resultado |
|---|---|---|
| HEAD / rama / remoto | `259ca6ee11878f114cdcab4cef500074b3bc1a48`, `main`, alineado | ✅ |
| Aprobación propietario | `VERIFICATION_REPRESENTATION_OWNER_APPROVAL: APPROVED` | ✅ |
| Auditoría de la aprobación | `R13-AUDIT-VERIFICATION-REPRESENTATION-OWNER-APPROVAL-R1 — ACCEPTED` | ✅ |
| Especificación Oracle R2 | SHA-256 `0ede7956…522e` | ✅ |
| Plan R2 | SHA-256 `d4d0c689…49e5` | ✅ |
| Decisiones D1–D6 | SHA-256 `6f408724…49e5` y aprobación `46b99d54…fbd8` | ✅ |
| Autorización de materialización | SHA-256 `d692e49e…49e5` | ✅ |

---

## 2. Archivos creados o modificados

| Archivo | Acción | SHA-256 | Git hash |
|---|---|---|---|
| `tests/oracle_verification_representation_v4_r5.py` | Creado | `9c4dcc4088dbd07f84a65e3accf633d708a12088403bf36748354fa3949bab20` | `05a7b1977fe9d75939d38e6d9e79b7aa349f46ac` |
| `tests/test_oracle_verification_representation_v4_r5.py` | Creado | `c01aae850729f8343b075cd80fb820a467ca8c2ba21336d5ba8c41ed7af66f48` | `8eca609dd055be16dab99244d5608e874e54f48b` |
| `docs/r13_oracle_g5_independent_verification_representation_implementation_r1.md` | Creado | Se reporta en el cierre | Se reporta en el cierre |

No se modificaron `provenance_v4.py`, schemas, dependencias ni artefactos Oracle existentes.

---

## 3. Justificación de arquitectura y fuentes

La representación vive íntegramente en `tests/`, como herramienta de CI/auditoría. No importa módulos productivos, no introduce dependencias externas (solo `pathlib`, `json`, `re`, `copy`, `contextlib`, `typing` y `pytest` en las pruebas, ya declarado) y no modifica el comportamiento del proyecto.

Fuentes normativas exclusivas:

- `docs/r13_phase_c_design_r9.md` §5.4: 109 filas plantilla → 139 rutas expandidas y nueve metadatos.
- `docs/aud04b_model_provenance_v4_design.md` §9.2: 24 filas de reglas → `rule_id` D1 `R9-9.2-NN`.
- `src/tradingai/schemas/manifest_v4.json`: contraste de tipo y nulabilidad.
- Decisiones D1–D6 aprobadas: `rule_id`, versión y convenciones.

**No se leen** ORACLE-ART-01, 02, 03 ni 05 como fuente. Las pruebas verifican que el módulo no contiene rutas `docs/oracle_artifacts` ni nombres de archivos de artefactos. ORACLE-ART-01, la representación de verificación y el código productivo permanecen como capas separadas y no intercambiables.

---

## 4. Trazabilidad de rutas y reglas

- `expected_entries()` produce **139 entradas únicas** ordenadas por `path`.
- Cada entrada conserva los **nueve metadatos** normativos: `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`.
- `rule_id` se mantiene **separado** del diccionario de metadatos; las 139 rutas usan **13 rule_id distintos** válidos dentro de las **24 filas normativas** mapeadas por `parse_design_rules()`.
- `schema_consistency_errors()` devuelve `[]`: tipos y nulabilidad coinciden con el schema v4, incluida la regla `shared_with` (obligatorio/permitido solo en calibration, prohibido en las demás particiones).
- Los bytes canónicos y el orden JCS no se usan para generar la representación; se evita cualquier dependencia de ORACLE-ART-03.

---

## 5. Capacidad preparada para ORACLE-ART-06 y ORACLE-ART-07

| Función | Propósito | Estado |
|---|---|---|
| `compare_observed(observed)` | Compara una observación con la representación; detecta paths ausentes/extra/duplicados, divergencia de los nueve metadatos y de `rule_id`; salida determinista y ordenada | Implementada; **ORACLE-ART-06 no creado** |
| `isolated_external_run_only_mutation(entries)` | Copia aislada y reversible; muta `external_run_only` → `always` en las tres rutas `calibration.base_*`; falla cerrado si no puede garantizar aislamiento | Implementada; **ORACLE-ART-07 no creado** |
| `mutation_detection_evidence(mutated)` | Detecta la mutación en las tres rutas y devuelve `DETECTED`/`NOT_DETECTED` con detalle | Implementada y probada en memoria |

No se escribió evidencia de ORACLE-ART-06 ni ORACLE-ART-07; la representación solo habilita su generación futura.

---

## 6. Pruebas y resultados

| Comando | Resultado | Detalle |
|---|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **7 passed**, 1 warning | 139 rutas, 13 reglas/24 normativas, esquema, comparación, mutación aislada, fail-closed e independencia de artefactos |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed**, 1 warning | Regresión v4; sin cambios productivos |

Cobertura evidenciada:

- **139 rutas:** unicidad, orden y pertenencia a la representación.
- **Nueve metadatos:** conjunto exacto por entrada y ausencia de `rule_id` dentro de metadatos.
- **Casos positivos:** observación idéntica a la representación → sin errores; mutación detectada en tres rutas.
- **Casos negativos:** tipo divergente, ruta ausente, ruta extra, entrada no aislada → errores deterministas.
- **Independencia:** el módulo no lee artefactos ni importa producción.
- **Dependencias:** sin imports productivos ni nuevas dependencias.

El único warning proviene del plugin `anyio` de pytest (`CallSpec2` renombrado); no afecta los resultados.

---

## 7. Limitaciones y hallazgos

**Hallazgos:** ninguno que bloquee la implementación. Durante las primeras ejecuciones se detectaron y corrigieron tres defectos en el propio código nuevo: recuento esperado de `rule_id`, manejo del campo `shared_with` prohibido fuera de calibration en el schema y una comprobación de independencia demasiado literal sobre el docstring. Las pruebas finales están en verde.

**Limitaciones:** la representación es de verificación, no normativa; no crea ORACLE-ART-06/07 ni sustituye la revisión humana pendiente de ORACLE-ART-04. G5 continúa `BLOCKED`.

---

## 8. Estado Git inicial y final

| Momento | HEAD | Rama / remoto | Estado |
|---|---|---|---|
| Inicial | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Sin staged ni diff; `diff --check` exit 0 |
| Final | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Dos archivos nuevos en `tests/` + este informe; sin staged ni diff; `diff --check` exit 0 |

Sin commits ni push; índice Git sin cambios. No se accedió a Parquet protegidos.

---

## 9. Estados finales

```text
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
ORACLE-ART-01: VERIFIED
ORACLE-ART-02: VERIFIED
ORACLE-ART-03: VERIFIED
ORACLE-ART-04: NOT_CREATED
ORACLE-ART-05: CREATED_UNVERIFIED
ORACLE-ART-06: NOT_CREATED
ORACLE-ART-07: NOT_CREATED
```

La implementación se detiene aquí. **No se ejecuta G5 ni G6**, no se crean artefactos adicionales y no se autoriza Fase C.

**Fin de R13-ORACLE-G5-INDEPENDENT-VERIFICATION-REPRESENTATION-IMPLEMENTATION-R1.**
