# AUDITORIA EXTERNA INDEPENDIENTE — R13 ORACLE-ART-04 — ENMIENDAS NORMATIVAS

**Informe:** `audit_report_r13_oracle_art_04_kilo_external.md`
**Proyecto:** `TradingAI_BTC`.
**Objeto:** auditoría documental independiente de las cinco propuestas normativas que incorporan `INDEPENDENT_AI_REVIEW` exclusivamente para `ORACLE-ART-04`.
**Naturaleza:** solo auditoría documental. No se implementan cambios, no se modifican archivos, no se ejecutan materializaciones, no se ejecutan G5 ni G6, no se crea ORACLE-ART-04, no se aprueba en nombre del propietario.

---

## 1. Identidad del auditor

| Campo | Valor |
|---|---|
| Auditor | Kilo (agente de auditoría normativa externa, entorno Kilo Code) |
| Rol | Auditor normativo independiente, externo al proceso de generación de las propuestas |
| Fecha y hora de ejecución | 2026-11-27T22:58:28Z |
| Entorno de ejecución | Kilo Code |

---

## 2. Proveedor, modelo y versión

| Campo | Valor |
|---|---|
| Proveedor de IA | kilo (Kilo Code) |
| Nombre exacto del modelo | kilo-auto/free |
| Versión del modelo | variante `free` del modelo `kilo-auto/free`; la plataforma no expone un número de versión de modelo adicional, por lo que se registra como `kilo-auto/free` (sin inventar versión numérica) |
| Identificador de sesión | no disponible como token de plataforma (sesión de auditoría externa independiente, sin historial compartido con el generador) |
| Parámetros de generación disponibles | temperatura, `seed`, `top_p`, límites y herramientas no expuestos por la plataforma; se registran como `no disponible` |
| Herramientas y permisos utilizados | lectura de archivos, cálculo de SHA-256, escritura de archivos de evidencia e informe de auditoría; sin ejecución de materialización, sin commits, sin push |

---

## 3. Declaración de independencia

Declaro que:

1. No participé en la generación de las cinco propuestas candidatas (C-01 a C-05).
2. No recibí informes ni conclusiones de auditorías anteriores.
3. No consulté conversaciones anteriores ni resúmenes elaborados por el generador.
4. No utilicé el dictamen previo de Nemotron 3.5 Lightning Free ni el informe `audit_report_r13_oracle_art_04.md`.
5. No utilicé las conclusiones de ChatGPT ni de OpenCode como contexto.
6. Reconstruí los requisitos exclusivamente desde las fuentes originales S-01..S-10 y A-01..A-04 del manifiesto de transferencia.
7. Si se encontraran informes de auditoría anteriores en el repositorio, no los abrí ni los utilicé como evidencia para construir mis conclusiones.

---

## 4. Evidencia de proveedor distinto del generador

El generador original utilizó **OpenCode con el modelo Hy4 Flash Free** (conforme al contexto de la tarea).

Esta auditoría se ejecutó con **Kilo Code, modelo kilo-auto/free (proveedor kilo)**.

`kilo` (Kilo Code) ≠ `OpenCode / Hy4` (proveedor del generador). Se trata de proveedores de modelo distintos, no solo de un cambio de nombre de modelo, interfaz, agente o entorno de ejecución. Por tanto, la condición de independencia de proveedor está demostrada y la auditoría se presenta como independiente.

No se inventaron datos de proveedor, versión, linaje o sesión.

---

## 5. Manifiesto de las 19 entradas y verificación de integridad

Todos los 19 archivos del manifiesto de transferencia `docs/r13_oracle_art_04_external_review_handoff_r1.md` fueron recalculados individualmente con SHA-256 y coinciden con el valor esperado. Resultado global: **19/19 COINCIDEN**. Ningún archivo fue modificado. Acceso de solo lectura.

### 5.1 Documentos candidatos (CANDIDATE) — 5 archivos

| ID | Ruta | SHA-256 esperado | SHA-256 calculado | Resultado |
|---|---|---|---|---|
| C-01 | `docs/r13_oracle_artifacts_decision_resolution_r3.md` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | COINCIDE |
| C-02 | `docs/r13_oracle_artifacts_specification_r3.md` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | COINCIDE |
| C-03 | `docs/r13_oracle_artifacts_materialization_plan_r3.md` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | COINCIDE |
| C-04 | `docs/r13_oracle_artifacts_materialization_authorization_r3.md` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | COINCIDE |
| C-05 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | COINCIDE |

### 5.2 Fuentes normativas originales (PRIMARY_ORIGINAL) — 10 archivos

| ID | Ruta | SHA-256 esperado | SHA-256 calculado | Resultado |
|---|---|---|---|---|
| S-01 | `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | COINCIDE |
| S-02 | `docs/aud04b_model_provenance_v4_design.md` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | COINCIDE |
| S-03 | `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | COINCIDE |
| S-04 | `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | COINCIDE |
| S-05 | `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | COINCIDE |
| S-06 | `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | COINCIDE |
| S-07 | `docs/r13_oracle_art_04_ai_review_owner_decision_package_r1.md` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` | COINCIDE |
| S-08 | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` | COINCIDE |
| S-09 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | COINCIDE |
| S-10 | `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | COINCIDE |

### 5.3 Registros de aprobación del propietario (OWNER_APPROVAL) — 4 archivos

| ID | Ruta | SHA-256 esperado | SHA-256 calculado | Resultado |
|---|---|---|---|---|
| A-01 | `docs/r13_owner_design_approval_r1.md` | `16cfd579db05289cca9a9140988128175136dffa1cba814b0a28f19c7b403b60` | `16cfd579db05289cca9a9140988128175136dffa1cba814b0a28f19c7b403b60` | COINCIDE |
| A-02 | `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | COINCIDE |
| A-03 | `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | COINCIDE |
| A-04 | `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | COINCIDE |

**Nota de alcance de la verificación de hashes:** el documento de aprobación de las decisiones normativas DEC-01..DEC-09 (`docs/aud04b_model_provenance_v4_approval_r1.md`), citado como autoridad para DEC-06 en S-01 §2 y S-03 §2, no forma parte de los 19 archivos del manifiesto de transferencia. Se leyó únicamente para extraer el texto de DEC-06 requerido en la reconstrucción del §8.3. Es un documento de aprobación normativa, no un informe de auditoría. Su hash no se verificó contra el manifiesto porque no está listado en él.

---

## 6. Metodología

La auditoría se ejecutó en las siguientes fases, sin utilizar las propuestas para reconstruir sus propios requisitos:

1. **Identidad e independencia (registrado en §1-§4):** proveedor, modelo, versión, entorno, fecha, sesión, parámetros, herramientas, declaración de independencia y evidencia de proveedor distinto del generador.
2. **Inventario y verificación de integridad (§5):** recálculo individual de los 19 hashes SHA-256 contra el manifiesto de transferencia. 19/19 coinciden.
3. **Reconstrucción normativa independiente (§8):** generación de un artefacto hashable (`docs/r13_reconstruccion_normativa_independiente_kilo.md`, SHA-256 `50f93e8bdaaad976373aa771fc1ba02189c578ef2113aa5682ac0da9345247b7`, creado 2026-11-27T22:58:28z) ANTES de abrir cualquiera de las cinco propuestas. Se reconstruyeron D1-D6, ORACLE-ART-01 a ORACLE-ART-07, jerarquía DEC-06 / §9.2 / `manifest_v4.json`, G0-G6, las ocho condiciones de G5, las cinco condiciones de G6, requisitos de revisión humana de ORACLE-ART-04, condiciones de independencia/trazabilidad/reproducibilidad, límites de autorización del propietario, y estado/condiciones de cierre de AUD_R8_02.
4. **Auditoría de las cinco propuestas (C-01 a C-05):** inspección documental individual y cruzada contra la reconstrucción del §8, usando los criterios del dictamen (§7) y las comprobaciones obligatorias A-G.
5. **Comprobaciones de consistencia cruzada (§11):** comparación entre las cinco propuestas y frente a las fuentes originales.
6. **Hallazgos y severidades (§12):** clasificación en BLOCKER/HIGH/MEDIUM/LOW/INFO.
7. **Dictamen final (§13):** uno de ACCEPTED / ACCEPTED_WITH_FINDINGS / REJECTED / INCONCLUSIVE.

**Clasificación de la naturaleza de cada afirmación en este informe:**
- **Comprobación realmente ejecutada:** verificación de hashes, lectura directa de archivos, comparación contra texto de fuentes.
- **Inspección documental:** lectura y cotejo del contenido de documentos candidatos y fuentes.
- **Declaración no verificable:** dato que el auditor no puede comprobar por sí mismo (p. ej., versión exacta de modelo no expuesta por la plataforma, identidad personal del propietario).
- **Inferencia:** conclusión derivada de la confrontación de requisitos y propuestas, no afirmada explícitamente en un solo documento.
- **Limitación:** comprobación que no pudo completarse y el motivo.

**Tipos de dictamen utilizados:** ACCEPTED, ACCEPTED_WITH_FINDINGS, REJECTED, INCONCLUSIVE.
**Severidades:** BLOCKER, HIGH, MEDIUM, LOW, INFO.

---

## 7. Reconstrucción normativa independiente y su hash

### 7.1 Artefacto de reconstrucción

**Ruta:** `docs/r13_reconstruccion_normativa_independiente_kilo.md`
**SHA-256:** `50f93e8bdaaad976373aa771fc1ba02189c578ef2113aa5682ac0da9345247b7`
**Fecha y hora de creación:** 2026-11-27T22:58:28Z
**Origen:** fuentes originales S-01..S-10 y A-01..A-04 del manifiesto de transferencia (más DEC-06 extraído del registro de decisiones normativas citado como autoridad en S-01 §2 y S-03 §2).

La reconstrucción cubre los diez requisitos del §4 de la misión:
1. Decisiones D1-D6 y sus aprobaciones.
2. Alcance y contenido de ORACLE-ART-01 a ORACLE-ART-07.
3. Jerarquía normativa entre DEC-06, diseño v4 §9.2 y `manifest_v4.json`.
4. Condiciones originales de G0-G6.
5. Ocho condiciones conjuntas de G5.
6. Cinco condiciones conjuntas de G6.
7. Requisitos originales de revisión humana para ORACLE-ART-04.
8. Condiciones de independencia, trazabilidad y reproducibilidad.
9. Limitaciones de autorización del propietario.
10. Estado y condiciones de cierre de AUD_R8_02.

### 7.2 Síntesis de la reconstrucción (puntos clave utilizados como línea base de auditoría)

**D1-D6 (S-03 §3, matriz §4, secuencia §4.1; aprobación A-02):** D1 `rule_id` secuencial por fila de §9.2; D2 ubicación física de artefactos/evidencias; D3 identidad del revisor humano independiente (rol funcional designado, identidad real al ejecutar); D4 formato de evidencias (UTF-8 determinista, JCS derivado exclusivamente auxiliar); D5 convención de versiones (`ORACLE_NORMATIVE_V4_R5` hasta cambio aprobado); D6 arquitectura de ORACLE-ART-02 (verificador en `tests/`, sin imports productivos ni dependencias nuevas). Solo D3 se modifica en las enmiendas R3; D1, D2, D4, D5, D6 permanecen sin cambios. La aprobación de las decisiones no se confunde con la aprobación de las cinco propuestas. La autoridad final de aceptación permanece en el propietario.

**ORACLE-ART-01 a ORACLE-ART-07 (S-04 §4, S-05 §2, S-01 §5.8.5):** siete artefactos, todos en estado `NOT_CREATED`. ORACLE-ART-01 (transcripción de 139 rutas, diez campos, `rule_id` como trazabilidad), ORACLE-ART-02 (versión ejecutable independiente), ORACLE-ART-03 (SHA-256 JCS de `{"version","entries"}` sin octavo artefacto), ORACLE-ART-04 (registro de revisión humana independiente), ORACLE-ART-05 (cobertura 139 rutas), ORACLE-ART-06 (nueve metadatos: path, type, manifest_required, manifest_required_when, manifest_allowed_when, projection_include_when, projection_optional, nullable, normalization; `rule_id` no es uno de los nueve), ORACLE-ART-07 (mutación aislada `external_run_only` en tres rutas `calibration.base_*`).

**Jerarquía (S-04 §2, S-01 §5.8, DEC-06):** Nivel 1 = DEC-06 y diseño v4 §9.2 (autoridad normativa); Nivel 2 = `manifest_v4.json` (contrato estructural); Nivel 3 = `ALLOWLIST_V4` (representación ejecutable); Nivel 4 = `ORACLE_NORMATIVE_V4_R5` (transcripción independiente solo CI/auditoría); Nivel 5 = validaciones Fase A/B. El oracle se transcribe directamente de §9.2/DEC-06, no de `ALLOWLIST_V4` ni del schema.

**G0-G6 (S-05 §8):** G0 especificación aprobada; G1 plan revisado; G2 fuentes/herramientas verificadas; G3 autorización de materialización (expresa del propietario); G4 artefactos generados; G5 verificación independiente (entrada: G4 completo + revisión humana realizada; salida: evidencia y dictamen); G6 resolución de AUD_R8_02 (cinco condiciones conjuntas). La aprobación de G0 no implica G1-G6. G3 es obligatoria antes de cualquier generación.

**Ocho condiciones de G5 (S-09 §6):** (1) 139 rutas expandidas; (2) 24 `rule_id` (13 allowlist + 11 exclusión); (3) nueve metadatos separados de `rule_id`; (4) tipos, condiciones, nulabilidad, normalización; (5) correspondencia R9 §5.4 / §9.2 / `manifest_v4.json`; (6) integridad JCS/SHA-256 de ORACLE-ART-03; (7) correspondencia ART-05/06/07 con reglas originales; (8) detección de omisiones, duplicados, divergencias y contradicciones.

**Cinco condiciones de G6 (S-05 §8, AUD-MAT-PLAN-R1-01):** (1) siete artefactos materializados y estados verificados; (2) informe de auditoría independiente favorable sobre AUD_R8_02; (3) sin hallazgos bloqueantes sin resolver; (4) aceptación expresa del propietario independiente de la aceptación técnica del auditor; (5) evidencia documental trazable de cada requisito. G5 favorable no equivale a superar G6. G6 no autoriza Fase C.

**Revisión humana ORACLE-ART-04 (S-04 §4.4, D3 S-03 §3.3):** revisión semántica real por revisor distinto del generador; identidad funcional designada por el propietario e identidad real al ejecutar; declaración de independencia, versión y checksum revisados, casos, hallazgos resueltos, dictamen, fecha real; fail-closed sin independencia; el checksum no sustituye la revisión humana.

**Independencia (DEC-OWNER-AI-04, S-07 §4; S-09 §6):** 9 condiciones: proveedor/modelo distintos del generador con linaje; sesión limpia; fuentes originales sin resúmenes del generador; ausencia de dictámenes previos en contexto; prompt íntegro y hashes de entradas; linaje y contexto registrados; reconstrucción independiente hashable antes de la comparación; auditor posterior distinto de IA y generador (a ciegas); limitaciones declaradas. Mismo proveedor o limitación no demostrable → `INCONCLUSIVE`. Dos ejecuciones del mismo modelo no son independencia suficiente.

**Límites de autorización del propietario (S-06 §3, S-07 DEC-OWNER-AI-06, S-08 §4):** no se autoriza Fase C, cierre automático de AUD_R8_02, omisión de revisión humana, omisión de auditoría, declaración de G6 sin criterios, fases D-G/S2, modificación de Parquet protegidos, cambios en producción/schemas/dependencias, commits/push. `INDEPENDENT_AI_REVIEW` no autoriza nada de lo anterior y se limita a ORACLE-ART-04.

**AUD_R8_02 (S-01 §10.6/10.7/10.8, S-04 §9, S-05 G6):** estado `OPEN` (antes AUD-R7-03). Los siete artefactos materiales del oracle no existen ni están verificados. Cierre solo con evidencia material y aceptación expresa del propietario conforme a G6 (cinco condiciones). Permanece `OPEN` hasta satisfacer sus condiciones.

---

## 8. Evaluación de cada una de las cinco propuestas

Cada propuesta se evalúa contra las comprobaciones obligatorias A-G (decisiones y autoridad, integridad normativa, independencia, reproducibilidad, evidencia, dictámenes y puertas, límites) y contra la reconstrucción del §7.

### 8.1 C-01 — `docs/r13_oracle_artifacts_decision_resolution_r3.md` (Resolución de decisiones R3, enmienda de D3)

**Tipo:** propuesta documental, `PREPARED_PENDING_INDEPENDENT_AUDIT`, no aprobada.

**A. Decisiones y autoridad:** CONFORME. R2 conservada íntegramente como registro histórico (§1). Solo D3 se modifica (D3-R3, §3); D1, D2, D4, D5, D6 sin cambios (§2 tabla). La aprobación de decisiones no se confunde con aprobación de las propuestas ("No aprobada. Sometida a auditoría independiente antes de cualquier aprobación", §5; §6). La autoridad final de aceptación permanece en el propietario (§3.8: "La aprobación de esta R3 es un acto separado y pendiente, posterior a su auditoría independiente").

**B. Integridad normativa:** CONFORME. R2 íntegra como histórico. Excepción de revisión IA limitada exclusivamente a ART-04 (§2, §3.3). Jerarquía intacta (§5: "Diseño R9 permanece intacto"). IA revisora no es fuente normativa (§3.4). No se crea octavo artefacto (solo D3 enmendada, no D7-D9, §2). No cambia semántica de ART-01/02/03/05/06/07 (§2: se rigen por R2).

**C. Independencia:** CONFORME. Cuatro roles inconfundibles y separados (§3.4: generador, IA revisora, auditor posterior, propietario). Proveedor y modelo distintos del generador con declaración de linaje (§3.5). Sesión limpia (§3.5). Ausencia de dictámenes previos en contexto inicial (§3.5). Trazabilidad de proveedor/modelo/versión/prompt/parámetros/entradas (§3.5). Consecuencias explícitas: mismo proveedor o limitación no demostrable obliga a `INCONCLUSIVE`; dos ejecuciones del mismo modelo no son independencia suficiente (§3.5).

**D. Reproducibilidad:** PARCIALMENTE COBERTA (por remisión). C-01 es una resolución de decisiones; los controles de reproducibilidad (prompt, hashes, parámetros, registro íntegro) se declaran en §3.5 y se remiten al protocolo R2. Como documento de decisión, es apropiado que no los contenga íntegro.

**E. Evidencia:** CONFORME como resolución de decisiones. Citra hashes de R2, del registro de aprobación y de la habilitación (S-08). No es una matriz de evidencia; esa corresponde al protocolo R2 (C-05) y a la ejecución.

**F. Dictámenes y puertas:** CONFORME. Dictámenes permitidos y severidades listadas (§3.6). IA propone dictamen, auditor confirma severidades, propietario decide aceptación (§3.6, §3.8). `INCONCLUSIVE` y `REJECTED` no desbloquean G5 (§3.6). `ACCEPTED_WITH_FINDINGS` no desbloquea G5 con BLOCKER/HIGH sin resolver (§3.6). G5 y G6 conservan requisitos propios, no automáticos (§6: G5 BLOCKED, G6 NOT_STARTED).

**G. Límites:** CONFORME. `AUD_R8_02` permanece `OPEN` (§6). No autorización implícita para Fase C (§6: "no autoriza Fase C"). No se autoriza producción/schemas/dependencias/Parquet. No ejecución automática de G5/G6. No ampliación de alcance a otros artefactos (§2, §3.3).

**Hallazgo C-01 (F-01, LOW):** En §3.1 se enumera "DEC-OWNER-AI-01, 03, 04 y 05" como aprobadas para superar la recomendación del análisis G5 R1, omitiendo DEC-OWNER-AI-02 y DEC-OWNER-AI-06. El registro S-08 confirma las seis (01-06) como APPROVED, por tanto no hay impacto normativo real, pero la enumeración en C-01 §3.1 está incompleta. **Clasificación: LOW (documentación).** No es BLOCKER/HIGH.

**Veredicto C-01:** ACCEPTED_WITH_FINDINGS (finding F-01, LOW).

### 8.2 C-02 — `docs/r13_oracle_artifacts_specification_r3.md` (Especificación Oracle R3, enmienda de ART-04)

**Tipo:** propuesta documental, `PREPARED_PENDING_INDEPENDENT_AUDIT`, no aprobada.

**A. Decisiones y autoridad:** CONFORME. Modifica exclusivamente §4.4 (ART-04) y consecuencias necesarias de secciones 5 y 6 (§1). Resto de secciones con contenido de R2. R2 conservada íntegramente. Autoridad final en el propietario (§3.5, §3.7 "aprobación expresa del propietario").

**B. Integridad normativa:** CONFORME. R2 íntegra como histórico (§1). Excepción limitada exclusivamente a ART-04 (§1, §2, §3.1, §6). Jerarquía intacta (§2: "Sin cambios respecto a R2 §2... La autoridad es DEC-06 y el diseño v4 §9.2... una IA revisora no es fuente normativa"). No octavo artefacto (§1: "El conjunto sigue siendo de siete artefactos. No se crea un octavo artefacto ni se altera la semántica de ART-01/02/03/05/06/07"). No cambia semántica de los otros seis artefactos.

**C. Independencia:** CONFORME. Roles separados (§3.2 tabla, §5). Proveedor y modelo distintos del generador con linaje (§3.4 punto 1). Sesión limpia (§3.4 punto 2). Fuentes originales sin resúmenes del generador (§3.4 punto 3). Ausencia de dictámenes previos (§3.4 punto 4). Trazabilidad (prompt/hash, hashes de entradas, linaje/contexto registrados, §3.4 puntos 5-7). Consecuencias explícitas (§3.5, §6: limitación no demostrable impide `ACCEPTED`; dos ejecuciones del mismo modelo no bastan, §3.4 punto 9).

**D. Reproducibilidad:** CONFORME como especificación (declara controles; la ejecución pertenece al protocolo y al registro). §3.4 punto 5 (prompt íntegro y hash), punto 6 (registro íntegro de respuestas, parámetros, inventario de herramientas), punto 7 (artefacto hashable de reconstrucción independiente anterior a la comparación).

**E. Evidencia:** CONFORME. Contenido mínimo obligatorio de ART-04 con 10 ítems (§3.3). Evidencias obligatorias de la revisión IA con 8 bullets (§3.4), incl. matriz 139 × 9 con esperado/observado/resultado por celda (punto 2) y tabla de discrepancias con trazabilidad (punto 3).

**F. Dictámenes y puertas:** CONFORME. Cuatro dictámenes y cinco severidades (§3.5). `ACCEPTED_WITH_FINDINGS` solo con hallazgos MEDIUM/LOW/INFO resueltos y verificados, sin contradicción normativa (§3.5) — más restrictivo que el mínimo requerido, no debilita. `INCONCLUSIVE`/`REJECTED` no sustentan ART-04 (§3.8). G5 no se desbloquea (§7: G5 BLOCKED).

**G. Límites:** CONFORME. `AUD_R8_02` `OPEN` (§7). No Fase C (§7). No automática G5/G6. No ampliación de alcance (§1, §6).

**Hallazgo C-02 (F-02, INFO):** §3.6 declara las dependencias de ART-04 como ART-01, ART-02, ART-03; R2 §4.4 lista dependencias ORACLE-ART-01 y ORACLE-ART-03. Es una adición de ART-02 como dependencia de ART-04 dentro de la enmienda de ART-04; no altera los otros seis artefactos ni crea dependencia circular. **Clasificación: INFO (desviación documental menor de R2 §4.4, dentro del alcance de la enmienda de ART-04).**

**Veredicto C-02:** ACCEPTED_WITH_FINDINGS (finding F-02, INFO).

### 8.3 C-03 — `docs/r13_oracle_artifacts_materialization_plan_r3.md` (Plan de materialización R3, enmienda de G5)

**Tipo:** propuesta documental, `PREPARED_PENDING_INDEPENDENT_AUDIT`, no aprobada.

**A. Decisiones y autoridad:** CONFORME. R2 conservada íntegramente (§1). Modifica exclusivamente la fila G5 de la tabla de puertas (§8) y consecuencias de roles (§7); secciones 1-6, 9-11 y filas G0-G4 y G6 con contenido de R2. G6 sin cambios sustantivos (§4.2 reproduce texto literal de R2). Autoridad final en el propietario (§4 fila G5: "aceptación expresa del propietario"; §4.1 punto 7: "aceptación expresa del propietario, independiente de la aceptación técnica").

**B. Integridad normativa:** CONFORME. R2 íntegra. Excepción limitada a ART-04 (fila G5: `INDEPENDENT_AI_REVIEW` para ART-04). Jerarquía intacta (G6 reproduce R2; siete artefactos). IA no fuente normativa (§3: "No aprueba, no firma, no modifica fuentes"). No octavo artefacto (§2: siete artefactos). No cambia semántica de otros seis artefactos.

**C. Independencia:** CONFORME por remisión a la modalidad autorizada. Roles distintos (§3 tabla). La fila G5 requiere "revisión independiente realizada conforme a modalidad autorizada: HUMAN_INDEPENDENT_REVIEW o INDEPENDENT_AI_REVIEW para ART-04"; los controles de independencia (proveedor/modelo distintos, sesión limpia, etc.) se definen en D3-R3/protocolo R2 y se remiten aquí. Como plan, es apropiado el remiso. Dos ejecuciones del mismo modelo no son independencia suficiente (remisión a DEC-OWNER-AI-04 vía "modalidad autorizada").

**D. Reproducibilidad:** CONFORME por remisión al protocolo R2 §7.

**E. Evidencia:** CONFORME. Fila G5 requiere "Evidencia de verificación y dictamen; informe de auditoría separada; aceptación expresa del propietario." §4.1 regla crítica de G5 con 8 condiciones conjuntas.

**F. Dictámenes y puertas:** CONFORME. Rechazo G5: "Discrepancia no resuelta; revisión no independiente; INCONCLUSIVE/REJECTED; ACCEPTED_WITH_FINDINGS con hallazgos BLOCKER/HIGH; falta de auditoría separada." §4.1: "INCONCLUSIVE y REJECTED nunca desbloquean G5." §4.2: G6 cinco condiciones preservadas literalmente. IA no cierra G5 automáticamente (§4.1).

**G. Límites:** CONFORME. `AUD_R8_02` `OPEN` (§6). G6 intacto y no autoriza Fase C (§4.2 cita literal). No automática G5/G6. No ampliación de alcance.

**Observación C-03 (F-03, INFO):** §4.1 condición 8 exige "siete artefactos en estado VERIFIED" para G5. R2 G5 entrada es "G4 completo; revisión humana realizada" (G4 = generados, no necesariamente verificados; la verificación completa de los siete es condición 1 de G6). C-03 sube el umbral de G5 (más restrictivo), no lo debilita. No es contradicción normativa. **Clasificación: INFO (criterio G5 más estricto que R2, coherente con G6).**

**Veredicto C-03:** ACCEPTED_WITH_FINDINGS (observación F-03, INFO).

### 8.4 C-04 — `docs/r13_oracle_artifacts_materialization_authorization_r3.md` (Autorización de materialización R3)

**Tipo:** propuesta documental, `MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE`, NO en vigor.

**A. Decisiones y autoridad:** CONFORME. R2 conservada íntegramente como registro histórico y autorización vigente (§1: "R2 sigue siendo la autorización vigente"). R3 solo describe versión futura. No confiere autorización ejecutable hasta auditoría independiente y aprobación expresa (§1). Autoridad final en el propietario (§3 condición 5: "aprobación expresa del propietario del resultado de esa auditoría, en registro separado").

**B. Integridad normativa:** CONFORME. R2 íntegra. Excepción limitada exclusivamente a ART-04 / `INDEPENDENT_AI_REVIEW` (§2.1: "Permitido únicamente mediante INDEPENDENT_AI_REVIEW aplicada a ORACLE-ART-04"). Jerarquía intacta (§6). IA no es revisión humana (§2.1). No octavo artefacto (§4: "El conjunto sigue siendo de siete artefactos"). No cambia semántica de otros seis artefactos (§4 tabla: otros "Según R2 / Sin cambios").

**C. Independencia:** CONFORME por remisión. Los controles específicos de independencia (proveedor/modelo distintos, sesión limpia, etc.) se declaran en D3-R3/protocolo R2 y se remiten (§3 condición 6: "protocolo R2 operativo"). Como autorización, apropiado el remiso.

**D. Reproducibilidad:** CONFORME por remisión al protocolo R2.

**E. Evidencia:** CONFORME. §6 verificación de referencias con hashes (R2, plan R2, diseño R9, registro de decisiones, HEAD). §3 condiciones previas a entrada en vigor (6 condiciones, incl. auditoría independiente y aprobación expresa del propietario).

**F. Dictámenes y puertas:** CONFORME. §5: no tratar `INCONCLUSIVE`/`REJECTED` como habilitante; un dictamen IA no cierra puertas (ejecutar G5/G6 automáticamente); `AUD_R8_02: OPEN` (§7); G6 no se declara superada sin sus cinco condiciones (§5). Fase C `NOT_GRANTED` (§7).

**G. Límites:** CONFORME. `AUD_R8_02` `OPEN` (§7). No Fase C ni fases D-G/S2 (§5, §7). No producción/schemas/dependencias/tests/Parquet (§5). No automática G5/G6 (§5). No ampliación de alcance a otros artefactos (§4: "No se amplía la autorización a artefactos distintos de ORACLE-ART-04"; §5). No commits/push (§5).

**Veredicto C-04:** ACCEPTED (no findings; correctamente declara que no está en vigor y no confiere autorización).

### 8.5 C-05 — `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md` (Protocolo de revisión IA independiente R2)

**Tipo:** propuesta documental, `PREPARED_PENDING_INDEPENDENT_AUDIT`, no aprobada.

**A. Decisiones y autoridad:** CONFORME. DEC-OWNER-AI-01…06 como "Habilitación expresa — Aprobadas" (§3). IA propone dictamen, auditor confirma, propietario acepta (§8.3). Autoridad final en el propietario (§8.3). Documento no aprobado ("propuesta documental. No aprobada; pendiente de auditoría independiente", §5).

**B. Integridad normativa:** CONFORME. Fuentes conservadas sin modificar (§2). Excepción limitada exclusivamente a ART-04 (§1: "Definir la modalidad INDEPENDENT_AI_REVIEW para sustentar exclusivamente ORACLE-ART-04"; §4 tabla: "Sí, solo ART-04"). Jerarquía intacta (§3: diseño R9 §5.4/§5.8 "Aprobado, sin cambios"). IA no es fuente normativa / no se denomina revisión humana (§4: prohibido denominarla revisión humana o cumplimiento directo de D3 R2). No octavo artefacto (§1: "este protocolo no ejecuta revisión alguna ni crea artefactos"). No cambia semántica de otros seis artefactos (§16: "no modifica R2 ni el diseño R9").

**C. Independencia:** CONFORME. Roles distintos (§10: auditor distinto del generador y de la IA, evaluación a ciegas). Proveedor y modelo distintos del generador con linaje (§6 punto 1). Sesión limpia (§6 punto 2). Fuentes originales sin resúmenes del generador (§6 punto 3). Ausencia de dictámenes previos en contexto (§6 punto 4). Trazabilidad completa: proveedor/modelo/versión (§7), prompt íntegro con hash (§7), hashes de todas las entradas (§7), parámetros de generación (§7), linaje/contexto registrados (§6 punto 6). Consecuencias explícitas: mismo proveedor o linaje no declarable → `INCONCLUSIVE` (§6 punto 1); limitaciones declaradas (§6 punto 8); dos ejecuciones del mismo modelo no son independencia suficiente (§6 punto 9); cualquier limitación de independencia/reproducibilidad se clasifica al menos HIGH (§8.2).

**D. Reproducibilidad:** CONFORME. §7: identificador y versión exacta del modelo (o `NO_DISPONIBLE` → `INCONCLUSIVE` para lo que dependa de él); parámetros (temperatura, seed, top_p, límites, herramientas); prompt completo verbatim con hash; hash de todos los archivos leídos; registro íntegro de respuestas; repetición con sesión nueva y mismo manifiesto; reglas de discrepancia (comprobaciones deterministas prevalecen; estocástica exige concordancia; divergencia → `INCONCLUSIVE`; resuelve auditor posterior, nunca la IA). §9.2: artefacto hashable de reconstrucción independiente anterior a la comparación (etapa C antes de D, §13).

**E. Evidencia:** CONFORME y completo. §9.1 matriz 139 × 9 metadatos con valor esperado reconstruido, valor observado y resultado por celda (`rule_id` separado). §9.2 reconstrucción hashable. §9.3 casos (positivo + 4 negativos por ruta). §9.4 tabla de discrepancias (ID, ruta/campo, severidad, fuente normativa, comprobación reproducible, resultado, resolución). §9.5 vinculación fuente → comprobación → resultado → entrada en tabla de discrepancias. **Verificación de ART-02 contra fuentes originales sin usar ART-01/ART-02 como fuente del esperado (§11):** reconstruir reglas desde R9 §5.4, §9.2 y `manifest_v4.json` sin usar ART-01 ni ART-02; comparar ART-01 y ART-02 contra la reconstrucción; ART-01↔ART-02 solo como comprobación secundaria. Esto cumple estrictamente el requisito E.5 de la misión.

**F. Dictámenes y puertas:** CONFORME. Cuatro dictámenes y cinco severidades (§8.1). `ACCEPTED_WITH_FINDINGS` solo hallazgos MEDIUM/LOW/INFO con resolución verificable, sin contradicción normativa, sin limitación bloqueante (§8.1). `INCONCLUSIVE` y `REJECTED` nunca desbloquean G5 (§8.4). `ACCEPTED_WITH_FINDINGS` tampoco mientras existan BLOCKER/HIGH sin resolver (§8.4). Solo `ACCEPTED` —o `ACCEPTED_WITH_FINDINGS` plenamente resuelto— con auditoría separada favorable, ART-04 verificado y aceptación expresa puede sustentar reevaluación de G5 (§8.4). IA no cierra G5/G6 automáticamente (§8.4, §12 punto 8: "Sin autorización R3 en vigor, la revisión no produce efecto normativo").

**G. Límites:** CONFORME. `AUD_R8_02` `OPEN` (§16). No Fase C (§16, §5). No producción/schemas/dependencies/Parquet (§12: acceso de solo lectura; §16). No automática G5/G6 (§8.4, §12 punto 8). No ampliación de alcance (§1 "exclusivamente ORACLE-ART-04"; §4 "solo ART-04"). No commits/push (§16).

**Hallazgo C-05 (F-04, INFO/LIMITACIÓN):** §2 "Fuentes verificadas" cita `docs/r13_audit_oracle_art_04_ai_independent_review_protocol_r1.md` (hash `146274794b1b2453c04e936e892a6fa39d6e15c3cafde80fe191650d73330693`) como fuente verificada. Ese documento NO forma parte de los 19 archivos del manifiesto de transferencia (el manifiesto §2 excluye informes de auditoría `r13_audit_*`). Su contenido no es verificable a partir de los inputs empaquetados. C-05 lo usa para fundamentar la resolución de los ocho hallazgos AUD-AI-REV-R1-01…08 (§5). Esto es coherente con S-07 (que cita esos hallazgos como antecedentes), pero el documento citado no está en el paquete de transferencia. **Clasificación: INFO/LIMITACIÓN (fuente citada fuera del paquete; no verificable desde los 19 inputs).** No es BLOCKER/HIGH porque los ocho hallazgos están también documentados en S-07 (paqueteado y verificado).

**Hallazgo C-05 (F-05, LIMITACIÓN de estado, no de la propuesta):** No existe evidencia de ejecución (ORACLE-ART-04 `NOT_CREATED`, G5 `BLOCKED`). No se ha ejecutado ninguna revisión IA, por lo que no existe registro íntegro de respuestas, prompt ejecutado ni hash de ejecución para verificar. Esto es una limitación del estado actual, no un defecto de las propuestas (que definen los controles para cuando se ejecuten). **Clasificación: INFO/LIMITACIÓN.**

**Veredicto C-05:** ACCEPTED_WITH_FINDINGS (observaciones F-04, F-05, INFO/LIMITACIÓN).

---

## 9. Matriz de trazabilidad normativa

| Requisito (reconstrucción §7) | Fuente | Verificado en | Resultado |
|---|---|---|---|
| D1-D6 representadas; solo D3 modificada | S-03 §3/§4, A-02 | C-01 §2, §3 | CONFORME (F-01 LOW) |
| R2 conservada íntegra como histórico | S-03 §1, S-04 §1, S-05 §1, S-06 §1 | C-01..C-04 §1 | CONFORME |
| Excepción IA limitada a ART-04 | D3-R3, DEC-OWNER-AI-01 (S-07) | C-01 §3.3, C-02 §3.1, C-03 fila G5, C-04 §2.1, C-05 §1/§4 | CONFORME |
| Jerarquía DEC-06 / §9.2 / manifest_v4.json intacta | S-04 §2, S-01 §5.8, DEC-06 | C-02 §2, C-05 §3 | CONFORME |
| IA revisora no es fuente normativa | R9 §5.8.1, DEC-OWNER-AI-05 | C-02 §2, C-05 §4 | CONFORME |
| No octavo artefacto Oracle | S-04 §4.3 (AUD-ORACLE-SPEC-R1-01) | C-01 §2, C-02 §1, C-05 §1 | CONFORME |
| Sin cambio semántica ART-01/02/03/05/06/07 | S-04 §4 | C-01 §2, C-02 §1, C-03 §2, C-05 §16 | CONFORME |
| Roles distintos (generador/IA/auditor/propietario) | D3 S-03 §3.3, DEC-OWNER-AI-04 | C-01 §3.4, C-02 §3.2/§5, C-03 §3, C-05 §10 | CONFORME |
| Proveedor/modelo distintos del generador | DEC-OWNER-AI-04 (1) | C-01 §3.5, C-02 §3.4-1, C-05 §6-1 | CONFORME |
| Sesión limpia | DEC-OWNER-AI-04 (2) | C-01 §3.5, C-02 §3.4-2, C-05 §6-2 | CONFORME |
| Sin dictámenes previos en contexto | DEC-OWNER-AI-04 (4) | C-01 §3.5, C-02 §3.4-4, C-05 §6-4 | CONFORME |
| Trazabilidad proveedor/modelo/versión/prompt/entradas | DEC-OWNER-AI-04 (5,6) | C-01 §3.5, C-02 §3.4-5/6/7, C-05 §6-5/6, §7 | CONFORME |
| Consecuencias explícitas de independencia | DEC-OWNER-AI-04 (9) | C-01 §3.5, C-05 §6-1/8/9, §8.2 | CONFORME |
| Dos ejecuciones mismo modelo ≠ independencia | DEC-OWNER-AI-04 | C-01 §3.5, C-02 §3.4-9, C-05 §6-9 | CONFORME |
| Prompt completo y hash | DEC-OWNER-AI-04 (5), S-09 §7 | C-02 §3.4-5, C-05 §7 | CONFORME |
| Hashes de todas las entradas | DEC-OWNER-AI-04 (5), S-09 §7 | C-02 §3.4-2, C-05 §7 | CONFORME |
| Parámetros de generación | DEC-OWNER-AI-04 (6), S-09 §7 | C-02 §3.4-6, C-05 §7 | CONFORME |
| Identidad exacta del modelo | DEC-OWNER-AI-04 (1), S-09 §7 | C-05 §7 | CONFORME (versión como `NO_DISPONIBLE` si no expuesta) |
| Registro íntegro de respuestas | S-09 §7 | C-02 §3.4-6, C-05 §7 | CONFORME (como control, no ejecución) |
| Reconstrucción independiente hashable antes de comparación | DEC-OWNER-AI-04 (7), S-09 §7 | C-02 §3.4-7, C-05 §9.2, §13 (etapa C antes de D) | CONFORME |
| Reglas de discrepancia entre ejecuciones | S-09 §7 | C-05 §7 | CONFORME |
| Matriz 139 × 9 con esperado/observado/resultado | S-09 §9.1, DEC-OWNER-AI-06 | C-02 §3.4-2, C-05 §9.1 | CONFORME |
| Tabla de discrepancias con trazabilidad | S-09 §9.4, §9.5 | C-02 §3.4-3, C-05 §9.4, §9.5 | CONFORME |
| ART-02 verificado contra fuentes sin ART-01/02 como esperado | S-09 §11, requisito E.5 | C-05 §11 | CONFORME |
| Dictámenes permitidos (4) y severidades (5) | DEC-OWNER-AI-05, S-09 §8 | C-01 §3.6, C-02 §3.5, C-05 §8 | CONFORME |
| IA propone, auditor confirma, propietario acepta | DEC-OWNER-AI-05 | C-01 §3.6/§3.8, C-02 §3.5, C-05 §8.3 | CONFORME |
| INCONCLUSIVE/REJECTED no desbloquean G5 | DEC-OWNER-AI-05, S-09 §8 | C-01 §3.6, C-03 §4.1, C-05 §8.4 | CONFORME |
| ACCEPTED_WITH_FINDINGS no desbloquea G5 con BLOCKER/HIGH | DEC-OWNER-AI-05, S-09 §8 | C-01 §3.6, C-02 §3.5, C-03 fila G5, C-05 §8.4 | CONFORME |
| G5 y G6 no automáticos | S-05 §8 | C-03 §4.1, C-05 §8.4 | CONFORME |
| AUD_R8_02 permanece OPEN | S-01 §10, S-05 G6 | C-01 §6, C-02 §7, C-03 §6, C-04 §7, C-05 §16 | CONFORME |
| No autorización implícita Fase C | S-06 §3, DEC-OWNER-AI-06 | C-01 §6, C-02 §7, C-03 §4.2, C-04 §5/§7, C-05 §5/§16 | CONFORME |
| No producción/schemas/dependencias/Parquet | S-06 §3, DEC-OWNER-AI-06 | C-04 §5, C-05 §12/§16 | CONFORME |
| No ejecución automática G5/G6 | DEC-OWNER-AI-06 (5) | C-03 §4.1, C-04 §5, C-05 §8.4/§12-8 | CONFORME |
| No ampliación de alcance a otros artefactos | DEC-OWNER-AI-06 (7) | C-01 §3.3, C-02 §1, C-04 §4, C-05 §1/§4 | CONFORME |

---

## 10. Comprobaciones de consistencia cruzada

Se compararon las cinco propuestas entre sí y frente a las fuentes originales:

1. **Estado común:** las cinco declaran `OWNER_DECISIONS: APPROVED`, `NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT`, `ORACLE-ART-04: NOT_CREATED`, `G5_STATUS: BLOCKED`, `G6_STATUS: NOT_STARTED`, `AUD_R8_02: OPEN`, `PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED`. **Consistente.**
2. **Solo D3 enmendada:** C-01 (D3-R3), C-02 (ART-04), C-03 (G5), C-04 (excepción versión R3), C-05 (protocolo). Ninguna enmenda D1, D2, D4, D5, D6. **Consistente.**
3. **Siete artefactos, no octavo:** todas afirman el conjunto de siete. **Consistente.**
4. **Hashes de R2 citados coinciden con el manifiesto:** C-01 cita R2 `6f408724…` (S-03/A-02 ✓), C-02 cita `0ede7956…` (S-04/A-03 ✓), C-03 cita `d4d0c689…` (S-05/A-04 ✓), C-04 cita `d692e49e…` (S-06 ✓). **Consistente.**
5. **Habilitación común:** todas citan el registro de decisiones del propietario S-08 (`3b6c946e…`) como habilitación. **Consistente.**
6. **No contradicciones normativas detectadas** entre las cinco propuestas y frente a S-01..S-10, A-01..A-04. C-01 §15 declara expresamente "Ninguna" contradicción; la auditoría independiente confirma que no hay contradicción normativa grave.
7. **C-01 §3.1 enumera incompletamente DEC-OWNER-AI-01/03/04/05 (omite 02/06):** aclarado por S-08 (seis APPROVED). No afecta consistencia normativa (F-01, LOW).
8. **C-02 §3.6 declara dependencia ART-02 para ART-04 (R2 §4.4 lista ART-01/ART-03):** desviación documental menor dentro de la enmienda de ART-04 (F-02, INFO).
9. **C-03 §4.1 condiciona G5 a siete artefactos VERIFIED (más estricto que R2 G5):** no debilita (F-03, INFO).
10. **C-05 §2 cita documento de auditoría previa fuera del paquete:** no verificable desde los 19 inputs (F-04, INFO/LIMITACIÓN).

No se detectó contradicción normativa grave. No hay fundamento para REJECTED ni INCONCLUSIVE por contradicción, entradas faltantes o independencia no demostrada.

---

## 11. Hallazgos y severidades

| ID | Origen | Hallazgo | Severidad | Tipo de evidencia | Estado / resolución requerida |
|---|---|---|---|---|---|
| F-01 | C-01 §3.1 | Enumeración incompleta de DEC-OWNER-AI (cita 01/03/04/05, omite 02/06). S-08 confirma las seis APPROVED. | LOW | Inspección documental (cotejo C-01 vs S-08) | Aclarar enumeración en versión aprobada; sin impacto normativo. |
| F-02 | C-02 §3.6 | Declara dependencias ART-04 = ART-01/02/03; R2 §4.4 lista ART-01/ART-03. | INFO | Inspección documental (cotejo C-02 vs S-04 §4.4) | Dentro del alcance de enmienda de ART-04; no altera otros artefactos. |
| F-03 | C-03 §4.1 | Condición 8 de G5 exige siete artefactos VERIFIED (más estricto que R2 G5). | INFO | Inspección documental (cotejo C-03 vs S-05 §8) | Criterio protector, no debilita; consistente con G6. |
| F-04 | C-05 §2 | Cita `docs/r13_audit_oracle_art_04_ai_independent_review_protocol_r1.md` fuera del paquete de 19; no verificable desde inputs empaquetados. | INFO / LIMITACIÓN | Inspección documental (cotejo vs manifiesto §2) | Los ocho hallazgos AUD-AI-REV-R1 están también en S-07 (paqueteado). |
| F-05 | Estado general | No existe evidencia de ejecución (ORACLE-ART-04 NOT_CREATED, G5 BLOCKED); no hay prompt ejecutado ni registro íntegro de respuestas para verificar. | INFO / LIMITACIÓN de estado | Comprobación de estado (S-01 §5, estados comunes) | Limitación del estado actual, no defecto de las propuestas. |

**Sin hallazgos BLOCKER ni HIGH.** Ningún hallazgo impide una aceptación sin reservas en el plano de consistencia normativa de las propuestas. Los hallazgos son LOW/INFO y limitaciones de estado.

---

## 12. Dictamen final

**Dictamen: `ACCEPTED_WITH_FINDINGS`**

Fundamento:
- Independencia demostrada: proveedor `kilo` (Kilo Code) distinto del generador `OpenCode / Hy4 Flash Free`. No es INCONCLUSIVE por independencia.
- Entradas esenciales: 19/19 hashes verificados y coincidentes. No es INCONCLUSIVE/REJECTED por entradas ausentes o hashes incorrectos.
- No hay contradicción normativa grave. No es REJECTED.
- No hay hallazgos BLOCKER ni HIGH sin resolver. Puede emitirse aceptación (con findings).

Los hallazgos F-01 (LOW), F-02 (INFO), F-03 (INFO), F-04 (INFO/limitación) y F-05 (INFO/limitación de estado) no son BLOCKER ni HIGH, por lo que el dictamen no se degrada a REJECTED ni se bloquea G5 por ellos.

**Este dictamen es un dictamen técnico de la auditoría externa. NO equivale a aprobación del propietario.** La autoridad final de aceptación permanece exclusivamente en el propietario del proyecto, mediante registro expreso (DEC-OWNER-AI-05).

**Este dictamen NO desbloquea G5.** G5 permanece `BLOCKED`. Solo `ACCEPTED` —o `ACCEPTED_WITH_FINDINGS` plenamente resuelto— con auditoría separada favorable, ORACLE-ART-04 verificado y aceptación expresa del propietario puede sustentar la reevaluación de G5 (plan R3 §4.1, protocolo R2 §8.4). `INCONCLUSIVE` y `REJECTED` nunca desbloquean G5.

**G6 conserva sus cinco condiciones propias y no se ejecuta automáticamente.** La superación de G6 no autoriza Fase C.

---

## 13. Limitaciones

1. **No se ejecutó revisión IA alguna:** ORACLE-ART-04 está `NOT_CREATED` y G5 `BLOCKED`. No existe registro íntegro de respuestas, prompt ejecutado con hash, ni hashes de ejecución para verificar reproducibilidad efectiva. Las propuestas definen los controles para cuando se ejecuten, pero la evidencia de ejecución no existe aún (F-05).
2. **Versión exacta del modelo no expuesta por la plataforma:** se registra `kilo-auto/free` (variante `free`); no se inventó un número de versión adicional.
3. **Identificador de sesión no disponible como token de plataforma:** sesión de auditoría externa independiente sin historial compartido.
4. **Parámetros de generación (temperatura, seed, top_p, herramientas) no expuestos por la plataforma:** registrados como `no disponible`.
5. **Documento de auditoría previa citado en C-05 §2 no está en el paquete de 19:** su contenido no es verificable desde los inputs empaquetados (F-04); los ocho hallazgos subyacentes están documentados en S-07 (paqueteado y verificado).
6. **DEC-06 extraído del registro `docs/aud04b_model_provenance_v4_approval_r1.md`**, que no está entre los 19 archivos del manifiesto (citado como autoridad en S-01 §2 y S-03 §2). Es un documento de aprobación normativa, no un informe de auditoría; su hash no se verificó contra el manifiesto.
7. Este informe no aprueba las propuestas en nombre del propietario, no crea ORACLE-ART-04, no ejecuta G5 ni G6, no implementa Fase C, no modifica producción, schemas, dependencias, tests ni Parquet, y no realiza commits ni push.

---

## 14. Condiciones pendientes para la aprobación del propietario

Antes de que el propietario pueda aceptar las enmiendas y antes de que G5 pueda ser reevaluado, deben cumplirse las siguientes condiciones (derivadas de la reconstrucción §7 y de los estados comunes de las propuestas):

1. **Auditoría independiente favorable** de las cinco propuestas (el presente informe la ejecuta y emite `ACCEPTED_WITH_FINDINGS`); el propietario debe emitir aceptación expresa del resultado de esta auditoría, independiente de la aceptación técnica del auditor.
2. **Aprobación expresa y separada de cada enmienda:** D3-R3 (C-01), especificación R3 (C-02), plan R3 (C-03), autorización de materialización R3 (C-04) y protocolo R2 (C-05), cada una posterior a su auditoría independiente.
3. **Autorización de materialización R3 en vigor:** solo tras cumplir las seis condiciones previas de C-04 §3 (incluida aprobación expresa del propietario del resultado de la auditoría en registro separado). Hasta entonces, `MATERIALIZATION_AUTHORIZATION_STATUS: PREPARED_NOT_EFFECTIVE`.
4. **ORACLE-ART-04 materializado y auditado** bajo `INDEPENDENT_AI_REVIEW` con dictamen `ACCEPTED` o `ACCEPTED_WITH_FINDINGS` (sin hallazgos BLOCKER/HIGH sin resolver) y auditoría separada favorable.
5. **G5 favorable:** concurrir las condiciones de plan R3 §4.1 (incluida autorización R3 en vigor, D3-R3/spec/plan R3 auditados y aprobados, revisión ejecutada conforme al protocolo, auditoría técnica separada favorable, aceptación expresa del propietario). `INCONCLUSIVE` y `REJECTED` nunca desbloquean G5.
6. **G6 superado:** las cinco condiciones conjuntas (siete artefactos materializados y verificados; informe de auditoría independiente favorable sobre AUD_R8_02; sin hallazgos bloqueantes sin resolver; aceptación expresa del propietario; evidencia documental trazable de cada requisito).
7. **AUD_R8_02 cerrado** con evidencia material y aceptación expresa del propietario conforme a G6. Hasta entonces permanece `OPEN`.
8. **Fase C sigue `NOT_GRANTED`:** la superación de G6 no autoriza por sí misma Fase C; requiere autorización técnica separada y explícita del propietario.
9. **Resolución de hallazgos menores:** aclarar la enumeración de DEC-OWNER-AI en C-01 §3.1 (F-01, LOW) en la versión aprobada.

**Resumen de estados que deben permanecer hasta cumplirse lo anterior:**
```
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

---

## 15. Confirmación de alcance de la auditoría

Esta auditoría es exclusivamente documental. Se confirmó:

- No se modificaron las cinco propuestas (C-01 a C-05).
- No se modificaron las fuentes originales (S-01 a S-10).
- No se modificaron documentos de aprobación (A-01 a A-04).
- No se creó ORACLE-ART-04.
- No se ejecutaron G5 ni G6.
- No se implementó Fase C.
- No se modificó código de producción, schemas, dependencias, tests ni archivos Parquet.
- No se realizaron commits ni push.
- No se aprobó las propuestas en nombre del propietario.

**Archivos creados en esta tarea:**
1. `docs/r13_reconstruccion_normativa_independiente_kilo.md` — reconstrucción normativa independiente y hashable (SHA-256 `50f93e8bdaaad976373aa771fc1ba02189c578ef2113aa5682ac0da9345247b7`, creado 2026-11-27T22:58:28Z).
2. `audit_report_r13_oracle_art_04_kilo_external.md` — el presente informe de auditoría externa independiente.

**No se modificó ningún otro archivo.**

La decisión de aceptación normativa y cualquier autorización posterior corresponden exclusivamente al propietario del proyecto.

**Fin de `audit_report_r13_oracle_art_04_kilo_external.md`.**
