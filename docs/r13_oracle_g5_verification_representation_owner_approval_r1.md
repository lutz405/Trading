# R13-ORACLE-G5-VERIFICATION-REPRESENTATION-OWNER-APPROVAL-R1 — Aprobación de representación independiente de verificación y paquete de revisión humana

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** registro documental y preparatorio. No implementa la representación, no crea ORACLE-ART-06 ni ORACLE-ART-07, no ejecuta G5/G6 y no inicia Fase C.

---

## 1. Decisión aprobada

```text
VERIFICATION_REPRESENTATION_OWNER_APPROVAL: APPROVED
```

El propietario aprueba expresamente el uso de una representación independiente de verificación en `tests/`, destinada **exclusivamente** a producir ORACLE-ART-06 y ORACLE-ART-07.

### 1.1 Alcance aprobado

| Elemento | Término aprobado |
|---|---|
| Ubicación | `tests/` |
| Propósito exclusivo | Verificación independiente para generar ORACLE-ART-06 y ORACLE-ART-07 |
| Base normativa | R9 §5.4 y schema v4 aprobado |
| Derivación | Debe derivarse independientemente de ORACLE-ART-01 |
| Naturaleza | No constituye fuente normativa, ni código de producción, ni un octavo artefacto Oracle |
| Producto | No modifica `provenance_v4.py`, schemas ni dependencias |
| Límites | No autoriza implementación de Fase C ni G6; no modifica los estados actuales de los artefactos |

La representación debe evitar circularidad y mantener trazabilidad hacia R9 §5.4 y el schema v4 aprobado. Su derivación no puede copiarse de ORACLE-ART-01 ni convertirse en una segunda fuente normativa.

---

## 2. Separación de responsabilidades

| Capa | Contenido | Estado |
|---|---|---|
| 1. Fuente normativa | R9 §5.4, diseño v4 §9.2 y `manifest_v4.json` aprobado | Documentos aprobados; solo lectura |
| 2. Transcripción normativa | ORACLE-ART-01 (`docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json`) | `VERIFIED`; no se modifica |
| 3. Representación independiente de verificación | Futuro contenido en `tests/` | **Aprobada pero no implementada**; derivable solo de la capa 1 |
| 4. Código productivo | `src/tradingai/ml/provenance_v4.py` | Permanece intacto; sin allowlist ni fingerprints |

La representación de `tests/` no puede derivar sus reglas de ORACLE-ART-01 ni sustituir a la fuente normativa. ORACLE-ART-01, la representación de verificación y el código productivo **no son intercambiables**.

---

## 3. Paquete documental para revisión humana independiente

Este paquete prepara ORACLE-ART-04. **No declara realizada la revisión, no asigna persona, fecha, firma ni resultado y no crea ORACLE-ART-04 como artefacto completado.**

### 3.1 Alcance de revisión

Revisión semántica independiente de ORACLE-ART-01, ORACLE-ART-02, ORACLE-ART-03 y ORACLE-ART-05, conforme a D3, especificación R2 §4.4 y plan R2 §5.

### 3.2 Versiones y hashes de referencia

| Artefacto | Versión | Git hash | SHA-256 | Estado actual |
|---|---|---|---|---|
| ORACLE-ART-01 | `ORACLE_NORMATIVE_V4_R5` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `VERIFIED` |
| ORACLE-ART-02 | `ORACLE_NORMATIVE_V4_R5` | `dcdd4c09236923c296ae635662f244bc8258a068` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` | `VERIFIED` |
| ORACLE-ART-03 | `ORACLE_NORMATIVE_V4_R5` | `83a84f653a1c55579733afe89b8a4a2c2268b711` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `VERIFIED` |
| ORACLE-ART-05 | `ORACLE_NORMATIVE_V4_R5` | `5286798016d1cd5ea446e1597e300bfaf8daab25` | `0cae6714d99f3f3acc6ab724577afb240f7610a6f17624effcd4f5f4dd74569f` | `CREATED_UNVERIFIED` |

Fuentes: análisis R1 (`00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7`), plan R2 (`d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0`) y especificación R2 (`0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e`).

### 3.3 Checklist de diez requisitos

| # | Requisito | Registro pendiente |
|---|---|---|
| 1 | Designación funcional del revisor por el propietario | Vacío; completar solo con designación real |
| 2 | Independencia del revisor respecto de generador y ejecutor del verificador | Declaración pendiente |
| 3 | Versión revisada coincidente con la fuente aprobada | `ORACLE_NORMATIVE_V4_R5` |
| 4 | Checksum revisado | `7c9c49a5…300b300b` |
| 5 | Alcance: 139 rutas, diez campos, `rule_id` separado, P1–P5, I1–I12, exclusiones y fail-closed | Casos por completar |
| 6 | Casos examinados | Lista pendiente |
| 7 | Hallazgos y resolución | Registro pendiente |
| 8 | Dictamen estructurado | Pendiente; sin firma criptográfica salvo decisión aprobada |
| 9 | Fecha real y referencia de evidencia | Pendiente |
| 10 | Evidencia de aprobación | Pendiente |

### 3.4 Procedimiento para registrar hallazgos

1. Identificar artefacto, versión, ruta/campo y caso examinado.
2. Describir el hallazgo con evidencia reproducible.
3. Clasificar severidad y determinar si bloquea.
4. Registrar resolución o escalamiento; no corregir silenciosamente el artefacto.
5. Conservar el registro con fecha real y referencia de evidencia.

### 3.5 Criterios de dictamen

- **Favorable:** los diez requisitos están documentados, no hay hallazgos bloqueantes y la independencia es verificable.
- **Desfavorable:** existe discrepancia no resuelta, revisión no independiente, evidencia incompleta o hallazgo bloqueante.
- La mera existencia de este paquete **no** equivale a revisión realizada ni a dictamen favorable.

### 3.6 Campos para la revisión futura

| Campo | Estado |
|---|---|
| Rol funcional del revisor | Pendiente de designación real |
| Identidad real del revisor | Pendiente; no inventar |
| Fecha real | Pendiente; no inventar |
| Referencia de evidencia | Pendiente |
| Declaración de independencia | Pendiente |
| Dictamen | Pendiente |

---

## 4. Estado de autorizaciones

```text
VERIFICATION_REPRESENTATION_OWNER_APPROVAL: APPROVED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La aprobación cubre exclusivamente la representación independiente descrita. La materialización de los siete artefactos continúa sujeta al plan R2 y sus gates. La implementación de producción sigue sin autorización; Fase C sigue bloqueada; G5 sigue `BLOCKED` hasta completar revisión humana, ORACLE-ART-06 y ORACLE-ART-07; G6 sigue `NOT_STARTED`. Los estados actuales de ORACLE-ART-01…07 no se modifican.

---

## 5. Trazabilidad

| Elemento | Referencia |
|---|---|
| Análisis de bloqueos R1 | `docs/r13_oracle_g5_blocker_resolution_analysis_r1.md` (`ebe75a481…844f`) |
| Alternativa A aprobada | Análisis R1 §3.4 y §6 |
| Checklist de revisión | Análisis R1 §4 |
| Evaluación ORACLE-ART-05 | Análisis R1 §5 |
| Plan de materialización | `docs/r13_oracle_artifacts_materialization_plan_r2.md` §§5, 8 |
| Especificación Oracle | `docs/r13_oracle_artifacts_specification_r2.md` §§4.1–4.7 |
| Decisiones D1–D6 | `docs/r13_oracle_artifacts_decision_resolution_r2.md` y su aprobación |
| Autorización vigente | `docs/r13_oracle_artifacts_materialization_authorization_r2.md` |

---

## 6. Estado Git y cierre

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni unstaged antes de este registro. `git diff --check`: exit 0. Sin commits ni push.

No se implementó la representación en `tests/`, no se crearon ORACLE-ART-06 ni ORACLE-ART-07, no se modificaron ORACLE-ART-01…05, código productivo, schemas, dependencias ni datasets, no se ejecutaron G5/G6 ni pruebas, y no se accedió a Parquet protegidos.

**Fin de R13-ORACLE-G5-VERIFICATION-REPRESENTATION-OWNER-APPROVAL-R1.**
