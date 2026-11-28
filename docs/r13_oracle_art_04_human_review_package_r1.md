# R13-ORACLE-ART-04-HUMAN-REVIEW-PACKAGE-R1 — Expediente de revisión humana independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** expediente documental preparatorio. **No** contiene una revisión realizada, **no** asigna revisor, **no** emite dictamen y **no** crea ORACLE-ART-04.

---

## 1. Propósito y estado

Preparar un paquete completo para que una **persona real e independiente** revise semánticamente ORACLE-ART-01 contra las fuentes normativas y, si procede, emita ORACLE-ART-04 en una tarea posterior.

| Hito | Estado actual |
|---|---|
| Expediente preparado | **SÍ — este documento** |
| Revisión humana pendiente | **SÍ** |
| Revisión humana completada | **NO** |
| ORACLE-ART-04 materializado | **NO** |
| ORACLE-ART-04 verificado | **NO** |

No se permite interpretar la existencia de este expediente como revisión realizada ni como aprobación.

---

## 2. Fuentes y hashes verificados

| Fuente | Git hash verificado | SHA-256 verificado |
|---|---|---|
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `83a84f653a1c55579733afe89b8a4a2c2268b711` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` |
| `docs/r13_oracle_artifacts_specification_r2.md` | `5179cad31e0a640837c785a8516bc46b126e4ea3` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `e37dfdae0663502e89cb522ca8605eb2791c828e` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| `docs/r13_phase_c_design_r9.md` | `d21de0f112329ad9a9c30f167189a1f81ecef685` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| `src/tradingai/schemas/manifest_v4.json` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` |
| `docs/aud04b_model_provenance_v4_design.md` (§9.2) | `fbe7215c5199c418e16f6968fb4b662427f8d70a` | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` |

Los hashes coinciden con los esperados. El revisor debe recalcularlos personalmente antes de iniciar.

---

## 3. Instrucciones críticas para el revisor

1. **No aceptar automáticamente** los resultados producidos por OpenCode, el verificador `tests/oracle_normative_v4_r5_verifier.py`, la representación independiente en `tests/`, ni las auditorías previas. Son evidencia auxiliar, no autoridad para la revisión humana.
2. La autoridad normativa es R9 §5.4, diseño v4 §9.2 y `manifest_v4.json`. ORACLE-ART-01 es el **objeto revisado**, no la fuente.
3. Verificar personalmente cada apartado de §4 y registrar evidencia reproducible.
4. No completar la plantilla de §5 hasta que la revisión haya sido ejecutada por una persona real.
5. No inventar nombre, rol, fecha, firma, hallazgo ni dictamen.
6. La identidad real se registra en ORACLE-ART-04 en el momento de la revisión; el rol funcional debe ser designado por el propietario conforme a D3.
7. El revisor debe ser distinto de quien generó ORACLE-ART-01, ORACLE-ART-03 y de quien ejecutó el verificador.
8. Ante duda o dato incompleto: **fail-closed**. No marcar conformidad por omisión.

---

## 4. Guía de revisión independiente

### 4.1 Correspondencia con R9 §5.4

| Comprobación | Qué verificar | Evidencia a registrar |
|---|---|---|
| Filas y expansión | 109 filas plantilla → 139 rutas expandidas (`train`, `validation`, `calibration`, `test`) | Conteo y lista de rutas |
| Metadatos | Nueve campos por entrada: `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization` | Campos presentes y valores |
| Condiciones | `always`, `external_run_only`, `partition == 'calibration'` aplicados correctamente | Casos por condición |
| Proyección | `base_*` incluidas solo con `external_run_only`; `shared_with` solo en calibration | Casos positivos/negativos |

### 4.2 Correspondencia con diseño v4 §9.2

- 24 filas normativas enumeradas en §9.2.
- 13 `rule_id` utilizados por las 139 rutas de la allowlist.
- 11 `rule_id` restantes corresponden a reglas de exclusión: identidad de salida, localizadores, `producer.command`, `data.snapshot_uri`, resultados derivados, digests, `artifacts`, `metrics`, `extensions`.
- Comprobar que cada `rule_id` de ORACLE-ART-01 apunta a la fila correcta y que ninguna ruta queda sin regla.

### 4.3 Correspondencia con `manifest_v4.json`

- Resolver rutas raíz y anidadas en `properties`; resolver `validation.partitions.<par>` vía `$defs/partition` y `$defs/calibration_partition`.
- Verificar `required`, `additionalProperties:false`, tipos y uniones con `null`.
- Confirmar que `shared_with` es obligatorio en calibration y prohibido en las otras tres particiones.
- Contrastar nulabilidad y tipos con los campos `nullable` y `type` de ORACLE-ART-01.

### 4.4 Cobertura de 139 rutas

- 139 rutas únicas, sin duplicados ni rutas desconocidas.
- Ninguna ruta normativa omitida; ninguna añadida.
- Compartimentos `train`/`validation`/`calibration`/`test` correctamente expandidos.
- Registrar cada ruta examinada con su `rule_id`.

### 4.5 Nueve metadatos y `rule_id` separado

- `rule_id` no debe formar parte del diccionario de nueve metadatos.
- Cada entrada de ORACLE-ART-01 debe contener los diez campos, con `rule_id` como campo de trazabilidad.
- Verificar que no haya campos normativos adicionales.

### 4.6 Tipos, condiciones, nulabilidad y normalización

- Tipos permitidos: `string`, `string_decimal`, `timestamp`, `integer`, `number`, `boolean`, `array`, `object`.
- Condiciones: `always`, `external_run_only`, `partition == 'calibration'`.
- `nullable=True` solo donde el schema acepte `null`.
- `normalization=timestamp_utc_9` solo en timestamps.
- Registrar casos positivos y negativos por categoría.

### 4.7 Integridad y reproducibilidad de ORACLE-ART-03

- Recalcular `SHA-256` de `rfc8785.dumps({"version": <versión>, "entries": [<entradas ordenadas por path>]})`.
- Comparar con el contenido de `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt`.
- Comprobar que la preimagen no incluye archivos auxiliares, el propio checksum ni el hash del ejecutable.
- Registrar bytes JCS, SHA-256 calculado y SHA-256 almacenado.

### 4.8 Registro de discrepancias y evidencias

Usar la tabla:

| ID | Sección | Ruta / campo | Evidencia | Severidad | Resolución |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

No dejar filas vacías si existen hallazgos; si no los hay, registrar「Sin hallazgos」con fecha y alcance.

---

## 5. Plantilla de dictamen (completar personalmente)

```text
IDENTIFICADOR DEL REGISTRO: ORACLE-ART-04
REVISOR — ROL FUNCIONAL: [completar por el revisor]
REVISOR — IDENTIDAD REAL: [completar por el revisor]
DESIGNACIÓN POR EL PROPIETARIO: [referencia verificable, completar]
DECLARACIÓN DE INDEPENDENCIA:
  [El revisor declara personalmente si es distinto del generador de ART-01/ART-03
   y de quien ejecutó el verificador. Completar.]
FECHA REAL DE LA REVISIÓN: [completar]
VERSIÓN REVISADA: ORACLE_NORMATIVE_V4_R5
ORACLE-ART-01 SHA-256 REVISADO: [recalcular y completar]
ORACLE-ART-03 SHA-256 REVISADO: [recalcular y completar]
ALCANCE: 139 rutas, 24 rule_id normativos, 9 metadatos, tipos, condiciones,
          nulabilidad, normalización e integridad JCS/SHA-256.
CASOS EXAMINADOS: [listar o referenciar evidencia]
HALLAZGOS: [listar o "Sin hallazgos" con alcance y fecha]
RESOLUCIÓN DE HALLAZGOS: [completar]
DICTAMEN: [FAVORABLE / DESFAVORABLE — completar por el revisor]
EVIDENCIA DE APROBACIÓN: [referencia verificable]
OBSERVACIONES: [completar]
```

No se exige firma criptográfica salvo decisión aprobada posterior. La evidencia de aprobación debe ser documental y verificable.

---

## 6. Límites y estados conservados

```text
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
ORACLE-ART-04: NOT_CREATED
```

Este expediente no completa G5, no autoriza G6, no inicia Fase C y no materializa ORACLE-ART-04. No se modificaron artefactos Oracle, producción, schemas, dependencias ni datasets.

**Fin de R13-ORACLE-ART-04-HUMAN-REVIEW-PACKAGE-R1.**
