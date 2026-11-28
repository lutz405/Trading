# R13-ORACLE-ARTIFACTS-R4-INDEPENDENT-AUDIT-R1 — Auditoría independiente del paquete de correcciones normativas R4

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** informe de auditoría normativa independiente de solo lectura sobre las cinco propuestas R4. **No** aprueba versiones, **no** declara cerrados hallazgos por autoridad del propietario, **no** crea `ORACLE-ART-04`, **no** ejecuta G5 ni G6 y **no** autoriza Fase C.

```text
AUDIT_VERDICT: INCONCLUSIVE
TECHNICAL_CORRECTIONS_ASSESSMENT (AUD-ANT-02..07): SOUND_WITH_LOW_FINDINGS
AUD_ANT_01_STATUS: INCONCLUSIVE (OPEN — HIGH)
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

---

## 1. Identidad del auditor y evidencia de independencia

### 1.1 Registro obligatorio previo

| Campo | Valor observado / declarado |
|---|---|
| **Proveedor** | Google / Google DeepMind (reportado por el entorno de plataforma) |
| **Modelo y versión** | `Gemini 4 Hydrogen (High)` (nombre legible reportado por la plataforma; identificador exacto de compilación/versión de pesos: `NO_DISPONIBLE`) |
| **Plataforma** | Antigravity (entorno Windows, workspace `Trading`) |
| **Sesión nueva** | Sí — conversación nueva `8e8ecd06-410b-4e85-828c-a6cf5522a98c`, iniciada el `2026-11-27T17:42:42-06:00` sin historial previo de generación ni de edición de R1–R4 |
| **Parámetros disponibles** | Selección de modelo: `Gemini 4 Hydrogen (High)`. Parámetros de muestreo (`temperature`, `top_p`, `seed`, `max_tokens`): `NO_DISPONIBLE` (no expuestos al agente en el entorno) |
| **Generador original conocido** | OpenCode con `Hy4 Flash Free`, cuyo proveedor real subyacente continúa sin estar acreditado en el repositorio |

### 1.2 Declaración de independencia y evidencia verificable

- **Evidencia verificable disponible:** metadatos locales de sesión de la plataforma Antigravity (`Conversation ID: 8e8ecd06-410b-4e85-828c-a6cf5522a98c`, marca temporal `2026-11-27T17:42:42-06:00`, cambio de configuración reportado por la plataforma hacia `Gemini 4 Hydrogen (High)`). No existe atestación criptográfica externa del proveedor ni registro verificable del proveedor real detrás de `Hy4 Flash Free` utilizado en OpenCode.
- **Declaración de independencia:** **NO SE DECLARA INDEPENDENCIA DEMOSTRADA.** Conforme al criterio de no presunción, no se presupone que Gemini y Hy4 pertenezcan al mismo proveedor ni que pertenezcan a proveedores distintos. Al permanecer sin acreditar el proveedor real del generador original (`Hy4 Flash Free`), la independencia respecto del generador original **no es demostrable**.

### 1.3 Limitaciones de identificación y reproducibilidad

1. **Proveedor del generador original no acreditado (`AUD-ANT-01`):** no existe evidencia verificable en el repositorio que acredite qué proveedor/modelo real sirvió `Hy4 Flash Free` en OpenCode.
2. **Versión exacta de compilación del modelo auditor (`NO_DISPONIBLE`):** la plataforma informa el nombre legible `Gemini 4 Hydrogen (High)`, pero no expone un identificador de revisión/checkpoint inmutable ni digest de pesos.
3. **Parámetros de generación no expuestos (`NO_DISPONIBLE`):** `temperature`, `top_p`, `seed` y límites de tokens no son visibles ni verificables desde el entorno de ejecución del agente.
4. **Ausencia de binario `git` en `PATH` del shell:** `git` no estuvo disponible como comando en PowerShell; los hashes Git blob (SHA-1 de `blob <len>\0<bytes>`) y referencias de `.git/HEAD` y `.git/refs/heads/main` se verificaron directamente mediante Python y lectura de archivos en `.git/`.

De acuerdo con `DEC-OWNER-AI-04`, Protocolo R3 §§6, 7, 8.1, 8.2 y la regla explícita de alcance de esta auditoría, estas limitaciones obligan a emitir dictamen formal **`INCONCLUSIVE`**. La evaluación técnica del contenido normativo (secciones 3–7 de este informe) se mantiene separada de la evaluación de independencia (sección 6).

---

## 2. Inventario e integridad (SHA-256 y Git)

Todos los cálculos se realizaron en modo de solo lectura mediante `Get-FileHash -Algorithm SHA256` y cálculo directo de Git blob SHA-1 sobre los bytes exactos en disco. **No se utilizó ninguna auditoría anterior como fuente de requisitos.**

### 2.1 Documentos candidatos R4/R3 y paquete de trazabilidad

| ID | Archivo | SHA-256 esperado (paquete R1) | SHA-256 calculado | Git blob esperado | Git blob calculado | Estado |
|---|---|---|---|---|---|---|
| N-01 | `docs/r13_oracle_artifacts_decision_resolution_r4.md` | `a95f6af90b212d8539e1818ad3680a51762504fc9025cc1ae7d2436311b66ea5` | `a95f6af90b212d8539e1818ad3680a51762504fc9025cc1ae7d2436311b66ea5` | `310915829fc90b04c3808c39092f0f58ef31e13c` | `310915829fc90b04c3808c39092f0f58ef31e13c` | COINCIDE |
| N-02 | `docs/r13_oracle_artifacts_specification_r4.md` | `ff722887189e6e5ca223e3699fae34b870c09d36810f81680b26689d978c1ba5` | `ff722887189e6e5ca223e3699fae34b870c09d36810f81680b26689d978c1ba5` | `2bdae65282062979a49191970640de123a52dfce` | `2bdae65282062979a49191970640de123a52dfce` | COINCIDE |
| N-03 | `docs/r13_oracle_artifacts_materialization_plan_r4.md` | `226c51d08a3171232098f40d4e22cf0d2d1487a1c373aa480e69d5651da63e71` | `226c51d08a3171232098f40d4e22cf0d2d1487a1c373aa480e69d5651da63e71` | `aa8c03700edf5c78b1a7602ce92e9f900c7924a8` | `aa8c03700edf5c78b1a7602ce92e9f900c7924a8` | COINCIDE |
| N-04 | `docs/r13_oracle_artifacts_materialization_authorization_r4.md` | `2db94133ef1f01b9f8ef6884efac95243c95b69b2fff489aac64f83bab55b2ec` | `2db94133ef1f01b9f8ef6884efac95243c95b69b2fff489aac64f83bab55b2ec` | `75c0790733930e9a6b4514c32afe42810a7728f6` | `75c0790733930e9a6b4514c32afe42810a7728f6` | COINCIDE |
| N-05 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r3.md` | `e538b144b575843ad528faf9220e1f6bffbf2f4a90710539b87032101d1e3f75` | `e538b144b575843ad528faf9220e1f6bffbf2f4a90710539b87032101d1e3f75` | `6c972eedfbb747c00da50d28d6ef078bf57238e9` | `6c972eedfbb747c00da50d28d6ef078bf57238e9` | COINCIDE |
| Evidencia | `docs/r13_oracle_artifacts_normative_correction_package_r1.md` | — (guía de cambios) | `906a9534ed8d963f6d5bfe422b66c54dc0b52651ca6845f1fbb8877fe32d74e8` | — | — | VERIFICADO |

### 2.2 Verificación de integridad de R3/R2 precedentes (sin alteración)

| Archivo | SHA-256 esperado (en R4/R3) | SHA-256 calculado | Git blob esperado | Git blob calculado | Estado |
|---|---|---|---|---|---|
| `docs/r13_oracle_artifacts_decision_resolution_r3.md` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | `fbbb05f9529e59b92a44fe65fca540d39839ec00` | `fbbb05f9529e59b92a44fe65fca540d39839ec00` | INTACTO |
| `docs/r13_oracle_artifacts_specification_r3.md` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | `6167d76a89a6bf4e37c1978c8357d732d7d4b7c9` | `6167d76a89a6bf4e37c1978c8357d732d7d4b7c9` | INTACTO |
| `docs/r13_oracle_artifacts_materialization_plan_r3.md` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | `10d7f4be8b36849916d26f87c4baf3457538bc54` | `10d7f4be8b36849916d26f87c4baf3457538bc54` | INTACTO |
| `docs/r13_oracle_artifacts_materialization_authorization_r3.md` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | `0489cb78ecbf6d6a44c106eb2747a3533c98c53c` | `0489cb78ecbf6d6a44c106eb2747a3533c98c53c` | INTACTO |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | `7c3223a0e4954c401c0f513c903d9ad708130335` | `7c3223a0e4954c401c0f513c903d9ad708130335` | INTACTO |

### 2.3 Versiones R2, R1, fuentes normativas originales, aprobaciones y artefactos existentes

| Archivo | SHA-256 esperado (fuentes/registros) | SHA-256 calculado | Estado |
|---|---|---|---|
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | INTACTO |
| `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | INTACTO |
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | INTACTO |
| `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | INTACTO |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | INTACTO |
| `docs/r13_oracle_artifacts_decision_resolution_r1.md` | — | `53a80a88f5153a1220a97c3d4ee2c85d942fc7496fedd7c3262a9fd1f660d0ab` | VERIFICADO |
| `docs/r13_oracle_artifacts_specification_r1.md` | — | `2e6f6816c9d0a41de9da7b436a49a7214b962ce87817a2d551ec7832df40b23d` | VERIFICADO |
| `docs/r13_oracle_artifacts_materialization_plan_r1.md` | — | `60a9923f0327039b1451a884a132e382f2f8380e63626007cd204f6585805593` | VERIFICADO |
| `docs/r13_oracle_artifacts_materialization_authorization_r1.md` | — | `8dfd46c927ba22f525b9a4c2269c66eaf6b70bda71dbb66e04331bb973012457` | VERIFICADO |
| `docs/r13_oracle_art_04_ai_review_owner_decision_package_r1.md` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` | COINCIDE |
| `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` | COINCIDE |
| `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | COINCIDE |
| `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | — | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | VERIFICADO |
| `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` | — | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | VERIFICADO |
| `docs/r13_oracle_g5_blocker_resolution_analysis_r1.md` | `00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7` | `00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7` | COINCIDE |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | COINCIDE |
| `docs/aud04b_model_provenance_v4_design.md` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | COINCIDE |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | COINCIDE |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | COINCIDE |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | COINCIDE |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | — | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` | VERIFICADO |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | — | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | VERIFICADO |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | — | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | VERIFICADO |

`HEAD`: `ref: refs/heads/main`, commit `259ca6ee11878f114cdcab4cef500074b3bc1a48`. En `docs/oracle_artifacts/v4/r5/` existen únicamente `ORACLE-ART-01.json`, `03.txt`, `05.json`, `06.json`, `07.json`; `ORACLE-ART-04` no existe (`NOT_CREATED`).

---

## 3. Evaluación por documento candidato R4

### 3.1 `docs/r13_oracle_artifacts_decision_resolution_r4.md` (N-01)

- **Alcance:** corrige la referencia interna rota de R3 §5 (`Especificación R3 §4.4` → `Especificación R4 §3`) y actualiza referencias cruzadas hacia Plan R4, Autorización R4 y Protocolo R3.
- **Preservación:** conserva R3 y R2 intactos; conserva literalmente el contenido de D3-R3, la superación acotada de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1, los controles de `DEC-OWNER-AI-04`/`05`, las decisiones D1/D2/D4/D5/D6 de R2 y todos los estados límite (`NOT_GRANTED`, `NOT_CREATED`, `OPEN`, `BLOCKED`).
- **Observación (`LOW`, `AUD-ANT-NEW-01`):** la tabla de §4 (`Después (R4 §5)`) cita literalmente `Especificación R4 §3 define el contenido de ART-04…`, mientras la redacción efectiva de §5 es `Especificación R4 §3, Plan R4 §4 y Autorización R4 §3 reflejan la misma modalidad y alcance`. Además, en Autorización R4 la modalidad y el alcance están desarrollados en §2 y §4 (y §3 regula las condiciones de entrada en vigor). No genera invalidez de sección (todas existen), pero es imprecisión editorial menor.

### 3.2 `docs/r13_oracle_artifacts_specification_r4.md` (N-02)

- **Alcance:** corrige `AUD-ANT-03` (restaura `Dependencias` de ART-04 a `ORACLE-ART-01, ORACLE-ART-03` y sitúa `ART-02` en el alcance de revisión de §3.6 sin crear dependencia formal), `AUD-ANT-05` (§3.3 punto 5: 24 `rule_id` desglosados en 13 en allowlist + 11 de exclusión), `AUD-ANT-06` (§3.5 y §3.7: `LOW`/`INFO` registrados y trazables; versión no disponible y limitación de independencia no demostrable obligan a `INCONCLUSIVE`) y `AUD-ANT-07` (§4: restaura columnas `CP-C` y `Estado actual (R2)` con nota de línea base histórica).
- **Preservación:** no altera la jerarquía normativa (DEC-06, diseño v4 §9.2, `manifest_v4.json`), no añade octavo artefacto, conserva intactos los requisitos y `CP-C` de ART-01/02/03/05/06/07 conforme a R2.

### 3.3 `docs/r13_oracle_artifacts_materialization_plan_r4.md` (N-03)

- **Alcance:** corrige `AUD-ANT-03` (§2 mantiene dependencias originales `01, 03` para ART-04 sin añadir ART-02 ni octavo artefacto) y `AUD-ANT-07` (§1 declara con exactitud el alcance real respecto de R2: modifica G5 en §8, roles en §7, decisiones pendientes en §10 y estado en §11, conservando §1–§6, §9 y G0–G4 y G6; §4 actualiza referencias de G0–G2 conservando la línea base R2).
- **Preservación:** mantiene la regla crítica de G5 (§4.1: el dictamen IA nunca cierra G5 automáticamente), la separación estricta de G6 (§4.2 con las cinco condiciones de R2 §8), las ocho verificaciones de R2 §5.1 (§5) y el bloqueo de Fase C.
- **Observación (`LOW`, `AUD-ANT-NEW-02`):** la tabla de §4 (G0 y G1) cita `(línea base: R2 aprobada en A-03)` y `(línea base: R2 en A-04)`. Los códigos cortos `A-03` y `A-04` no están definidos en Plan R4 ni en Plan R2 (provienen de tablas de inventario externas), en lugar de citar explícitamente `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` y `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` (o Plan R2 §1.2). Asimismo, `cotejado con R9/R4` en G1 abrevia `Especificación R4` como `R4`.

### 3.4 `docs/r13_oracle_artifacts_materialization_authorization_r4.md` (N-04)

- **Alcance:** corrige `AUD-ANT-02` (§3 elimina la condición 6 de R3 «protocolo R2 operativo», ausente en `DEC-OWNER-AI-02`, distinguiendo condiciones de entrada en vigor vs. prerrequisito operativo del Protocolo R3 §3), `AUD-ANT-03` (§4 retira la asignación `HUMAN_INDEPENDENT_REVIEW` a `ORACLE-ART-01`, alineándola con D3-R4 y con el hecho de que ORACLE-ART-04 es el registro de revisión de ART-01) y `AUD-ANT-04` (§2 añade Nota de versión explicando que las referencias literales a R3 en el texto aprobado de `DEC-OWNER-AI-02` se entienden referidas a D3-R4, Especificación R4 y Plan R4 tras su auditoría y aprobación, sin modificar la decisión).
- **Preservación:** mantiene R2 (`GRANTED`) y R3 íntegros, mantiene estado `PREPARED_NOT_EFFECTIVE`, prohíbe aprobaciones implícitas y preserva todos los límites de `DEC-OWNER-AI-06` (`NOT_GRANTED` para Fase C, D–G y S2, protección de Parquet, sin commits ni push).

### 3.5 `docs/r13_oracle_art_04_ai_independent_review_protocol_r3.md` (N-05)

- **Alcance:** corrige `AUD-ANT-02` (§3 distingue aprobación del protocolo como prerrequisito operativo de ejecución vs. entrada en vigor de Autorización R4), `AUD-ANT-03` (§13 Etapa D excluye que ART-04 se compare contra sí mismo y precisa ART-05/06/07 como alcance auxiliar de correspondencia, no como dependencia de ART-04), `AUD-ANT-04` (§5 y §14 sustituyen `§5.01`, `§5.02`, `§6.1` y `§13` por encabezados y secciones reales existentes), `AUD-ANT-05` (§9.6 incorpora literalmente los 24 `rule_id` [13 usados + 11 exclusión] y los 15 campos mínimos de R1 §9 en orden y significado) y `AUD-ANT-06` (§5 sustituye las 8 etiquetas `RESUELTO` por `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`; §7–§8 armonizan severidades, dictámenes y consecuencias).
- **Observaciones (`LOW`, `AUD-ANT-NEW-03`; `INFO`, `AUD-ANT-NEW-04`):**
  - `AUD-ANT-NEW-03` (`LOW`): en §7 se indica `INCONCLUSIVE para la revisión completa cuando una conclusión dependa de la identidad del modelo`, mientras §8.1 y Especificación R4 §3.5 listan `versión [del modelo] no disponible` de forma incondicional bajo `INCONCLUSIVE` y §8.2 clasifica toda limitación de reproducibilidad al menos como `HIGH`. Aplicando §8.1/§8.2/Spec §3.5 (fail-closed), el condicional de §7 es redundante y podría inducir lectura laxa si no se interpreta subordinado a §8.1–§8.2.
  - `AUD-ANT-NEW-04` (`INFO`): en §13 Etapa D la expresión `ART-05/06/07 como alcance auxiliar de correspondencia, no como entrada ni dependencia de ART-04` quiere decir que no son entrada normativa ni dependencia de ART-04; tomada literalmente como «no como entrada» impediría inspeccionar los archivos ART-05/06/07 para verificar su correspondencia auxiliar.

---

## 4. Auditoría individual de hallazgos (AUD-ANT-02 a AUD-ANT-07)

### 4.1 AUD-ANT-02 — Circularidad entre Autorización y Protocolo

| Criterio comprobado | Evidencia verificada | Resultado |
|---|---|---|
| **Eficacia de Autorización R4** | Auth R4 §3 exige 5 condiciones (D3-R4, Spec R4, Plan R4, Auth R4 auditados y aprobación expresa del propietario en registro separado), correspondiendo exactamente a `DEC-OWNER-AI-02` | Correcto |
| **Separación entre aprobación normativa y prerrequisitos operativos** | Auth R4 §3 elimina la condición 6 («protocolo operativo»); Protocolo R3 §3 declara explícitamente que aprobar el protocolo es prerrequisito operativo para ejecutar una revisión, no condición de vigencia de Auth R4 | Correcto |
| **Consistencia entre Autorización R4 y Protocolo R3** | Auth R4 §3 ↔ Protocolo R3 §3 y §12 (`sin autorización R4 en vigor la revisión no produce efecto normativo`) ↔ Plan R4 §4.1 | Consistente |
| **Ausencia de circularidad** | Grafo acíclico verificado: `DEC-OWNER-AI-01..06` → correcciones R4/R3 → auditoría → aprobación expresa del propietario → vigencia de Auth R4 + vigencia de Protocolo R3 → ejecución de revisión → ART-04 | Sin circularidad |

### 4.2 AUD-ANT-03 — Dependencias de ART-04, Etapa D y asignación de ART-01

| Criterio comprobado | Evidencia verificada | Resultado |
|---|---|---|
| **Dependencias de ART-04** | Spec R4 §3.1, §3.6, §4 y Plan R4 §2 declaran exclusivamente `ORACLE-ART-01, ORACLE-ART-03` (idéntico a Spec R2 §4.4/§5 y Plan R2 §2/§4) | Correcto |
| **Separación dependencias vs. alcance de verificación** | Spec R4 §3.1 y §3.6 distinguen explícitamente que `ART-02` se verifica dentro del **alcance** contra reconstrucción independiente (§9.2/R9 §5.4/schema), no como dependencia formal de ART-04 | Correcto |
| **Etapa D** | Protocolo R3 §13 Etapa D compara contra ART-01/ART-02/ART-03 y fuentes normativas; ART-05/06/07 como alcance auxiliar de correspondencia (sin ser dependencia de ART-04); ART-04 **no se compara contra sí mismo** (redacción menor en `AUD-ANT-NEW-04`) | Correcto (con nota `INFO`) |
| **Asignación de revisión humana** | Auth R4 §4 retira `HUMAN_INDEPENDENT_REVIEW` de `ORACLE-ART-01` (contradicción de Auth R3 §4) y la remite a D3-R4 registrada en `ORACLE-ART-04`, sin ampliar alcance a otros artefactos | Correcto |
| **Responsabilidades de los siete artefactos** | Spec R4 §2/§4 y Plan R4 §2 conservan intactos los 7 artefactos, sus requisitos, criterios de aceptación, `CP-C` y dependencias originales | Correcto |

### 4.3 AUD-ANT-04 — Validez de referencias internas

| Documento / referencia citada | Destino comprobado | ¿Existe y corresponde? | Resultado |
|---|---|---|---|
| Resolución R4 §4 y §5 → `Especificación R4 §3` | `r13_oracle_artifacts_specification_r4.md` `## 3. ORACLE-ART-04-R4` (§3.1–§3.8) | Sí | Válido |
| Resolución R4 §5 → `Plan R4 §4` | `r13_oracle_artifacts_materialization_plan_r4.md` `## 4. Puertas de control` | Sí | Válido |
| Resolución R4 §5 → `Autorización R4 §3` | `r13_oracle_artifacts_materialization_authorization_r4.md` `## 3` (vigencia; modalidad/alcance en §§2, 4) | Existe (imprecisión menor `AUD-ANT-NEW-01`) | Válido con nota `LOW` |
| Protocolo R3 §5 y §14 → `§3`, `§5 (AUD-AI-REV-R1-02)`, `§6`, `§7`, `§8`, `§9`, `§10`, `§11`, `§12` | Encabezados reales de `protocol_r3.md` (desaparecen `§5.01`, `§5.02`, `§6.1`, `§13`) | Sí | Válido |
| Protocolo R3 §5 y §14 → `Resolución R4 §3.1` | `decision_resolution_r4.md` `### 3.1 Antecedentes y superación documentada` | Sí | Válido |
| Protocolo R3 §14 → Matriz completa `DEC-OWNER-AI-01..06` y `AUD-AI-REV-R1-01..08` | Todas las cláusulas citadas en Resolución R4, Spec R4, Plan R4, Auth R4 y Protocolo R3 | Sí, todas existen y corresponden | Válido |
| Plan R4 §4 G0/G1 → `A-03`, `A-04` | Códigos externos no definidos dentro de Plan R4 | Referencia abreviada no definida (`AUD-ANT-NEW-02`) | Observación `LOW` |

### 4.4 AUD-ANT-05 — Preservación de 24 `rule_id` y 15 campos de R1

Verificación directa contra `docs/aud04b_model_provenance_v4_design.md` §9.2 (24 filas de la tabla Allowlist propuesta), `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` (139 entradas, 13 `rule_id` distintos) y `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` §9:

| Elemento comprobado | Fuente normativa / R1 | Verificación en R4 / Protocolo R3 | Resultado |
|---|---|---|---|
| **13 `rule_id` usados** | `R9-9.2-01`, `03`, `05`, `07`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `19`, `20` (verificados en `ORACLE-ART-01.json` y filas de inclusión de §9.2) | Exactos en Protocolo R3 §9.6; conteo `13 en allowlist` en Spec R4 §3.3 | Exacto |
| **11 `rule_id` de exclusión** | `R9-9.2-02`, `04`, `06`, `08`, `16`, `17`, `18`, `21`, `22`, `23`, `24` (filas `Excluir` de §9.2) | Exactos en Protocolo R3 §9.6; conteo `11 de exclusión` en Spec R4 §3.3 | Exacto |
| **24 `rule_id` totales** | Unión disjunta completa `R9-9.2-01…24` (24 filas de §9.2) | Exactos en Protocolo R3 §9.6 y Spec R4 §3.3 | Exacto |
| **15 campos mínimos de registro** | R1 §9 ítems 1–15 + regla `NO_DISPONIBLE` | Protocolo R3 §9.6 conserva los 15 campos en idéntico orden y significado, sin omisiones ni cambios semánticos | Exacto |
| **Trazabilidad hacia R1** | R1 §§6, 7, 8, 9, 10, 11 | Conservada íntegramente en Protocolo R3 §§8, 9, 10, 12, 13 y Spec R4 §3.3–§3.5 | Correcto |

### 4.5 AUD-ANT-06 — Estado de hallazgos, severidades y dictámenes

| Criterio comprobado | Evidencia verificada | Resultado |
|---|---|---|
| **Uso de `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`** | Presente en encabezado de los 5 documentos candidatos, en las 8 filas de Protocolo R3 §5 y en estados de R4 | Correcto |
| **Ausencia de declaraciones prematuras de resolución** | Eliminadas las 8 etiquetas `RESUELTO` de Protocolo R2 §5; los 5 documentos prohíben declarar cerrados hallazgos o aprobada la modalidad | Correcto |
| **Armonización de severidades** | Spec R4 §3.5 y Protocolo R3 §8.2 coinciden: `BLOCKER`/`HIGH` bloquean; `MEDIUM` requiere resolución documentada; `LOW`/`INFO` se registran y son trazables sin bloquear; toda limitación de independencia/reproducibilidad ≥ `HIGH` | Correcto |
| **Tratamiento de versiones no disponibles** | Spec R4 §3.5 y Protocolo R3 §8.1 incluyen versión del modelo no disponible bajo `INCONCLUSIVE`; §7 corrige «para lo que dependa de él» a `INCONCLUSIVE para la revisión completa…`, con tensión residual menor ya anotada en `AUD-ANT-NEW-03` | Correcto con nota `LOW` |
| **Consistencia de los cuatro dictámenes permitidos** | `ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED`, `INCONCLUSIVE` armonizados en Spec R4 §3.5, Protocolo R3 §8.1, Plan R4 §4/§4.1 y `DEC-OWNER-AI-05` | Correcto |

### 4.6 AUD-ANT-07 — Restauración de columnas, alcance real del plan e historial R2

| Criterio comprobado | Evidencia verificada | Resultado |
|---|---|---|
| **Columnas `CP-C` y `Estado actual`** | Restauradas en Spec R4 §4 (`CP-C` idénticos a R2 §5: `05, 13`, `05, 08`, `05, 07, 13`, `05, 08, 13`; columna `Estado actual (R2)` con nota explícita de línea base histórica) | Correcto |
| **Alcance real de modificaciones del plan** | Plan R4 §1 declara explícitamente las modificaciones reales respecto de R2 (G5 §8, roles §7, decisiones §10 y estado §11) y precisa que §1–§6, §9 y G0–G4/G6 conservan su contenido actualizando solo referencias documentales | Correcto |
| **Referencias G0–G2** | Plan R4 §4 G0–G2 actualizadas a Spec R4/Plan R4 conservando línea base R2 (salvo abreviaturas `A-03`/`A-04` anotadas en `AUD-ANT-NEW-02`) | Correcto con nota `LOW` |
| **Conservación del historial R2 (y R3)** | Verificados SHA-256 y Git blob de todas las versiones R2 y R3: intactos al bit | Correcto |

---

## 5. Matriz de trazabilidad normativa

| Fuente / decisión / hallazgo | Cobertura verificada en R4 / Protocolo R3 | Trazabilidad |
|---|---|---|
| `DEC-OWNER-AI-01` (modalidad solo ART-04; humana preferente) | Res. R4 §3.2; Spec R4 §3.1–§3.2; Plan R4 §4 (G5); Auth R4 §2.1/§4; Prot. R3 §4 | Completa |
| `DEC-OWNER-AI-02` (Auth versionada sin condición espuria) | Auth R4 §§1–3; Prot. R3 §§3, 12 | Completa |
| `DEC-OWNER-AI-03` (superación acotada de Análisis R1 §8.1/§6.1 P1) | Res. R4 §3.1; Prot. R3 §5 (`AUD-AI-REV-R1-02`) | Completa |
| `DEC-OWNER-AI-04` (9 controles; no demostrable ⇒ `INCONCLUSIVE`) | Res. R4 §3.4–§3.5; Spec R4 §3.4/§3.7; Prot. R3 §§6, 10 | Completa |
| `DEC-OWNER-AI-05` (4 dictámenes, severidades, autoridad del propietario) | Res. R4 §3.4; Spec R4 §3.5; Prot. R3 §8; Plan R4 §4.1 | Completa |
| `DEC-OWNER-AI-06` (límites: sin Fase C, D–G/S2, Parquet ni commits) | Auth R4 §5; Plan R4 §4.2/§6; Prot. R3 §§12, 16 | Completa |
| `D1`, `D2`, `D4`, `D5`, `D6` (R2 aprobadas) | Res. R4 §2; Spec R4 §3.3/§4; Plan R4 §§2, 6; Prot. R3 §9.6 | Completa |
| `AUD-ANT-02` … `AUD-ANT-07` | Verificada correspondencia individual en §4 de este informe | Completa |

---

## 6. Evaluación separada de AUD-ANT-01 (independencia)

1. **Separación de planos:** la evaluación de `AUD-ANT-01` es independiente de la calidad técnica de las correcciones R4 (`AUD-ANT-02…07`). Un texto normativo internamente coherente no demuestra independencia del auditor ni del proceso de generación.
2. **Regla de no presunción:** no se presupone que `Gemini 4 Hydrogen (High)` y `Hy4 Flash Free` pertenezcan al mismo proveedor, ni se presupone que pertenezcan a proveedores distintos.
3. **Hecho verificable:** el proveedor real subyacente de `Hy4 Flash Free` utilizado en OpenCode para generar las propuestas originales y R4 no está acreditado con evidencia verificable. Asimismo, esta sesión de auditoría carece de versión de compilación verificable y parámetros de muestreo expuestos (`NO_DISPONIBLE`).
4. **Aplicación de `DEC-OWNER-AI-04`:** «El mismo proveedor o una limitación no demostrable obliga a `INCONCLUSIVE`».
5. **Estado resultante de `AUD-ANT-01`:** **`INCONCLUSIVE` (abierto, severidad `HIGH` conforme a Protocolo R3 §8.2)**. Este auditor no puede cerrar `AUD-ANT-01`.

---

## 7. Matriz de regresiones y consistencia global

| Elemento comprobado | Resultado | Evidencia |
|---|---|---|
| **D1–D6 preservadas** | SIN REGRESIÓN | Res. R4 §2 conserva D1, D2, D4, D5, D6 de R2; §3 conserva D3-R4 acotada |
| **Jerarquía normativa** | SIN REGRESIÓN | DEC-06 / diseño v4 §9.2 / `manifest_v4.json` arriba; IA nunca es fuente normativa (Spec R4 §2; Prot. R3 §§3, 11, 12) |
| **Requisitos de los siete artefactos** | SIN REGRESIÓN | Spec R4 §§2, 4 y Plan R4 §2 mantienen 7 artefactos y criterios de ART-01/02/03/05/06/07 |
| **Nueve metadatos exactos** | SIN REGRESIÓN | Prot. R3 §9.1 enumera los 9 campos exactos de R9 §5.1 manteniendo `rule_id` separado |
| **139 rutas normativas** | SIN REGRESIÓN | Spec R4 §3.3/§3.4, Prot. R3 §§9.1/9.6/10 y Plan R4 §5 mantienen las 139 rutas |
| **Separación de roles (4 roles)** | SIN REGRESIÓN | Generador, IA revisora, auditor posterior (evaluación a ciegas) y propietario distintos en los 5 docs |
| **Independencia y reproducibilidad** | SIN REGRESIÓN NORMATIVA (limitación operativa `AUD-ANT-01` abierta) | Prot. R3 §§6–7, Spec R4 §3.4/§3.7 incorporan los 9 controles de `DEC-OWNER-AI-04` |
| **Autoridad exclusiva del propietario** | SIN REGRESIÓN | Aprobación expresa separada exigida en Auth R4 §3, Plan R4 §4, Res. R4 §3.5, Prot. R3 §8.3 |
| **Límites de G5 y G6** | SIN REGRESIÓN | Plan R4 §§4, 4.1, 4.2 conservan G5 no autocerrable por IA y las 5 condiciones separadas de G6 |
| **Ausencia de autorización de Fase C** | SIN REGRESIÓN | `PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED` y `D–G/S2: NOT_GRANTED` en todo el paquete |
| **Protección de Parquet y alcance de solo lectura** | SIN REGRESIÓN | Auth R4 §5 y Prot. R3 §16 prohíben tocar producción, tests, schemas, dependencias y Parquet |

---

## 8. Hallazgos de esta auditoría

| ID | Severidad | Ámbito | Descripción | Impacto en dictamen |
|---|---|---|---|---|
| **AUD-ANT-01 (persistente)** | **`HIGH`** | Independencia / reproducibilidad | El proveedor real de `Hy4 Flash Free` (OpenCode) sigue sin estar acreditado; además, en el entorno auditor la versión exacta de compilación y los parámetros de muestreo figuran como `NO_DISPONIBLE`. | Obliga a **`INCONCLUSIVE`** por `DEC-OWNER-AI-04` y Protocolo R3 §§6, 7, 8.1, 8.2 |
| **AUD-ANT-NEW-01** | `LOW` | Resolución R4 §4 vs. §5 | La tabla §4 resume `Después (R4 §5)` con texto que no coincide literalmente con la redacción de §5, y §5 remite a `Autorización R4 §3` al referirse a modalidad y alcance (tratados en §§2 y 4). | No bloqueante; mejora de precisión editorial |
| **AUD-ANT-NEW-02** | `LOW` | Plan R4 §4 (G0, G1) | G0 y G1 citan los códigos `A-03` y `A-04` sin definirlos en el documento (en lugar de las rutas de los registros de aprobación R1 o Plan R2 §1.2), y `R9/R4` abrevia `Especificación R4`. | No bloqueante; mejora de autocontención documental |
| **AUD-ANT-NEW-03** | `LOW` | Protocolo R3 §7 vs. §8.1–§8.2 | §7 condiciona `INCONCLUSIVE` por versión no disponible a «cuando una conclusión dependa de la identidad del modelo», mientras §8.1/§8.2 y Spec R4 §3.5 lo establecen de forma incondicional. | No bloqueante; subordinar §7 explícitamente a §§8.1–8.2 |
| **AUD-ANT-NEW-04** | `INFO` | Protocolo R3 §13 Etapa D | La frase «ART-05/06/07… no como entrada ni dependencia de ART-04» significa no como entrada normativa ni dependencia; conviene precisar que sí se inspeccionan como objetos de correspondencia auxiliar cuando existan. | Informativo |

---

## 9. Dictamen y distinción de planos

1. **Evaluación técnica de correcciones normativas (AUD-ANT-02…07 y regresiones):** las cinco propuestas R4/R3 resuelven correctamente en el plano documental y semántico los hallazgos `AUD-ANT-02` a `AUD-ANT-07`, preservan las decisiones `D1–D6`, los siete artefactos, los nueve metadatos, las 139 rutas, los 24 `rule_id`, los 15 campos de R1, la jerarquía normativa y los límites de G5, G6, Fase C y Parquet, con únicamente tres observaciones `LOW` y una `INFO` (sin `BLOCKER` ni `HIGH` en el texto normativo).
2. **Dictamen formal de auditoría independiente:** **`INCONCLUSIVE`**.
   - **Motivo exclusivo del dictamen `INCONCLUSIVE`:** la imposibilidad de demostrar independencia de proveedor respecto del generador original (`AUD-ANT-01`, `HIGH`) y la indisponibilidad de versión de compilación/parámetros de muestreo (`NO_DISPONIBLE`), en aplicación estricta de `DEC-OWNER-AI-04`, Protocolo R3 §§6–8 y la Sección 1 del mandato de auditoría.
3. **Distinción obligatoria entre planos:**
   - **Aceptación técnica:** no puede emitirse `ACCEPTED` ni `ACCEPTED_WITH_FINDINGS` mientras `AUD-ANT-01` (`HIGH`) permanezca abierto.
   - **Cierre de hallazgos:** este informe **no** declara cerrados `AUD-ANT-02` a `AUD-ANT-07` ni `AUD-ANT-01`; el cierre formal requiere auditoría con independencia acreditada (o decisión expresa del propietario) y registro posterior.
   - **Aprobación del propietario:** las propuestas R4/R3 siguen **no aprobadas** y **no en vigor**; toda entrada en vigor requiere acto expreso del propietario en registro separado, y bajo un dictamen `INCONCLUSIVE` no puede desbloquearse G5 ni activarse la revisión IA sin resolver primero el requisito de independencia acreditada.

---

## 10. Limitaciones y estados conservados

- Auditoría ejecutada en estricto modo de solo lectura; único archivo creado: este informe (`docs/r13_oracle_artifacts_r4_independent_audit_r1.md`).
- No se modificaron R4, R3, R2, R1, fuentes normativas, `ORACLE-ART-*`, código de producción, tests, schemas, dependencias ni Parquet; no se ejecutaron G5 ni G6; no se realizaron commits ni push.

```text
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
AUD_ANT_01_STATUS: INCONCLUSIVE
```

**Fin de R13-ORACLE-ARTIFACTS-R4-INDEPENDENT-AUDIT-R1.**
