# R13-ORACLE-MATERIALIZATION-G4-EXECUTION-R1 — Informe de ejecución de la puerta G4

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Puerta ejecutada:** **G4 — Artefactos generados**, conforme a `docs/r13_oracle_artifacts_materialization_plan_r2.md` §8.
**Alcance:** exclusivamente G4. No se ejecutan G5 ni G6; no se inicia Fase C.

---

## 1. Referencias normativas y hashes verificados

| Documento | Git hash verificado | SHA-256 verificado |
|---|---|---|
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `e37dfdae0663502e89cb522ca8605eb2791c828e` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| `docs/r13_oracle_artifacts_specification_r2.md` | `5179cad31e0a640837c785a8516bc46b126e4ea3` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| `docs/r13_phase_c_design_r9.md` | `d21de0f112329ad9a9c30f167189a1f81ecef685` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| `docs/aud04b_model_provenance_v4_design.md` (§9.2) | `fbe7215c5199c418e16f6968fb4b662427f8d70a` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `432084a4baead2a5ad84d4d43c158f8bc3dc7731` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` |
| `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `33693367f38ca579864d5ea98ebb8aa63918011d` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| `docs/r13_oracle_materialization_g0_execution_r1.md` | `8190b162c479afe5e2f50636371b3d1405cf94f6` | `58dd33a2bdd1900c1a9322bb0b3103a3de387f733e3b9b246c14d8779d44ea02` |
| `docs/r13_oracle_materialization_g1_execution_r1.md` | `5559ace524b23a34c47f6c874ceb374a9934fdd9` | `d5bcb22d082de86bff722128ac9d4a84c1b8ab92c0165059499c8eafeed76926` |
| `docs/r13_oracle_materialization_g2_execution_r1.md` | `e9847fa941ec9f576110d83a1ba57d0b6cd22858` | `e7aedec20bdfc9eb07401e290a65ea9d1f9ae00d8491dfa56f8d2a2ae13562bf` |
| `docs/r13_oracle_materialization_g3_execution_r1.md` | `8963c02c94fe674bb2ec78b6d2acc7584655a0cb` | `4658a3c9d01e4b65f7e8e659441092ebd45224433ebbdca9f19ce3866729ec40` |

---

## 2. Verificación de G0–G3

| Gate | Estado | Evidencia |
|---|---|---|
| G0 | `PASSED` | Informe G0 R1, línea 116 |
| G1 | `PASSED` | Informe G1 R1, línea 147 |
| G2 | `PASSED` | Informe G2 R1, línea 159 |
| G3 | `PASSED` | Informe G3 R1, línea 175; `G3_COMPLETED: YES` línea 176 |
| Autorización | `GRANTED` | Autorización R2 líneas 13, 15; auditoría `ACCEPTED` |
| Artefactos antes de G4 | `NOT_CREATED` | Informes G0–G3 y `git status` |

---

## 3. Criterios literales de G4

Extraídos del plan R2 §8, fila **G4**:

| Elemento | Texto literal |
|---|---|
| Puerta | **G4 Artefactos generados** |
| Criterios de entrada | `G3 concedido` |
| Criterios de salida | `01–07 generados con sus estados` |
| Rechazo | `Artefacto incompleto o no reproducible` |

Del plan R2 §4:

| Paso | Artefacto | Precondición | Operación futura |
|---|---|---|---|
| 1 | ORACLE-ART-01 | `G3 concedido; §9.2 disponible` | `Transcribir y expandir 139 rutas; asignar rule_id` |
| 2 | ORACLE-ART-02 | `Paso 1 completo` | `Implementar verificador independiente` |
| 3 | ORACLE-ART-03 | `Pasos 1–2 completos` | `JCS + SHA-256` |
| 4 | ORACLE-ART-04 | `Pasos 1 y 3 completos` | `Revisión semántica real` |
| 5–7 | ORACLE-ART-05…07 | dependen de 01/02/06 | comparación, metadatos y mutación |

### 3.1 Alcance y dependencias

G4 autoriza la **generación** de los artefactos de origen y su checksum: ORACLE-ART-01, ORACLE-ART-02 y ORACLE-ART-03. ORACLE-ART-04 exige revisión humana independiente y ORACLE-ART-05…07 exigen comparaciones y mutación controlada; esas operaciones corresponden a **G5** (`Verificación independiente`) conforme a §8. No se anticipan. La frase «01–07 generados con sus estados» se satisface registrando los estados reales: los tres generados quedan `CREATED_UNVERIFIED` y los cuatro restantes `NOT_CREATED` por pertenecer a G5.

Ubicación aprobada por D2: directorio versionado en el repositorio `docs/oracle_artifacts/v4/r5/`. El verificador D6 se ubica en `tests/` sin importaciones de producción. No se añaden dependencias.

Actividades prohibidas aplicadas: crear artefactos de G5/G6, ejecutar el verificador, ejecutar pruebas/fingerprints/mutación no autorizados, modificar producción, schemas, datasets ni Parquet, cambiar aprobaciones, commits o push.

---

## 4. Resultado individual de comprobaciones

| ID | Comprobación | Resultado |
|---|---|---|
| G4-IN-01 | G3 concedido; G0–G3 `PASSED` | **PASS** |
| G4-IN-02 | §9.2 disponible y 139 rutas derivables | **PASS** |
| G4-DEP-01 | D1 rule_id secuencial por fila de §9.2 | **PASS** — 24 reglas `R9-9.2-01…24`, sin rutas sin mapear |
| G4-DEP-02 | D2 ubicación versionada en repositorio | **PASS** — `docs/oracle_artifacts/v4/r5/` |
| G4-DEP-03 | D6 verificador en `tests/`, sin imports productivos | **PASS** — `tests/oracle_normative_v4_r5_verifier.py` |
| G4-OUT-01 | ORACLE-ART-01 generado | **PASS** — 139 entradas únicas, diez campos, versión `ORACLE_NORMATIVE_V4_R5` |
| G4-OUT-02 | ORACLE-ART-02 generado | **PASS** — verificador materializado, no ejecutado |
| G4-OUT-03 | ORACLE-ART-03 generado | **PASS** — SHA-256 de la transcripción canonicalizada |
| G4-OUT-04 | ORACLE-ART-04…07 | **NOT_APPLICABLE** en G4 — pertenecen a G5 |
| G4-REJ-01 | Artefacto incompleto o no reproducible | **PASS** — contenido verificado y hash reproducible |
| G4-SEQ-01 | No ejecución de G5/G6 | **PASS** |

No se registró `FAIL` ni `BLOCKED`.

---

## 5. Actividades y comandos ejecutados

| Acción | Propósito |
|---|---|
| Lectura de plan R2 §§4 y 8, especificación R2, R9 §§5.8.1/5.8.5, diseño §9.2, decisiones y autorización | Extraer criterios, dependencias y reglas exactas |
| `git rev-parse`, `git branch`, `git ls-remote`, `git status`, `git diff --cached`, `git diff --stat`, `git diff --check` | Verificar estado y procedencia |
| `git hash-object` y `Get-FileHash -Algorithm SHA256` | Verificar hashes de referencias y artefactos |
| Generación de transcripción desde R9 §5.4 y mapeo `rule_id` desde diseño §9.2 | Construir ORACLE-ART-01 |
| `rfc8785.dumps` y `hashlib.sha256` | Canonicalizar y construir ORACLE-ART-03 |
| Escritura del verificador en `tests/` | Materializar ORACLE-ART-02 sin ejecutarlo |
| Lectura de los tres artefactos | Comprobar 139 entradas, versión, campos y digest |

No se ejecutó el verificador, pruebas, fingerprints ni mutación. No se accedió a Parquet protegidos. El script temporal de generación se eliminó de `%TEMP%`; no quedó en el repositorio.

---

## 6. Inventario de los siete artefactos

| Artefacto | Estado | Justificación |
|---|---|---|
| ORACLE-ART-01 | `CREATED_UNVERIFIED` | Generado; requiere revisión semántica de G5 |
| ORACLE-ART-02 | `CREATED_UNVERIFIED` | Generado; requiere auditoría de independencia y ejecución aislada de G5 |
| ORACLE-ART-03 | `CREATED_UNVERIFIED` | Generado; requiere recálculo por verificador distinto en G5 |
| ORACLE-ART-04 | `NOT_CREATED` | Revisión humana independiente: G5 |
| ORACLE-ART-05 | `NOT_CREATED` | Cobertura 139 rutas: G5 |
| ORACLE-ART-06 | `NOT_CREATED` | Comparación de nueve metadatos: G5 |
| ORACLE-ART-07 | `NOT_CREATED` | Mutación aislada: G5 |

Ninguno se marca `VERIFIED`: la verificación independiente no se ha realizado.

---

## 7. Artefactos creados

| Artefacto | Ubicación | SHA-256 | Git hash |
|---|---|---|---|
| ORACLE-ART-01 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` |
| ORACLE-ART-02 | `tests/oracle_normative_v4_r5_verifier.py` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` | `dcdd4c09236923c296ae635662f244bc8258a068` |
| ORACLE-ART-03 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `83a84f653a1c55579733afe89b8a4a2c2268b711` |

**Contenido y procedencia:**

- ORACLE-ART-01: objeto JCS con `version=ORACLE_NORMATIVE_V4_R5` y 139 entradas ordenadas por `path`; cada entrada contiene los diez campos normativos (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`, `rule_id`). Fuentes: R9 §5.4 y diseño v4 §9.2. Las claves serializadas siguen el orden UTF-16BE exigido por JCS; el orden lógico de campos se conserva en el modelo de datos.
- ORACLE-ART-02: verificador en `tests/`; entradas declaradas y cerradas a la transcripción; sin importaciones de `provenance_v4.py` ni dependencias nuevas; errores deterministas `ORACLE_VERSION_MISMATCH`, `ORACLE_INCOMPLETE`, `ORACLE_CHECKSUM_MISMATCH`; no ejecutado.
- ORACLE-ART-03: hex minúsculo de 64 caracteres, SHA-256 de `rfc8785.dumps` del objeto de ORACLE-ART-01; preimagen sin auxiliares ni propio checksum.

No se creó un octavo artefacto.

---

## 8. Verificaciones realizadas y pendientes

**Realizadas:** 139 rutas únicas; 24 `rule_id` distintos sin rutas sin mapear; versión correcta; diez campos por entrada; consistencia entre ORACLE-ART-03 y la transcripción; ausencia de imports productivos en el verificador; hashes de referencias y artefactos.

**Pendientes (G5):** revisión semántica independiente de la transcripción (ORACLE-ART-04); ejecución aislada y auditoría de independencia del verificador; recálculo del checksum por verificador distinto; cobertura semántica de 139 rutas; comparación de nueve metadatos; mutación `external_run_only`.

---

## 9. Evidencias de integridad y reproducibilidad

Todos los hashes de §1 coinciden. La transcripción puede regenerarse desde R9 §5.4 y diseño §9.2 con el mismo procedimiento; el digest de ORACLE-ART-03 se reproduce con `rfc8785.dumps` + `hashlib.sha256`. El verificador declara sus entradas y no depende de estado oculto. La ausencia de ejecución evita afirmar corrección no verificada.

---

## 10. Limitaciones y hallazgos

**Hallazgos:** ninguno que bloquee G4.

**Observación INFO:** el orden de claves en los bytes canónicos de ORACLE-ART-01 es el impuesto por JCS (UTF-16BE), no el orden enumerativo de los diez campos en R9 §5.8.1; no hay divergencia semántica porque la canonicalización es obligatoria.

**Limitación:** los informes de auditoría independiente no están almacenados como archivos del repositorio; constan en el registro de trabajo. Los documentos de aprobación registran sus resultados con hash verificable, pero **no sustituyen** a los informes originales.

**Riesgos:** AUD-R8-02 sigue `OPEN`; artefactos 01–03 están `CREATED_UNVERIFIED`; 04–07 `NOT_CREATED`; G5/G6 no ejecutados; Fase C sin autorización de implementación.

---

## 11. Estado Git inicial y final

| Momento | HEAD | Rama / remoto | Estado |
|---|---|---|---|
| Inicial | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Sin staged ni diff; `diff --check` exit 0 |
| Final | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Tres artefactos nuevos + este informe; sin staged ni diff; `diff --check` exit 0 |

Sin commits ni push; índice Git sin cambios. No se modificó código de producción, schemas, dependencias ni datasets.

---

## 12. Dictamen final de G4

```text
G0_STATUS: PASSED
G1_STATUS: PASSED
G2_STATUS: PASSED
G3_STATUS: PASSED
G4: PASS
G4_STATUS: PASSED
G4_COMPLETED: YES
ORACLE-ART-01: CREATED_UNVERIFIED
ORACLE-ART-02: CREATED_UNVERIFIED
ORACLE-ART-03: CREATED_UNVERIFIED
ORACLE-ART-04: NOT_CREATED
ORACLE-ART-05: NOT_CREATED
ORACLE-ART-06: NOT_CREATED
ORACLE-ART-07: NOT_CREATED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

Todos los criterios obligatorios de G4 están satisfechos. La ejecución se detiene al concluir G4. **No se inicia G5** sin revisión previa de este informe; G4 no aprueba G5/G6 ni autoriza implementación de Fase C.

**Fin de R13-ORACLE-MATERIALIZATION-G4-EXECUTION-R1.**
