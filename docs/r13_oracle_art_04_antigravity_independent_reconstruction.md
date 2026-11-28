# R13-ORACLE-ART-04 — Reconstrucción normativa independiente (Google Antigravity)

**Naturaleza:** reconstrucción normativa independiente previa a la lectura y comparación de las cinco propuestas candidatas (`C-01`…`C-05`).
**Fuentes utilizadas exclusivamente:** `docs/r13_oracle_art_04_external_review_handoff_r1.md` (`S-01`…`S-10` y `A-01`…`A-04`), cuyos 19 SHA-256 fueron verificados antes del análisis.
**Exclusión verificada:** no se consultaron las cinco propuestas candidatas (`C-01`…`C-05`), informes `r13_audit_*`, `audit_report_r13_oracle_art_04.md`, conclusiones del generador ni resúmenes previos.
**Fecha y hora de creación:** `2026-11-27T17:19-06:00` (el hash SHA-256 y la marca temporal exacta del archivo se registran inmediatamente tras su escritura en el informe de auditoría).

---

## 1. Decisiones D1–D6, decisiones `DEC-OWNER-AI-01`–`06` y aprobaciones del propietario

### 1.1 Decisiones D1–D6 (S-03 §3–§4, A-02 §2.1)

Aprobadas expresamente por el propietario en `docs/r13_oracle_artifacts_decision_owner_approval_r1.md` (`A-02`, fecha `2026-11-27`, `DECISION_RESOLUTION_OWNER_APPROVAL: APPROVED`), sobre `docs/r13_oracle_artifacts_decision_resolution_r2.md` (`S-03`):

| ID | Decisión aprobada | Estado original (A-02) | Alcance / regla clave |
|---|---|---|---|
| **D1** | Formato `rule_id`: identificadores secuenciales por fila de §9.2, con tabla de correspondencia revisada (`ruta expandida → rule_id → fila §9.2`) | `APPROVED` | Se asigna durante `ORACLE-ART-01`; `rule_id` ausente o duplicado rechaza la transcripción (fail-closed) |
| **D2** | Ubicación física: versionada de artefactos en el repositorio; referencias externas únicamente para recursos inmutables; `ORACLE-ART-02` separado de transcripción y evidencias, en ámbito de CI/auditoría y sin importaciones productivas | `APPROVED` | Política de no sobrescritura de versiones revisadas; nunca en el camino productivo |
| **D3** | Revisor independiente designado por función, con identidad funcional real y evidencia documentada de independencia | `APPROVED` | En `S-03` §3.3 / `A-02`: exige **revisor humano independiente** distinto del generador; identidad real registrada al ejecutar; sin independencia declarada se rechaza `ORACLE-ART-04` |
| **D4** | Formato de evidencias: texto UTF-8 determinista con campos obligatorios y JSON JCS derivado exclusivamente auxiliar, sin modificar la preimagen de `ORACLE-ART-03` | `APPROVED` | La preimagen de `ORACLE-ART-03` sigue siendo exclusivamente `{"version": ..., "entries": [...]}` según R9 §5.8.5; sin octavo artefacto |
| **D5** | Convención de versiones: mantener `ORACLE_NORMATIVE_V4_R5` mientras §9.2 no cambie; correcciones no semánticas documentadas sin incrementar versión (si no alteran bytes canonicalizados); cambios semánticos sujetos a nueva versión aprobada y auditada | `APPROVED` | Versión desalineada activa `ORACLE_VERSION_MISMATCH` |
| **D6** | Arquitectura de `ORACLE-ART-02`: verificador ubicado en `tests/`, sin importaciones de producción ni dependencias nuevas en `pyproject.toml`, con entradas declaradas y cerradas | `APPROVED` | Sin fallback silencioso; determinista; producción no importa el oracle |

Secuencia de resolución de `S-03` §4.1: `D1, D2, D5` antes de `ORACLE-ART-01`; `D6` antes de `ORACLE-ART-02`; `D4` antes de `ORACLE-ART-05/06`; `D3` antes de `ORACLE-ART-04`.

### 1.2 Decisiones habilitantes `DEC-OWNER-AI-01`–`06` (S-07, S-08)

Propuestas en `S-07` y aprobadas individualmente en `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` (`S-08`, fecha `2026-11-27`, `OWNER_DECISIONS: APPROVED`, `AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS`):

| ID | Contenido aprobado | Restricción esencial |
|---|---|---|
| `DEC-OWNER-AI-01` | Admite `INDEPENDENT_AI_REVIEW` **exclusivamente** para `ORACLE-ART-04`, bajo controles de protocolo R2 y previa resolución de AI-02..AI-06 | No equivale a revisión humana; no modifica ART-01/02/03/05/06/07; no crea excepción general; no autoriza Fase C; `HUMAN_INDEPENDENT_REVIEW` sigue válida y preferente |
| `DEC-OWNER-AI-02` | Autoriza preparar y aprobar **Autorización de Materialización R3**, conservando R2 como registro histórico (`d692e49e...`) | R3 levanta la prohibición de R2 §3 únicamente para `INDEPENDENT_AI_REVIEW` en ART-04; surte efecto solo tras aprobar enmienda D3, Spec R3 y Plan R3, y tras auditoría independiente |
| `DEC-OWNER-AI-03` | Supera literalmente `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1 únicamente para admitir revisión automatizada regulada en ART-04 por indisponibilidad de revisor humano real | La recomendación original se conserva íntegra sin borrarse ni reinterpretarse; vía humana vigente para cualquier otro artefacto/revisión |
| `DEC-OWNER-AI-04` | Fija 9 controles obligatorios de independencia para toda `INDEPENDENT_AI_REVIEW` | Mismo proveedor o limitación no demostrable obliga a `INCONCLUSIVE`; dos ejecuciones del mismo modelo no bastan |
| `DEC-OWNER-AI-05` | Separa dictamen técnico de la IA, confirmación de severidad por auditor posterior y autoridad de aceptación del propietario | Solo dictámenes `ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED`, `INCONCLUSIVE` y severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`; `INCONCLUSIVE` y `REJECTED` nunca desbloquean G5; `ACCEPTED_WITH_FINDINGS` no desbloquea G5 con `BLOCKER`/`HIGH` abiertos |
| `DEC-OWNER-AI-06` | Confina los límites de la modalidad | No autoriza Fase C, cambios productivos/schemas/dependencias, Parquet, ejecución automática de G5/G6, cambios a ART-01/02/03/05/06/07 ni commits/push |

Orden de enmiendas exigido por `S-08` §3: (1) protocolo R1 → R2; (2) enmienda versionada de D3; (3) especificación R3; (4) plan R3; (5) autorización de materialización R3; (6) auditoría independiente del paquete de enmiendas; (7) aprobación expresa posterior del resultado de esa auditoría.

---

## 2. Jerarquía normativa entre DEC-06, diseño v4 §9.2 y `manifest_v4.json`

Según `S-01` §5.8, `S-02` §9.2, `S-04` §2 y `S-10`:

1. **Nivel 1 — Autoridad normativa (`DEC-06` y `docs/aud04b_model_provenance_v4_design.md` §9.2):** determinan qué rutas entran en `run_fingerprint`, cuáles se excluyen y las condiciones normativas (`external_run_only` para `calibration.base_*`, `shared_with == "validation"` en `calibration`, normalización UTC de timestamps, exclusión de timestamps de auditoría/salida y digests derivados). Ningún documento de implementación ni test las modifica.
2. **Nivel 2 — Contrato estructural canónico (`src/tradingai/schemas/manifest_v4.json`, `S-10`):** define `required`, nulabilidad (`["<tipo>", "null"]`), tipos JSON, `additionalProperties: false`, `$defs/partition` y `$defs/calibration_partition`. No codifica condiciones normativas de proyección como `external_run_only`.
3. **Nivel 3 — Representación ejecutable única (`ALLOWLIST_V4` en `provenance_v4.py`):** representación derivada en producción; no es una fuente normativa nueva y debe demostrar igualdad con Nivel 1 y Nivel 2.
4. **Nivel 4 — Oracle normativo independiente (`ORACLE_NORMATIVE_V4_R5`):** transcrito directamente desde §9.2/DEC-06 (no copiado de `ALLOWLIST_V4` ni del schema); utilizado únicamente en CI/auditoría, nunca importado por producción.
5. **Nivel 5 — Implementación aceptada de Fase A/B (`validate_manifest_v4` y rutinas auxiliares):** contrato de validaciones productivas ya aprobadas; permanece intacto.

La IA revisora o auditora externa **no** constituye fuente normativa en ningún nivel.

---

## 3. Los siete artefactos Oracle y sus responsabilidades

Según `S-01` §5.8.5, `S-04` §4–§5 y `S-05` §2 y §4 (todos en estado `NOT_CREATED`, sin octavo artefacto):

1. **ORACLE-ART-01 — Transcripción normativa completa e independiente:** objeto `{"version": ..., "entries": [...]}` ordenado por `path` con **139 rutas expandidas** (`{partition}` → `train`, `validation`, `calibration`, `test`) y **10 campos** por entrada (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`, `rule_id`), transcrita directamente de §9.2/DEC-06; incluye P1–P5, matriz O/A de 9 combinaciones, I1–I12, §§5.2/5.5/5.7, fail-closed. Dependencias: ninguna.
2. **ORACLE-ART-02 — Versión ejecutable del oracle:** verificador independiente en CI/auditoría (ubicado en `tests/` según D6), sin importaciones productivas ni dependencias nuevas en `pyproject.toml`, determinista y sin fallback. Dependencias: `ORACLE-ART-01`.
3. **ORACLE-ART-03 — SHA-256 de la transcripción canonicalizada:** `SHA-256` hex minúsculo de 64 caracteres sobre `rfc8785.dumps({"version": ..., "entries": [...]})` en UTF-8 sin BOM ni LF final. No hashea archivos auxiliares, el propio checksum ni los bytes ejecutables de `ORACLE-ART-02`. Dependencias: `ORACLE-ART-01`, `ORACLE-ART-02`.
4. **ORACLE-ART-04 — Registro de revisión humana independiente:** evidencia de revisión semántica contra §9.2 por revisor independiente distinto del generador (bajo R2/D3: humano; bajo `DEC-OWNER-AI-01..06` tras enmiendas aprobadas: alternativamente `INDEPENDENT_AI_REVIEW` sin llamarla revisión humana). Dependencias: `ORACLE-ART-01`, `ORACLE-ART-03`.
5. **ORACLE-ART-05 — Evidencia de cobertura de las 139 rutas:** matriz de 139 filas únicas expandidas con ruta normativa, condición de aplicabilidad, comportamiento esperado, resultado observado, caso positivo/negativo, evidencia reproducible y `rule_id`; igualdad de conjuntos bidireccional (`ALLOWLIST_MISSING_PATH` / `ALLOWLIST_EXTRA_PATH`). Dependencias: `ORACLE-ART-01`, `ORACLE-ART-02`.
6. **ORACLE-ART-06 — Evidencia de comprobación de los nueve metadatos:** comparación campo por campo de los **9 metadatos** exactos de `AllowlistEntry` (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`) para cada ruta común; `rule_id` queda excluido de los 9; divergencias con `ALLOWLIST_ORACLE_METADATA_DIVERGENCE`. Dependencias: `ORACLE-ART-01`, `ORACLE-ART-02`, `ORACLE-ART-05`.
7. **ORACLE-ART-07 — Evidencia de la mutación `external_run_only`:** en copia aislada de `ALLOWLIST_V4`, mutar `projection_include_when` de `external_run_only` a `always` únicamente en `calibration.base_model_id`, `calibration.base_artifact_sha256.rf` y `calibration.base_artifact_sha256.xgb`; verificar detección por el oracle (`ALLOWLIST_ORACLE_METADATA_DIVERGENCE` en esas 3 rutas y ninguna adicional), con reversibilidad y aislamiento. Dependencias: `ORACLE-ART-01`, `ORACLE-ART-02`, `ORACLE-ART-06`.

---

## 4. Condiciones de G0–G6

Según `S-05` §8 y `S-06` §§1, 3 y 5:

- **G0 (Especificación aprobada):** `S-04` (`R2`) aprobada por el propietario (`A-03`) y auditada `ACCEPTED`; registro de aprobación vigente; rechazo si hash diverge o auditoría no favorable.
- **G1 (Plan revisado):** plan documental completo y cotejado con R9/R2 (`S-05`, aprobado en `A-04`), sin contradicciones y sin convertir decisiones pendientes en aprobadas.
- **G2 (Fuentes y herramientas verificadas):** §9.2, schema y R2 disponibles; decisiones críticas registradas/resueltas; procedencia documentada; rechazo si fuente modificada o decisión crítica sin resolver.
- **G3 (Autorización de materialización):** decisión expresa del propietario registrada (`S-06`, `MATERIALIZATION_AUTHORIZATION_STATUS: GRANTED` para `ORACLE-ART-01`…`07` bajo Plan R2); ninguna aprobación previa equivale a G3.
- **G4 (Artefactos generados):** G3 concedido; `ORACLE-ART-01`…`07` generados con sus estados documentados; rechazo si artefacto incompleto o no reproducible.
- **G5 (Verificación independiente):** G4 completo; revisión independiente realizada (en Plan R2: revisión humana); evidencia de verificación y dictamen; rechazo por discrepancia no resuelta o revisión no independiente.
- **G6 (Resolución de AUD-R8-02):** superación sujeta a las 5 condiciones conjuntas de §6 siguiente.

---

## 5. Las ocho condiciones conjuntas de G5

Observación verificable en las fuentes originales `S-01`…`S-10` y `A-01`…`A-04`:
- En `S-05` §8 (tabla de puertas), G5 se formula con criterio de entrada (`G4 completo; revisión humana realizada`), criterio de salida (`Evidencia de verificación y dictamen`) y rechazo (`Discrepancia no resuelta; revisión no independiente`).
- En `S-05` §5.1 («Protocolo» de verificación independiente), se enumeran exactamente **8 verificaciones obligatorias**:
  1. **Integridad:** recalcular `SHA-256` de `ORACLE-ART-03` desde la transcripción (preimagen y valor reproducibles por verificador distinto).
  2. **Correspondencia R2:** cotejar cada artefacto con §4.1–§4.7 de `S-04` (matriz sin campo omitido ni añadido).
  3. **139 rutas:** igualdad de conjuntos en ambos sentidos (`ORACLE-ART-05`, 139 rutas únicas con semántica).
  4. **Nueve metadatos:** comparación campo por campo (`ORACLE-ART-06`, 9 nombres exactos de `S-04` §4.6).
  5. **`rule_id`:** comprobar que es décimo campo de trazabilidad en `ORACLE-ART-01`, no contado entre los nueve.
  6. **P1–P5 e I1–I12:** revisión semántica de la transcripción contra R9 §5.8.3 y §5.7.
  7. **Revisión humana (o vía autorizada tras enmienda):** auditoría de `ORACLE-ART-04` (real, independiente, con hallazgos resueltos).
  8. **Mutación:** comparar salida antes/después en copia aislada (`ORACLE-ART-07`, detección por oracle en las 3 rutas `base_*`).
- Adicionalmente, `S-06` §5 lista condiciones operativas de ejecución (G0–G3 cumplidas, generación conforme a D1–D6, revisión + auditoría independiente, 139 rutas/9 metadatos/`rule_id`/P1–P5/I1–I12, mutación aislada).
- **Nota de rigor:** en `S-01`…`S-10` y `A-01`…`A-04` no figura una lista explícita rotulada literalmente «ocho condiciones conjuntas de G5» (presumiblemente originada en `r13_oracle_g5_blocker_resolution_analysis_r1.md`, que no forma parte de `S-01`…`S-10`). Se auditará la coherencia de cualquier formulación candidata frente a estos requisitos verificables en `S-05` y `S-08`.

---

## 6. Las cinco condiciones conjuntas de G6

Según `S-05` §8 (`G6 (AUD-MAT-PLAN-R1-01)`, línea 190), G5 favorable **no** equivale a superar G6; deben concurrir conjuntamente:

1. Los **siete artefactos** requeridos están materializados y sus estados individuales verificados.
2. Existe un **informe de auditoría independiente favorable** que verifica los criterios correspondientes a `AUD-R8-02`.
3. **No quedan hallazgos bloqueantes** sin resolver.
4. El **propietario ha emitido aceptación expresa** del resultado de la auditoría, independiente de la aceptación técnica del auditor.
5. Existe **evidencia documental trazable** de cada requisito anterior.

Superar G6 **no** autoriza por sí mismo la implementación de Fase C (requiere decisión técnica separada y explícita).

---

## 7. Requisitos originales de revisión humana para ART-04

Según `S-01` §5.8.1 y §5.8.5, `S-03` §3.3 (D3), `S-04` §3.2 y §4.4, `S-05` §§2, 4 y 7, y `S-06` §§3 y 5:

- Revisor **persona real funcionalmente independiente**, distinto del generador (el generador no puede ser su propio/único revisor).
- Identidad funcional designada por el propietario e identidad real verificable registrada al ejecutarse (sin inventar nombres ni firmas).
- Revisión semántica real fila por fila contra §9.2; el checksum de `ORACLE-ART-03` **no** sustituye la revisión semántica.
- Contenido mínimo obligatorio de `ORACLE-ART-04`: identidad funcional del revisor, declaración de independencia respecto de la implementación, versión revisada, checksum revisado, alcance, casos examinados (cubriendo 139 rutas, 9 metadatos y mutación), hallazgos, resolución de hallazgos, dictamen favorable, fecha real de la revisión y evidencia de aprobación.
- Fail-closed: plantilla vacía, revisor no independiente, ausencia de hallazgos examinados, fecha/dictamen no verificables o checksum divergente provocan rechazo.
- La revisión humana **no** equivale a aprobación del propietario.

---

## 8. Condiciones de independencia, trazabilidad y reproducibilidad

### 8.1 Del sistema de oracle (`S-01` §5.8, `S-04` §6, `S-05` §§3, 5, 7)

- **No circularidad:** `ORACLE-ART-01` se transcribe de §9.2/DEC-06, nunca desde `ALLOWLIST_V4` ni desde el schema; producción no importa el oracle (`provenance_v4.py` usa solo `ALLOWLIST_V4`); el schema se contrasta por separado; los tests no se convierten en fuente normativa.
- **Trazabilidad:** `rule_id` por cada una de las 139 rutas hacia una fila de §9.2; conservación de fuentes exactas consultadas, notas de expansión y correspondencia `rule_id`.
- **Reproducibilidad:** mismas entradas → misma salida determinista, ordenada y deduplicada (`list[str]`), sin timestamps ni aleatoriedad en decisiones; recálculo independiente de `ORACLE-ART-03` (`SHA-256(JCS)`), conservación de copias antes/después en `ORACLE-ART-07`.

### 8.2 Específicas para `INDEPENDENT_AI_REVIEW` (`DEC-OWNER-AI-04`, `DEC-OWNER-AI-05` en `S-07`/`S-08`, y controles `S-09` §§5–11)

1. Proveedor y modelo distintos del generador, con declaración de linaje.
2. Sesión limpia sin historial previo.
3. Fuentes normativas originales, sin resúmenes derivados del generador.
4. Ausencia de dictámenes o conclusiones previos en el contexto inicial.
5. Prompt íntegro y hashes de todos los archivos de entrada conservados.
6. Linaje y contexto registrados, con inventario de herramientas y parámetros disponibles.
7. Reconstrucción independiente de las reglas en artefacto hashable anterior a la comparación.
8. Auditor posterior distinto de la IA revisora y del generador, con evaluación a ciegas.
9. Limitaciones de independencia expresamente declaradas.
10. Mismo proveedor o limitación no demostrable obliga a `INCONCLUSIVE`; dos ejecuciones del mismo modelo no constituyen independencia suficiente.
11. Registro íntegro de evidencias y referencia a la transcripción/salida original; prohibido inventar versiones, fechas o identidades (`NO_DISPONIBLE` si faltan).

---

## 9. Límites de autoridad del propietario

Según `A-01`…`A-04`, `S-06` §3 y `S-07`/`S-08`:

- El propietario (`Project Owner — TradingAI_BTC`, sin nombre personal inventado) conserva exclusivamente la autoridad para aprobar diseños, especificaciones, planes, decisiones (`D1`–`D6`, `DEC-OWNER-AI-01`–`06`), otorgar autorización de materialización (G3), superar recomendaciones previas, aceptar resultados de auditoría (G6) y conceder autorización técnica de Fase C.
- Las aprobaciones existentes cubren **únicamente** su documento objeto (`R9`, `R2` de especificación, `R2` de plan, `R2` de decisiones `D1`–`D6`, autorización `R2` de materialización de ART-01…07, y registro `DEC-OWNER-AI-01`–`06` pendiente de las enmiendas versionadas).
- Ningún dictamen técnico (`ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, etc.), ninguna revisión (humana o IA) y ninguna auditoría independiente sustituyen la aceptación o autorización expresa del propietario.
- Ninguna aprobación de la excepción `INDEPENDENT_AI_REVIEW` autoriza Fase C, cambios en código de producción, schemas o dependencias, acceso/modificación de Parquet protegidos, ejecución automática de G5/G6, modificación de ART-01/02/03/05/06/07 ni commits/push.

---

## 10. Condiciones de cierre de `AUD_R8_02`

Según `S-01` §1, §5.8.5, §10.8, `S-04` §1, §9, `S-05` §8 (G6) y `S-06` §§3, 5:

- `AUD_R8_02` (originalmente `AUD-R7-03`) registra que los siete artefactos materiales del oracle no existen ni están verificados.
- Permanece **`OPEN`** hasta que concurran todas las condiciones de G6:
  1. Existencia material y verificación individual de los siete artefactos (`ORACLE-ART-01`…`07`, incluidas las 139 rutas, los 9 metadatos, `rule_id` separado, P1–P5, I1–I12 y la mutación aislada `external_run_only`).
  2. Informe de auditoría independiente favorable sobre dichos criterios.
  3. Cero hallazgos bloqueantes (`BLOCKER`/`HIGH` o equivalentes bloqueantes) sin resolver.
  4. Aceptación expresa del propietario del resultado de la auditoría.
  5. Evidencia documental trazable de los cuatro puntos anteriores.
- Mientras `AUD_R8_02` esté `OPEN`, `PHASE_C_IMPLEMENTATION_AUTHORIZATION` permanece `NOT_GRANTED`.

---

## 11. Reconstrucción de referencia de 139 rutas y 9 metadatos (S-01 §5.4 + S-02 §9.2 + S-10)

Derivación independiente previa a la lectura de `C-01`…`C-05`:

- **Conteo verificado en `S-01` §5.4 + `S-10`:** 87 rutas raíz/no-partición previas + 10 plantillas `{partition}` × 4 (`train`, `validation`, `calibration`, `test`) = 40 rutas de partición + 12 rutas posteriores (`validation.purge.*` [3], `calibration.*` [9]) = **139 rutas expandidas**.
- **Los 9 metadatos exactos (`S-01` §5.1, `S-04` §4.6):** `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`. (`rule_id` es el 10.º campo de trazabilidad en `ORACLE-ART-01`, no comparado en los 9).
- **Verificación estructural contra `S-10` (`manifest_v4.json`):**
  - `nullable=True` exactamente en las 7 rutas donde `S-10` declara `["<tipo>", "null"]` dentro de las 139 incluidas: `training.models.rf.params.max_depth`, `training.models.rf.params.class_weight`, `training.models.rf.params.random_state`, `training.environment.cuda_version`, `training.environment.cudnn_version`, `training.hardware.gpu_model`, `training.hardware.cuda_version` (las dos últimas con `MR=True, PO=False, N=True`; las cinco primeras con `MR=False, PO=True, N=True`).
  - `shared_with` en `validation.partitions.{partition}.shared_with`: requerido y `const: "validation"` únicamente en `$defs/calibration_partition`; ausente y prohibido (`additionalProperties: false`) en `$defs/partition` (`train`, `validation`, `test`) → patrón **P2** (`MR=False`, `MRW=partition == 'calibration'`, `MAW=partition == 'calibration'`, `PIW=always`, `PO=True`, `N=False`, `Norm=none`).
  - `calibration.base_model_id`, `calibration.base_artifact_sha256.rf`, `calibration.base_artifact_sha256.xgb`: requeridos por `S-10` (`calibration.required` y `base_artifact_sha256.required`) → `MR=True`, `MRW=None`, `MAW=None`, `PIW=external_run_only` (normativo de `S-02` §9.2, ausente del schema), `PO=True` (exigido por I6(b)), `N=False`, `Norm=none`.
  - Timestamps (`normalization=timestamp_utc_9`, `type=timestamp`): 10 rutas expandidas (`data.time_range.start`, `data.time_range.end`, y `validation.partitions.{train,validation,calibration,test}.{time_start,time_end}`), todas con `format: date-time` y `MR=True, PO=False, N=False` en `S-10`.
  - `string_decimal`: 3 rutas (`target.vol_mult` [`MR=True, PO=False`], `training.ensemble.weights.rf` [`MR=False, PO=True`], `training.ensemble.weights.xgb` [`MR=False, PO=True`]), todas `"type": "string"` en `S-10` y `Norm=none`.
  - Exclusiones normativas (§9.2 / §5.5): `model_id`, `created_at`, `sealed_at`, `status_at_seal`, `run_fingerprint`, `git.commit`, `git.dirty`, `git.branch`, `git.tag`, `producer.command`, `data.snapshot_uri`, `validation.purge.label_purge_satisfied`, `validation.leakage_checks.*`, `validation.partition_manifest_sha256`, `validation.evaluation.*`, `calibration.calibration_input_sha256`, `calibration.artifact_sha256`, `artifacts[]`, `metrics.*`, `extensions`.
