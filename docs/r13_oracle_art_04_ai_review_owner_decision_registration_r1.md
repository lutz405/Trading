# R13-ORACLE-ART-04-AI-REVIEW-OWNER-DECISION-REGISTRATION-R1 — Registro de aprobación expresa del propietario

**Proyecto:** `TradingAI_BTC`.
**Fecha del registro:** 2026-11-27.
**Naturaleza:** registro formal de decisiones del propietario. **No** es un dictamen técnico de OpenCode, **no** es una auditoría y **no** materializa artefacto alguno.

---

## 1. Fuente y datos de la aprobación

| Dato | Valor |
|---|---|
| Documento fuente | `docs/r13_oracle_art_04_ai_review_owner_decision_package_r1.md` |
| SHA-256 verificado del fuente | `5a0d7a6d024db72ea20c1d3b8028837f77372ddd45125deddc8a8fb84530b70d` |
| Git hash verificado del fuente | `9ec2c09a0c586ce7fd23bb29f1512af48528f903` |
| Fecha real de aprobación | `2026-11-27` |
| Identidad funcional del propietario | `Project Owner — TradingAI_BTC` |
| Referencia | `R13-ORACLE-ART-04-AI-REVIEW-OWNER-DECISION-PACKAGE-R1` |
| Evidencia | Aprobación expresa del propietario manifestada en la conversación de ChatGPT |

El paquete fuente permanece **intacto**: su campo de aprobación sigue sin completar y todos sus hashes se conservan. La aprobación se documenta exclusivamente en este registro nuevo. No se inventa nombre personal, firma, fecha distinta ni referencia adicional. La identidad consignada es la **identidad funcional declarada**, no una persona inventada.

**Clasificación:** la aprobación aquí registrada es una **decisión del propietario**. Los dictámenes técnicos, auditorías y verificaciones de OpenCode son evidencia auxiliar y **no** constituyen esta aprobación.

---

## 2. Decisiones aprobadas individualmente

### DEC-OWNER-AI-01 — Modalidad automatizada — `APPROVED`

**Texto aprobado:**
> Se autoriza admitir la modalidad `INDEPENDENT_AI_REVIEW` **exclusivamente** para la revisión de ORACLE-ART-04, bajo los controles del protocolo R2 y previa resolución de DEC-OWNER-AI-02 a DEC-OWNER-AI-06. Esta modalidad **no equivale a revisión humana**, **no modifica** los requisitos de los artefactos ORACLE-ART-01/02/03/05/06/07, **no crea** una excepción general a las auditorías independientes y **no autoriza** la implementación de Fase C. La vía `HUMAN_INDEPENDENT_REVIEW` permanece válida y preferente.

**Alcance exacto:** Solo ORACLE-ART-04. Sin efectos sobre otros artefactos, gates G0–G4, G6 ni autorizaciones de fases posteriores.

**Estado:** `APPROVED`.

---

### DEC-OWNER-AI-02 — Hallazgo HIGH AUD-AI-REV-R1-01 (autorización versionada) — `APPROVED`

**Texto aprobado:**
> Se autoriza preparar y aprobar una **Autorización de Materialización R3**, documento nuevo que conserva íntegramente la R2 como registro histórico (SHA-256 `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9`). R3 levanta la prohibición de R2 §3 **únicamente** para `INDEPENDENT_AI_REVIEW` aplicada a ORACLE-ART-04, registra la decisión habilitante, mantiene todos los demás límites de R2, surte efecto solo tras aprobadas la enmienda de D3, la especificación R3 y el plan R3, y se somete a auditoría independiente antes de su aprobación definitiva.

**Alcance exacto:** Exclusivamente el levantamiento de la prohibición de revisión humana para la modalidad autorizada y el artefacto indicado. Todos los demás límites de R2 permanecen: sin Fase C, sin cierre automático de AUD-R8-02, sin G6 automático, sin omitir auditoría independiente.

**Estado:** `APPROVED`.

---

### DEC-OWNER-AI-03 — Hallazgo HIGH AUD-AI-REV-R1-02 (superación de la recomendación del análisis R1) — `APPROVED`

**Texto aprobado:**
> El propietario, habiendo examinado la recomendación literal de `R13-ORACLE-G5-BLOCKER-RESOLUTION-ANALYSIS-R1` §8.1 y §6.1 P1, autoriza **superarla exclusivamente** en el sentido de admitir la revisión automatizada regulada como sustituto de la revisión humana para ORACLE-ART-04, motivándolo en la indisponibilidad de revisor humano real. La recomendación original **se conserva íntegramente** en su documento y **no se borra ni se reinterpretan sus términos**; la superación se registra en una decisión versionada nueva con fecha real y referencia verificable. La vía humana sigue vigente para cualquier artefacto o revisión futura no cubierta por esta excepción.

**Alcance exacto:** Solo la exigencia de revisor humano real para ORACLE-ART-04 bajo la modalidad autorizada. No afecta la exigencia de representación de verificación aprobada ni las demás recomendaciones del análisis R1.

**Estado:** `APPROVED`.

---

### DEC-OWNER-AI-04 — Condiciones de independencia — `APPROVED`

**Texto aprobado:**
> Toda revisión bajo `INDEPENDENT_AI_REVIEW` deberá cumplir: (1) proveedor y modelo distintos del generador, con declaración de linaje; (2) sesión limpia sin historial previo; (3) fuentes normativas originales, sin resúmenes derivados del generador; (4) ausencia de dictámenes o conclusiones previos en el contexto inicial; (5) prompt íntegro y hashes de todos los archivos de entrada conservados; (6) linaje y contexto registrados, con inventario de herramientas y parámetros; (7) reconstrucción independiente de las reglas, en artefacto hashable anterior a la comparación; (8) auditor posterior distinto de la IA revisora y del generador, con evaluación a ciegas; (9) limitaciones de independencia expresamente declaradas. El mismo proveedor o una limitación no demostrable obliga a `INCONCLUSIVE`. Dos ejecuciones del mismo modelo **no** constituyen independencia suficiente.

**Alcance exacto:** Todas las revisiones bajo la modalidad autorizada, sin excepción.

**Estado:** `APPROVED`.

---

### DEC-OWNER-AI-05 — Autoridad y aceptación — `APPROVED`

**Texto aprobado:**
> La IA revisora emite **únicamente un dictamen técnico** (`ACCEPTED`, `ACCEPTED_WITH_FINDINGS`, `REJECTED` o `INCONCLUSIVE`) con severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`. El auditor posterior evalúa la evidencia y confirma la severidad. El propietario **conserva exclusivamente la autoridad de aceptación**, mediante registro expreso. `INCONCLUSIVE` y `REJECTED` **no desbloquean G5** en ningún caso; tampoco `ACCEPTED_WITH_FINDINGS` mientras existan hallazgos `BLOCKER` o `HIGH` sin resolver. Ningún dictamen de IA equivale a aprobación del propietario ni sustituye la auditoría independiente.

**Alcance exacto:** Dictamen, evaluación y aceptación de la revisión automatizada y de ORACLE-ART-04.

**Estado:** `APPROVED`.

---

### DEC-OWNER-AI-06 — Límites — `APPROVED`

**Texto aprobado:**
> La admisión de `INDEPENDENT_AI_REVIEW` **no autoriza**: (1) la implementación de Fase C; (2) cambios en código de producción; (3) cambios en schemas o dependencias; (4) acceso o modificación de Parquet protegidos; (5) ejecución automática de G5 ni de G6; (6) modificación de ORACLE-ART-01/02/03/05/06/07 ni de ningún otro artefacto Oracle; (7) ampliación de la autorización a artefactos distintos de ORACLE-ART-04; (8) commits o push. G5 y G6 requieren sus propios registros de ejecución y aprobación expresa; Fase C continúa con `PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED`.

**Alcance exacto:** Toda la ruta de revisión automatizada y sus consecuencias documentales.

**Estado:** `APPROVED`.

---

## 3. Efecto inmediato de la aprobación

Esta aprobación **permite avanzar únicamente a la preparación de las enmiendas normativas versionadas y de sus auditorías independientes**, conforme al orden corregido en `R13-ORACLE-ART-04-AI-REVIEW-BLOCKER-RESOLUTION-ANALYSIS-R1` §5:

1. revisión del protocolo R1 → R2;
2. enmienda versionada de D3;
3. especificación R3;
4. plan R3;
5. autorización de materialización R3;
6. auditoría independiente del paquete de enmiendas;
7. aprobación expresa posterior del resultado de esa auditoría.

Ninguno de esos documentos existe todavía como versión aprobada. **No se ha preparado, aprobado ni ejecutado ninguna de esas enmiendas en esta tarea.**

---

## 4. No autorizado por este registro

Esta aprobación **NO** autoriza:

- crear ORACLE-ART-04;
- ejecutar G5 ni G6;
- modificar producción, schemas ni dependencias;
- modificar los Parquet protegidos;
- implementar Fase C;
- modificar otros artefactos Oracle;
- realizar commits ni push;
- modificar D3, la autorización R2, la especificación R2, el plan R2 ni el protocolo R1 en esta tarea.

Las enmiendas deberán prepararse como **versiones nuevas**, conservando las anteriores como registros históricos, y someterse a auditoría independiente antes de nueva aprobación expresa.

---

## 5. Estados finales

```text
OWNER_DECISIONS: APPROVED
AI_REVIEW_MODE: APPROVED_PENDING_NORMATIVE_AMENDMENTS
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff. `git diff --check`: exit 0. Sin commits ni push. Único archivo creado: este registro. Paquete fuente y todos los artefactos sin modificar.

**Fin de R13-ORACLE-ART-04-AI-REVIEW-OWNER-DECISION-REGISTRATION-R1.**
