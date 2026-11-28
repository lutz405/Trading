# R13-ORACLE-ARTIFACTS-SPECIFICATION-R3 — Especificación Oracle (enmienda de ART-04)

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** **propuesta documental**. No aprobada; pendiente de auditoría independiente y aprobación expresa.

```text
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
```

---

## 1. Versión anterior conservada y alcance

| Dato | Valor |
|---|---|
| Documento de origen | `docs/r13_oracle_artifacts_specification_r2.md` |
| SHA-256 de R2 | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| Git hash de R2 | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| Habilitación | `docs/r13_oracle_art_04_ai_review_owner_decision_registration_r1.md`, SHA-256 `3b6c946ec6f54511d066159f6408f6b8914bb01eb87d94f453b60d6ff0641726` |

R2 se conserva **íntegramente**. R3 modifica **exclusivamente** la sección 4.4 (ORACLE-ART-04) y las consecuencias estrictamente necesarias de las secciones 5 y 6. Las secciones 1, 2, 3, 4.1, 4.2, 4.3, 4.5, 4.6, 4.7 y 7 permanecen con el contenido de R2.

**El conjunto sigue siendo de siete artefactos.** No se crea un octavo artefacto ni se altera la semántica de ART-01/02/03/05/06/07.

---

## 2. Jerarquía normativa

Sin cambios respecto a R2 §2. La autoridad es DEC-06 y el diseño v4 §9.2, con el contrato estructural `manifest_v4.json`. La modalidad de revisión no altera esa jerarquía: una IA revisora **no es fuente normativa** y sus conclusiones no sustituyen a §9.2, R9 §5.4 ni al schema.

---

## 3. ORACLE-ART-04-R3 — Registro de revisión independiente

### 3.1 Identidad y naturaleza

| Campo | Especificación R3 |
|---|---|
| Identificador estable | `ORACLE-ART-04` |
| Propósito | Evidenciar que la transcripción normativa fue revisada independientemente contra §9.2 por un agente distinto del generador |
| Fuente normativa | R9 §5.8.1 y §5.8.5; D3-R3; decisiones `DEC-OWNER-AI-01…06` |
| Modalidades admitidas | `HUMAN_INDEPENDENT_REVIEW` (preferente) e `INDEPENDENT_AI_REVIEW` (excepcional, solo ART-04) |
| Estado en esta propuesta | `NOT_CREATED` |

**La revisión por IA nunca se denomina revisión humana.** Todo registro debe consignar literalmente la modalidad utilizada.

### 3.2 Diferencia entre modalidades

| Aspecto | `HUMAN_INDEPENDENT_REVIEW` | `INDEPENDENT_AI_REVIEW` |
|---|---|---|
| Agente | Persona real, funcionalmente independiente | Sistema de IA de terceros |
| Base | Juicio semántico humano | Reconstrucción independiente + comprobaciones reproducibles |
| Dictamen | Favorable/desfavorable estructurado | `ACCEPTED`/`ACCEPTED_WITH_FINDINGS`/`REJECTED`/`INCONCLUSIVE` |
| Autoridad de aceptación | Propietario | Propietario (el dictamen IA es solo técnico) |
| Auditoría posterior | Auditoría del registro | Auditoría del registro **y** del informe de la IA |
| ¿Sustituye a la otra? | No | No; es una excepción acotada por D3-R3 |

### 3.3 Contenido mínimo obligatorio

El registro de ART-04 debe contener:

1. identificador de revisión y **modalidad** (`HUMAN_INDEPENDENT_REVIEW` o `INDEPENDENT_AI_REVIEW`);
2. identidad funcional del revisor (rol designado; en IA: proveedor, modelo y versión disponible, sin nombre inventado);
3. declaración de independencia y de limitaciones;
4. versión revisada (`ORACLE_NORMATIVE_V4_R5`) y hashes verificados de las fuentes;
5. alcance: 139 rutas, 24 `rule_id`, nueve metadatos, ART-02, tipos, condiciones, nulabilidad y normalización;
6. casos examinados, con matriz verificable y resultados positivos/negativos;
7. hallazgos con ID, severidad, fuente normativa, comprobación, resultado y resolución;
8. dictamen y, si aplica, confirmación de severidades por el auditor posterior;
9. fecha real de la revisión y referencia a la evidencia original;
10. evidencia de aprobación del propietario, registrada por separado.

### 3.4 Evidencias obligatorias de la revisión IA

- proveedor y modelo distintos del generador, con declaración de linaje;
- sesión limpia, sin conclusiones previas del generador en el contexto inicial;
- prompt completo y hash de todos los archivos de entrada;
- registro íntegro de respuestas, parámetros de generación e inventario de herramientas;
- artefacto hashable de reconstrucción independiente de reglas, anterior a la comparación;
- matriz **139 rutas × 9 metadatos** con esperado, observado y resultado por celda;
- tabla de discrepancias con trazabilidad por conclusión;
- auditoría separada del informe de la IA, a cargo de un rol distinto.

Dos ejecuciones del mismo modelo **no** constituyen independencia suficiente.

### 3.5 Dictámenes y severidades

Solo se admiten `ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED` e `INCONCLUSIVE`. La escala de severidad es `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

- `ACCEPTED`: todas las comprobaciones reproducidas sin discrepancias y sin limitaciones que afecten independencia o reproducibilidad.
- `ACCEPTED_WITH_FINDINGS`: solo hallazgos `MEDIUM`/`LOW`/`INFO` resueltos y verificados.
- `REJECTED`: contradicción normativa, discrepancia bloqueante o dependencia circular demostrada.
- `INCONCLUSIVE`: evidencia insuficiente, versión no disponible, contradicción no resuelta o independencia no demostrable.

**`INCONCLUSIVE` y `REJECTED` no pueden sustentar ART-04.** `ACCEPTED_WITH_FINDINGS` no puede hacerlo mientras existan hallazgos `BLOCKER`/`HIGH` sin resolver. Ningún dictamen equivale a aprobación del propietario.

### 3.6 Relación con ART-01, ART-02 y ART-03

- ART-01 es el **objeto revisado**, no la fuente de los esperados.
- ART-02 se verifica contra la reconstrucción independiente de §9.2/R9 §5.4/schema; la comparación ART-01 ↔ ART-02 es secundaria y nunca prueba de corrección mutua.
- ART-03 se verifica por recálculo JCS/SHA-256 independiente; un hash correcto **no** demuestra corrección semántica.
- Dependencias declaradas: ART-01, ART-02, ART-03. No se crea dependencia de ART-04 sobre ART-05/06/07 que altere sus criterios.

### 3.7 Criterios de aceptación

Revisión ejecutada y documentada; modalidad correctamente etiquetada; independencia demostrada o limitación resuelta; hashes coincidentes; matriz y tabla de discrepancias completas; hallazgos bloqueantes resueltos; auditoría separada favorable; dictamen `ACCEPTED` o `ACCEPTED_WITH_FINDINGS` conforme a §3.5; fecha real; aprobación expresa del propietario.

### 3.8 Condiciones de rechazo

Registro vacío o plantilla sin revisión; revisor que es el generador o auditor que es la IA revisora; afirmación de revisión humana cuando se usó IA; ausencia de evidencia hashable; `INCONCLUSIVE`/`REJECTED`; hallazgos `BLOCKER`/`HIGH` sin resolver; fecha o dictamen no verificables; modificación de las fuentes auditadas.

---

## 4. Matriz consolidada de aceptación

La tabla siguiente reproduce la línea base de R2 §5; **solo la fila ART-04 se sustituye**. Los estados mostrados son los declarados en R2 como línea base histórica; los estados corrientes se rigen por los registros de verificación correspondientes.

| Artefacto | Requisitos clave (R2, sin cambios salvo ART-04) | Criterio de aceptación | Verificación independiente | Dependencias |
|---|---|---|---|---|
| ORACLE-ART-01 | 139 rutas, diez campos, P1–P5, I1–I12 | Revisión semántica contra §9.2 | Revisor distinto del generador | — |
| ORACLE-ART-02 | Independiente, determinista, reproducible | Auditoría de independencia y resultados | Ejecución aislada | 01 |
| ORACLE-ART-03 | JCS y SHA-256 | Recálculo independiente | Verificador distinto | 01, 02 |
| **ORACLE-ART-04 (R3)** | Registro de revisión independiente con modalidad explícita, evidencias de §3.4, severidades y auditoría separada | Revisión real y documentada; §3.7 | Auditoría del registro **y del informe IA** si aplica | 01, 02, 03 |
| ORACLE-ART-05 | 139 filas con semántica por ruta | Cobertura completa y correcta | Comparación de conjuntos | 01, 02 |
| ORACLE-ART-06 | Nueve metadatos por ruta | Sin divergencia no reportada | Comparación campo por campo | 01, 02, 05 |
| ORACLE-ART-07 | Mutación aislada de `external_run_only` | Detección por oracle en tres rutas | Revisión de antes/después | 01, 02, 06 |

No se altera el número de artefactos ni la dependencia de los otros seis.

---

## 5. Independencia y circularidad

Se mantienen los controles de R2 §6 y se añade:

| Riesgo nuevo | Control exigido |
|---|---|
| IA que repite conclusiones del generador | Sesión limpia, fuentes originales, sin dictámenes previos en contexto, artefacto de reconstrucción hashable |
| Dictamen IA tomado como aprobación | Autoridad de aceptación reservada al propietario |
| Auditor dependiente de la IA revisora | Rol distinto, evaluación a ciegas, herramientas deterministas |
| Hash correcto interpretado como corrección semántica | Revisión semántica obligatoria; el hash solo demuestra integridad |
| Excepción extendida a otros artefactos | Alcance limitado a ORACLE-ART-04 en D3-R3 y autorización R3 |

---

## 6. Trazabilidad y versiones

R1 → R2 (sha `0ede7956…`) → **R3 (propuesta)**. Las versiones anteriores permanecen intactas. La adopción de R3 requiere auditoría independiente y aprobación expresa del propietario. Las decisiones aprobadas y los hallazgos de auditoría se vinculan en el protocolo R2 §14.

---

## 7. Estados y límites

```text
OWNER_DECISIONS: APPROVED
NORMATIVE_AMENDMENTS: PREPARED_PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

Esta propuesta **no** aprueba la modalidad, **no** crea ART-04, **no** altera los otros seis artefactos, **no** autoriza Fase C ni modifica R2.

**Fin de R13-ORACLE-ARTIFACTS-SPECIFICATION-R3.**
