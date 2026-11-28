# R13-ORACLE-ARTIFACTS-R5-EXTERNAL-AUDIT-HANDOFF-R1 — Transferencia para auditoría externa R5

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** manifiesto de transferencia de **solo lectura**. **No** contiene conclusiones sobre la conformidad de R5, **no** aprueba versiones y **no** ejecuta auditoría.

**Destinatario previsto:** auditor externo con proveedor **distinto y verificable** respecto del generador original.

---

## 1. Estado del paquete

```text
R5: NOT_APPROVED / NOT_AUDITED
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

Los hashes SHA-256 y los Git blob SHA-1 se recalcularon directamente antes de redactar este manifiesto.

---

## 2. Inventario — ETAPA 1 (reconstrucción ciega)

### 2.1 Documentos candidatos — `CANDIDATE`

| ID | Ruta | SHA-256 | Git blob SHA-1 |
|---|---|---|---|
| C-01 | `docs/r13_oracle_artifacts_decision_resolution_r5.md` | `551037ef24714fcdcb56f2eda0e5f499307647e64f6b00b1786c741b2e4dbac9` | `7269c4184a046f855209788b790f7f89d996d3bb` |
| C-02 | `docs/r13_oracle_artifacts_specification_r5.md` | `c124cd74045ed7721bff5f0a91cd1ec379ca0aac683e729fd1bf785801dde409` | `3fefaf051db7eecdfff9364bcc81c77a2828d679` |
| C-03 | `docs/r13_oracle_artifacts_materialization_plan_r5.md` | `2a79269bbc3add9be5cdabd26c6e26976450aaea1f54cced5f9327ea229ff80e` | `d73b6cfb596a207cf3d09bce39f628a6d2f244f0` |
| C-04 | `docs/r13_oracle_artifacts_materialization_authorization_r5.md` | `bdde15664efa39811f783106f1c031d0e134cd2ec29530467bcf4ae12db9c3fb` | `4ad671080d9f661be2d721f1bc2e1a955e841f29` |
| C-05 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r4.md` | `09145c2f36daf688b43ee796ba4e32bb65914fe3294857a60c3431483e7b7d4b` | `102a3582c2adeed3674f74501991a29a75bdc4df` |

### 2.2 Fuentes normativas originales — `PRIMARY_ORIGINAL`

| ID | Ruta | SHA-256 | Git blob SHA-1 |
|---|---|---|---|
| S-01 | `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| S-02 | `docs/aud04b_model_provenance_v4_design.md` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | `fbe7215c5199c418e16f6968fb4b662427f8d70a` |
| S-03 | `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |
| S-04 | `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| S-05 | `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| S-06 | `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `e37dfdae0663502e89cb522ca8605eb2791c828e` |
| S-07 | `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | `33693367f38ca579864d5ea98ebb8aa63918011d` |
| S-08 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | `96c03f832c4d017a0b562c137fa9bb1b12b5ce7e` |

### 2.3 Registros de aprobación del propietario — `OWNER_APPROVAL`

| ID | Ruta | SHA-256 | Git blob SHA-1 |
|---|---|---|---|
| P-01 | `docs/r13_oracle_art_04_ai_review_owner_decision_package_r1.md` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` | `9ec2c09a0c586ce7fd23bb29f1512af48528f903` |
| P-02 | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` | `10a1f93306246a7adc2356248db881f6f7289218` |
| P-03 | `docs/r13_owner_design_approval_r1.md` | `16cfd579db05289cca9a9140988128175136dffa1cba814b0a28f19c7b403b60` | `6ecdf341fba3e2324505dd546cc1b792f20a6ad5` |
| P-04 | `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | `432084a4baead2a5ad84d4d43c158f8bc3dc7731` |
| P-05 | `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | `22052a44e2f090fea294a7a51c676507bcaeefab` |
| P-06 | `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | `4cd2d20f92b161217ab6334d10039e6b17172e3a` |
| P-07 | `docs/r13_oracle_g5_verification_representation_owner_approval_r1.md` | `22bcd83cd8d2c1c3a46df53231c4980319cefb086af183fbaab23593fe95d63d` | `c390f3067ad05048c939a24cc76b073e627422dd` |

### 2.4 Evolución normativa R1–R4 — `EVOLUTION`

| Ruta | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `docs/r13_oracle_artifacts_decision_resolution_r1.md` | `53a80a88f5153a1220a97c3d4ee2c85d942fc7496fedd7c3262a9fd1f660d0ab` | `1d183f847769ffc268a54f7ca814972dcec323e2` |
| `docs/r13_oracle_artifacts_decision_resolution_r3.md` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | `fbbb05f9529e59b92a44fe65fca540d39839ec00` |
| `docs/r13_oracle_artifacts_decision_resolution_r4.md` | `a95f6af90b212d8539e1818ad3680a51762504fc9025cc1ae7d2436311b66ea5` | `310915829fc90b04c3808c39092f0f58ef31e13c` |
| `docs/r13_oracle_artifacts_specification_r1.md` | `2e6f6816c9d0a41de9da7b436a49a7214b962ce87817a2d551ec7832df40b23d` | `1ea0ee22111a9058ec33d2b00a00c56151609acd` |
| `docs/r13_oracle_artifacts_specification_r3.md` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | `6167d76a89a6bf4e37c1978c8357d732d7d4b7c9` |
| `docs/r13_oracle_artifacts_specification_r4.md` | `ff722887189e6e5ca223e3699fae34b870c09d36810f81680b26689d978c1ba5` | `2bdae65282062979a49191970640de123a52dfce` |
| `docs/r13_oracle_artifacts_materialization_plan_r1.md` | `60a9923f0327039b1451a884a132e382f2f8380e63626007cd204f6585805593` | `e9ef0651cdb2fe86cf4b34bff1fbfd85046dbefd` |
| `docs/r13_oracle_artifacts_materialization_plan_r3.md` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | `10d7f4be8b36849916d26f87c4baf3457538bc54` |
| `docs/r13_oracle_artifacts_materialization_plan_r4.md` | `226c51d08a3171232098f40d4e22cf0d2d1487a1c373aa480e69d5651da63e71` | `aa8c03700edf5c78b1a7602ce92e9f900c7924a8` |
| `docs/r13_oracle_artifacts_materialization_authorization_r1.md` | `8dfd46c927ba22f525b9a4c2269c66eaf6b70bda71dbb66e04331bb973012457` | `4f5c57b33c907ebab7989b0a1397f6b33ecb26c0` |
| `docs/r13_oracle_artifacts_materialization_authorization_r3.md` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | `0489cb78ecbf6d6a44c106eb2747a3533c98c53c` |
| `docs/r13_oracle_artifacts_materialization_authorization_r4.md` | `2db94133ef1f01b9f8ef6884efac95243c95b69b2fff489aac64f83bab55b2ec` | `75c0790733930e9a6b4514c32afe42810a7728f6` |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | `7c3223a0e4954c401c0f513c903d9ad708130335` |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r3.md` | `e538b144b575843ad528faf9220e1f6bffbf2f4a90710539b87032101d1e3f75` | `6c972eedfbb747c00da50d28d6ef078bf57238e9` |

### 2.5 Inventario de los siete artefactos Oracle y evidencia de estado

| Artefacto | Archivo / evidencia | SHA-256 | Git blob SHA-1 | Estado registrado |
|---|---|---|---|---|
| ORACLE-ART-01 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` | `VERIFIED` |
| ORACLE-ART-02 | `tests/oracle_normative_v4_r5_verifier.py` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` | `dcdd4c09236923c296ae635662f244bc8258a068` | `VERIFIED` |
| ORACLE-ART-03 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `83a84f653a1c55579733afe89b8a4a2c2268b711` | `VERIFIED` |
| **ORACLE-ART-04** | **No existe** | — | — | `NOT_CREATED` |
| ORACLE-ART-05 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` | `ec0803f2d47f4fe2a64191662018f69183bb5a2a` | `VERIFIED` |
| ORACLE-ART-06 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | `fa812bd125b01a7a4e7a9b994b7124e1b0d6fd0a` | `VERIFIED` |
| ORACLE-ART-07 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | `9f10594fea28152a7f651e8f8d1864b0d63f7f40` | `VERIFIED` |

Evidencia de estado adicional:

| Ruta | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `docs/r13_oracle_art_05_verification_status_registration_r1.md` | `fd140513aa380c2b46633e35645f38e03cbfb5687a3210ddc9c787b281ca4806` | `955838e6e033e69a6df6bd6374fcf9358f045bd6` |
| `docs/r13_oracle_art_06_07_verification_status_registration_r1.md` | `1be1c153ae880a0f52d05b2c233e599aad10db1a599cccd4a46e911fc8c756dd` | `00bb8963c23d3c1ffd655ae3dc8ad79280771e57` |
| `docs/r13_oracle_g5_art_05_coverage_completion_r1.md` | `eb704f4127a14020f44d70dd23be05d2fb70a0d216857511ff09a93da38893a2` | `f959824caebd6742032fedc2ac40fba118e5f1fd` |
| `docs/r13_oracle_g5_art_06_07_materialization_r1.md` | `71a1575901c419d6628a335be3256a7ad7fc53a5116af496aa6066a5e3ab2b90` | `cfc7f36218fbde61d705b2ba6ff1c721f5518703` |
| `docs/r13_oracle_materialization_g4_execution_r1.md` | `7855ac9170ceb499e2e8a7c1f29d332b050099c274432fbfefaf5b980d1d44a3` | `2023101d666476856bd35ea1b8ebf7476d42bb4d` |
| `docs/r13_oracle_materialization_g5_execution_r1.md` | `0cbb980301422a030061ffa84846a211b85a0c49fd8736e225e3677ff1be4f02` | `445ec10bda5c34720298c606024fa7b350d9575c` |

---

## 3. Evidencia en ETAPA 2 — no entregar en la reconstrucción inicial

Estos documentos **no** forman parte del contexto inicial de reconstrucción normativa. Se entregan solo para la revisión de regresiones, después de que el auditor haya reconstruido sus criterios:

| Ruta | SHA-256 | Git blob SHA-1 | Etiqueta |
|---|---|---|---|
| `docs/r13_oracle_artifacts_r5_correction_report_r1.md` | `85fce7d7bd7f48c45b23839073461c00aa81a87a52f2e5985c52ee7973b367bc` | `7a88386d9713781a1338a56626dd933ae059d203` | Informe del generador; evidencia auxiliar |
| `docs/r13_oracle_artifacts_r5_independent_audit_r1.md` | `163f8745334ab5041d5896d090b07cf78ef86be3344396b6808a2ecd24e1428d` | `00accfa206a825aabc64ec97171784269ac4ad61` | **NO INDEPENDIENTE** — autoevaluación del generador |
| `docs/r13_oracle_artifacts_r4_independent_audit_r1.md` | `94152ea9b8a53a5f66f6f051983fbad048e57210b7c218a4a5dc32744c51308a` | `90bf44ee1896b9219221b66e17a8b673c823af57` | Auditoría previa; no autoridad normativa |

No se solicita al auditor que acepte las conclusiones del generador ni las de auditorías anteriores.

---

## 4. Archivos no disponibles o inexistentes

| Elemento | Situación |
|---|---|
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-04.json` | **No existe**; estado `NOT_CREATED` |
| Informe de auditoría independiente R5 (distinto de la autoevaluación) | **No existe** |
| Aprobación expresa del propietario de R5 | **No existe**; `NOT_APPROVED` |
| Parquet `data/raw/BTC_USDT_1m.parquet`, `data/raw/BTC_USDT_5m.parquet` | **No se entregan**: acceso prohibido por DEC-OWNER-AI-06; solo se registra su existencia |
| Archivos inaccesibles en este manifiesto | **Ninguno**: todas las rutas listadas fueron verificadas |

---

## 5. Instrucciones de reconstrucción ciega

1. Abrir una **sesión nueva** del auditor, sin historial compartido con el generador.
2. Declarar proveedor, modelo, versión exacta (o `NO_DISPONIBLE`), parámetros disponibles, plataforma e identificador de sesión **antes** de leer los candidatos.
3. Acreditar con evidencia verificable que el proveedor es **distinto** del proveedor del generador original. No inferir independencia de nombres comerciales, interfaces ni sesiones nuevas.
4. Si la separación no puede demostrarse: registrar **`INCONCLUSIVE`** y detener la emisión de dictamen de auditoría.
5. Recalcular SHA-256 y Git blob SHA-1 de todas las entradas de §2 y compararlos con los valores del manifiesto.
6. Leer primero las fuentes originales (§2.2), aprobaciones (§2.3), evolución (§2.4) y evidencia de artefactos (§2.5).
7. Reconstruir por escrito los requisitos —siete artefactos, 139 rutas, nueve metadatos, 24 `rule_id` (13 usados y 11 de exclusión), 15 campos de R1 §9, dependencias `01, 03`, G0–G6, D1–D6 y `DEC-OWNER-AI-01…06`— **antes** de abrir C-01…C-05.
8. Solo después abrir los candidatos y contrastarlos con la reconstrucción propia.
9. No modificar archivo alguno: acceso de solo lectura.

---

## 6. Procedimiento por etapas

| Etapa | Acción | Entradas | Salida |
|---|---|---|---|
| 1 | Declaración de identidad e independencia | §5.2–5.4 | Registro de auditor |
| 2 | Verificación de hashes | §2 | Tabla de hashes |
| 3 | Reconstrucción ciega | §2.2–§2.5 | Requisitos reconstruidos |
| 4 | Auditoría de los candidatos | C-01…C-05 | Hallazgos y evidencia |
| 5 | Revisión de regresiones | §3 (segunda etapa) | Contraste con hallazgos previos |
| 6 | Dictamen y limitaciones | Etapas 1–5 | Informe final del auditor |

La etapa 5 **no** puede realizarse antes de la etapa 3.

---

## 7. Criterios de aceptación y clasificación de hallazgos

| Dictamen | Criterio |
|---|---|
| `ACCEPTED` | Independencia acreditada; reconstrucción completa; sin hallazgos `BLOCKER`/`HIGH`; evidencia reproducible |
| `ACCEPTED_WITH_FINDINGS` | Solo hallazgos `MEDIUM`/`LOW`/`INFO` con trazabilidad; sin `BLOCKER`/`HIGH`; independencia acreditada |
| `REJECTED` | Contradicción normativa, dependencia circular o pérdida de requisitos preservados |
| `INCONCLUSIVE` | Proveedor no acreditado como distinto, versión/parámetros no disponibles cuando afecten la conclusión, o evidencia insuficiente |

Severidades: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`. `INCONCLUSIVE` y cualquier `BLOCKER`/`HIGH` pendiente **impiden** desbloquear G5. Ningún dictamen equivale a aprobación del propietario.

---

## 8. Límites de autorización

La transferencia **no** autoriza: aprobar R5; crear ORACLE-ART-04; ejecutar G5 o G6; implementar Fase C; modificar producción, tests, schemas, dependencias o Parquet; cambiar artefactos Oracle; ampliar `DEC-OWNER-AI-01…06`; realizar commits o push. El auditor debe operar en modo de solo lectura.

---

## 9. Campos para registro del auditor (sin completar)

| Campo | Valor |
|---|---|
| Proveedor acreditado | __________________________ |
| Modelo y versión exacta | __________________________ |
| Plataforma | __________________________ |
| Identificador de sesión | __________________________ |
| Parámetros disponibles | __________________________ |
| Evidencia de separación de proveedor | __________________________ |
| Fecha real de la auditoría | __________________________ |
| Hashes de entrada verificados | __________________________ |
| Limitaciones declaradas | __________________________ |

---

## 10. Estado Git y cierre

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff. `git diff --check`: exit 0. Sin commits ni push. Único archivo creado: este manifiesto. No se modificaron R5, predecesores, fuentes, artefactos, tests, producción, schemas, dependencias ni Parquet.

```text
R5: NOT_APPROVED / NOT_AUDITED
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

**Fin de R13-ORACLE-ARTIFACTS-R5-EXTERNAL-AUDIT-HANDOFF-R1.**
