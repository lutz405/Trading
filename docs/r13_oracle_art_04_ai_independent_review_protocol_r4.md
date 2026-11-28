# R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R4 — Protocolo de revisión IA (corrección R5)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** revisión documental R5. **No aprobada ni auditada.** Estado: `PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`.

```text
AI_REVIEW_PROTOCOL_R4: PREPARED_PENDING_INDEPENDENT_AUDIT
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
```

---

## 1. Versión anterior conservada y alcance

| Dato | Valor |
|---|---|
| Documento corregido | `docs/r13_oracle_art_04_ai_independent_review_protocol_r3.md` |
| SHA-256 de R3 | `e538b144b575843ad528faf9220e1f6bffbf2f4a90710539b87032101d1e3f75` |
| Git hash de R3 | `6c972eedfbb747c00da50d28d6ef078bf57238e9` |
| Base histórica | Protocolo R2 `6a095901…`, R1 `3a01e20d…` |

R4 corrige **exclusivamente** `AUD-ANT-NEW-03` (§7 subordinado a §§8.1–8.2) y `AUD-ANT-NEW-04` (redacción de Etapa D). No se modifica el alcance de `DEC-OWNER-AI-01…06`, D1–D6, los siete artefactos, las 139 rutas, los nueve metadatos, los 24 `rule_id` ni los 15 campos.

---

## 2. Fuentes verificadas

Protocolo R3 `e538b144…`; Protocolo R1 `3a01e20d…`; resolución R2 `6f408724…`; especificación R2 `0ede7956…`; plan R2 `d4d0c689…`; autorización R2 `d692e49e…`; paquete de decisiones `5a0d7a6d…`; registro de aprobación `3b6c946e…`; R9 `884ee501…`; diseño v4 §9.2 `78addb74…`; `manifest_v4.json` `c98ef476…`.

---

## 3. Fundamento normativo y prerrequisitos operativos

Decisiones `DEC-OWNER-AI-01…06` aprobadas; D3-R5, Especificación R5, Plan R5 y Autorización R5 como versiones corregidas pendientes de auditoría y aprobación; R9 como autoridad técnica.

La aprobación del protocolo **no** es condición de entrada en vigor de la autorización R5. Es **prerrequisito operativo**: antes de ejecutar revisión bajo este protocolo deben concurrir Autorización R5 en vigor; D3-R5, Especificación R5 y Plan R5 auditados y aprobados; este protocolo aprobado y auditado; fuentes y hashes verificados.

---

## 4. Modalidades

| Modalidad | Naturaleza | ¿Sustenta ART-04? |
|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | Persona real independiente | Sí, vía preferente |
| `INDEPENDENT_AI_REVIEW` | IA de terceros | Sí, solo ART-04 y bajo este protocolo |
| `AUTOMATED_INTERNAL_VERIFICATION` | Verificadores internos | No; evidencia auxiliar |

La IA nunca se denomina revisora humana.

---

## 5. Estado de los hallazgos anteriores

Los ocho hallazgos de la auditoría del protocolo R1 tienen propuesta de cierre con estado **`PROPOSED_CORRECTION_PENDING_INDEPENDENT_AUDIT`**: `-01` (§3, §6, §12), `-02` (Resolución R5 §3.1 y este §5), `-03` (§6), `-04` (§7), `-05` (§8), `-06` (§9), `-07` (§10), `-08` (§11). Solo auditoría independiente posterior puede confirmar el cierre técnico; la aceptación final corresponde al propietario. Las referencias internas son encabezados reales; no se usan `§5.01`, `§5.02`, `§6.1` ni remisión a `§13` para `-02`.

---

## 6. Controles de independencia (DEC-OWNER-AI-04)

1. Proveedor y modelo distintos del generador, con linaje declarado.
2. Sesión limpia, sin historial previo; hash del manifiesto de apertura.
3. Fuentes normativas originales; prohibidos resúmenes del generador.
4. Sin dictámenes ni conclusiones previos en el contexto inicial; prompt íntegro con hash.
5. Hashes de todas las entradas y registro íntegro de respuestas.
6. Linaje y contexto: herramientas, parámetros y archivos leídos.
7. Reconstrucción independiente en artefacto hashable, anterior a la comparación.
8. Auditor posterior distinto del generador y de la IA, con evaluación a ciegas.
9. Limitaciones declaradas; limitación no demostrable ⇒ `INCONCLUSIVE`.

El mismo proveedor o dos ejecuciones del mismo modelo no bastan.

---

## 7. Reproducibilidad (corregido AUD-ANT-NEW-03)

Modelo con identificador y versión exacta; si no está disponible: `NO_DISPONIBLE`. **Conforme a §8.1 y §8.2 y a la Especificación R5 §3.5, la versión no disponible produce `INCONCLUSIVE` de forma incondicional.** Este §7 queda expresamente **subordinado** a §§8.1–8.2: no se admite una lectura condicional más laxa como «solo para lo que dependa de la identidad del modelo». Parámetros de generación, prompt verbatim con hash, hashes de entradas y respuestas íntegras. Las comprobaciones deterministas prevalecen; divergencia estocástica ⇒ `INCONCLUSIVE`. El auditor posterior resuelve las discrepancias, nunca la IA.

---

## 8. Dictámenes, severidades y autoridad

### 8.1 Dictámenes permitidos

| Dictamen | Criterio |
|---|---|
| `ACCEPTED` | Comprobaciones reproducidas sin discrepancias ni limitaciones; sin hallazgos abiertos |
| `ACCEPTED_WITH_FINDINGS` | Solo `MEDIUM` resuelto y `LOW`/`INFO` registrados y trazables; sin `BLOCKER`/`HIGH`; sin contradicción |
| `REJECTED` | Contradicción normativa, discrepancia bloqueante o dependencia circular |
| `INCONCLUSIVE` | Evidencia insuficiente, **versión del modelo no disponible**, contradicción no resuelta o independencia no demostrable |

### 8.2 Severidades

`BLOCKER` y `HIGH` bloquean; `MEDIUM` exige resolución documentada; `LOW` e `INFO` se registran sin bloquear. Toda limitación de independencia o reproducibilidad se clasifica al menos `HIGH`.

### 8.3 Autoridad

La IA **propone**; el auditor **evalúa y confirma** severidades; el propietario **acepta** mediante registro expreso. `INCONCLUSIVE`/`REJECTED` nunca desbloquean G5; `ACCEPTED_WITH_FINDINGS` tampoco con `BLOCKER`/`HIGH` abiertos.

---

## 9. Evidencia verificable

### 9.1 Matriz

139 rutas × 9 metadatos (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`), con esperado, observado y resultado por celda; `rule_id` separado.

### 9.2 Reconstrucción

Artefacto hashable e inmutable con reglas de §9.2/R9 §5.4/schema, anterior a la comparación; no derivado de ART-01 ni ART-02.

### 9.3 Casos

Por ruta: un positivo y cuatro negativos (ausencia, duplicación, ruta desconocida, divergencia), con error esperado y resultado.

### 9.4 Tabla de discrepancias

| ID | Ruta/campo | Severidad | Fuente normativa | Comprobación reproducible | Resultado | Resolución |
|---|---|---|---|---|---|---|

### 9.5 Vinculación

Cada conclusión → fuente normativa → comprobación reproducible → resultado verificable → entrada en la tabla.

### 9.6 Preservación de R1: 24 `rule_id` y 15 campos

| Categoría | Identificadores exactos |
|---|---|
| 13 usados | `R9-9.2-01`, `R9-9.2-03`, `R9-9.2-05`, `R9-9.2-07`, `R9-9.2-09`, `R9-9.2-10`, `R9-9.2-11`, `R9-9.2-12`, `R9-9.2-13`, `R9-9.2-14`, `R9-9.2-15`, `R9-9.2-19`, `R9-9.2-20` |
| 11 exclusión | `R9-9.2-02`, `R9-9.2-04`, `R9-9.2-06`, `R9-9.2-08`, `R9-9.2-16`, `R9-9.2-17`, `R9-9.2-18`, `R9-9.2-21`, `R9-9.2-22`, `R9-9.2-23`, `R9-9.2-24` |

15 campos mínimos (R1 §9, orden y significado conservados): 1. Identificador de revisión; 2. Modalidad; 3. Proveedor y modelo de IA; 4. Fecha real y versión del modelo, si está disponible; 5. Identidad funcional del sistema revisor; 6. Hashes de todas las fuentes revisadas; 7. Fuentes normativas utilizadas; 8. Alcance y cobertura (139 rutas, 24 `rule_id`, nueve metadatos); 9. Método de reconstrucción independiente; 10. Pruebas realizadas; 11. Resultados reproducibles; 12. Hallazgos y severidad; 13. Limitaciones; 14. Dictamen; 15. Referencia a la evidencia original de la revisión. No se inventan identificadores ni campos; `NO_DISPONIBLE` cuando falte un dato.

---

## 10. Auditoría posterior

Auditor distinto del generador y de la IA, designado funcionalmente, evaluación a ciegas. Deterministas para hashes, JCS, cobertura y comparaciones; juicio humano para identidad, versión, fecha y limitaciones. Registros separados.

---

## 11. ART-02 sin circularidad

Reconstrucción desde §9.2/R9 §5.4/schema, sin usar ART-01 ni ART-02 como esperado; ART-01 y ART-02 se comparan contra la reconstrucción; su comparación mutua es secundaria; ART-02 es alcance, no dependencia de ART-04.

---

## 12. Controles contra falsos positivos

Sin coincidencias superficiales; hash correcto ≠ corrección semántica; pruebas internas no son auditoría; sin trazabilidad normativa no se acepta conclusión; contradicción ⇒ `INCONCLUSIVE`/`REJECTED`; la IA no modifica fuentes; sin Autorización R5 en vigor la revisión no produce efecto normativo.

---

## 13. Procedimiento A–H

| Etapa | Acción | Salida |
|---|---|---|
| A | Preparación de fuentes originales | Manifiesto de fuentes |
| B | Verificación de hashes | Tabla de hashes |
| C | Reconstrucción independiente, antes de D | Artefacto hashable |
| D | Comparación de reglas reconstruidas contra **ART-01, ART-02, ART-03 y fuentes normativas**. **ART-05, ART-06 y ART-07, cuando existan, se inspeccionan como objetos de correspondencia auxiliar: no son entrada normativa ni dependencia de ART-04.** **ART-04 es el resultado de la revisión y no se compara contra sí mismo.** | Matriz y resultados |
| E | Análisis de discrepancias con severidades | Tabla de discrepancias |
| F | Integridad JCS/SHA-256 y reproducibilidad | Evidencia |
| G | Dictamen técnico propuesto | Dictamen |
| H | Limitaciones, trazabilidad y auditoría posterior | Registro completo |

El orden C antes de D es obligatorio.

---

## 14. Matriz de trazabilidad

| Decisión / hallazgo | Documento | Cláusula real |
|---|---|---|
| DEC-OWNER-AI-01 | Resolución R5, Especificación R5, Plan R5, este protocolo | §3.2 / §3.2 / §4 / §4 |
| DEC-OWNER-AI-02 | Autorización R5, este protocolo | §1–§4 / §3 |
| DEC-OWNER-AI-03 | Resolución R5, este protocolo | §3.1 / §5 |
| DEC-OWNER-AI-04 | Resolución R5, Especificación R5, este protocolo | §3.4 / §3.4 / §6, §10 |
| DEC-OWNER-AI-05 | Resolución R5, Especificación R5, este protocolo | §3.4 / §3.5 / §8 |
| DEC-OWNER-AI-06 | Autorización R5, Plan R5, este protocolo | §6 / §4.2 / §12 |
| AUD-AI-REV-R1-01 | Autorización R5, este protocolo | §3–§4 / §3, §6, §12 |
| AUD-AI-REV-R1-02 | Resolución R5, este protocolo | §3.1 / §5 |
| AUD-AI-REV-R1-03 | este protocolo | §6 |
| AUD-AI-REV-R1-04 | este protocolo | §7, §8 |
| AUD-AI-REV-R1-05 | este protocolo | §8 |
| AUD-AI-REV-R1-06 | Especificación R5, este protocolo | §3.3 / §9 |
| AUD-AI-REV-R1-07 | este protocolo | §10 |
| AUD-AI-REV-R1-08 | Especificación R5, este protocolo | §3.6 / §11 |

---

## 15. Comprobación interna

Realizada por el generador. **No es auditoría independiente** y no declara hallazgos cerrados. Verificado: consistencia entre los cinco documentos; D1–D6 y DEC-OWNER-AI-01…06 preservadas; jerarquía normativa intacta; siete artefactos; 139 rutas; nueve metadatos; 24 `rule_id`; 15 campos; dependencias y etapas conservadas; referencias válidas; G5 no autocerrable y G6 separado; Parquet protegidos; Fase C `NOT_GRANTED`. Resultado: propuesta coherente, pendiente de auditoría.

---

## 16. Estados y límites

```text
AI_REVIEW_PROTOCOL_R4: PREPARED_PENDING_INDEPENDENT_AUDIT
AUDIT_VERDICT_R4: INCONCLUSIVE
AUD_ANT_01_STATUS: HIGH / INCONCLUSIVE
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

No aprueba versiones, no ejecuta revisión IA, no crea ART-04, no ejecuta G5/G6, no modifica R1–R3 ni fuentes, no toca producción, tests, schemas, dependencias ni Parquet, sin commits ni push.

**Fin de R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R4.**
