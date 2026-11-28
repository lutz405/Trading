# R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R1 — Protocolo propuesto de revisión independiente por IA de terceros

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** propuesta normativa y técnica. **No** es una decisión aprobada, **no** es una revisión ejecutada y **no** autoriza la modalidad propuesta.

**DICTAMEN DE ESTA TAREA: `PREPARED_PENDING_OWNER_APPROVAL`.**

---

## 1. Propósito y estado de la propuesta

Preparar una modalidad alternativa para sustentar ORACLE-ART-04 cuando no haya revisor humano disponible, mediante una **IA de terceros** que no sea presentada falsamente como revisión humana.

| Hito | Estado actual |
|---|---|
| Protocolo propuesto | **SÍ — este documento** |
| Decisión del propietario sobre la modalidad | **PENDIENTE** |
| Modalidad `INDEPENDENT_AI_REVIEW` autorizada | **NO** |
| Revisión externa por IA ejecutada | **NO** |
| Resultado de revisión externa registrado | **NO** |
| ORACLE-ART-04 creado | **NO** |

La existencia de esta propuesta **no** desbloquea G5, **no** modifica D3 ni **no** cambia el estado de ningún artefacto.

---

## 2. Fuentes inspeccionadas y hashes verificados

Todos los hashes se recalcularon antes de usar las fuentes y coinciden con los registros previos.

| Fuente | SHA-256 | Git hash |
|---|---|---|
| `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `e37dfdae0663502e89cb522ca8605eb2791c828e` |
| `docs/r13_oracle_art_04_human_review_package_r1.md` | `1b7630c1a82405ba06df3e7b95d64e81e694f744b9e6a19a9e6cba29a9647cdc` | `7b01df60e949545b24d481cc026ee87c8400ce1e` |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `83a84f653a1c55579733afe89b8a4a2c2268b711` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` | `ec0803f2d47f4fe2a64191662018f69183bb5a2a` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | `fa812bd125b01a7a4e7a9b994b7124e1b0d6fd0a` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | `9f10594fea28152a7f651e8f8d1864b0d63f7f40` |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |

---

## 3. Decisión normativa que debe respetarse (D3)

D3 («Identidad del revisor humano independiente», decisión R2 §3.3) exige:

- revisión semántica real por revisor **distinto del generador**;
- designación de **identidad funcional** por el propietario y registro de la **identidad real** al ejecutar la revisión;
- declaración de independencia, versión y checksum revisados, casos, hallazgos resueltos, dictamen y fecha reales;
- fail-closed: sin independencia declarada, ORACLE-ART-04 se rechaza.

**Una IA no satisface D3 automáticamente.** D3 habla de «persona funcionalmente independiente»; la modalidad automatizada propuesta es una desviación que **requiere decisión expresa del propietario**. Esta tarea no modifica D3 ni ninguna otra decisión aprobada; solo documenta la discrepancia y la decisión pendiente (§12 y §13).

---

## 4. Modalidad de revisión

Se propone la modalidad **`INDEPENDENT_AI_REVIEW`**, con las siguientes distinciones obligatorias:

| Modalidad | Quién ejecuta | Naturaleza | ¿Equivale a revisión humana? | ¿Sustenta ORACLE-ART-04 hoy? |
|---|---|---|---|---|
| `HUMAN_INDEPENDENT_REVIEW` | Persona real, funcionalmente independiente, distinta del generador | Revisión semántica humana | Sí | Sí, conforme a D3 y R2 §4.4 |
| `INDEPENDENT_AI_REVIEW` | Sistema de IA de terceros, distinto del generador | Revisión técnica automatizada externa | **NO — nunca debe denominarse revisión humana** | **NO, salvo decisión expresa del propietario que la admita** |
| `AUTOMATED_INTERNAL_VERIFICATION` | Verificadores propios del repositorio | Prueba/regresión interna | No | No: es evidencia auxiliar, no revisión independiente |

Toda comunicación, registro o artefacto debe usar literalmente `INDEPENDENT_AI_REVIEW`. Queda prohibido llamarla «revisión humana», «revisor independiente» sin calificador, o presentarla como cumplimiento directo de D3.

---

## 5. Controles de independencia

Para reducir el riesgo de que la IA de terceros repita los resultados de OpenCode:

1. **Proveedor/modelo distinto** del usado por el generador, cuando sea viable; si no lo es, documentar la limitación y no afirmar independencia absoluta.
2. **No entregar inicialmente** el dictamen, conclusiones ni hallazgos del generador; entregar solo fuentes normativas y artefactos.
3. **Entregar fuentes originales:** R9 §5.4, diseño v4 §9.2, `manifest_v4.json`, R2 y artefactos bajo revisión.
4. **Solicitar reconstrucción independiente** de las reglas antes de mostrar cualquier oracle o resultado esperado.
5. **No usar ART-01 como única fuente de verdad:** ART-01 es objeto revisado; la autoridad es §9.2, R9 §5.4 y el schema.
6. **Registrar** proveedor, modelo, versión disponible, fecha real de ejecución y configuración relevante (p. ej., temperatura, contexto, herramientas habilitadas). Si la versión no está disponible, consignar «no disponible», sin inventarla.
7. **Registrar toda limitación de independencia** (mismo proveedor, sesgo de prompt, acceso a resultados previos, falta de reproducibilidad del modelo).
8. **No afirmar independencia absoluta** cuando no pueda demostrarse; en ese caso, el dictamen debe ser `INCONCLUSIVE` o `REJECTED`.

La identidad funcional del sistema revisor será designada por el propietario; no se inventa nombre, firma ni atribución humana.

---

## 6. Alcance técnico obligatorio

La revisión por IA debe cubrir, como mínimo:

- las **139 rutas** normativas expandidas;
- los **24 `rule_id`** normativos, con la distinción entre **13 utilizados** por la allowlist y **11 reglas de exclusión**;
- los **nueve metadatos** (`path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`) y su separación de `rule_id`;
- tipos, condiciones (`always`, `external_run_only`, `partition == 'calibration'`), nulabilidad y normalización;
- correspondencia con **R9 §5.4**, **diseño v4 §9.2** y **`manifest_v4.json`**;
- integridad **JCS** y **SHA-256** de **ORACLE-ART-03**;
- correspondencia de **ART-05, ART-06 y ART-07** con las reglas originales;
- detección de omisiones, duplicados, divergencias y contradicciones normativas.

La IA revisora debe **explicar cada comprobación** y proporcionar evidencia verificable (reglas reconstruidas, casos, comandos o transformaciones reproducibles), no solo un dictamen.

---

## 7. Procedimiento de revisión

| Etapa | Nombre | Acción obligatoria | Salida |
|---|---|---|---|
| A | Preparación de fuentes | Reunir fuentes normativas originales y artefactos; sin inclusiones tutoras | Manifiesto de fuentes |
| B | Verificación de hashes | Recalcular SHA-256 de todas las fuentes y comparar con §2 | Tabla de hashes |
| C | Reconstrucción independiente | Derivar reglas desde §9.2/§5.4/schema antes de consultar resultados | Reglas reconstruidas |
| D | Comparación | Contrastar reglas reconstruidas contra ART-01/03/05/06/07 | Matriz de comparación |
| E | Análisis de discrepancias | Clasificar cada discrepancia con severidad y trazabilidad | Lista de hallazgos |
| F | Integridad y reproducibilidad | Verificar JCS/SHA-256 de ART-03 y repetibilidad de comprobaciones | Evidencia de integridad |
| G | Dictamen técnico | Emitir uno de los cuatro valores permitidos con criterios verificables | Dictamen |
| H | Limitaciones y trazabilidad | Registrar proveedor, modelo, versión, fecha, configuración y límites | Registro completo |

El orden C antes de D es obligatorio; invertirlo invalida la reconstrucción independiente.

---

## 8. Dictamen permitido

Solo se admiten estos cuatro valores:

| Valor | Criterio verificable |
|---|---|
| `ACCEPTED` | Todas las comprobaciones de §6 reproducidas sin discrepancias; evidencia trazable a fuentes normativas; sin limitaciones que afecten la independencia; ningún hallazgo abierto. |
| `ACCEPTED_WITH_FINDINGS` | Comprobaciones completas con hallazgos no bloqueantes, cada uno con resolución documentada y evidencia; sin contradicción normativa; limitaciones declaradas y aceptables. |
| `REJECTED` | Discrepancia bloqueante, contradicción normativa, artefacto ausente/alterado, falsos positivos o dependencia circular demostrada. |
| `INCONCLUSIVE` | Falta evidencia, versión del modelo o información indispensable; contradicción no resuelta; independencia no demostrable; resultados no reproducibles. |

**`INCONCLUSIVE` nunca puede utilizarse para desbloquear G5.** Tampoco `ACCEPTED_WITH_FINDINGS` con hallazgos bloqueantes sin resolver. Solo `ACCEPTED` — y, si el propietario lo admite expresamente, `ACCEPTED_WITH_FINDINGS` con resolución verificada — podría sustentar una revisión, siempre después de la auditoría separada de §11.

---

## 9. Campos mínimos del registro de evidencia

El registro de la revisión externa debe contener:

1. Identificador de revisión.
2. Modalidad (`INDEPENDENT_AI_REVIEW`).
3. Proveedor y modelo de IA.
4. Fecha real y versión del modelo, si está disponible.
5. Identidad funcional del sistema revisor.
6. Hashes de todas las fuentes revisadas.
7. Fuentes normativas utilizadas.
8. Alcance y cobertura (139 rutas, 24 `rule_id`, nueve metadatos).
9. Método de reconstrucción independiente.
10. Pruebas realizadas.
11. Resultados reproducibles.
12. Hallazgos y severidad.
13. Limitaciones.
14. Dictamen.
15. Referencia a la evidencia original de la revisión (transcripción de la sesión, salida íntegra o artefacto equivalente).

No se inventan identidades, fechas, versiones, firmas ni resultados. Los campos no disponibles se marcan explícitamente como `NO_DISPONIBLE` con explicación.

---

## 10. Controles contra falsos positivos

- No aceptar coincidencias superficiales de texto o formato como prueba de corrección semántica.
- No considerar un hash correcto como prueba de corrección semántica: el hash demuestra integridad, no validez normativa.
- No considerar las pruebas automatizadas existentes (`tests/`) como evidencia independiente suficiente.
- No aceptar conclusiones sin trazabilidad directa a fuentes normativas.
- Ante una contradicción normativa, declarar `INCONCLUSIVE` o `REJECTED`; nunca `ACCEPTED`.
- No permitir que la IA modifique las fuentes que está auditando: acceso de solo lectura a artefactos y production.
- Registrar el orden de entrega de fuentes para demostrar que no se filtraron conclusiones previas.
- Rechazar dictámenes que no puedan reproducirse con la evidencia original conservada.

---

## 11. Revisión posterior obligatoria

El informe de la tercera IA debe someterse a una **auditoría técnica separada** antes de cualquier efecto normativo. Esa auditoría debe verificar, manualmente o con herramientas reproducibles:

- que los hashes del informe corresponden a las fuentes reales;
- que la reconstrucción de reglas es anterior a la comparación (etapa C antes de D);
- que el proveedor/modelo/versión y la fecha son reales y verificables;
- que los 139 casos están cubiertos individualmente, no solo por contadores;
- que cada hallazgo tiene resolución documentada;
- que no se filtraron los dictámenes del generador;
- que la modalidad fue etiquetada `INDEPENDENT_AI_REVIEW` y no como revisión humana;
- que el dictamen es uno de los cuatro permitidos y que `INCONCLUSIVE` no se usa para desbloquear.

**La aceptación de este protocolo no equivale a la aceptación de una revisión concreta.** Cada revisión requiere su propia auditoría y su propio registro.

---

## 12. Compatibilidad normativa y cambios necesarios

| Elemento | Situación actual | Compatibilidad de `INDEPENDENT_AI_REVIEW` | Cambio normativo necesario |
|---|---|---|---|
| **D3** | Revisor humano, identidad funcional designada e identidad real al ejecutar | **Incompatible tal como está redactada** | Nueva decisión del propietario que admita expresamente revisor automatizado, o enmienda controlada de D3 con versión nueva |
| **ORACLE-ART-04** | Registro de revisión humana independiente, `NOT_CREATED` | No puede emitirse como revisión humana | Definir que el registro consigne modalidad `INDEPENDENT_AI_REVIEW` y no «revisión humana» |
| **R2 §4.4** | Exige «persona funcionalmente independiente»; fecha real de revisión; dictamen favorable | **Incompatible sin cambio** | Revisar §4.4 para incluir modalidad automatizada, campos de proveedor/modelo/versión y fecha real de ejecución |
| **R2 §3.1** | Estados `NOT_CREATED`/`CREATED_UNVERIFIED`/`VERIFIED`/`REJECTED` | Compatible en estados, no en origen de la evidencia | Precisar que `VERIFIED` puede sustentarse en revisión por IA solo si hay decisión habilitante |
| **G0–G4** | Ejecutados y `PASSED` | Sin impacto directo | Ninguno |
| **G5** | Exige «revisión humana realizada» y evidencia de verificación | **Bloqueante** | Reformular el criterio de G5 para admitir `INDEPENDENT_AI_REVIEW` con auditoría separada; mientras tanto permanece `BLOCKED` |
| **G6** | Exige siete artefactos verificados, auditoría favorable, aceptación expresa | Parcialmente dependiente de G5 | Ajustar referencia a la modalidad de revisión admitida; no modificar sus cinco condiciones sustantivas |
| **AUD-R8-02** | `OPEN`; limitación relativa a existencia y verificación de los siete artefactos | No se resuelve con la propuesta | Cierre solo con evidencia material y aceptación expresa conforme a G6 |

Estos cambios **no se resuelven unilateralmente** en esta tarea: se proponen para decisión del propietario.

---

## 13. Decisión pendiente del propietario

**Pregunta:** ¿Se autoriza admitir `INDEPENDENT_AI_REVIEW` como modalidad válida para sustentar ORACLE-ART-04, bajo los controles y limitaciones definidos en este protocolo?

**Respuesta: PENDIENTE DE APROBACIÓN EXPRESA DEL PROPIETARIO.**

Opciones disponibles para el propietario:

1. **Aprobar** la modalidad con los controles de §5, §7, §8, §10 y §11, ordenando además las enmiendas normativas de §12.
2. **Rechazar** la modalidad y mantener `HUMAN_INDEPENDENT_REVIEW` como única vía.
3. **Solicitar cambios** al protocolo antes de decidir.

Ninguna de estas opciones ha sido seleccionada. No se declara aprobada la modalidad automatizada. Esta propuesta no ejecuta G5 ni G6 y no autoriza Fase C.

---

## 14. Límites y estados conservados

No se creó ORACLE-ART-04. No se modificaron D3 ni otras decisiones aprobadas; ORACLE-ART-01/02/03/05/06/07; el expediente humano existente; producción, schemas, dependencias, código ni Parquet protegidos. No se implementó Fase C ni se realizaron commits o push. No se inventó ningún resultado de revisión externa.

```text
PROTOCOLO: PREPARED_PENDING_OWNER_APPROVAL
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

**Fin de R13-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R1.**
