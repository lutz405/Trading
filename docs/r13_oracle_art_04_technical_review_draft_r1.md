# R13 — ORACLE-ART-04 TECHNICAL REVIEW DRAFT R1

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto:** borrador de revisión técnica trazable de ORACLE-ART-04.

> **BORRADOR TÉCNICO NO INDEPENDIENTE.** Ha sido preparado por el asistente técnico que participó en la generación de la documentación normativa. **No** es auditoría, **no** acredita independencia externa, **no** certifica ART-04, **no** declara satisfecho `DEC-OWNER-AI-04`, **no** cierra EXT-01 ni EXT-02 y **no** habilita etapa posterior alguna.

---

## 1. Identificación, propósito y alcance

| Campo | Valor |
|---|---|
| Identificador del registro proyectado | `ORACLE-ART-04` |
| Estado material | **`NOT_CREATED`** — no existe `docs/oracle_artifacts/v4/r5/ORACLE-ART-04.json` |
| Propósito normativo | Evidenciar que la transcripción normativa fue revisada independientemente contra §9.2 por un agente distinto del generador |
| Modalidades previstas | `HUMAN_INDEPENDENT_REVIEW` (preferente) e `INDEPENDENT_AI_REVIEW` (excepcional, solo ART-04), según D3-R5 y Especificación R5 §3.1–§3.2 |
| Dependencias declaradas | **`ORACLE-ART-01`, `ORACLE-ART-03`** (R2 §4.4; Especificación R5 §3.6; Plan R5 §2) |
| Alcance de este borrador | Reconstrucción técnica y comprobación de evidencia disponible; **sin** emisión de dictamen, firma, fecha de revisión independiente ni aceptación |

---

## 2. Fuentes normativas y de evidencia utilizadas

| Fuente | SHA-256 |
|---|---|
| `docs/r13_oracle_art_04_ai_review_owner_decision_package_r1.md` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` |
| `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` |
| `tests/oracle_normative_v4_r5_verifier.py` (ORACLE-ART-02) | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` |
| `docs/r13_oracle_art_05_verification_status_registration_r1.md` | `fd140513aa380c2b46633e35645f38e03cbfb5687a3210ddc9c787b281ca4806` |
| `docs/r13_oracle_art_06_07_verification_status_registration_r1.md` | `1be1c153ae880a0f52d05b2c233e599aad10db1a599cccd4a46e911fc8c756dd` |
| `docs/r13_oracle_artifacts_decision_resolution_r5.md` | `551037ef24714fcdcb56f2eda0e5f499307647e64f6b00b1786c741b2e4dbac9` |
| `docs/r13_oracle_artifacts_specification_r5.md` | `c124cd74045ed7721bff5f0a91cd1ec379ca0aac683e729fd1bf785801dde409` |
| `docs/r13_oracle_artifacts_materialization_plan_r5.md` | `2a79269bbc3add9be5cdabd26c6e26976450aaea1f54cced5f9327ea229ff80e` |
| `docs/r13_oracle_artifacts_materialization_authorization_r5.md` | `bdde15664efa39811f783106f1c031d0e134cd2ec29530467bcf4ae12db9c3fb` |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r4.md` | `09145c2f36daf688b43ee796ba4e32bb65914fe3294857a60c3431483e7b7d4b` |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| `docs/aud04b_model_provenance_v4_design.md` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` |
| `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `132bad37b05960e828e8271b7b3cfeaebe220df7506d0af8a1fa0d9367649058` |
| `docs/r13_oracle_artifacts_r5_external_audit_handoff_r1.md` | `8af6fbddb39bbfdee81e1d70c3f042beab14dcfc894cee9356f7e69b035105df` |
| `docs/r13_oracle_artifacts_r5_external_independent_audit_r1.md` | `771011ea61d7c01f9e2cd0783e5cb39fd183bf6a90c0c43c5dece85e7cf8ad86` |
| `docs/r13_original_generator_provenance_investigation_r1.md` | `85222386b9b28138439a34553247bdc6ae2f45e40db0880ed1f43ce1e9b75551` |
| `docs/r13_oracle_artifacts_r4_independent_audit_r1.md` | `94152ea9b8a53a5f66f6f051983fbad048e57210b7c218a4a5dc32744c51308a` |
| `docs/audit_report_r13_oracle_art_04_antigravity_external.md` | `65218a58167708ed8b959bac89337f1c070bf0a556759bd6ceb6d66e64aa866f` |

Los hashes se recalcularon directamente y coinciden. Los informes de auditoría se usan como **evidencia de lo que otros informes afirman**, no como autoridad normativa.

---

## 3. Reconstrucción técnica de requisitos aplicables

1. **Jerarquía:** DEC-06 y diseño v4 §9.2 definen qué rutas entran en `run_fingerprint`; `manifest_v4.json` define tipos, `required` y nulabilidad; la IA revisora no es fuente normativa (Especificación R5 §2; R9 §5.8).
2. **Artefactos:** siete Oracle; ART-04 depende de ART-01 y ART-03, sin dependencia formal sobre ART-02/05/06/07 (Especificación R5 §3.1 y §3.6).
3. **Cobertura:** 139 rutas expandidas; 9 metadatos; `rule_id` como décimo campo de trazabilidad.
4. **Reglas:** 24 `rule_id` normativos `R9-9.2-01…24`; 13 usados por la allowlist y 11 de exclusión (Protocolo R4 §9.6).
5. **Registro:** 15 campos mínimos de R1 §9, conservados en Protocolo R4 §9.6.
6. **Dictámenes:** `ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED`, `INCONCLUSIVE`; severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`; la IA propone, el auditor confirma y el propietario acepta (Protocolo R4 §8).
7. **Independencia:** nueve controles de `DEC-OWNER-AI-04`; proveedor real distinto acreditado; limitación no demostrable ⇒ `INCONCLUSIVE` (Protocolo R4 §6).
8. **Puertas:** G5 no se cierra automáticamente por dictamen IA; G6 conserva cinco condiciones (Plan R5 §4.1–§4.2).

---

## 4. Revisión de 139 paths y 24 `rule_id`

**Hechos verificados por recuento directo sobre los archivos existentes:**

| Comprobación | Resultado |
|---|---|
| Entradas de `ORACLE-ART-01.json` | **139** |
| Rutas únicas en ART-01 | **139** |
| Campos por entrada | 10 (9 metadatos + `rule_id`) |
| `rule_id` distintos en ART-01 | **13**: `01,03,05,07,09,10,11,12,13,14,15,19,20` (prefijo `R9-9.2-`) |
| Filas de ART-05 | 139, con 139 únicas |
| Casos en ART-05 | 139 positivos + 556 negativos |
| Filas de ART-06 | 139, con 139 rutas únicas |

**Afirmaciones de fuentes documentales:** el total normativo es 24 `rule_id`; los 11 restantes (`02,04,06,08,16,17,18,21,22,23,24`) son reglas de exclusión, según Protocolo R4 §9.6 y la reconstrucción independiente. **No se ha ejecutado en esta tarea una reconstrucción propia** de las 24 reglas desde §9.2, por lo que ese extremo se registra como `CORROBORATED` por documentos, no como verificación independiente del borrador.

**No se han detectado** rutas duplicadas u omitidas en los recuentos realizados sobre ART-01/05/06.

---

## 5. Revisión de los nueve campos de metadatos

ART-06 declara `metadata_fields` con los nueve nombres exactos: `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`. ART-01 contiene esos nueve campos más `rule_id`, separado. ART-06 registra `comparison_status: NO_DIVERGENCE` y `negative_probe_failures: []` para 139 rutas.

**Hecho verificado:** presencia y separación de los nueve metadatos en los artefactos. **Limitación:** la comparación campo por campo fue producida por el ejecutor de ART-06; este borrador no la ha reproducido con una representación propia.

---

## 6. Trazabilidad entre artefactos

| Artefacto | Hash verificado | Estado según registro | Función respecto de ART-04 |
|---|---|---|---|
| ART-01 | `7c9c49a5…` | `VERIFIED` | Objeto revisado; 139 rutas, diez campos |
| ART-02 | `a67bf35a…` | `VERIFIED` | Verificador; se inspecciona en el alcance (no dependencia formal) |
| ART-03 | `23306196…` | `VERIFIED` | Checksum JCS/SHA-256; dependencia formal de ART-04 |
| ART-05 | `35b705b9…` | `VERIFIED` | Cobertura de 139 rutas (alcance auxiliar) |
| ART-06 | `9c133937…` | `VERIFIED` | Comparación de nueve metadatos (alcance auxiliar) |
| ART-07 | `9a3d4674…` | `VERIFIED` | Mutación `external_run_only` (alcance auxiliar) |
| ART-04 | — | `NOT_CREATED` | Registro de revisión pendiente |

**Discrepancia observada:** los JSON de ART-06 y ART-07 conservan internamente `status: CREATED_UNVERIFIED`, mientras los registros de verificación documentan `VERIFIED`. El estado corriente declarado en los registros prevalece; los archivos no fueron modificados.

**No verificado en esta tarea:** recálculo JCS de ART-03 y ejecución de ART-02; se registran como `NOT_VERIFIED` en el borrador, sin contradecir los registros previos.

---

## 7. Evidencias de cobertura y resultados de pruebas

**Reproducido en esta tarea (lectura directa):**

- ART-01: 139 entradas / 139 rutas únicas / 13 `rule_id` usados.
- ART-05: 139 filas, 139 positivos, 556 negativos, `NO_DIVERGENCE`, 0 fallos.
- ART-06: 139 filas, 139 rutas únicas, 9 metadatos, `NO_DIVERGENCE`, 0 fallos.
- ART-07: control `NOT_DETECTED`, mutación `DETECTED`, restauración `True`, 0 errores posteriores, determinismo `True`.

**Afirmado por informes previos (no reejecutado aquí):** auditorías de ART-05, ART-06 y ART-07 con resultados favorables; 17 pruebas de representación, 66 de regresión v4 y 182 de suite provenance; auditoría externa R5 con resultado independiente `INCONCLUSIVE`. Se registran como `REPORTED`, no como ejecución propia.

**No ejecutado:** G5, G6, revisión IA, pytest, ni regeneración de artefactos.

---

## 8. Hallazgos técnicos, discrepancias y limitaciones

| ID | Naturaleza | Descripción |
|---|---|---|
| D-01 | Hecho verificado | ART-04 no existe; no hay revisión independiente registrada |
| D-02 | Hecho verificado | El borrador es producido por el generador; no acredita independencia |
| D-03 | Hecho verificado | Investigación de procedencia: `PROVENANCE_UNVERIFIABLE`; proveedor real del generador desconocido |
| D-04 | Afirmación de informes | Auditorías R4/R5 y externas: `INCONCLUSIVE`; `AUD-ANT-01` `HIGH` |
| D-05 | Hecho verificado | Estados internos `CREATED_UNVERIFIED` en ART-06/07 frente a registros `VERIFIED` |
| D-06 | Limitación | No se recalculó JCS de ART-03 ni se ejecutó ART-02 en esta tarea |
| D-07 | Limitación | No se realizó reconstrucción propia de las 24 reglas desde §9.2 |
| D-08 | Inferencia (rechazada como prueba) | Hipótesis `Hy4`/`Hydrogen 4` sobre proveedor compartido: sin evidencia |
| D-09 | Hecho verificado | No existen aprobación de R5 ni registro de aceptación de ART-04 |

---

## 9. Tabla de requisitos

| Requisito | Estado | Fuente / evidencia |
|---|---|---|
| 139 rutas en ART-01 | `VERIFIED` | Recuento directo |
| 13 `rule_id` usados en ART-01 | `VERIFIED` | Recuento directo |
| 24 `rule_id` normativos (13 + 11) | `VERIFIED` (13) / `CORROBORATED` (11) | Artefacto + Protocolo R4 §9.6 |
| Nueve metadatos separados de `rule_id` | `VERIFIED` | ART-01/ART-06 |
| ART-05 cobertura 139 × casos | `VERIFIED` | Recuento directo sobre ART-05 |
| ART-06 comparación sin divergencia | `VERIFIED` | Contenido de ART-06 |
| ART-07 mutación aislada | `VERIFIED` (evidencia declarada) | Contenido de ART-07 |
| ART-03 JCS/SHA-256 recalculado aquí | `NOT_VERIFIED` | No ejecutado |
| ART-02 ejecución aquí | `NOT_VERIFIED` | No ejecutado |
| Dependencias ART-04 = `01, 03` | `VERIFIED` | Especificación R5 / Plan R5 |
| 15 campos de R1 §9 | `VERIFIED` | Protocolo R4 §9.6 |
| Independencia `DEC-OWNER-AI-04` | `BLOCKED` | Procedencia no verificable; auditorías `INCONCLUSIVE` |
| Dictamen y auditoría de ART-04 | `BLOCKED` | ART-04 no creado |
| Aceptación del propietario de ART-04 | `BLOCKED` | No emitida |
| Aprobación de R5 | `BLOCKED` | `NOT_APPROVED / NOT_AUDITED` |
| G5 / G6 | `BLOCKED` / `NOT_STARTED` | Plan R5 §4 |
| Autorización de Fase C | `BLOCKED` | `NOT_GRANTED` |
| Criterio de revisión humana alternativa | `NOT_APPLICABLE` a este borrador | No se emite modalidad ni dictamen |

---

## 10. Conclusión técnica provisional

La evidencia existente permite afirmar, con base en recuentos directos, que los artefactos Oracle materializados conservan 139 rutas únicas, 13 `rule_id` usados, nueve metadatos separados de `rule_id`, cobertura positiva/negativa y evidencia de mutación, con hashes inalterados. Esa conclusión es **técnica y documental**, no una auditoría.

**No es posible emitir un dictamen para ORACLE-ART-04.** El registro no existe, no hay revisión independiente acreditada, la procedencia del generador original es `PROVENANCE_UNVERIFIABLE`, `DEC-OWNER-AI-04` no está satisfecho y las auditorías disponibles son `INCONCLUSIVE`. El borrador no declara `ACCEPTED` ni `ACCEPTED_WITH_FINDINGS`, no cierra EXT-01/EXT-02, no habilita G5/G6 ni Fase C y no sustituye la aprobación expresa del propietario.

---

## 11. Estado y cierre

```text
ORACLE-ART-04: NOT_CREATED
ART04_DRAFT: TECHNICAL_DRAFT_NON_INDEPENDENT
DEC_OWNER_AI_04_STATUS: NOT_SATISFIED
EXT_01: NOT_CLOSED
EXT_02: NOT_CLOSED
R5: NOT_APPROVED / NOT_AUDITED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff; `git diff --check` exit 0. Sin commits ni push. Único archivo creado: este borrador. No se modificaron normativas R2–R5, artefactos, producción, tests, schemas, dependencias ni Parquet.

**Fin de R13-ORACLE-ART-04-TECHNICAL-DRAFT-R1.**
