# RECONSTRUCCION NORMATIVA INDEPENDIENTE — ORACLE-ART-04 (R13)
## Auditoria externa independiente — Tratamiento hashable previo a comparacion de candidatas

**Proyecto:** `TradingAI_BTC`.
**Auditor:** Kilo Code (modelo kilo-auto/free, proveedor kilo).
**Fecha y hora de creacion:** 2026-11-27T22:58:28Z.
**Sesion:** sesion de auditoria externa independiente (sin historial compartido con el generador).
**Origen de requisitos:** fuentes originales S-01..S-10 y aprobaciones A-01..A-04 del manifiesto de transferencia `docs/r13_oracle_art_04_external_review_handoff_r1.md`. Adicionalmente, DEC-06 se extrae del registro de decisiones normativas `docs/aud04b_model_provenance_v4_approval_r1.md`, citado como autoridad normativa en S-01 §2 y S-03 §2 (no es informe de auditoria).

**Regla de orden:** este documento se genera ANTES de abrir o comparar cualquiera de las cinco propuestas candidatas C-01..C-05. No se utiliza contenido de las candidatas para reconstruir sus propios requisitos.

---

## 1. Identidad del auditor y sesion limpia

| Campo | Valor |
|---|---|
| Proveedor de IA | kilo (Kilo Code) |
| Modelo y version exacta | kilo-auto/free |
| Entorno de ejecucion | Kilo Code |
| Fecha y hora de ejecucion | 2026-11-27T22:58:28Z |
| Identificador de sesion | sesion de auditoria externa independiente (no disponible como token de plataforma) |
| Parametros de generacion | temperatura/contexto/herramientas no expuestos por la plataforma; se registra como "no disponible" en el informe final |
| Herramientas y permisos utilizados | lectura de archivos, calculo de SHA-256, escritura de archivos de evidencia e informe; sin ejecucion de materializacion, sin commits, sin push |
| Generador original | OpenCode con modelo Hy4 Flash Free |
| Independencia de proveedor | kilo != OpenCode/Hy4 (proveedor distinto del generador) |
| Declaracion de independencia | No participe en la generacion de las cinco propuestas candidatas. No recibi informes ni conclusiones de auditorias anteriores. No utilice el dictamen de Nemotron 3.5 Lightning Free ni el informe `audit_report_r13_oracle_art_04.md`. Reconstruyo los requisitos unicamente desde las fuentes originales S-01..S-10 y A-01..A-04. |

---

## 2. Inventario de entradas y verificacion de integridad (SHA-256)

Todos los 19 archivos del manifiesto fueron recalculados y coinciden con el valor esperado.

### 2.1 Documentos candidatos (CANDIDATE) — 5 archivos

| ID | Ruta | SHA-256 esperado | SHA-256 calculado | Resultado |
|---|---|---|---|---|
| C-01 | `docs/r13_oracle_artifacts_decision_resolution_r3.md` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | COINCIDE |
| C-02 | `docs/r13_oracle_artifacts_specification_r3.md` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | COINCIDE |
| C-03 | `docs/r13_oracle_artifacts_materialization_plan_r3.md` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | COINCIDE |
| C-04 | `docs/r13_oracle_artifacts_materialization_authorization_r3.md` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | COINCIDE |
| C-05 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | COINCIDE |

### 2.2 Fuentes normativas originales (PRIMARY_ORIGINAL) — 10 archivos

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

### 2.3 Registros de aprobacion del propietario (OWNER_APPROVAL) — 4 archivos

| ID | Ruta | SHA-256 esperado | SHA-256 calculado | Resultado |
|---|---|---|---|---|
| A-01 | `docs/r13_owner_design_approval_r1.md` | `16cfd579db05289cca9a9140988128175136dffa1cba814b0a28f19c7b403b60` | `16cfd579db05289cca9a9140988128175136dffa1cba814b0a28f19c7b403b60` | COINCIDE |
| A-02 | `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | COINCIDE |
| A-03 | `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | COINCIDE |
| A-04 | `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | COINCIDE |

**Resultado global:** 19/19 hashes coinciden. Ningun archivo modificado. Acceso de solo lectura.

---

## 3. Reconstruccion normativa (requisitos desde fuentes originales)

### 3.1 Decisiones D1–D6 y sus aprobaciones

Fuente: S-03 §3 (matriz consolidada §4 y secuencia §4.1), A-02 (aprobacion del propietario), S-05 §8 (puertas).

| ID | Decision | Contenido aprobado (A-02 §2.1) | Estado | Autoridad requerida | Dependencia de resolucion (S-03 §4.1) |
|---|---|---|---|---|---|
| D1 | Formato estable de identificadores `rule_id` | Identificadores `rule_id` secuenciales por fila de §9.2, con tabla de correspondencia revisada | APPROVED | Propietario / autoridad designada | Antes de ORACLE-ART-01 (paso 1) |
| D2 | Ubicacion fisica de artefactos ejecutables y evidencias | Ubicacion versionada de artefactos en el repositorio; referencias externas unicamente para recursos inmutables | APPROVED | Propietario / autoridad designada | Antes de ORACLE-ART-01 y G2/G4 (paso 2) |
| D3 | Identidad del revisor humano independiente | Revisor independiente designado por funcion, con identidad funcional real y evidencia documentada de independencia | APPROVED | Propietario | Antes de ORACLE-ART-04 (paso 6) |
| D4 | Formato de las evidencias de ejecucion | Evidencias deterministas UTF-8 y JSON JCS derivado exclusivamente auxiliar, sin modificar la preimagen de ORACLE-ART-03 | APPROVED | Autoridad tecnica; propietario si amplia alcance | Antes de ORACLE-ART-05 y ORACLE-ART-06 (pasos 5 y 6) |
| D5 | Convencion de versiones de los artefactos | Correcciones no semanticas documentadas sin incrementar version; cambios semanticos sujetos a nueva version | APPROVED | Propietario | Antes de ORACLE-ART-01 (paso 3) |
| D6 | Arquitectura de ORACLE-ART-02, version ejecutable del oracle | Verificador ORACLE-ART-02 ubicado en `tests/`, sin importaciones de produccion ni dependencias nuevas, con entradas declaradas y cerradas | APPROVED | Propietario si amplia alcance; autoridad tecnica para implementar | Antes de ORACLE-ART-02 (paso 4) |

**Secuencia propuesta de resolucion (AUD-DEC-RES-R1-04, S-03 §4.1):**
1. D1 formato `rule_id` — antes de ORACLE-ART-01.
2. D2 ubicacion fisica — antes de ORACLE-ART-01 y G2/G4.
3. D5 convencion de versiones — antes de ORACLE-ART-01.
4. D6 arquitectura de ORACLE-ART-02 — antes de ORACLE-ART-02.
5. D4 formato de evidencias — antes de ORACLE-ART-05 y ORACLE-ART-06.
6. D3 identidad del revisor — antes de ORACLE-ART-04.

D1, D2 y D5 son paralelas y previas al paso 1; D6 precede al paso 2; D4 precede a pasos 5 y 6; D3 precede al paso 4. No existe circularidad. Las seis son prerrequisitos de decision, no resultados de la materializacion.

**Estados declarados (S-03 §7, S-05 §11, S-06 §6, S-07 §5):**
```
DECISION_RESOLUTION_STATUS: PROPOSAL
MATERIALIZATION_PLAN_OWNER_APPROVAL: APPROVED
ORACLE_ARTIFACT_MATERIALIZATION_AUTHORIZATION: NOT_GRANTED
ORACLE_ARTIFACTS_STATUS: NOT_CREATED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```
La aprobacion de las decisiones NO equivale a aprobacion de las cinco propuestas candidatas. La autoridad final de aceptacion permanece en el propietario.

### 3.2 Alcance y contenido de ORACLE-ART-01 a ORACLE-ART-07

Fuente: S-04 §4 (artefactos 4.1–4.7), S-05 §2 (inventario), S-01 §5.8.5 (artefactos exigibles). Todos en estado `NOT_CREATED`.

**ORACLE-ART-01 — Transcripcion normativa completa e independiente.**
- Propósito: fijar, de forma revisable, la autoridad normativa §9.2/DEC-06 como datos comparables frente a `ALLOWLIST_V4`.
- Fuente normativa: R9 §5.8.1 y §5.8.5 artefato 1; diseño v4 §9.2; DEC-06.
- Contenido minimo obligatorio: (1) 139 rutas expandidas ({partition} → train, validation, calibration, test); (2) los diez campos por entrada de R9 §5.8.1: `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`, `rule_id`; (3) cada `rule_id` referencia la fila correspondiente de §9.2 (esquema de identificacion registrado durante la generacion y sometido a revision semantica); (4) patrones P1–P5 y matriz O/A de nueve combinaciones de R9 §5.8.3; (5) invariantes I1–I12 y codigos `ALLOWLIST_*` de R9 §5.7; (6) reglas de normalizacion temporal de R9 §7 y semantica de tipos de R9 §5.2; (7) reglas de exclusion de proyeccion de R9 §5.5 y separacion admision/proyeccion de R9 §5.1 y §5.6; (8) condiciones fail-closed y codigos `ORACLE_INCOMPLETE`, `ORACLE_VERSION_MISMATCH`, `ORACLE_CHECKSUM_MISMATCH`, `ALLOWLIST_ORACLE_METADATA_DIVERGENCE`, `ALLOWLIST_MISSING_PATH`, `ALLOWLIST_EXTRA_PATH` de R9 §5.8.2; (9) separacion explicita entre texto normativo, datos derivados y material auxiliar.
- Formato y estructura: objeto con `version` y `entries`; entradas ordenadas por `path`; diez campos en orden fijo. Condiciones como literales del vocabulario de R9 §5.3, no texto libre.
- Metodo de generacion futuro: transcripcion directa desde §9.2/DEC-06, sin copiar `ALLOWLIST_V4` ni derivar del schema; expansion controlada de `{partition}`; registro de decisiones de transcripcion.
- Metodo de verificacion independiente: revision semantica fila por fila contra §9.2; comprobacion de que las 139 rutas coinciden con la allowlist normativa y de que la transcripcion no procede del codigo productivo.
- Criterios de aceptacion: completitud de diez campos por entrada; 139 rutas; coherencia con P1–P5, I1–I12 y §§5.2/5.5/5.7; separacion texto/datos/auxiliar; revision documentada.
- Condiciones de rechazo: campo ausente; ruta duplicada u omitida; `rule_id` sin referencia normativa; condicion fuera del vocabulario; texto normativo mezclado con datos derivados; transcripcion copiada del codigo productivo.
- Dependencias: ninguna para su generacion; prerrequisito de ORACLE-ART-02, -03, -04, -05, -06 y -07.
- Evidencia de reproducibilidad: conservar version exacta de §9.2/DEC-06 consultada, notas de expansion y correspondencia `rule_id` → fila normativa.
- Responsable: revisor independiente; aprobacion final del propietario como prerrequisito de autorizacion tecnica. CP-C-05, CP-C-13.

**ORACLE-ART-02 — Version ejecutable del oracle.**
- Propósito: proporcionar una implementacion independiente de la transcripcion para las verificaciones de CI/auditoria.
- Fuente de verdad: ORACLE-ART-01 y la autoridad normativa §9.2/DEC-06. No `ALLOWLIST_V4`, no el schema como sustituto de la norma, no resultados de Fase C.
- Independencia: no importa modulos productivos para obtener la transcripcion; el modulo productivo no importa este artefacto; las verificaciones se ejecutan fuera del camino productivo.
- Comportamiento exigible: determinista, reproducible, sin fallback silencioso, manejo explicito de errores con codigos deterministas (`ORACLE_INCOMPLETE`, `ORACLE_VERSION_MISMATCH`, `ORACLE_CHECKSUM_MISMATCH`), cobertura verificable de los casos normativos.
- Formato y estructura: a decidir en futura tarea autorizada; esta especificacion no impone lenguaje, biblioteca ni arquitectura.
- Dependencias: ORACLE-ART-01.
- Responsable: revisor independiente y auditor; aprobacion del propietario para cualquier decision de arquitectura que amplie alcance. CP-C-05, CP-C-13.

**ORACLE-ART-03 — SHA-256 de la transcripcion canonicalizada.**
- Propósito: fijar la integridad de la transcripcion canonicalizada y detectar cambios no revisados.
- Fuente normativa: R9 §5.8.1 «Version y checksum»; §5.8.5 artefato 3; §6.4.
- Aclaracion de objeto: el objeto sometido a hash es la transcripcion canonicalizada definida por R9 §5.8.5 artefato 3, serializada segun R9 §5.8.1. R9 NO exige un checksum adicional de la version ejecutable de ORACLE-ART-02. No se crea un octavo artefacto; el conjunto normativo permanece en siete.
- Bytes exactos sometidos a hash: serializacion JCS de `{"version": <version>, "entries": [<entradas ordenadas por path>]}` donde cada entrada usa los diez campos de R9 §5.8.1 en orden fijo.
- Codificacion: UTF-8 sin BOM. JCS no emite salto de linea final.
- Archivos auxiliares: no se incluyen en la preimagen. El propio checksum no se incluye en su preimagen.
- Procedimiento de calculo: sobre la transcripcion canonicalizada de ORACLE-ART-01, mediante RFC 8785, y posterior SHA-256 de esos bytes.
- Formato del resultado: hex minúsculo de 64 caracteres.
- Verificacion reproducible: recalcular desde ORACLE-ART-01 y comparar con el valor registrado; discrepancia → `ORACLE_CHECKSUM_MISMATCH`.
- Dependencias: ORACLE-ART-01, ORACLE-ART-02.
- Responsable: revisor independiente; el checksum no sustituye su dictamen. CP-C-05, CP-C-13.

**ORACLE-ART-04 — Registro de revision humana independiente.**
- Propósito: evidenciar que la transcripcion fue revisada semanticamente contra §9.2 por un revisor distinto del generador.
- Fuente normativa: R9 §5.8.1 «Revision humana»; §5.8.5 artefato 4.
- Contenido minimo: identidad funcional del revisor (rol, no nombre inventado); declaracion de independencia respecto de la implementacion; version revisada; checksum revisado; alcance de la revision; casos examinados; hallazgos; resolucion de hallazgos; dictamen; fecha real de la revision; evidencia de aprobacion.
- Formato: registro documental estructurado, con secciones para alcance, hallazgos, resolucion y dictamen.
- Metodo de generacion futuro: revision efectiva realizada por persona funcionalmente independiente, posterior a ORACLE-ART-01/03.
- Metodo de verificacion independiente: auditoria del registro, comprobando que los casos examinados cubren las 139 rutas, los nueve metadatos y la mutacion; que los hallazgos tienen resolucion; y que la fecha y el dictamen son reales.
- Criterios de aceptacion: revision realizada y documentada; independencia declarada; version y checksum coincidentes con los artefactos revisados; hallazgos resueltos; dictamen favorable.
- Condiciones de rechazo: registro vacio o plantilla sin revision; revisor que es el unico generador; ausencia de hallazgos examinados; fecha o dictamen no verificables; checksum distinto del artefacto revisado.
- Dependencias: ORACLE-ART-01, ORACLE-ART-03.
- Responsable: revisor independiente; aprobacion del propietario como prerrequisito de autorizacion tecnica. CP-C-05, CP-C-13.

**ORACLE-ART-05 — Evidencia de cobertura de las 139 rutas.**
- Propósito: demostrar que cada ruta normativa fue comparada semanticamente, no solo contada.
- Fuente normativa: R9 §5.4 (allowlist), §5.8.2 pasos 2–3, §5.8.5 artefato 5.
- Estructura de la matriz: una fila por cada una de las 139 rutas expandidas, con columnas: ruta normativa; condicion de aplicabilidad; comportamiento esperado; resultado observado (a registrar en futura ejecucion); caso positivo/negativo; evidencia reproducible; correspondencia con el oracle (`rule_id` y metadatos de ORACLE-ART-01).
- Criterios de aceptacion: 139 filas unicas; cada fila con resultado observado y caso asociado; compartimentos train/validation/calibration/test correctamente expandidos; coincidencia con la tabla §5.4.
- Dependencias: ORACLE-ART-01, ORACLE-ART-02. CP-C-05, CP-C-08.

**ORACLE-ART-06 — Evidencia de comprobacion de los nueve metadatos.**
- Propósito: demostrar que `ALLOWLIST_V4` coincide con el oracle en los nueve campos de `AllowlistEntry`.
- Fuente normativa: R9 §5.1 (estructura), §5.8.1 (diez campos del oracle), §5.8.2 paso 4, §5.8.5 artefato 6.
- Los nueve metadatos exactos (de R9 §5.1, no reconstruidos de memoria): 1 `path`; 2 `type`; 3 `manifest_required`; 4 `manifest_required_when`; 5 `manifest_allowed_when`; 6 `projection_include_when`; 7 `projection_optional`; 8 `nullable`; 9 `normalization`. El décimo campo del oracle, `rule_id`, se usa para trazabilidad normativa, NO forma parte de los nueve metadatos comparados.
- Estructura de la evidencia: una fila por ruta comun y por campo, con valor del oracle, valor de `ALLOWLIST_V4`, resultado de la comparacion y codigo de error si hay divergencia (`ALLOWLIST_ORACLE_METADATA_DIVERGENCE`).
- Casos minimos: al menos los casos de `base_*` (`external_run_only`), `shared_with` (P2), un campo con `nullable=True`, un timestamp con `timestamp_utc_9` y un `string_decimal`.
- Dependencias: ORACLE-ART-01, ORACLE-ART-02, ORACLE-ART-05. CP-C-05, CP-C-07, CP-C-13.

**ORACLE-ART-07 — Evidencia de la mutacion `external_run_only`.**
- Propósito: demostrar que el oracle detecta una alteracion de la condicion normativa `external_run_only`, aunque el schema no la codifica.
- Fuente normativa: R9 §5.8.2 «Deteccion de external_run_only»; §5.8.5 artefato 7; diseno v4 §9.2.
- Estado original: las tres rutas `calibration.base_model_id`, `calibration.base_artifact_sha256.rf` y `calibration.base_artifact_sha256.xgb` declaran `projection_include_when=external_run_only` en `ALLOWLIST_V4` y en el oracle.
- Mutacion exacta: en una copia aislada de `ALLOWLIST_V4`, cambiar `external_run_only` por `always` en esas tres rutas, manteniendo los demas metadatos sin cambios.
- Resultado esperado antes de la mutacion: la comparacion no reporta divergencia de `projection_include_when`.
- Resultado esperado despues de la mutacion: la comparacion contra el oracle reporta `ALLOWLIST_ORACLE_METADATA_DIVERGENCE` con campo `projection_include_when` para las tres rutas.
- Dependencias: ORACLE-ART-01, ORACLE-ART-02, ORACLE-ART-06. CP-C-05, CP-C-08, CP-C-13.

**Matriz consolidada de aceptacion (S-04 §5):** todos los siete artefactos en estado `NOT_CREATED`; ninguno marcado `VERIFIED`. La transicion entre estados solo puede producirse con evidencia material.

### 3.3 Jerarquia normativa entre DEC-06, diseno v4 §9.2 y manifest_v4.json

Fuente: S-04 §2 (Fuentes y jerarquia normativa), S-01 §5.8 (Fuente normativa unica, oracle y verificaciones de consistencia), Aprobacion de decisiones normativas (DEC-06).

| Nivel | Fuente | Uso |
|---|---|---|
| 1 (autoridad normativa) | DEC-06 y diseno v4 §9.2 | Autoridad normativa para rutas, exclusiones y condiciones (`external_run_only`, `shared_with`, timestamps normalizados) |
| 2 (contrato estructural canónico) | `src/tradingai/schemas/manifest_v4.json` | Contrato estructural canónico: `required`, nulabilidad, tipos, `$defs/partition` y `$defs/calibration_partition` |
| 3 (representacion ejecutable aprobada) | `ALLOWLIST_V4` en `provenance_v4.py` | Representacion ejecutable aprobada; unico listado que usara el codigo productivo |
| 4 (transcripcion independiente) | `ORACLE_NORMATIVE_V4_R5` | Transcripcion independiente de §9.2, usada solo en CI/auditoria |
| 5 (validaciones productivas) | Implementacion aceptada de Fase A/B (`validate_manifest_v4` y rutinas auxiliares) | Contrato de validaciones productivas ya aprobadas; no se altera |

**DEC-06 (APPROVED, registro de decisiones normativas):** `run_fingerprint` se calcula sobre la allowlist normativa de §9.2. La preimagen conserva presencia frente a null, incluye configuracion efectiva y excluye identificadores de salida, timestamps, artefactos, metricas y hashes derivados. Se canonicaliza con JCS y se hashea con SHA-256.

**Jerarquia clave:** el oracle (`ORACLE_NORMATIVE_V4_R5` / ORACLE-ART-01) se transcribe DIRECTAMENTE de §9.2/DEC-06, NO de `ALLOWLIST_V4` ni del schema. Es una herramienta de verificación de CI/auditoria; nunca es una allowlist de produccion. El modulo productivo no importa la transcripcion desde tests. La jerarquía original permanece intacta.

### 3.4 Condiciones originales de G0–G6

Fuente: S-05 §8 (Puertas de control), S-05 §8 G6 precision (AUD-MAT-PLAN-R1-01).

| Puerta | Criterios de entrada | Criterios de salida | Rechazo |
|---|---|---|---|
| G0 Especificacion aprobada | R2 aprobada y auditada `ACCEPTED` | Registro de aprobacion vigente | Hash R2 divergente o auditoria no favorable |
| G1 Plan revisado | Plan documental completo y cotejado con R9/R2 | Revision documental sin contradicciones | Convertir decisiones pendientes en aprobadas |
| G2 Fuentes y herramientas verificadas | §9.2, schema y R2 disponibles; decisiones críticas registradas | Procedencia documentada | Fuente modificada o decision crítica sin resolver |
| G3 Autorizacion de materializacion | Decision expresa del propietario | Autorizacion registrada | Cualquier aprobacion anterior interpretada como autorizacion |
| G4 Artefactos generados | G3 concedido | 01–07 generados con sus estados | Artefacto incompleto o no reproducible |
| G5 Verificacion independiente | G4 completo; revision humana realizada | Evidencia de verificacion y dictamen | Discrepancia no resuelta; revision no independiente |
| G6 Resolucion de AUD-R8-02 | G5 favorable; siete artefactos materializados y estados verificados; informe de auditoria independiente favorable; sin hallazgos bloqueantes; aceptacion expresa del propietario | Cierre documentado de AUD-R8-02 con evidencia trazable de los cinco requisitos | Artefacto ausente o no verificado; informe desfavorable; hallazgo bloqueante sin resolver; falta de aceptacion expresa del propietario; evidencia incompleta |

La aprobacion de G0 NO implica aprobar G1–G6. G3 es obligatoria antes de cualquier generacion.

### 3.5 Las ocho condiciones conjuntas de G5

Fuente: S-09 §6 (Alcance tecnico obligatorio de la revision por IA), que define lo que la verificacion independiente de G5 debe cubrir. Ocho condiciones de cobertura:

1. Las 139 rutas normativas expandidas.
2. Los 24 `rule_id` normativos, con la distinción entre 13 utilizados por la allowlist y 11 reglas de exclusión.
3. Los nueve metadatos (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`) y su separacion de `rule_id`.
4. Tipos, condiciones (`always`, `external_run_only`, `partition == 'calibration'`), nulabilidad y normalizacion.
5. Correspondencia con R9 §5.4, diseno v4 §9.2 y `manifest_v4.json`.
6. Integridad JCS y SHA-256 de ORACLE-ART-03.
7. Correspondencia de ORACLE-ART-05, ORACLE-ART-06 y ORACLE-ART-07 con las reglas originales.
8. Deteccion de omisiones, duplicados, divergencias y contradicciones normativas.

Reglas de G5 (S-05 §8, S-09 §8): `INCONCLUSIVE` y `REJECTED` no desbloquean G5. `ACCEPTED_WITH_FINDINGS` no desbloquea G5 con hallazgos BLOCKER/HIGH sin resolver. Solo `ACCEPTED` — y, si el propietario lo admite expresamente, `ACCEPTED_WITH_FINDINGS` con resolucion verificada — podría sustentar una revision, siempre despues de la auditoria separada de S-09 §11. G5 conserva sus requisitos propios y no se ejecuta automaticamente.

### 3.6 Las cinco condiciones conjuntas de G6

Fuente: S-05 §8 G6 (AUD-MAT-PLAN-R1-01). G5 favorable NO equivale a superar G6. Solo puede considerarse superada cuando concurran conjuntamente:

1. Los siete artefactos requeridos estan materializados y sus estados individuales verificados.
2. Existe un informe de auditoria independiente favorable que verifica los criterios correspondientes a AUD-R8-02.
3. No quedan hallazgos bloqueantes sin resolver.
4. El propietario ha emitido aceptacion expresa del resultado de la auditoria, independiente de la aceptacion tecnica del auditor.
5. Existe evidencia documental trazable de cada requisito anterior.

La superacion de G6 NO autoriza por si misma la implementacion de Fase C: esa autorizacion continua siendo una decision separada y explicita.

### 3.7 Requisitos originales de revision humana para ORACLE-ART-04

Fuente: S-04 §4.4 (ORACLE-ART-04), D3 (S-03 §3.3), R9 §5.8.1.

- Revision semantica real por revisor distinto del generador.
- Designacion de identidad funcional por el propietario y registro de la identidad real al ejecutar la revision.
- Declaracion de independencia, version y checksum revisados, casos, hallazgos resueltos, dictamen y fecha reales.
- Fail-closed: sin independencia declarada, ORACLE-ART-04 se rechaza.
- El checksum NO sustituye la revision humana (R9 §5.8.1).
- Contenido minimo del registro: identidad funcional del revisor (rol, no nombre inventado); declaracion de independencia respecto de la implementacion; version revisada; checksum revisado; alcance de la revision; casos examinados; hallazgos; resolucion de hallazgos; dictamen; fecha real de la revision; evidencia de aprobacion.
- Criterios de aceptacion: revision realizada y documentada; independencia declarada; version y checksum coincidentes con los artefactos revisados; hallazgos resueltos; dictamen favorable.
- Condiciones de rechazo: registro vacio o plantilla sin revision; revisor que es el unico generador; ausencia de hallazgos examinados; fecha o dictamen no verificables; checksum distinto del artefacto revisado.

**Nota sobre INDEPENDENT_AI_REVIEW:** S-09 §3 (D3) establece que D3 habla de "persona funcionalmente independiente"; la modalidad automatizada propuesta es una desviacion que requiere decision expresa del propietario. S-09 §12 (Compatibilidad normativa y cambios necesarios) marca D3 como "Incompatible tal como esta redactada" para `INDEPENDENT_AI_REVIEW` y requiere una nueva decision del propietario que admita expresamente revisor automatizado, o enmienda controlada de D3 con version nueva. DEC-OWNER-AI-01 a DEC-OWNER-AI-06 (S-07) fueron aprobadas por el propietario (S-08), admitiendo `INDEPENDENT_AI_REVIEW` exclusivamente para ORACLE-ART-04 bajo controles.

### 3.8 Condiciones de independencia, trazabilidad y reproducibilidad

Fuente: S-09 §5 (Controles de independencia), S-09 §7 (Campos minimos del registro de evidencia), S-09 §9 (Revision posterior obligatoria), DEC-OWNER-AI-04 (S-07 §4).

**Independencia (DEC-OWNER-AI-04, 9 condiciones):**
1. Proveedor y modelo distintos del generador, con declaracion de linaje.
2. Sesion limpia sin historial previo.
3. Fuentes normativas originales, sin resumenes derivados del generador.
4. Ausencia de dictamenes o conclusiones previas en el contexto inicial.
5. Prompt íntegro y hashes de todos los archivos de entrada conservados.
6. Linaje y contexto registrados, con inventario de herramientas y parametros.
7. Reconstruccion independiente de las reglas, en artefacto hashable anterior a la comparacion.
8. Auditor posterior distinto de la IA revisora y del generador, con evaluacion a ciegas.
9. Limitaciones de independencia expresamente declaradas.

Consecuencias: el mismo proveedor o una limitacion no demostrable obliga a `INCONCLUSIVE`. Dos ejecuciones del mismo modelo NO constituyen independencia suficiente.

**Trazabilidad:** cada hallazgo con trazabilidad directa a fuentes normativas; correspondencia `rule_id` → fila de §9.2; matriz de aceptacion; registro de revision con casos examinados.

**Reproducibilidad:** prompt completo y hash; hashes de todas las entradas; parametros de generacion; identidad exacta del modelo; registro íntegro de respuestas; reconstruccion independiente hashable; reglas para resolver discrepancias entre ejecuciones. Mismo input → misma salida; sin fecha ni aleatoriedad en la decision.

### 3.9 Limitaciones de autorizacion del propietario

Fuente: S-06 §3 (Limites explicitos de la autorizacion de materializacion), S-07 DEC-OWNER-AI-06 (Limites), S-08 §4 (No autorizado por este registro).

La autorizacion de materializacion (S-06) NO concede permiso para:
1. Implementar Fase C.
2. Cerrar automaticamente AUD-R8-02.
3. Omitir revision humana independiente.
4. Omitir auditoria independiente de los siete artefactos.
5. Declarar G6 superada sin satisfacer todos sus criterios.
6. Iniciar fases D, E, F, G o S2.
7. Modificar los Parquet protegidos.
8. Cambiar codigo de produccion, esquemas o dependencias fuera del alcance aprobado.
9. Realizar commits o push por esta autorizacion.

DEC-OWNER-AI-06 (aprobado, S-07): la admisión de `INDEPENDENT_AI_REVIEW` NO autoriza: (1) la implementacion de Fase C; (2) cambios en codigo de produccion; (3) cambios en schemas o dependencias; (4) acceso o modificacion de Parquet protegidos; (5) ejecucion automatica de G5 ni de G6; (6) modificacion de ORACLE-ART-01/02/03/05/06/07 ni de ningun otro artefacto Oracle; (7) ampliacion de la autorizacion a artefactos distintos de ORACLE-ART-04; (8) commits o push. G5 y G6 requieren sus propios registros de ejecucion y aprobacion expresa; Fase C continua con `PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED`.

S-08 §4: esta aprobacion NO autoriza crear ORACLE-ART-04; ejecutar G5 ni G6; modificar produccion, schemas ni dependencias; modificar los Parquet protegidos; implementar Fase C; modificar otros artefactos Oracle; realizar commits ni push; modificar D3, la autorizacion R2, la especificacion R2, el plan R2 ni el protocolo R1 en esta tarea.

### 3.10 Estado y condiciones de cierre de AUD_R8_02

Fuente: S-01 §10.6/10.7/10.8, S-04 §9, S-05 G6, A-01 §1, A-02 §3, A-03 §3, A-04 §3.

**Estado actual:** `AUD_R8_02: OPEN` (antes AUD-R7-03, limitacion pendiente). No existen ni estan verificados los siete artefactos materiales del oracle; R9 no inventa transcripcion, checksum ni evidencia de revision; la autorizacion de implementacion sigue bloqueada hasta que existan y sean revisados.

**Condiciones de cierre (G6, cinco condiciones):**
1. Los siete artefactos requeridos estan materializados y sus estados individuales verificados.
2. Existe un informe de auditoria independiente favorable que verifica los criterios correspondientes a AUD-R8-02.
3. No quedan hallazgos bloqueantes sin resolver.
4. El propietario ha emitido aceptacion expresa del resultado de la auditoria, independiente de la aceptacion tecnica del auditor.
5. Existe evidencia documental trazable de cada requisito anterior.

El cierre solo con evidencia material y aceptacion expresa conforme a G6. AUD-R8-02 permanece OPEN hasta satisfacer sus condiciones. No existe autorizacion implicita para Fase C.

---

## 4. Hash de la reconstruccion independiente

Este documento de reconstruccion se genera como artefacto hashable ANTES de comparar las propuestas candidatas.

**SHA-256 de este archivo de reconstruccion:** [se calcula y registra tras escritura]
**Fecha y hora de creacion:** 2026-11-27T22:58:28Z

Fin de la reconstruccion normativa independiente.
