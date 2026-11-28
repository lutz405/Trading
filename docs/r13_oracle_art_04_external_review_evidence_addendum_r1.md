# R13 — ART-04 EXTERNAL REVIEW EVIDENCE ADDENDUM R1

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **ANEXO DE EVIDENCIA, NO NORMATIVO Y NO EQUIVALENTE A UNA AUDITORÍA.**

Complementa `docs/r13_oracle_art_04_external_review_handoff_r1.md` (SHA-256 `f9cfce4bfd11e340d8292b1e982a6d024242b26398cf1aebcbb2d6e018190d85`), **sin modificarlo**. No introduce excepciones a los requisitos de independencia de `DEC-OWNER-AI-04` ni cambia el Protocolo ART-04 vigente (SHA-256 `09145c2f36daf688b43ee796ba4e32bb65914fe3294857a60c3431483e7b7d4b`).

---

## 1. Propósito y estado

Incorporar al handoff externo las evidencias técnicas G-01…G-04 producidas con posterioridad, manteniéndolas **separadas** de la reconstrucción ciega inicial. Este anexo **no** confirma hallazgos, **no** aprueba R5, **no** declara ART-04 creado ni aceptado, y **no** desbloquea G5/G6 ni Fase C.

---

## 2. Fuentes nuevas y hashes verificados

| Documento | SHA-256 | Git blob SHA-1 | Estado registrado en el informe |
|---|---|---|---|
| `docs/r13_oracle_art_04_technical_review_draft_r1.md` | `82c7d9d600ed306de0bfdfda4e4aecb53097b94623126cac2b8015a0bdb90aae` | `c3cdfc2cfdecb10567ff02bae4f7e34b46105564` | `TECHNICAL_DRAFT_NON_INDEPENDIENTE` |
| `docs/r13_art_04_evidence_gap_resolution_r1.md` | `1052f23e0b1f520e66c01576451e309e0696245c05be3caad9b194e6228d6b10` | `073dd1f760ecdc43d8993ed368e9ce148c77bae2` | G-01/G-02/G-03 `VERIFIED`; G-04 `CORROBORATED` en ese momento |
| `docs/r13_art_04_exclusion_evidence_completion_r1.md` | `befc580b9601ce394d1b81f799206796493bdfcec2c66fa060312aa586459d88` | `43b9d3f22ce2237989d831f9742efaeea279cc88` | `G-04: VERIFIED` |
| `docs/r13_oracle_artifacts_r5_external_audit_handoff_r1.md` | `8af6fbddb39bbfdee81e1d70c3f042beab14dcfc894cee9356f7e69b035105df` | `64e860e4156b4ca9d16900eeb01de5b45f802bf4` | Handoff R5 (paquete paralelo) |
| `docs/r13_original_generator_provenance_investigation_r1.md` | `85222386b9b28138439a34553247bdc6ae2f45e40db0880ed1f43ce1e9b75551` | `57e325628a7719a5b936921047f921069eb20848` | `PROVENANCE_UNVERIFIABLE` |

Todos los hashes se recalcularon y coinciden con los registrados en los respectivos informes. Artefactos y verificadores citados: ART-01 `7c9c49a5…`, ART-03 `23306196…`, ART-05 `35b705b9…`, ART-06 `9c133937…`, ART-07 `9a3d4674…`, ART-02 `a67bf35a…`, representación `23e37afa…`.

---

## 3. Correspondencia entre requisitos y evidencias G-01…G-04

| Requisito / brecha del borrador | Evidencia | Fuente | Estado |
|---|---|---|---|
| Estados internos ART-06/07 vs. registros `VERIFIED` (G-01) | Registro §3 declara que los JSON no se modifican y que el estado corriente es el registrado | `r13_oracle_art_06_07_verification_status_registration_r1.md` (`1be1c153…`); gap §2 | `VERIFIED` como discrepancia documentada |
| Integridad JCS/SHA-256 de ART-03 (G-02) | `rfc8785.dumps` sobre ART-01 → `7c9c49a5…`, igual al contenido de ART-03; versión `0.1.4` | gap §3; ART-01/ART-03 | **`VERIFIED` (reproducido)** |
| Ejecución aislada de ART-02 (G-03) | Copia en `%TEMP%`; `verify() == []`, sin fallback | gap §4; ART-02 `a67bf35a…` | **`VERIFIED` (reproducido)** |
| 11 reglas excluidas y casos negativos (G-04) | Tabla D1 de 11 reglas; 35 rutas ausentes en ART-01/ART-05 y 35/35 detectadas como `EXTRA_PATH` | exclusion completion §2–§4; §9.2 `78addb74…`; representación `23e37afa…` | **`VERIFIED`** |
| Independencia del revisor | Procedencia del generador no acreditada | provenance investigation | `NOT_VERIFIED` / `BLOCKED` |
| Dictamen de ART-04 | No existe ART-04; no hay revisión independiente | borrador técnico §1, §10 | `BLOCKED` |

---

## 4. Resultados reproducidos incorporados

| ID | Resultado |
|---|---|
| G-01 | `status: CREATED_UNVERIFIED` permanece en los JSON de ART-06/07; los registros declaran `VERIFIED`; discrepancia explicada, no resuelta en los archivos |
| G-02 | JCS con `rfc8785 0.1.4`: 37678 bytes; SHA-256 `7c9c49a5…` = contenido de ART-03. El SHA-256 del archivo ART-03.txt es `23306196…` (magnitud distinta) |
| G-03 | ART-02 ejecutado sobre copias aisladas: versión `ORACLE_NORMATIVE_V4_R5`, checksum coincidente, `verify() == []` |
| G-04 | 11 reglas `R9-9.2-02/04/06/08/16/17/18/21/22/23/24`; 35 rutas de exclusión; 35/35 ausentes en ART-01 y ART-05; 35/35 `EXTRA_PATH`; suite aislada 17 passed |

Estos resultados son **evidencia producida por el generador**, realizada con verificaciones existentes en entorno aislado de solo lectura. No sustituyen la ejecución del auditor.

---

## 5. Separación de materiales

### 5.1 Material para reconstrucción ciega inicial

Se entrega **antes** de que el auditor lea conclusiones: handoff R1 (inventario y hashes), fuentes normativas originales, aprobaciones del propietario, evolución normativa y artefactos Oracle con sus registros de estado, más el Protocolo ART-04 vigente. El auditor debe reconstruir sus criterios desde esas fuentes.

### 5.2 Evidencia suplementaria posterior a la reconstrucción

Se entrega **solo después** de completada la reconstrucción propia:

1. `docs/r13_oracle_art_04_technical_review_draft_r1.md`
2. `docs/r13_art_04_evidence_gap_resolution_r1.md`
3. `docs/r13_art_04_exclusion_evidence_completion_r1.md`
4. Este anexo.

El borrador técnico está etiquetado `TECHNICAL_DRAFT_NON_INDEPENDIENTE`. Ninguno de estos archivos debe leerse como autoridad normativa ni como dictamen.

---

## 6. Archivos que debe recibir el auditor y orden de revisión

| Orden | Archivo | SHA-256 |
|---|---|---|
| 1 | `docs/r13_oracle_art_04_external_review_handoff_r1.md` | `f9cfce4bfd11e340d8292b1e982a6d024242b26398cf1aebcbb2d6e018190d85` |
| 2 | `docs/r13_oracle_art_04_ai_independent_review_protocol_r4.md` | `09145c2f36daf688b43ee796ba4e32bb65914fe3294857a60c3431483e7b7d4b` |
| 3 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` |
| 4 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` |
| 5 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` |
| 6 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` |
| 7 | `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` |
| 8 | `tests/oracle_normative_v4_r5_verifier.py` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` |
| 9 | `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` |
| 10 | `docs/r13_oracle_art_04_technical_review_draft_r1.md` | `82c7d9d600ed306de0bfdfda4e4aecb53097b94623126cac2b8015a0bdb90aae` |
| 11 | `docs/r13_art_04_evidence_gap_resolution_r1.md` | `1052f23e0b1f520e66c01576451e309e0696245c05be3caad9b194e6228d6b10` |
| 12 | `docs/r13_art_04_exclusion_evidence_completion_r1.md` | `befc580b9601ce394d1b81f799206796493bdfcec2c66fa060312aa586459d88` |
| 13 | `docs/r13_original_generator_provenance_investigation_r1.md` | `85222386b9b28138439a34553247bdc6ae2f45e40db0880ed1f43ce1e9b75551` |

Procedimiento: verificar hashes → reconstruir criterios de fuentes originales (órdenes 1–9) → solo entonces leer 10–13 → emitir dictamen propio. No se entrega ORACLE-ART-04 porque no existe.

---

## 7. Limitaciones de independencia aún abiertas

- **PROVENANCE_UNVERIFIABLE:** no consta el proveedor real del generador `opencode / hy4-flash-free`; no se infiere de nombres comerciales ni de plataformas distintas.
- **EXT-01 y EXT-02:** permanecen `NOT_CLOSED`.
- **DEC-OWNER-AI-04:** permanece `NOT_SATISFIED`; no se propone excepción ni relajación.
- Dictámenes previos `INCONCLUSIVE`: R4, R5 y auditoría externa R5.
- R5: `NOT_APPROVED / NOT_AUDITED`; la aprobación del propietario no se presume.

---

## 8. Obligación de reconstrucción del auditor

El auditor **debe** realizar su propia reconstrucción de requisitos y sus propias pruebas. **No puede** aceptar los resultados G-01…G-04 por declaración, ni tratar este anexo como auditoría, ni usar la autoevaluación del generador como sustituto. Si la separación de proveedor no puede acreditarse, debe registrar `INCONCLUSIVE` conforme al Protocolo ART-04 §8.1 y §6.9. Ningún resultado aquí descrito desbloquea G5 ni autoriza Fase C.

---

## 9. Estados y cierre

```text
ADDENDUM: EVIDENCE_ONLY / NON_NORMATIVE / NOT_AN_AUDIT
ORACLE-ART-04: NOT_CREATED
DEC_OWNER_AI_04_STATUS: NOT_SATISFIED
EXT_01: NOT_CLOSED
EXT_02: NOT_CLOSED
R5: NOT_APPROVED / NOT_AUDITED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni unstaged; `git diff --check` exit 0. Sin commits ni push. Único archivo creado: este anexo. No se modificaron handoff R1, normativas, protocolo, artefactos, producción, tests, schemas, dependencias ni Parquet.

**Fin de R13-ART-04-EXTERNAL-REVIEW-EVIDENCE-ADDENDUM-R1.**
