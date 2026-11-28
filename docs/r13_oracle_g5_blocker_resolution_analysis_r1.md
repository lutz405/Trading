# R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1 — Análisis de bloqueos de G5 y propuesta correctiva

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** análisis técnico y documental. No ejecuta correcciones, no reintenta G5, no inicia G6 ni Fase C.
**Estado:** `G5_STATUS: BLOCKED`; `G6_STATUS: NOT_STARTED`; `AUD_R8_02: OPEN`.

---

## 1. Diagnóstico individual de los tres bloqueos

### Bloqueo A — Revisión humana independiente (ORACLE-ART-04)

**Causa.** G5 exige como entrada `revisión humana realizada` (plan R2 §8) y ORACLE-ART-04 exige una revisión semántica real por persona distinta del generador y, cuando corresponda, del ejecutor del verificador (especificación R2 §4.4, D3 aprobado). No existe persona revisora designada con identidad real. No se inventó nombre, fecha, firma ni dictamen.

**Estado actual.** ORACLE-ART-04: `NOT_CREATED`. Criterio G5-ART04-01: `BLOCKED`.

**Consecuencia.** No puede emitirse el dictamen exigido por la salida de G5 (`Evidencia de verificación y dictamen`). G5 no puede declararse completado.

### Bloqueo B — Ausencia de representación ejecutable `ALLOWLIST_V4`

**Causa.** `src/tradingai/ml/provenance_v4.py` es validación estructural de Fase B; no contiene `ALLOWLIST_V4`, `project_allowlist` ni `build_run_fingerprint`. Las búsquedas no producen coincidencias. El plan R2 §3 sitúa la representación ejecutable en `provenance_v4.py`, pero su implementación pertenece a Fase C, que está `NOT_GRANTED`. Sin esa representación no pueden ejecutarse la comparación de nueve metadatos (ORACLE-ART-06) ni la mutación `external_run_only` (ORACLE-ART-07).

**Estado actual.** ORACLE-ART-06 y ORACLE-ART-07: `NOT_CREATED`.

**Consecuencia.** Dos verificaciones normativas de G5 carecen de entrada ejecutable. No se implementó código de producción ni se simuló la representación dentro del verificador.

### Bloqueo C — ORACLE-ART-05 no alcanza `VERIFIED`

**Causa.** La matriz generada contiene 139 rutas únicas y reproduciblemente derivadas, pero sus columnas no cubren íntegramente los requisitos de la especificación R2 §4.5: no incorpora un identificador de caso positivo/negativo por ruta, y la correspondencia con el oracle se limita a `rule_id`, sin columna explícita de valor del oracle frente al valor observado. Además, `observed_result = MATCH_R9_5_4` se deriva de la misma fuente usada para construir ORACLE-ART-01 (R9 §5.4), por lo que no constituye comparación independiente contra el oracle.

**Estado actual.** ORACLE-ART-05: `CREATED_UNVERIFIED`.

**Consecuencia.** La cobertura cuantitativa está demostrada; la cobertura semántica independiente exigida para `VERIFIED` no lo está.

---

## 2. Referencias normativas y hashes

| Documento | Git hash verificado | SHA-256 verificado |
|---|---|---|
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `e37dfdae0663502e89cb522ca8605eb2791c828e` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` |
| `docs/r13_oracle_artifacts_specification_r2.md` | `5179cad31e0a640837c785a8516bc46b126e4ea3` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` |
| `docs/r13_phase_c_design_r9.md` | `d21de0f112329ad9a9c30f167189a1f81ecef685` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` |
| `docs/r13_oracle_artifacts_decision_resolution_owner_approval_r1.md` | `432084a4baead2a5ad84d4d43c158f8bc3dc7731` | `46b99d54b4f043c74f04a83d2f633367fef6b2a9ec90e62e8336b0b9d0cffbd8` |
| `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `33693367f38ca579864d5ea98ebb8aa63918011d` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` |
| `docs/r13_oracle_materialization_g5_execution_r1.md` | `445ec10bda5c34720298c606024fa7b350d9575c` | `0cbb980301422a030061ffa84846a211b85a0c49fd8736e225e3677ff1be4f02` |
| `src/tradingai/ml/provenance_v4.py` | — | `3216d8919a82e61ff4c1fba238f130ce2283e2c363e46c315114042c002c8a6b` |

**Artefactos existentes (states y hashes conservados):**

| Artefacto | Git hash | SHA-256 | Estado |
|---|---|---|---|
| ORACLE-ART-01 | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `VERIFIED` |
| ORACLE-ART-02 | `dcdd4c09236923c296ae635662f244bc8258a068` | `a67bf35a70b5b4d0a591245f4b05c9d990c106c5fa51bc0666b27d2299f48c5f` | `VERIFIED` |
| ORACLE-ART-03 | `83a84f653a1c55579733afe89b8a4a2c2268b711` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `VERIFIED` |
| ORACLE-ART-04 | — | — | `NOT_CREATED` |
| ORACLE-ART-05 | `5286798016d1cd5ea446e1597e300bfaf8daab25` | `0cae6714d99f3f3acc6ab724577afb240f7610a6f17624effcd4f5f4dd74569f` | `CREATED_UNVERIFIED` |
| ORACLE-ART-06 | — | — | `NOT_CREATED` |
| ORACLE-ART-07 | — | — | `NOT_CREATED` |

---

## 3. Análisis de `ALLOWLIST_V4`

### 3.1 Dónde se define en R9

- **Autoridad normativa:** R9 §5.4 (tabla de 109 filas plantilla, 139 rutas expandidas) y diseño v4 §9.2 (24 reglas normativas). R9 §5.8.1 fija los diez campos del oracle y la preimagen del checksum.
- **Representación ejecutable prevista:** R9 §5.8.5 y plan R2 §3 la sitúan en `provenance_v4.py` como único listado usado por Fase C.
- **Transcripción verificada:** ORACLE-ART-01 es la representación normativa independiente; no es la representación ejecutable ni código de producción.

### 3.2 Relación entre representaciones

| Representación | Naturaleza | Ubicación/estado | No intercambiable con |
|---|---|---|---|
| Normativa | R9 §5.4 + diseño §9.2 | Documentos aprobados | Código ejecutable |
| Ejecutable de verificación | Estructura de datos para comparar los nueve metadatos y mutar `external_run_only` | **No existe**; propuesta: área de pruebas/CI | ORACLE-ART-01 (transcripción) y producción |
| Código de producción | Validación Fase B en `provenance_v4.py` | Existe; sin allowlist ni fingerprints | Oracle de verificación |

ORACLE-ART-01 no puede sustituir a `ALLOWLIST_V4` en la comparación de ORACLE-ART-06 sin crear circularidad: ambos derivarían de la misma tabla normativa. Para evitarla, la representación de verificación debe construirse desde R9 §5.4 y el schema v4 con un procedimiento independiente de la generación de ORACLE-ART-01, o bien compararse contra ORACLE-ART-01 con auditoría de independencia documentada.

### 3.3 Por qué no existe actualmente

`provenance_v4.py` declara explícitamente en su docstring que **no** compute JCS/fingerprints (Fase C). No hay constantes `ALLOWLIST_V4`, ni funciones `project_allowlist` o `build_run_fingerprint`. Los tests v4 solo validan esquema y dispatch; no hay allowlist ejecutable. Implementarla en producción correspondería a Fase C, cuyo estado es `NOT_GRANTED`. Por tanto, G5 no puede crearla modificando producción.

### 3.4 Alternativas técnicas

| Alternativa | Ventajas | Riesgos | Compatibilidad |
|---|---|---|---|
| **A. Representación de verificación en `tests/`**, derivada de R9 §5.4 y schema, separada de ORACLE-ART-01 y de producción | Sin tocar producción; compatible con D6; permite ART-06/07 | Requiere autorización/confirmación expresa de que no es un octavo artefacto; riesgo de circularidad si se copia de ORACLE-ART-01 | Alta, si se declara como entrada de verificación y no fuente normativa |
| **B. Implementar `ALLOWLIST_V4` en `provenance_v4.py`** | Única representación ejecutable prevista por R9 | Es Fase C; no autorizada; rompe límite de G5 | **Baja** en este momento |
| **C. Derivar representación desde ORACLE-ART-01 dentro del verificador** | Rápida | Circularidad: el oracle verificaría su propia transcripción | **Baja**; no recomendable |
| **D. Postergar ART-06/07 a una tarea posterior con autorización de Fase C** | Máxima conservación de límites | G5 permanece bloqueada | Alta, pero no resuelve G5 ahora |

**Recomendación técnica:** alternativa A condicionada a confirmación del propietario de que la estructura de verificación no amplía el conjunto de siete artefactos ni se convierte en fuente normativa. La alternativa B requiere autorización separada de Fase C.

### 3.5 Comparación exacta de los nueve metadatos

Los nueve campos son (especificación R2 §4.6): `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`. `rule_id` es décimo campo de trazabilidad, no metadato comparado. La comparación debe ser fila por ruta y campo, con salida determinista, errores `ALLOWLIST_ORACLE_METADATA_DIVERGENCE` ordenados y deduplicados, sin fallback.

---

## 4. Checklist de revisión humana (ORACLE-ART-04)

| # | Elemento | Requisito verificable |
|---|---|---|
| 1 | Designación | Rol funcional designado por el propietario; identidad real registrada en el momento de la revisión |
| 2 | Independencia | Revisor distinto de quien generó ORACLE-ART-01/03/05 y de quien ejecutó el verificador; declaración documentada |
| 3 | Versión revisada | `ORACLE_NORMATIVE_V4_R5`, coincidente con ORACLE-ART-01 y con la fuente normativa aprobada |
| 4 | Checksum revisado | `7c9c49a5…300b300b`, verificado por el revisor |
| 5 | Alcance | 139 rutas, diez campos, `rule_id` separado, P1–P5, I1–I12, exclusiones y fail-closed |
| 6 | Casos examinados | Lista de casos positivos/negativos con referencia a fila y campo |
| 7 | Hallazgos | Registro de hallazgos, severidad y resolución |
| 8 | Dictamen | Texto libre estructurado: favorable/desfavorable; no firma criptográfica salvo decisión aprobada |
| 9 | Fecha y referencia | Fecha real y referencia verificable a la evidencia revisada |
| 10 | Evidencia de aprobación | Registro trazable sin inventar identidad ni resultado |

**Preparación posible antes de la persona revisora:** índice de evidencias, checklist impreso, copias de artefactos, matriz de casos y registro de hashes. **No se puede preparar** el dictamen ni la identidad real del revisor.

---

## 5. Evaluación de ORACLE-ART-05

| Aspecto | Observación |
|---|---|
| Rutas | 139 filas, 139 únicas, ordenadas por `path` |
| Columnas presentes | `path`, `applicability`, `expected_behavior`, `observed_result`, `case`, `evidence`, `rule_id` |
| Columnas exigidas por R2 §4.5 | Ruta ✓, aplicabilidad ✓, comportamiento esperado ✓, resultado observado ✓, **caso positivo/negativo ✗**, evidencia reproducible ✓, correspondencia con oracle parcial (`rule_id` solo) |
| Valores | `observed_result` uniforme `MATCH_R9_5_4`; `case` uniforme `COVERAGE_139` |
| Reproducibilidad | Alta: regenerable desde R9 §5.4; SHA-256 estable |
| Independencia | Insuficiente: `MATCH_R9_5_4` se deriva de la misma fuente usada para ORACLE-ART-01 |
| Estado | `CREATED_UNVERIFIED`; no `VERIFIED` |

**Para alcanzar `VERIFIED`:** añadir identificadores de caso positivo/negativo por fila, columna de valor del oracle frente a valor observado, comparación independiente no derivada de ORACLE-ART-01 y revisión documentada. No se modifica el artefacto original en este análisis.

---

## 6. Alternativas técnicas y secuencia correctiva

### 6.1 Secuencia propuesta

| Paso | Actividad | Clasificación de autorización |
|---|---|---|
| P0 | Preparar paquete documental de revisión (checklist, índice de evidencias, hashes) | Cubierta por autorización de materialización |
| P1 | Designación de persona revisora real por el propietario | Acto humano del propietario; no creación de artefacto |
| P2 | Revisión efectiva y generación de ORACLE-ART-04 | Cubierta por materialización, condicionada a P1 |
| P3 | Declarar/aprobar alternativa A para representación de verificación | Requiere confirmación expresa del propietario por posible extensión de alcance |
| P4 | Construir representación de verificación desde R9 §5.4 y schema, independiente de ORACLE-ART-01 | Cubierta si P3 es aprobada; prohibida si se hace en producción |
| P5 | Generar y verificar ORACLE-ART-06 (nueve metadatos) | Cubierta tras P4 |
| P6 | Ejecutar mutación aislada y generar/verificar ORACLE-ART-07 | Cubierta tras P4; entorno aislado |
| P7 | Completar campos de caso y correspondencia de ORACLE-ART-05 y verificarlo | Cubierta tras P2/P4 |
| P8 | Reejecutar G5 | Cubierta tras P2, P5, P6 y P7 |

### 6.2 Matriz de autorizaciones

| Actividad | Autorización vigente | Autorización adicional requerida |
|---|---|---|
| Preparar checklist e índice | Sí | No |
| Designar revisor real | Decisión del propietario | Sí, acto expreso de designación |
| Crear ORACLE-ART-04 con revisión real | Sí, tras designación | No, si la revisión es real |
| Crear representación de verificación en `tests/` | No expresamente | **Sí**, confirmación de que no es octavo artefacto |
| Modificar `provenance_v4.py` | No | **Sí**, autorización de Fase C |
| Generar ORACLE-ART-06/07 | Sí, tras representación aprobada | No, si P3 aprobada |
| Completar ORACLE-ART-05 | Sí | No |
| Reejecutar G5 | Sí, tras resolver bloqueos | No |
| Iniciar G6 | No | Sí, revisión y aprobación de G5 |

No se asume que una modificación de producción está autorizada.

---

## 7. Riesgos y criterios de aceptación

| Riesgo | Criterio de aceptación para mitigarlo |
|---|---|
| Circularidad oracle/verificador | Representación de verificación construida desde R9 §5.4 y schema, no copiada de ORACLE-ART-01 |
| Octavo artefacto encubierto | Declaración expresa de que la estructura de verificación es entrada técnica, no artefacto Oracle |
| Revisión ficticia | Identidad real, fecha real y hallazgos documentados; ausencia ⇒ ORACLE-ART-04 `NOT_CREATED` |
| Mutación no aislada | Copia controlada, sin tocar producción ni fuentes normativas |
| Cobertura parcial presentada como completa | Casos positivo/negativo por fila y correspondencia explícita con oracle |
| Divergencia de hash | Recálculo independiente antes de cada reejecución de G5 |

---

## 8. Recomendación técnica final

1. No reintentar G5 hasta que exista revisor humano real y representación de verificación aprobada.
2. Preparar P0 sin tocar artefactos; no fabricar ORACLE-ART-04.
3. Solicitar al propietario: (a) designación de revisor, (b) confirmación de la alternativa A para la representación de verificación.
4. Mantener Fase C y G6 sin iniciar; no modificar `provenance_v4.py`.
5. Conservar los hashes y estados actuales; toda corrección futura debe auditarse.

---

## 9. Estados finales obligatorios

```text
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

Este análisis no corrige bloqueos, no reejecuta G5, no inicia G6 ni autoriza Fase C.

**Fin de R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1.**
