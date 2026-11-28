# R13 — ART-04 EXCLUSION EVIDENCE COMPLETION R1

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Alcance:** completar la evidencia pendiente de `G-04` relativa a las 11 reglas excluidas de ORACLE-ART-01.

**Resultado: `G-04: VERIFIED`.** Las 11 exclusiones tienen correspondencia normativa explícita y evidencia negativa reproducible y trazable.

---

## 1. Fuentes, hashes y clasificación

| Fuente | SHA-256 | Uso |
|---|---|---|
| `docs/r13_art_04_evidence_gap_resolution_r1.md` | `1052f23e0b1f520e66c01576451e309e0696245c05be3caad9b194e6228d6b10` | Origen de la brecha G-04 |
| `docs/aud04b_model_provenance_v4_design.md` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | §9.2, 24 filas normativas |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | §5.4, autoridad de las 139 rutas |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | D1: `rule_id` secuencial por fila de §9.2 |
| `docs/r13_oracle_artifacts_specification_r5.md` | `c124cd74045ed7721bff5f0a91cd1ec379ca0aac683e729fd1bf785801dde409` | Requisitos vigentes |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | 139 rutas, 13 `rule_id` usados |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` | Cobertura y negativos existentes |
| `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` | Representación independiente |
| `tests/test_oracle_verification_representation_v4_r5.py` | `132bad37b05960e828e8271b7b3cfeaebe220df7506d0af8a1fa0d9367649058` | Suite de 17 pruebas |
| `tests/oracle_normative_v4_r5_verifier.py` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` | ORACLE-ART-02 |

Todos los hashes se recalcularon y coinciden.

**Nota sobre la numeración:** §9.2 no imprime los identificadores `rule_id`; D1 (aprobado) prescribe asignación secuencial `R9-9.2-NN` por fila. La tabla siguiente aplica ese convenio normativo a las 24 filas en orden. No es una inferencia de contenido: es la ejecución determinista de una decisión aprobada, y coincide con los 13 identificadores usados observados en ART-01 y con los 11 enumerados en Protocolo R4 §9.6.

---

## 2. Tabla D1 explícita de las 11 reglas excluidas

| `rule_id` | Fuente normativa | Condición de exclusión | Justificación (según §9.2) | Evidencia correspondiente | Resultado esperado al evaluarla como excluida |
|---|---|---|---|---|---|
| `R9-9.2-02` | Diseño v4 §9.2 fila 2 | `model_id`, `created_at`, `sealed_at`, `status_at_seal`, `run_fingerprint` | Identidad de salida, timestamps, estado de sello y resultado del propio cálculo | 5 rutas ausentes en ART-01 y ART-05; 5/5 `EXTRA_PATH` reproducidos | No incorporar; si se inyectan ⇒ `EXTRA_PATH:<ruta>` |
| `R9-9.2-04` | §9.2 fila 4 | `git.commit`, `git.dirty`, `git.branch`, `git.tag` | Localizador/meta; `dirty=false` se valida como admisión | 4 rutas ausentes; 4/4 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-06` | §9.2 fila 6 | `producer.command` | Texto de invocación sin normalización entre shells | 1 ruta ausente; 1/1 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-08` | §9.2 fila 8 | `data.snapshot_uri` | Ubicación; el hash del contenido identifica los datos | 1 ruta ausente; 1/1 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-16` | §9.2 fila 16 | `validation.purge.label_purge_satisfied`, `validation.leakage_checks.disjoint`, `validation.leakage_checks.purge_satisfied`, `validation.leakage_checks.labels_within_partition` | Resultados derivados; todos deben validarse como `true` | 4 rutas ausentes; 4/4 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-17` | §9.2 fila 17 | `validation.partition_manifest_sha256` | Digest derivado de las cuatro particiones | 1 ruta ausente; 1/1 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-18` | §9.2 fila 18 | `validation.evaluation.metric_spec_version`, `primary_metric`, `test_evaluated_once`, `evaluation_code_sha256`, `evaluated_at` | Protocolo/resultado de evaluación; `evaluated_at` temporal | 5 rutas ausentes; 5/5 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-21` | §9.2 fila 21 | `calibration.calibration_input_sha256`, `calibration.artifact_sha256` | Digest de entradas derivadas y artefacto de salida | 2 rutas ausentes; 2/2 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-22` | §9.2 fila 22 | `artifacts[]` y `role`, `path`, `sha256`, `bytes`, `media_type`, `format`, `serializer` | Outputs; se valida exactamente un artefacto por rol | 8 rutas ausentes; 8/8 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-23` | §9.2 fila 23 | `metrics.path`, `metrics.sha256`, `metrics.schema_version` | Resultados evaluativos | 3 rutas ausentes; 3/3 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |
| `R9-9.2-24` | §9.2 fila 24 | `extensions` | Excluido del fingerprint; queda cubierto por `manifest.sha256` | 1 ruta ausente; 1/1 `EXTRA_PATH` | No incorporar; inyección ⇒ `EXTRA_PATH` |

**Totales:** 11 reglas, **35 rutas excluidas** contrastadas, 35/35 ausentes en ART-01 y ART-05, 35/35 detectadas como `EXTRA_PATH`.

---

## 3. Casos negativos y contraste con ART-02 y ART-05

### 3.1 Construcción de los casos negativos

En un directorio aislado bajo `%TEMP%` se copiaron, sin modificar los originales: la representación independiente, su suite de pruebas, ART-01, ART-05, R9, diseño v4 §9.2 y `manifest_v4.json`. Se construyó una línea base con las 139 entradas de ART-01 y para cada una de las 35 rutas excluidas se inyectó una entrada con esa ruta y el `rule_id` de su regla. Se ejecutó `compare_observed()` sobre cada variante.

| Comprobación | Resultado |
|---|---|
| Línea base ART-01 (139 entradas) | 0 errores |
| Rutas en ART-01 / ART-05 | 139 / 139 |
| Rutas excluidas presentes en ART-01 | 0 de 35 |
| Rutas excluidas presentes en ART-05 | 0 de 35 |
| Inyecciones detectadas como `EXTRA_PATH` | **35 de 35** |
| `ART-02 verify()` en copia aislada | `[]` (sin errores) |
| Suite de representación (copia aislada) | **17 passed**, 1 warning `anyio` |

### 3.2 Contraste con ART-02

ART-02 verifica versión, integridad y checksum de la transcripción; **no evalúa reglas de exclusión**. Su resultado `[]` confirma que la transcripción es íntegra, pero **no** constituye evidencia directa de las exclusiones. Por tanto, la evidencia negativa de G-04 proviene de la representación independiente y del cotejo de conjuntos con ART-01/ART-05, no de ART-02. Esta distinción se registra expresamente.

### 3.3 Contraste con ART-05

ART-05 contiene 139 filas, 139 casos positivos y 556 negativos (ausencia, duplicación, ruta desconocida y divergencia), con `NO_DIVERGENCE` y 0 fallos. Su mecanismo de detección de ruta desconocida es el mismo que se aplicó a las 35 rutas excluidas: una ruta no incluida en la representación produce `EXTRA_PATH`. La diferencia es que ART-05 ejecuta ese mecanismo sobre una ruta genérica, mientras que esta tarea lo ejecuta sobre las rutas concretas de las 11 reglas excluidas, con trazabilidad a §9.2.

---

## 4. Clasificación por regla

| Grupo | Reglas | Clasificación | Motivo |
|---|---|---|---|
| Demostradas | `02`, `04`, `06`, `08`, `16`, `17`, `18`, `21`, `22`, `23`, `24` (11/11) | **`VERIFIED`** | Correspondencia normativa explícita en §9.2 + D1; 35/35 rutas ausentes en artefactos y detectadas como `EXTRA_PATH` en ejecución aislada reproducible |
| Corroboradas | — | Sin reglas | No aplica tras la ejecución |
| No demostrables con evidencia disponible | — | Sin reglas | No aplica |

Si un auditor externo requiere una reconstrucción realizada por proveedor distinto, esa circunstancia pertenece a la independencia general (EXT-01/EXT-02), no a la suficiencia técnica de esta evidencia; no reabre G-04 por sí sola.

---

## 5. Impacto y cierre de G-04

| Elemento | Antes | Después |
|---|---|---|
| Correspondencia normativa | Derivada de filas §9.2, sin tabla explícita | Tabla D1 explícita de 11 reglas en §2 |
| Evidencia negativa | Genérica (ART-05), no por regla | 35/35 rutas con caso negativo reproducido |
| Estado | `CORROBORATED` | **`VERIFIED`** |

`G-04: VERIFIED` conforme al criterio de cierre: las 11 exclusiones tienen correspondencia normativa explícita y evidencia negativa suficiente, reproducible y trazable. Este cierre es **técnico y documental**; no declara ART-04 aceptado, no resuelve `DEC-OWNER-AI-04` y no desbloquea G5/G6 ni Fase C.

---

## 6. Limitaciones

- ART-02 no cubre exclusiones; su resultado `[]` solo acredita integridad de ART-01.
- La asignación `rule_id` → fila aplica el convenio D1; §9.2 no imprime los identificadores.
- Las ejecuciones se realizaron sobre copias en `%TEMP%`; los archivos del repositorio no fueron modificados.
- No se ejecutó una reconstrucción por proveedor acreditado como distinto; la procedencia del generador sigue `PROVENANCE_UNVERIFIABLE`.

---

## 7. Estados y cierre

```text
G-04: VERIFIED
ORACLE-ART-04: NOT_CREATED
DEC_OWNER_AI_04_STATUS: NOT_SATISFIED
EXT_01: NOT_CLOSED
EXT_02: NOT_CLOSED
R5: NOT_APPROVED / NOT_AUDITED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni unstaged; `git diff --check` exit 0. Sin commits ni push. Único archivo creado: este informe. No se modificaron ARTs, normativas, producción, tests, schemas, dependencias ni Parquet; no se creó ART-04 ni se ejecutaron G5/G6.

**Fin de R13-ART-04-EXCLUSION-EVIDENCE-COMPLETION-R1.**
