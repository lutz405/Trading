# R13-ORACLE-ARTIFACTS-R5-CORRECTION-REPORT-R1 — Informe de correcciones R5

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** informe de correcciones documentales. **R5 no está aprobado ni auditado**; la aprobación del propietario **no se presume**.

---

## 1. Entradas verificadas

| Entrada | SHA-256 verificado |
|---|---|
| `docs/r13_oracle_artifacts_r4_independent_audit_r1.md` | `94152ea9b8a53a5f66f6f051983fbad048e57210b7c218a4a5dc32744c51308a` (coincide con el esperado) |
| Resolución R4 | `a95f6af90b212d8539e1818ad3680a51762504fc9025cc1ae7d2436311b66ea5` |
| Especificación R4 | `ff722887189e6e5ca223e3699fae34b870c09d36810f81680b26689d978c1ba5` |
| Plan R4 | `226c51d08a3171232098f40d4e22cf0d2d1487a1c373aa480e69d5651da63e71` |
| Autorización R4 | `2db94133ef1f01b9f8ef6884efac95243c95b69b2fff489aac64f83bab55b2ec` |
| Protocolo R3 | `e538b144b575843ad528faf9220e1f6bffbf2f4a90710539b87032101d1e3f75` |

---

## 2. Versiones creadas

| Documento nuevo | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `docs/r13_oracle_artifacts_decision_resolution_r5.md` | `551037ef24714fcdcb56f2eda0e5f499307647e64f6b00b1786c741b2e4dbac9` | `7269c4184a046f855209788b790f7f89d996d3bb` |
| `docs/r13_oracle_artifacts_specification_r5.md` | `c124cd74045ed7721bff5f0a91cd1ec379ca0aac683e729fd1bf785801dde409` | `3fefaf051db7eecdfff9364bcc81c77a2828d679` |
| `docs/r13_oracle_artifacts_materialization_plan_r5.md` | `2a79269bbc3add9be5cdabd26c6e26976450aaea1f54cced5f9327ea229ff80e` | `d73b6cfb596a207cf3d09bce39f628a6d2f244f0` |
| `docs/r13_oracle_artifacts_materialization_authorization_r5.md` | `bdde15664efa39811f783106f1c031d0e134cd2ec29530467bcf4ae12db9c3fb` | `4ad671080d9f661be2d721f1bc2e1a955e841f29` |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r4.md` | `09145c2f36daf688b43ee796ba4e32bb65914fe3294857a60c3431483e7b7d4b` | `102a3582c2adeed3674f74501991a29a75bdc4df` |

R4, R3, R2 y R1 permanecen intactos; sus hashes se verificaron antes y después.

---

## 3. Matriz de trazabilidad: observación → cambio → evidencia

| Observación | Severidad | Documento / sección | Cambio exacto | Evidencia |
|---|---|---|---|---|
| `AUD-ANT-NEW-01` | `LOW` | Resolución R5 §4 y §5 | La tabla de §4 reproduce literalmente el texto de §5 (`Especificación R5 §3, Plan R5 §4 y Autorización R5 §§2–4 reflejan la misma modalidad y alcance`) y precisa que modalidad/alcance están en Autorización R5 §§2 y 4, con vigencia en §3 | Resolución R5 §4 tabla y §5; cotejo textual |
| `AUD-ANT-NEW-02` | `LOW` | Plan R5 §1.1 y §4 G0/G1 | Se definen `A-03` = `docs/r13_oracle_artifacts_specification_owner_approval_r1.md` y `A-04` = `docs/r13_oracle_artifacts_materialization_plan_owner_approval_r1.md`; G0/G1 citan las rutas completas; `R9/R4` se sustituye por `R9 y la Especificación R5` | Plan R5 §1.1, §4 filas G0/G1; verificación de rutas |
| `AUD-ANT-NEW-03` | `LOW` | Protocolo R4 §7 | Se elimina la lectura condicional: versión no disponible ⇒ `INCONCLUSIVE` de forma incondicional, con §7 expresamente subordinado a §§8.1–8.2 y a Especificación R5 §3.5 | Protocolo R4 §7, §8.1, §8.2; Especificación R5 §3.5 |
| `AUD-ANT-NEW-04` | `INFO` | Protocolo R4 §13 Etapa D | Se aclara que ART-05/06/07, cuando existan, **se inspeccionan como objetos de correspondencia auxiliar**; no son entrada normativa ni dependencia de ART-04; ART-04 no se compara contra sí mismo | Protocolo R4 §13 Etapa D; Especificación R5 §3.6 |

No se realizaron cambios adicionales por conveniencia estilística. Especificación R5 y Autorización R5 solo actualizan referencias de versión.

---

## 4. Verificaciones de regresión

Script temporal de solo lectura, ejecutado sobre los cinco documentos nuevos:

| Comprobación | Resultado |
|---|---|
| D1–D6 preservadas | PASS |
| Decisiones `DEC-OWNER-AI-01…06` | PASS |
| Jerarquía normativa (DEC-06 / §9.2 / schema) | PASS |
| Siete artefactos Oracle | PASS |
| Nueve campos de metadatos (con `rule_id` separado) | PASS |
| 139 rutas | PASS |
| 24 `rule_id` (13 usados + 11 excluidos) | PASS |
| 15 campos de R1 §9 | PASS |
| Dependencias `01, 03` de ART-04 y etapas A–H | PASS |
| G5 no autocerrable y cinco condiciones de G6 | PASS |
| Protección de Parquet | PASS |
| `PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED` | PASS |
| Correcciones NEW-01 a NEW-04 aplicadas | PASS |

**Resultado: 17/17 PASS.** Las cinco versiones son coherentes entre sí; las referencias cruzadas apuntan a secciones existentes (Resolución R5 §3.1/§4/§5; Especificación R5 §3; Plan R5 §1.1/§4; Autorización R5 §§2–4; Protocolo R4 §§3, 5, 6, 7, 8, 9, 10, 11, 13, 14).

La comprobación fue realizada por el generador de las propuestas. **No constituye auditoría independiente.**

---

## 5. Estado de auditoría

```text
AUD-ANT-NEW-01: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUD-ANT-NEW-02: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUD-ANT-NEW-03: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUD-ANT-NEW-04: PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT
AUD-ANT-01: HIGH / INCONCLUSIVE (sin cambios)
AUDIT_VERDICT_R4: INCONCLUSIVE (sin cambios)
R5: NOT_APPROVED / NOT_AUDITED
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

Ninguna observación se declara cerrada. R5 no desbloquea G5/G6, no materializa ART-04 y no implementa Fase C.

---

## 6. Riesgos y limitaciones

- La corrección R5 proviene del mismo generador de los documentos R4; requiere auditoría independiente posterior.
- `AUD-ANT-01` sigue `HIGH / INCONCLUSIVE`: no se ha acreditado proveedor distinto del generador.
- El dictamen global R4 permanece `INCONCLUSIVE`; R5 no lo modifica.
- La aprobación del propietario de R5 no se presume; debe ser expresa y posterior a la auditoría.
- No se han ejecutado pruebas de la revisión IA ni se ha materializado ART-04.
- Los archivos Parquet protegidos y sus hashes no fueron modificados ni accedidos.

---

## 7. Estado Git

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado, sin cambios staged, `git diff --check` exit 0. Sin commits ni push. Se crearon exclusivamente los cinco documentos R5 y este informe. R4 y todos sus predecesores, fuentes normativas, `tests/`, código, schemas, dependencias y Parquet permanecen intactos.

**Fin de R13-ORACLE-ARTIFACTS-R5-CORRECTION-REPORT-R1.**
