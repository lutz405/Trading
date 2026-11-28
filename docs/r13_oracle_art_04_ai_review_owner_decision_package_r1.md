# R13-ORACLE-ART-04-AI-REVIEW-OWNER-DECISION-PACKAGE-R1 — Paquete de decisiones del propietario

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** propuesta de decisiones para el propietario. **Ninguna decisión ha sido tomada ni aprobada.**

```text
AI_REVIEW_MODE: NOT_APPROVED
OWNER_DECISIONS: PENDING
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

---

## 1. Fuentes verificadas

| Fuente | SHA-256 | Git hash |
|---|---|---|
| `docs/r13_oracle_art_04_ai_review_blocker_resolution_analysis_r1.md` | `df79f9e9fc19d987fed740d9c4815ff669e0c7e4b41ece0b65554c6c05a108b9` | `816a87f4383f7256d2c077c5f2a5bf24f83004b2` |
| `docs/r13_audit_oracle_art_04_ai_independent_review_protocol_r1.md` | `146274794b1b2453c04e936e892a6fa39d6e15c3cafde80fe191650d73330693` | `aa5137325dbe9c4d989048cc88ae9e6f3d746257` |
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | `96c03f832c4d017a0b562c137fa9bb1b12b5ce7e` |
| `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | `33693367f38ca579864d5ea98ebb8aa63918011d` |
| `docs/r13_oracle_g5_blocker_resolution_analysis_r1.md` | `00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7` | `ebe75a481b224d5fd611306fb3cdbd688dcc844f` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `e37dfdae0663502e89cb522ca8605eb2791c828e` |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |

---

## DEC-OWNER-AI-01 — Modalidad automatizada

**Antecedentes.** El protocolo R1 propone `INDEPENDENT_AI_REVIEW` como modalidad alternativa ante la indisponibilidad de revisor humano. La auditoría independiente dictaminó `ACCEPTED_WITH_FINDINGS`, con dos hallazgos HIGH bloqueantes. El análisis de resolución dictaminó `VIABLE_CONDITIONED_ON_OWNER_DECISIONS`.

**Referencias normativas.** Auditoría §1, §9 y §10; análisis de resolución §1 y §5; resolución R2 §3.3 (D3); especificación R2 §3.1 y §4.4; plan R2 §8 (G5); diseño R9 §5.8.1.

**Problema que resuelve.** Existe una laguna de disponibilidad de revisor humano, pero ninguna norma vigente admite sustituirlo por IA. Se requiere decisión expresa sobre el principio, sin aprobarlo automáticamente.

**Texto propuesto de decisión.**
> Se autoriza admitir la modalidad `INDEPENDENT_AI_REVIEW` **exclusivamente** para la revisión de ORACLE-ART-04, bajo los controles del protocolo R2 y previa resolución de DEC-OWNER-AI-02 a DEC-OWNER-AI-06. Esta modalidad **no equivale a revisión humana**, **no modifica** los requisitos de los artefactos ORACLE-ART-01/02/03/05/06/07, **no crea** una excepción general a las auditorías independientes y **no autoriza** la implementación de Fase C. La vía `HUMAN_INDEPENDENT_REVIEW` permanece válida y preferente.

**Alcance.** Solo ORACLE-ART-04. Sin efectos sobre otros artefactos, gates G0–G4, G6 ni autorizaciones de fases posteriores.

**Riesgos.** Confusión terminológica; presión para tratar el dictamen IA como revisión humana; extensión involuntaria a otros artefactos.

**Consecuencias de aprobar.** Habilita la preparación de las enmiendas versionadas; no desbloquea G5 por sí sola; exige las decisiones restantes.

**Consecuencias de rechazar.** Se mantiene `HUMAN_INDEPENDENT_REVIEW` como única vía; G5 sigue `BLOCKED`; ORACLE-ART-04 sigue `NOT_CREATED`.

**Estado:** `PENDING_OWNER_DECISION`.

---

## DEC-OWNER-AI-02 — Hallazgo HIGH AUD-AI-REV-R1-01 (autorización versionada)

**Antecedentes.** La autorización R2 §3 prohíbe «Omitir revisión humana independiente» y §5.3 exige revisión humana como condición de ejecución futura. El protocolo no la consideró; la auditoría la clasificó HIGH y bloqueante.

**Referencias normativas.** Auditoría hallazgo AUD-AI-REV-R1-01; análisis de resolución §3 (01); autorización R2 §2, §3 y §5, con SHA-256 `d692e49e…`.

**Problema que resuelve.** Aprobar la modalidad sin levantar esa prohibición produciría una autorización ineficaz o contradictoria. No se puede modificar R2 retroactivamente.

**Texto propuesto de decisión.**
> Se autoriza preparar y aprobar una **Autorización de Materialización R3**, documento nuevo que conserva íntegramente la R2 como registro histórico (SHA-256 `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9`). R3 levanta la prohibición de R2 §3 **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04, registra la decisión habilitante, mantiene todos los demás límites de R2, surte efecto solo tras aprobadas la enmienda de D3, la especificación R3 y el plan R3, y se somete a auditoría independiente antes de su aprobación definitiva.

**Alcance.** Exclusivamente el levantamiento de la prohibición de revisión humana para la modalidad autorizada y el artefacto indicado. Todos los demás límites de R2 permanecen: sin Fase C, sin cierre automático de AUD-R8-02, sin G6 automático, sin omitir auditoría independiente.

**Riesgos.** Interpretación extensiva de la excepción; pérdida de trazabilidad entre R2 y R3; aprobación antes de las enmiendas dependientes.

**Consecuencias de aprobar.** Requiere crear R3 con aprobación expresa separada; R2 no se altera; la excepción queda documentada y versionada.

**Consecuencias de rechazar.** La prohibición vigente subsiste; ninguna revisión por IA puede sustentar ORACLE-ART-04; G5 permanece `BLOCKED`.

**Estado:** `PENDING_OWNER_DECISION`.

---

## DEC-OWNER-AI-03 — Hallazgo HIGH AUD-AI-REV-R1-02 (superación de la recomendación del análisis R1)

**Antecedentes.** `docs/r13_oracle_g5_blocker_resolution_analysis_r1.md` §8.1 recomienda literalmente: *«No reintentar G5 hasta que exista revisor humano real y representación de verificación aprobada»*. Su §6.1 P1 exige *«Designación de persona revisora real por el propietario»* y su §4 exige identidad real registrada. La auditoría clasificó HIGH la omisión de esta recomendación en el protocolo.

**Referencias normativas.** Auditoría hallazgo AUD-AI-REV-R1-02; análisis de bloqueos R1 §4, §6.1 P1 y §8.1, con SHA-256 `00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7`; análisis de resolución §3 (02).

**Problema que resuelve.** No se puede reinterpretar silenciosamente una recomendación vigente. Su superación debe ser un acto expreso, versionado y motivado del propietario.

**Texto propuesto de decisión.**
> El propietario, habiendo examinado la recomendación literal de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1, autoriza **superarla exclusivamente** en el sentido de admitir la revisión automatizada regulada como sustituto de la revisión humana para ORACLE-ART-04, motivándolo en la indisponibilidad de revisor humano real. La recomendación original **se conserva íntegramente** en su documento y **no se borra ni se reinterpretan sus términos**; la superación se registra en una decisión versionada nueva con fecha real y referencia verificable. La vía humana sigue vigente para cualquier artefacto o revisión futura no cubierta por esta excepción.

**Alcance.** Solo la exigencia de revisor humano real para ORACLE-ART-04 bajo la modalidad autorizada. No afecta la exigencia de representación de verificación aprobada ni las demás recomendaciones del análisis R1.

**Riesgos.** Borrado efectivo de la recomendación por desuso; falta de motivación; extensión de la excepción a otros artefactos.

**Consecuencias de aprobar.** Requiere decisión versionada y auditoría de la enmienda; no habilita por sí sola la revisión IA si faltan DEC-OWNER-AI-01/02.

**Consecuencias de rechazar.** La exigencia de revisor humano real permanece íntegra; la modalidad automatizada no puede aplicarse.

**Estado:** `PENDING_OWNER_DECISION`.

---

## DEC-OWNER-AI-04 — Condiciones de independencia

**Antecedentes.** La auditoría hallazgos AUD-AI-REV-R1-03 y AUD-AI-REV-R1-07; el análisis de resolución §3 (03, 07) define los controles verificables y la separación de roles.

**Referencias normativas.** Auditoría §4 y §8; análisis de resolución §3; protocolo R1 §5 y §11.

**Problema que resuelve.** Un modelo distinto por sí solo no demuestra independencia: pueden compartirse linaje, contexto, resúmenes del generador o herramientas.

**Texto propuesto de decisión.**
> Toda revisión bajo `INDEPENDENT_AI_REVIEW` deberá cumplir: (1) proveedor y modelo distintos del generador, con declaración de linaje; (2) sesión limpia sin historial previo; (3) fuentes normativas originales, sin resúmenes derivados del generador; (4) ausencia de dictámenes o conclusiones previos en el contexto inicial; (5) prompt íntegro y hashes de todos los archivos de entrada conservados; (6) linaje y contexto registrados, con inventario de herramientas y parámetros; (7) reconstrucción independiente de las reglas, en artefacto hashable anterior a la comparación; (8) auditor posterior distinto de la IA revisora y del generador, con evaluación a ciegas; (9) limitaciones de independencia expresamente declaradas. El mismo proveedor o una limitación no demostrable obliga a `INCONCLUSIVE`. Dos ejecuciones del mismo modelo **no** constituyen independencia suficiente.

**Alcance.** Todas las revisiones bajo la modalidad autorizada, sin excepción.

**Riesgos.** Coste operativo; no disponibilidad de proveedor alternativo; imposibilidad de verificar linaje de entrenamiento.

**Consecuencias de aprobar.** La revisión sin estos controles no será aceptable; el incumplimiento produce `INCONCLUSIVE`.

**Consecuencias de rechazar.** No existe base verificable para afirmar independencia; la modalidad no debiera admitirse.

**Estado:** `PENDING_OWNER_DECISION`.

---

## DEC-OWNER-AI-05 — Autoridad y aceptación

**Antecedentes.** El protocolo R1 §8 define cuatro dictámenes; la auditoría hallazgo AUD-AI-REV-R1-05 observa ambigüedad en `ACCEPTED_WITH_FINDINGS` y ausencia de autoridad de aceptación definida.

**Referencias normativas.** Auditoría §7; análisis de resolución §3 (05); protocolo R1 §8, §9 y §13; plan R2 §8 (G5 y G6); autorización R2 §3.

**Problema que resuelve.** Evitar que el dictamen de la IA se trate como aprobación del propietario o que un hallazgo material se degrade a «no bloqueante» por decisión de la propia IA.

**Texto propuesto de decisión.**
> La IA revisora emite **únicamente un dictamen técnico** (`ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED` o `INCONCLUSIVE`) con severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`. El auditor posterior evalúa la evidencia y confirma la severidad. El propietario **conserva exclusivamente la autoridad de aceptación**, mediante registro expreso. `INCONCLUSIVE` y `REJECTED` **no desbloquean G5** en ningún caso; tampoco `ACCEPTED_WITH_FINDINGS` mientras existan hallazgos `BLOCKER` o `HIGH` sin resolver. Ningún dictamen de IA equivale a aprobación del propietario ni sustituye la auditoría independiente.

**Alcance.** Dictamen, evaluación y aceptación de la revisión automatizada y de ORACLE-ART-04.

**Riesgos.** Confusión entre dictamen técnico y aprobación; presión sobre el auditor; hallazgos mal clasificados.

**Consecuencias de aprobar.** Define cadena de autoridad inequívoca y protege G5/G6.

**Consecuencias de rechazar.** Persiste ambigüedad; riesgo de aprobación ficticia o desbloqueo indebido de G5.

**Estado:** `PENDING_OWNER_DECISION`.

---

## DEC-OWNER-AI-06 — Límites

**Antecedentes.** Autorización R2 §3; análisis de resolución §11; protocolo R1 §14; plan R2 §8.

**Referencias normativas.** Autorización R2 §3 y §5; plan R2 G5/G6; diseño R9 §5.8.5; análisis de resolución §12.

**Problema que resuelve.** Garantizar que la excepción de revisión no se convierta en autorización general de cambios ni en desbloqueo automático de fases.

**Texto propuesto de decisión.**
> La admisión de `INDEPENDENT_AI_REVIEW` **no autoriza**: (1) la implementación de Fase C; (2) cambios en código de producción; (3) cambios en schemas o dependencias; (4) acceso o modificación de Parquet protegidos; (5) ejecución automática de G5 ni de G6; (6) modificación de ORACLE-ART-01/02/03/05/06/07 ni de ningún otro artefacto Oracle; (7) ampliación de la autorización a artefactos distintos de ORACLE-ART-04; (8) commits o push. G5 y G6 requieren sus propios registros de ejecución y aprobación expresa; Fase C continúa con `PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED`.

**Alcance.** Toda la ruta de revisión automatizada y sus consecuencias documentales.

**Riesgos.** Extensión incremental del alcance; interpretación de la enmienda como autorización de materialización general.

**Consecuencias de aprobar.** La excepción queda confinada y trazable; los estados obligatorios se conservan.

**Consecuencias de rechazar.** No puede garantizarse el confinamiento de la modalidad; el paquete no debiera aprobarse.

**Estado:** `PENDING_OWNER_DECISION`.

---

## 2. Sección de aprobación expresa (sin completar)

**Instrucción:** esta sección debe ser completada personalmente por el propietario. No se completa, firma ni fecha en este documento.

| Campo | Valor |
|---|---|
| Decisión aprobada | ______________________________________________ |
| Fecha real de aprobación | ______________________________________________ |
| Identidad funcional del propietario | ______________________________________________ |
| Referencia de aprobación | ______________________________________________ |

La aprobación de una decisión no implica la aprobación de las restantes. Cada decisión requiere su propio registro, con fecha real y referencia verificable. No se aceptan aprobaciones implícitas, presuntas o derivadas de la aprobación del protocolo.

---

## 3. Estados finales y cierre

```text
AI_REVIEW_MODE: NOT_APPROVED
OWNER_DECISIONS: PENDING
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

No se aprobó decisión alguna; no se modificaron D3, la autorización R2, la especificación R2, el plan R2, el protocolo R1, artefactos Oracle, producción, schemas, dependencias ni Parquet. No se creó ART-04 ni se ejecutaron G5/G6. Sin commits ni push.

**Fin de R13-ORACLE-ART-04-AI-REVIEW-OWNER-DECISION-PACKAGE-R1.**
