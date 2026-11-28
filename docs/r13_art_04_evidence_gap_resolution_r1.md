# R13 — ART-04 EVIDENCE GAP RESOLUTION R1

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Alcance:** investigación de las cinco brechas registradas en `docs/r13_oracle_art_04_technical_review_draft_r1.md`. **No** modifica artefactos, normativas, producción, tests, schemas ni dependencias.

**Clasificación de evidencia usada en este documento:**
- **Evidencia reproducida:** ejecutada en esta tarea con script temporal de solo lectura en `%TEMP%`.
- **Evidencia heredada:** afirmación documentada en artefactos, registros o informes previos.
- **Inferencia:** deducción no respaldada por evidencia primaria; no se usa como prueba.
- **Pendiente:** sin evidencia suficiente; se marca `NOT_VERIFIED`.

---

## 1. Fuentes consultadas y hashes verificados

| Fuente | SHA-256 | Uso |
|---|---|---|
| `docs/r13_oracle_art_04_technical_review_draft_r1.md` | `82c7d9d600ed306de0bfdfda4e4aecb53097b94623126cac2b8015a0bdb90aae` | Origen de las brechas |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | Preimagen JCS |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | Archivo que contiene el checksum |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | Estado interno |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | Estado interno |
| `tests/oracle_normative_v4_r5_verifier.py` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` | ORACLE-ART-02, ejecución aislada |
| `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` | Representación independiente |
| `docs/r13_oracle_art_06_07_verification_status_registration_r1.md` | `1be1c153ae880a0f52d05b2c233e599aad10db1a599cccd4a46e911fc8c756dd` | Registro de estados |
| `docs/r13_oracle_art_05_verification_status_registration_r1.md` | `fd140513aa380c2b46633e35645f38e03cbfb5687a3210ddc9c787b281ca4806` | Registro de estados |
| `docs/r13_oracle_artifacts_specification_r5.md` | `c124cd74045ed7721bff5f0a91cd1ec379ca0aac683e729fd1bf785801dde409` | Requisitos ART-04 |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r4.md` | `09145c2f36daf688b43ee796ba4e32bb65914fe3294857a60c3431483e7b7d4b` | 24 `rule_id`, 15 campos |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | Autoridad normativa |
| `docs/aud04b_model_provenance_v4_design.md` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | §9.2, 24 filas |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | Contrato estructural |

Todos los hashes se recalcularon y coinciden.

---

## 2. Brecha 1 — Estados internos de ART-06/07 frente a registros

**Evidencia reproducida:** los JSON de ART-06 y ART-07 contienen `status: CREATED_UNVERIFIED`; el registro `r13_oracle_art_06_07_verification_status_registration_r1.md` §5 declara `VERIFIED` para ambos.

**Evidencia heredada:** el propio registro §2 explica: *«Los JSON de ORACLE-ART-06 y ORACLE-ART-07 no se modifican… los campos `status` internos de los JSON permanecen intactos como contenido original de los artefactos; el estado corriente es el registrado aquí»* (§3). La transición se apoya en la auditoría `R13-AUDIT-ORACLE-ART-06-07-R1 — ACCEPTED`.

**Conclusión:** la discrepancia está **documentada y explicada**; no es una contradicción normativa abierta. Representa dos capas: contenido inmutable del artefacto vs. estado corriente en registro externo. Impacto residual: un consumidor que lea solo el campo `status` del JSON obtendrá el valor histórico. No se modifica ningún artefacto.

**Estado:** `VERIFIED` como discrepancia documentada; `NOT_VERIFIED` para cualquier afirmación de que los campos internos fueron actualizados (no lo fueron).

**Condición para resolver el impacto:** que los consumidores y ART-04 tomen el estado corriente del registro de verificación, no del campo interno. Registrar esa preferencia en el futuro ART-04 cuando se materialice.

---

## 3. Brecha 2 — Recálculo independiente del hash de ART-03

**Procedimiento reproducido (script temporal en `%TEMP%`, solo lectura):**

1. Leer bytes de `ORACLE-ART-01.json`, calcular `SHA-256` → `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b`.
2. Parsear el objeto y aplicar `rfc8785.dumps` (JCS) → **37678 bytes**, igual longitud que el archivo.
3. Calcular `SHA-256` de los bytes canónicos → `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b`.
4. Leer contenido de `ORACLE-ART-03.txt` → `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b`.
5. Versión de `rfc8785`: `0.1.4` (conforme a la decisión de diseño Q-05).

**Resultado:** coincidencia exacta. El hash de ART-03 **puede recalcularse de forma independiente** usando exclusivamente la preimagen y la canonicalización normativa. El checksum **dentro** de ART-03 es `7c9c49a5…`; el SHA-256 del **archivo** ART-03.txt es `23306196…`; son magnitudes distintas y no debe confundirse.

**Estado:** `VERIFIED` (reproducido). Sin modificación de artefactos.

---

## 4. Brecha 3 — Ejecución aislada de ART-02

**Procedimiento reproducido:** se copiaron `ORACLE-ART-01.json` y `oracle_normative_v4_r5_verifier.py` a un directorio aislado bajo `%TEMP%`, preservando la estructura relativa que el verificador espera (`tests/` y `docs/oracle_artifacts/v4/r5/`). Se importó el verificador desde esa copia y se ejecutó `verify()`. El repositorio no fue modificado.

| Salida | Valor |
|---|---|
| `load_transcription()['version']` | `ORACLE_NORMATIVE_V4_R5` |
| `expected_checksum()` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` |
| `EXPECTED_CHECKSUM` interno | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` |
| `verify()` | `[]` (sin errores) |

**Resultado:** ART-02 **puede ejecutarse** en entorno de verificación aislado, sin modificar fuentes ni artefactos, con resultado determinista y sin fallback.

**Estado:** `VERIFIED` (reproducido en esta tarea). Los resultados previos de auditoría sobre ART-02 pasan a ser evidencia heredada concordante, no necesaria para esta conclusión.

---

## 5. Brecha 4 — Las 11 reglas `CORROBORATED`

Contraste directo con §9.2 de `aud04b_model_provenance_v4_design.md` (24 filas, líneas 345–368) y con el convenio D1 de `R9-9.2-NN` secuencial por fila.

| `rule_id` | Fila §9.2 (contenido abreviado) | Clasificación |
|---|---|---|
| `R9-9.2-02` | `model_id, created_at, sealed_at, status_at_seal, run_fingerprint` — excluir identidad/timestamps/resultado | `VERIFIED` (fila), `CORROBORATED` (etiqueta) |
| `R9-9.2-04` | `git.commit, git.dirty, git.branch, git.tag` — excluir meta/localizador | ídem |
| `R9-9.2-06` | `producer.command` — excluir texto de invocación | ídem |
| `R9-9.2-08` | `data.snapshot_uri` — excluir ubicación | ídem |
| `R9-9.2-16` | `validation.purge.label_purge_satisfied`, `validation.leakage_checks.*` — excluir resultados derivados | ídem |
| `R9-9.2-17` | `validation.partition_manifest_sha256` — excluir digest derivado | ídem |
| `R9-9.2-18` | `validation.evaluation.*` — excluir protocolo/resultado de evaluación | ídem |
| `R9-9.2-21` | `calibration.calibration_input_sha256`, `calibration.artifact_sha256` — excluir digests/salida | ídem |
| `R9-9.2-22` | `artifacts[]` y propiedades — excluir outputs | ídem |
| `R9-9.2-23` | `metrics.path`, `metrics.sha256`, `metrics.schema_version` — excluir resultados | ídem |
| `R9-9.2-24` | `extensions` — excluir del fingerprint | ídem |

**Hecho verificado:** las 11 filas existen y su contenido de exclusión coincide con las reglas descritas en Protocolo R4 §9.6. El total es 24 filas; 13 incluidas y 11 excluidas, coincidiendo con los `rule_id` usados en ART-01.

**Evidencia que falta para pasar de `CORROBORATED` a `VERIFIED`:** una tabla de correspondencia explícita `fila §9.2 → rule_id → ruta expandida/aplicabilidad`, aprobada bajo D1; casos negativos que demuestren que esas 11 reglas **excluyen** rutas y que cualquier inclusión indebida se detecta; y reconstrucción por un agente distinto del generador. El borrador no ha ejecutado esos casos: se mantienen como `CORROBORATED`, no cerrados.

---

## 6. Matriz actualizada de brechas

| ID | Brecha | Evidencia | Impacto | Estado | Condición necesaria |
|---|---|---|---|---|---|
| G-01 | `status` interno ART-06/07 vs. registro | Reproducida + heredada | Consumidores que lean solo JSON ven valor histórico | `VERIFIED` (discrepancia documentada) | ART-04 debe tomar estado del registro externo |
| G-02 | Recálculo JCS de ART-03 | **Reproducida**: `rfc8785.dumps` → `7c9c49a5…` = contenido ART-03 | Ninguno; confirma integridad | `VERIFIED` | Ninguna adicional |
| G-03 | Ejecución aislada de ART-02 | **Reproducida**: `verify() == []` en `%TEMP%` | Ninguno; confirma verificador | `VERIFIED` | Ninguna adicional |
| G-04 | 11 reglas de exclusión | Heredada + contraste directo de 24 filas | Cobertura de exclusiones no ejecutada | `CORROBORATED` | Tabla D1 explícita y casos negativos de exclusión |
| G-05 | Independencia / procedencia del generador | Informes previos | Impide dictamen de ART-04 | `NOT_VERIFIED` / `BLOCKED` | Proveedor real acreditado del generador y del auditor |
| G-06 | Dictamen y materialización de ART-04 | ART-04 no existe | G5 permanece bloqueada | `BLOCKED` | Revisión independiente y aceptación expresa |

---

## 7. Pruebas realizadas y control de no modificación

| Prueba | Resultado |
|---|---|
| SHA-256 de 14 fuentes | Todos coincidentes |
| `rfc8785.dumps` sobre ART-01 | 37678 bytes; SHA `7c9c49a5…` |
| Comparación con contenido de ART-03 | Igualdad exacta |
| Ejecución de `verify()` en copia aislada | `[]` |
| Verificación de que el repositorio no cambió | `git diff --check` exit 0; sin staged; hashes de artefactos intactos |

No se ejecutaron G5/G6, pytest ni revisión IA; no se creó ART-04; no se tocaron Parquet.

---

## 8. Limitaciones

- G-04 permanece `CORROBORATED`: la numeración de `rule_id` proviene del convenio D1 y del contraste de filas, no de una tabla aprobada explícita ni de casos negativos ejecutados.
- G-05 permanece `NOT_VERIFIED`: la investigación de procedencia concluyó `PROVENANCE_UNVERIFIABLE`.
- G-01 solo se resuelve en su dimensión documental; el impacto en consumidores automáticos sigue requiriendo una convención de estado corriente.
- ART-04 no ha sido dictaminado; este documento no lo acepta ni desbloquea etapas.

---

## 9. Estados de gobernanza

```text
ORACLE-ART-04: NOT_CREATED
ART04_DRAFT: TECHNICAL_DRAFT_NON_INDEPENDIENTE
DEC_OWNER_AI_04_STATUS: NOT_SATISFIED
EXT_01: NOT_CLOSED
EXT_02: NOT_CLOSED
R5: NOT_APPROVED / NOT_AUDITED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin commits ni push. Único archivo creado: este informe.

**Fin de R13-ART-04-EVIDENCE-GAP-RESOLUTION-R1.**
