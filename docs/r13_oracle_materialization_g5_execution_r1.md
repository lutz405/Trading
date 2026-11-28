# R13-ORACLE-MATERIALIZATION-G5-EXECUTION-R1 — Informe de ejecución de la puerta G5

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Puerta ejecutada:** **G5 — Verificación independiente**, conforme a `docs/r13_oracle_artifacts_materialization_plan_r2.md` §8.
**Resultado:** ejecución parcial. **G5: BLOCKED** por falta de revisión humana independiente real y por ausencia de `ALLOWLIST_V4` para las comparaciones exigidas en ORACLE-ART-06 y ORACLE-ART-07. No se inicia G6.

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
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `83a84f653a1c55579733afe89b8a4a2c2268b711` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` |
| `tests/oracle_normative_v4_r5_verifier.py` | `dcdd4c09236923c296ae635662f244bc8258a068` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` |

Los hashes de ORACLE-ART-01, 02 y 03 coinciden con los registrados en el informe G4.

---

## 2. Verificación de G0–G4

| Gate | Estado | Evidencia |
|---|---|---|
| G0 | `PASSED` | Informe G0 R1 línea 116 |
| G1 | `PASSED` | Informe G1 R1 línea 147 |
| G2 | `PASSED` | Informe G2 R1 línea 159 |
| G3 | `PASSED` | Informe G3 R1 línea 175 |
| G4 | `PASSED` | Informe G4 R1 línea 187; `G4_COMPLETED: YES` línea 188 |
| Artefactos iniciales | 01–03 `CREATED_UNVERIFIED`; 04–07 `NOT_CREATED` | Informe G4 líneas 189–195 |

---

## 3. Criterios literales de G5

Extraídos del plan R2 §8, fila **G5**:

| Elemento | Texto literal |
|---|---|
| Puerta | **G5 Verificación independiente** |
| Criterios de entrada | `G4 completo; revisión humana realizada` |
| Criterios de salida | `Evidencia de verificación y dictamen` |
| Rechazo | `Discrepancia no resuelta; revisión no independiente` |

Del plan R2 §5.1, verificaciones exigidas: integridad de ORACLE-ART-03; correspondencia R2; cobertura de 139 rutas; nueve metadatos; `rule_id`; P1–P5 e I1–I12; revisión humana; mutación `external_run_only`.

---

## 4. Resultado individual de criterios

| ID | Criterio | Resultado |
|---|---|---|
| G5-IN-01 | G4 completo | **PASS** |
| G5-IN-02 | Revisión humana realizada | **BLOCKED** — no existe persona revisora real designada; no se inventa identidad ni resultado |
| G5-ART01-01 | 139 rutas y unicidad | **PASS** — 139 entradas únicas, ordenadas por `path` |
| G5-ART01-02 | Correspondencia con R9 §5.4 y diseño §9.2 | **PASS** — comparación campo por campo sin errores |
| G5-ART01-03 | `rule_id` y versión | **PASS** — 24 reglas `R9-9.2-01…24`; versión `ORACLE_NORMATIVE_V4_R5` |
| G5-ART01-04 | Diez campos y `rule_id` separado | **PASS** |
| G5-ART02-01 | Arquitectura D6 y entradas declaradas | **PASS** — verificador en `tests/`; única entrada declarada ORACLE-ART-01 |
| G5-ART02-02 | Sin imports productivos ni dependencias nuevas | **PASS** — solo stdlib y `rfc8785` ya declarado |
| G5-ART02-03 | Determinismo y fail-closed | **PASS** — `verify()` devolvió `[]` sin errores |
| G5-ART03-01 | Recálculo SHA-256 de la preimagen normativa | **PASS** — `7c9c49a5…300b300b` coincide con ORACLE-ART-03 |
| G5-JCS-01 | Orden canónico JCS vs orden lógico de campos | **PASS** — bytes ordenados por UTF-16BE; los diez campos y valores están presentes y correctos en el modelo |
| G5-ART04-01 | Revisión humana independiente | **BLOCKED** |
| G5-ART05-01 | Evidencia de cobertura de 139 rutas | **PASS** — ORACLE-ART-05 generado con 139 filas únicas |
| G5-ART06-01 | Comparación de nueve metadatos contra `ALLOWLIST_V4` | **BLOCKED** — `ALLOWLIST_V4` no está implementado en `provenance_v4.py`; G5 no autoriza implementarlo |
| G5-ART07-01 | Mutación controlada `external_run_only` | **BLOCKED** — requiere `ALLOWLIST_V4`; no se modifica código ni se simula fuera del escenario normativo |
| G5-OUT-01 | Evidencia de verificación y dictamen completos | **BLOCKED** — falta revisión humana y dos evidencias |
| G5-SEQ-01 | No ejecución de G6 | **PASS** |

---

## 5. Comparación de las 139 rutas

Se reconstruyó independientemente la tabla R9 §5.4 (109 filas plantilla expandidas a 139 rutas) y el mapeo de `rule_id` desde el diseño v4 §9.2 (24 filas). La comparación campo por campo contra ORACLE-ART-01 produjo `ERRORS []`. No hay rutas extra, ausentes, duplicadas ni metadatos divergentes. ORACLE-ART-05 conserva la matriz de cobertura con `path`, aplicabilidad, comportamiento esperado, resultado observado, caso, evidencia y `rule_id`.

---

## 6. ORACLE-ART-02

Inspección: archivo en `tests/`, sin `from tradingai`/`import tradingai`, sin `pytest`, entradas declaradas limitadas a ORACLE-ART-01, errores deterministas `ORACLE_VERSION_MISMATCH`, `ORACLE_INCOMPLETE`, `ORACLE_CHECKSUM_MISMATCH`. Ejecución de su función `verify()`: salida `[]`. No se incorporó a producción ni se amplió su alcance.

---

## 7. ORACLE-ART-03 y orden JCS

Recálculo independiente con `rfc8785.dumps` del objeto `{"version","entries"}` y `hashlib.sha256`: `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b`, idéntico al contenido de ORACLE-ART-03. La preimagen no incluye auxiliares, propio checksum ni hash del ejecutable.

La observación INFO de G4 se resuelve así: JCS exige orden de claves por unidades UTF-16BE, por lo que los bytes canónicos presentan las claves en orden alfabético; el orden enumerativo de los diez campos en R9 §5.8.1 es un orden lógico del modelo de datos, no una regla de serialización adicional. No se alteró JCS y se comprobó que los diez campos y sus valores están presentes y correctamente asociados a cada ruta.

---

## 8. Revisión humana independiente

No se dispone de persona revisora real. D3 aprobó un rol funcional, pero no designó identidad; G5 exige que la revisión sea realizada y que el revisor sea distinto del generador y, cuando corresponda, del ejecutor del verificador. Este agente ejecutó la verificación automatizada, por lo que no puede atribuirse la revisión humana. No se crea ORACLE-ART-04, no se inventan nombre, fecha, firma ni dictamen. El criterio se declara **BLOCKED** y G5 no se declara completado.

---

## 9. Evidencias ORACLE-ART-05, 06 y 07

| Artefacto | Estado | Evidencia / limitación |
|---|---|---|
| ORACLE-ART-05 | `CREATED_UNVERIFIED` | `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json`; SHA-256 `0cae6714d99f3f3acc6ab724577afb240f7610a6f17624effcd4f5f4dd74569f`; 139 filas únicas |
| ORACLE-ART-06 | `NOT_CREATED` | La comparación normativa exige `ALLOWLIST_V4`, ausente en `provenance_v4.py`; no se implementa en G5 |
| ORACLE-ART-07 | `NOT_CREATED` | La mutación requiere una copia aislada de `ALLOWLIST_V4`; no se simula ni modifica código |

No se aceptaron resultados parciales como cobertura completa.

---

## 10. Inventario actualizado

| Artefacto | Estado |
|---|---|
| ORACLE-ART-01 | `VERIFIED` — verificación independiente documentada sin errores |
| ORACLE-ART-02 | `VERIFIED` — inspección y `verify()` sin errores |
| ORACLE-ART-03 | `VERIFIED` — checksum recalculado y coincidente |
| ORACLE-ART-04 | `NOT_CREATED` — revisión humana no realizada |
| ORACLE-ART-05 | `CREATED_UNVERIFIED` — evidencia generada; pendiente de revisión independiente |
| ORACLE-ART-06 | `NOT_CREATED` — dependencia `ALLOWLIST_V4` no disponible |
| ORACLE-ART-07 | `NOT_CREATED` — dependencia `ALLOWLIST_V4` no disponible |

---

## 11. Comandos, entradas y salidas

| Herramienta | Uso | Salida |
|---|---|---|
| `git rev-parse`, `git branch`, `git ls-remote`, `git status`, `git diff --cached`, `git diff --stat`, `git diff --check` | Estado y procedencia | HEAD `259ca6ee…`, `main`, alineado; sin staged/diff; exit 0 |
| `git hash-object`, `Get-FileHash` | Hashes de referencias y artefactos | Todos coincidentes con §1 |
| Script de verificación independiente (temporal, eliminado) | Reconstruir R9 §5.4 y diseño §9.2; comparar 139 entradas y recalcular checksum | `ERRORS []`, checksum coincidente |
| `python -c` con import de `tests/oracle_normative_v4_r5_verifier.py` | Ejecutar `verify()` | `[]` |
| Lectura de `provenance_v4.py` | Comprobar ausencia de `ALLOWLIST_V4` | Sin coincidencias |

No se ejecutaron pruebas de software, fingerprints de producción ni mutación. No se accedió a Parquet protegidos.

---

## 12. Limitaciones y hallazgos

**Hallazgos bloqueantes:**

1. `G5-IN-02`/`G5-ART04-01`: no hay revisor humano real designado; no se fabrica ORACLE-ART-04.
2. `G5-ART06-01`: `ALLOWLIST_V4` no existe; no se puede comparar nueve metadatos.
3. `G5-ART07-01`: sin `ALLOWLIST_V4` no se puede ejecutar la mutación controlada.

**Limitación de evidencia:** los informes de auditoría independiente no están como archivos del repositorio; constan en el registro de trabajo. Los documentos de aprobación registran sus resultados con hash verificable, pero no sustituyen a los informes originales.

**Riesgos:** G6 no ejecutado; AUD-R8-02 sigue `OPEN`; Fase C sin autorización de implementación.

---

## 13. Estado Git inicial y final

| Momento | HEAD | Rama / remoto | Estado |
|---|---|---|---|
| Inicial | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Sin staged ni diff; `diff --check` exit 0 |
| Final | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Nuevos: ORACLE-ART-05 y este informe; sin staged ni diff; `diff --check` exit 0 |

Sin commits ni push; índice Git sin cambios.

---

## 14. Dictamen final de G5

```text
G0_STATUS: PASSED
G1_STATUS: PASSED
G2_STATUS: PASSED
G3_STATUS: PASSED
G4_STATUS: PASSED
G5: BLOCKED
G5_STATUS: BLOCKED
G5_COMPLETED: NO
ORACLE-ART-01: VERIFIED
ORACLE-ART-02: VERIFIED
ORACLE-ART-03: VERIFIED
ORACLE-ART-04: NOT_CREATED
ORACLE-ART-05: CREATED_UNVERIFIED
ORACLE-ART-06: NOT_CREATED
ORACLE-ART-07: NOT_CREATED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

No se inicia G6. Se requieren una tarea posterior con revisor humano real designado y la representación ejecutable `ALLOWLIST_V4` para completar ORACLE-ART-04, 06 y 07. Este informe no aprueba G6 ni autoriza implementación de Fase C.

**Fin de R13-ORACLE-MATERIALIZATION-G5-EXECUTION-R1.**
