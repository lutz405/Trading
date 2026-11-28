# R13-ORACLE-ART-04-EXTERNAL-REVIEW-HANDOFF-R1 — Transferencia documental para auditoría externa independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** manifiesto de transferencia de solo lectura. **No** contiene conclusiones sobre la conformidad de las propuestas, **no** aprueba documentos y **no** ejecuta revisión alguna.

**Destinatario previsto:** proveedor y modelo de IA **distintos** del generador, actuando conforme a `DEC-OWNER-AI-04`.

---

## 1. Inventario completo

Todos los hashes se recalcularon directamente antes de redactar este manifiesto.

### 1.1 Documentos candidatos a revisión — `CANDIDATE`

| ID | Ruta | SHA-256 | Git hash |
|---|---|---|---|
| C-01 | `docs/r13_oracle_artifacts_decision_resolution_r3.md` | `25ab20320dec91d5fb7ac20e190eda5ad821c6821678aa401122c69c1935f8fb` | `fbbb05f9529e59b92a44fe65fca540d39839ec00` |
| C-02 | `docs/r13_oracle_artifacts_specification_r3.md` | `d627f23603a7de7e7444c5bc76397ea7e4b2b896eac3e7de5b6afcd53a86160d` | `6167d76a89a6bf4e37c1978c8357d732d7d4b7c9` |
| C-03 | `docs/r13_oracle_artifacts_materialization_plan_r3.md` | `2f6f48a223c9974b7b56a9ac71ba2f8cca8cc39cc8ef322fe8bf4f8e846278be` | `10d7f4be8b36849916d26f87c4baf3457538bc54` |
| C-04 | `docs/r13_oracle_artifacts_materialization_authorization_r3.md` | `7571faf5ff17f450e2059a9e28deff056a75e09f738ccc843920a148cc2bea67` | `0489cb78ecbf6d6a44c106eb2747a3533c98c53c` |
| C-05 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r2.md` | `6a095901769e1cd2166db4b1a59495f3b1692d81cb915b9469524eb3224a6bc9` | `7c3223a0e4954c401c0f513c903d9ad708130335` |

### 1.2 Fuentes normativas originales — `PRIMARY_ORIGINAL`

| ID | Ruta | SHA-256 | Git hash |
|---|---|---|---|
| S-01 | `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| S-02 | `docs/aud04b_model_provenance_v4_design.md` (diseño v4 §9.2) | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | `fbe7215c5199c418e16f6968fb4b662427f8d70a` |
| S-03 | `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| S-04 | `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| S-05 | `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `e37dfdae0663502e89cb522ca8605eb2791c828e` |
| S-06 | `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | `33693367f38ca579864d5ea98ebb8aa63918011d` |
| S-07 | `docs/r13_oracle_art_04_ai_review_owner_decision_package_r1.md` | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` | `9ec2c09a0c586ce7fd23bb29f1512af48528f903` |
| S-08 | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md` | `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` | `10a1f93306246a7adc2356248db881f6f7289218` |
| S-09 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | `96c03f832c4d017a0b562c137fa9bb1b12b5ce7e` |
| S-10 | `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |

S-04 define los siete artefactos; S-05 define las puertas G0–G6; S-01/S-02 constituyen la autoridad normativa técnica para las 139 rutas y el diseño v4 §9.2.

### 1.3 Registros de aprobación originales — `OWNER_APPROVAL`

| ID | Ruta | SHA-256 | Git hash |
|---|---|---|---|
| A-01 | `docs/r13_owner_design_approval_r1.md` | `16cfd579db05289cca9a9140988128175136dffa1cba814b0a28f19c7b403b60` | `6ecdf341fba3e2324505dd546cc1b792f20a6ad5` |
| A-02 | `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` | `432084a4baead2a5ad84d4d43c158f8bc3dc7731` |
| A-03 | `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` | `a9179103ab49a85c369b5d3ecce69a6eba7ab0b289a4c889454f19bd8c0857f3` | `22052a44e2f090fea294a7a51c676507bcaeefab` |
| A-04 | `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md` | `baa012392bff618b8136d9a632e4e14bf418653901179f1e0c7c2e4982f12bf9` | `4cd2d20f92b161217ab6334d10039e6b17172e3a` |

---

## 2. Exclusiones del paquete inicial

Se confirma que **no se incluyen** en este paquete de transferencia:

- informes de auditoría normativa ni ningún otro informe `r13_audit_*`;
- hallazgos, severidades ni conclusiones de auditorías anteriores;
- resúmenes, explicaciones, dictámenes ni recomendaciones producidas por el generador de las propuestas;
- dictámenes previos sobre los cinco documentos candidatos;
- versiones históricas distintas de las fuentes originales listadas en §1.2 y §1.3.

Solo se entregan las rutas y los hashes indicados. El auditor externo debe **reconstruir sus propios criterios** a partir de S-01…S-10 y A-01…A-04, sin recibir conclusiones anticipadas.

---

## 3. Instrucciones de transferencia

1. Utilizar un **proveedor y modelo distintos** de los del generador, con sesión nueva y sin historial compartido.
2. Recibir primero las fuentes originales (§1.2, §1.3); recién después los candidatos (§1.1).
3. No entregar este manifiesto como guía de contenido: contiene únicamente inventario, hashes e instrucciones.
4. Recalcular personalmente cada SHA-256 y compararlo con el valor listado antes de analizar el contenido.
5. No modificar ningún archivo: acceso de solo lectura.
6. Reconstruir las reglas desde las fuentes originales antes de compararlas con los candidatos.
7. Registrar proveedor, modelo, versión, sesión, prompt completo, fecha y hashes de todas las entradas, conforme a §4.
8. Emitir el resultado en documento separado, sin comunicarlo al generador antes de su finalización.
9. No ejecutar G5 ni G6, no crear ORACLE-ART-04 y no modificar producción, schemas, dependencias ni Parquet.

---

## 4. Campos para registro del auditor externo (sin completar)

| Campo | Valor |
|---|---|
| Proveedor de IA | ______________________________________________ |
| Modelo y versión exacta | ______________________________________________ |
| Identificador de sesión | ______________________________________________ |
| Prompt completo utilizado | ______________________________________________ |
| Configuración relevante (parámetros/herramientas) | ______________________________________________ |
| Fecha real de la revisión | ______________________________________________ |
| Hashes de entrada verificados | ______________________________________________ |
| Declaración de independencia | ______________________________________________ |
| Limitaciones declaradas | ______________________________________________ |

Estos campos deben ser completados por el auditor externo. No se completa, firma ni inventa dato alguno en este manifiesto.

---

## 5. Estado y límites

```text
HANDOFF_STATUS: PREPARED
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff. `git diff --check`: exit 0. Sin commits ni push. Único archivo creado: este manifiesto. No se modificararon los documentos listados ni ningún otro archivo.

**Fin de R13-ORACLE-ART-04-EXTERNAL-REVIEW-HANDOFF-R1.**
