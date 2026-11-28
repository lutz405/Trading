# R13-AUDIT-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R1 — Auditoría técnica y normativa independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto:** `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md`.
**Restricción:** auditoría de solo lectura, salvo este informe. No se modificó el protocolo ni fuente alguna.

---

## 1. Dictamen

**`ACCEPTED_WITH_FINDINGS`.**

El protocolo es una propuesta segura en su forma: no declara aprobada la modalidad, mantiene G5 bloqueada, prohíbe llamar «revisión humana» a la IA e impide usar `INCONCLUSIVE` para desbloquear. Sin embargo, **no es normativamente completo**: omite dos fuentes que prohíben expresamente omitir la revisión humana, y sus controles de independencia, reproducibilidad y evidencia son insuficientes para una desviación de esta magnitud.

**Condición del dictamen:** los hallazgos `AUD-AI-REV-R1-01` y `AUD-AI-REV-R1-02` son **bloqueantes para cualquier decisión del propietario** y deben resolverse en una versión posterior del protocolo antes de someter la modalidad a aprobación. Los demás deben resolverse antes de ejecutar la primera revisión. Este dictamen **no aprueba** la modalidad en nombre del propietario.

---

## 2. Hashes verificados

| Fuente | SHA-256 | Git hash |
|---|---|---|
| `docs/r13_oracle_art_04_ai_independent_review_protocol_r1.md` | `3a01e20d2acce0c32772410e9958ebf853f681018dedbb4efc7b7dd733a48f7a` | `96c03f832c4d017a0b562c137fa9bb1b12b5ce7e` |
| `docs/r13_oracle_artifacts_specification_r2.md` | `0ede7956eeab931b679859ea216c8aeeb7f05b801cc75ed049ae2582ba3b522e` | `5179cad31e0a640837c785a8516bc46b126e4ea3` |
| `docs/r13_oracle_artifacts_decision_resolution_r2.md` | `6f40872467de2d932fc1367fabda8c7500abe192abc5f55ced3d031ee92849e5` | `cccbe4dfa6531f1cce0d3014e46eedf7d36fb265` |
| `docs/r13_oracle_artifacts_materialization_plan_r2.md` | `d4d0c689e68698040a581047cc2386056fffb3f9c6f0ec3b3a6c68f92ca0beb0` | `e37dfdae0663502e89cb522ca8605eb2791c828e` |
| `docs/r13_oracle_art_04_human_review_package_r1.md` | `1b7630c1a82405ba06df3e7b95d64e81e694f744b9e6a19a9e6cba29a9647cdc` | `7b01df60e949545b24d481cc026ee87c8400ce1e` |
| `docs/r13_phase_c_design_r9.md` | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| `docs/r13_oracle_artifacts_materialization_authorization_r2.md` | `d692e49ee50d7313afecb4b9b3693469cc0ebda47eb1ff9d70ef2557f40c61f9` | `33693367f38ca579864d5ea98ebb8aa63918011d` |
| `docs/r13_oracle_g5_blocker_resolution_analysis_r1.md` | `00afad8bb76df06e32415a2e0792a2d91ee6a0b24c2f342b2b3ca3f4c6b36fa7` | `ebe75a481b224d5fd611306fb3cdbd688dcc844f` |

Todos los hashes se recalcularon directamente y coinciden. No se aceptaron valores declarados sin reproducción.

---

## 3. Compatibilidad normativa

| Norma | Exigencia real | Tratamiento en el protocolo | Evaluación |
|---|---|---|---|
| **D3** (resolución R2 §3.3, líneas 133–155) | Revisor humano, identidad funcional designada, identidad real al ejecutar, independencia declarada | §3 la reconoce e declara que una IA no la satisface automáticamente | Correcto, pero la «enmienda controlada de D3» de §12 no especifica versión, criterios de aprobación ni qué ocurre con el criterion de identidad real |
| **R2 §3.1** (líneas 43–52) | Estados `NOT_CREATED`/`CREATED_UNVERIFIED`/`VERIFIED`/`REJECTED` | §12 propone precisar que `VERIFIED` puede apoyarse en IA | Compatible solo si hay decisión habilitante; bien identificado |
| **R2 §4.4** (líneas 188–213) | «Persona funcionalmente independiente», fecha real, dictamen favorable, revisión posterior de ART-04 | §12 la declara incompatible sin cambio | Correcto |
| **Plan R2 §8 G5** (línea 185) | Entrada: «G4 completo; **revisión humana realizada**» | §12 propone reformular G5 | Correcto, pero incompleto: ver hallazgo 02 |
| **Plan R2 §8 G6** (líneas 186, 190) | Cinco condiciones sustantivas + aceptación expresa | §12 promete no modificar las cinco condiciones | Correcto; cualquier reajuste textual requiere aprobación expresa |
| **ORACLE-ART-04** | Registro de revisión humana independiente, `NOT_CREATED` | §1 y §12 conservan el estado y prohíben emitirlo como humano | Correcto |
| **AUD-R8-02** | `OPEN`; cierre exige siete artefactos verificados, auditoría favorable y aceptación | §12 afirma que la propuesta no la resuelve | Correcto |
| **Autorización R2 §3 y §5** (líneas 53–63, 95–105) | **Prohíbe expresamente «Omitir revisión humana independiente»** y exige revisión humana como condición de ejecución futura | **Ausente del protocolo** | **Ver hallazgo 01 — bloqueante** |
| **Análisis de bloqueos R1 §4, §6.1 y §8** (líneas 104–119, 146, 188) | Exige designación de persona revisora real; no reintentar G5 sin revisor humano real | **Ausente del protocolo** | **Ver hallazgo 02 — bloqueante** |

**Modificaciones normativas necesarias identificadas:** nueva decisión o enmienda versionada de D3; R2 §4.4; R2 §3.1; criterio de entrada de G5; referencia a la modalidad en G6; definición del contenido de ORACLE-ART-04; **y adicionalmente, detectado por esta auditoría: nueva autorización de materialización que revoque la prohibición de omitir revisión humana, y superación documentada de la recomendación del análisis de bloqueos R1**. Estas modificaciones no se resuelven unilateralmente.

---

## 4. Independencia real

El protocolo introduce controles adecuados en dirección correcta (§5): proveedor distinto «cuando sea viable», no entrega inicial de dictámenes, fuentes originales, reconstrucción previa a la comparación, registro de modelo/versión/fecha/configuración y prohibición de afirmar independencia absoluta.

No obstante, **no son suficientes**:

- La cláusula «cuando sea viable» no define criterios de viabilidad ni consecuencias; un mismo proveedor quedaría amparado por una simple declaración de limitación.
- No se prohíbe el uso de resúmenes, notas o prompts derivados del generador, ni se exige sesión limpia con manifiesto de fuentes sellado por hash.
- No se controlan linajes de entrenamiento compartidos ni errores sistemáticos comunes: dos modelos distintos pueden reproducir el mismo sesgo si ambos fueron expuestos a las mismas conclusiones previas.
- No se exige inventario de herramientas ni registro íntegro del contexto entregado; por tanto, la afirmación «no se filtraron conclusiones del generador» (§11) no es verificable.
- No se define reproducibilidad para un modelo estocástico: §7-F exige «repetibilidad de comprobaciones» y §8 exige evidencia reproducible, sin especificar qué se repite, cuántas veces ni con qué criterio de concordancia.

**Conclusión:** el protocolo reduce pero **no demuestra** independencia real. No debe afirmarse independencia absoluta; cualquier revisión concreta con limitación de independencia no demostrable debe concluir `INCONCLUSIVE`.

---

## 5. Cobertura técnica

§6 cubre correctamente 139 rutas, 24 `rule_id` (13 usados / 11 exclusiones), nueve metadatos separados de `rule_id`, tipos, condiciones, nulabilidad, normalización, R9 §5.4, diseño §9.2, `manifest_v4.json`, JCS/SHA-256 de ART-03, ART-05/06/07 y detección de omisiones, duplicados, divergencias y contradicciones.

**Gap:** ART-02 (versión ejecutable del oracle, uno de los siete artefactos exigidos por G6) no aparece en el alcance de §6 ni en §2. Dado que el propósito declarado es sustentar la verificación del conjunto Oracle, la exclusión debe justificarse o incorporarse (hallazgo 07).

---

## 6. Calidad de la evidencia

§6 exige explicar cada comprobación y §9 exige «resultados reproducibles» y «referencia a la evidencia original». Sin embargo:

- No se exige un registro por ruta y por metadato (139 × 9) que vincule cada conclusión con: fuente normativa citada, comprobación reproducible, resultado verificable y entrada en el registro de discrepancias.
- No se exige que la reconstrucción de reglas se conserve como artefacto hashable e inmutable.
- No se define el formato del registro de discrepancias ni su relación con los hallazgos del dictamen.
- En consecuencia, afirmaciones como «cobertura completa» o «sin divergencias» podrían no ser verificables objetivamente si solo se apoya en el texto libre de la IA.

Ver hallazgo 05.

---

## 7. Dictámenes

Los cuatro valores permitidos existen y `INCONCLUSIVE` está explícitamente impedido de desbloquear G5 (§8). `ACCEPTED` y `REJECTED` tienen criterios razonablemente inequívocos.

`ACCEPTED_WITH_FINDINGS` es **ambiguo**: «hallazgos no bloqueantes», «limitaciones declaradas y aceptables» y «resolución documentada» no se definen; no hay escala de severidad ni se determina quién decide la aceptabilidad (¿la propia IA?, ¿el auditor?, ¿el propietario?). tampoco se distingue operativamente entre evidencia ausente (`INCONCLUSIVE`) y evidencia contradictoria (`REJECTED`) cuando ambas coexisten. Ver hallazgo 04.

**Qué bloquea G5:** G5 ya está `BLOCKED` por ORACLE-ART-04 `NOT_CREATED`. Ningún dictamen de una revisión por IA puede desbloquearla mientras: (a) no exista decisión habilitante del propietario; (b) no se hayan enmendado D3, R2 §4.4, el criterio de G5 y la autorización R2; (c) no exista ORACLE-ART-04 materializado y auditado; y (d) no se haya emitido auditoría separada favorable. `INCONCLUSIVE`, `REJECTED` y `ACCEPTED_WITH_FINDINGS` con hallazgos sin resolver bloquean G5 en cualquier caso.

---

## 8. Auditoría posterior

§11 exige auditoría técnica separada y lista ocho comprobaciones, lo cual es positivo. Sin embargo:

- No exige que el auditor sea un rol funcionalmente distinto del generador **y** de la IA revisora, ni que trabaje a ciegas respecto del dictamen de la IA.
- No distingue qué verificaciones deben ser deterministas (hashes, JCS, reconstrucción de reglas, cobertura de 139 rutas) de las que requieren juicio humano (veracidad de fecha/versión, independencia efectiva, aceptabilidad de limitaciones).
- Una auditoría ejecutada por la misma herramienta o con acceso previo al dictamen sería circular. Ver hallazgo 06.

---

## 9. Seguridad normativa — verificada

Se confirma que el protocolo, **tal como está redactado**:

| Riesgo | Resultado |
|---|---|
| Desbloquear G5 con `INCONCLUSIVE` | **Impedido** (§8, línea 137) |
| Alterar fuentes durante la revisión | **Prohibido** (§10, línea 172: solo lectura) |
| Crear aprobación ficticia | **Impedido** (§1, §13: decisión pendiente; §9: no inventar) |
| Convertir verificación interna en auditoría independiente | **Impedido** (§4: `AUTOMATED_INTERNAL_VERIFICATION` no sustenta ART-04; §10) |
| Modificar G6 sin satisfacer sus condiciones | **Impedido** (§12 promete no cambiar las cinco condiciones) |
| Autorizar Fase C automáticamente | **Impedido** (§14 conserva `NOT_GRANTED`) |

Estos controles son adecuados y se registran como evidencia positiva.

---

## 10. Hallazgos

### AUD-AI-REV-R1-01 — HIGH — Bloqueante para decisión del propietario

- **Referencia:** protocolo §2 (líneas 32–44) y §12 (líneas 195–208); autorización R2 §3 (líneas 53–63) y §5.3 (línea 101).
- **Evidencia:** la autorización vigente prohíbe «Omitir revisión humana independiente» y exige «Revisión humana independiente (ORACLE-ART-04)» como condición de ejecución futura. El protocolo no incluye ese documento entre sus fuentes ni lo menciona en el análisis de compatibilidad.
- **Riesgo:** el propietario podría aprobar la modalidad creyendo que basta con enmendar D3/R2/G5, cuando la autorización GRANTED seguiría prohibiendo la sustitución. Aprobación ineficaz o contradictoria.
- **Corrección:** añadir la autorización R2 a §2 y §12; exigir una autorización nueva/versionada que revoque expresamente la prohibición antes de cualquier revisión por IA; condicionar la decisión de §13 a esa enmienda.

### AUD-AI-REV-R1-02 — HIGH — Bloqueante para decisión del propietario

- **Referencia:** protocolo §12 (línea 204); análisis de bloqueos R1 §4 (líneas 104–119), §6.1 P1 (línea 146) y §8.1 (línea 188).
- **Evidencia:** el análisis normativo previo exige «designación de persona revisora real por el propietario» y «no reintentar G5 hasta que exista revisor humano real». El protocolo propone reformular G5 sin citar ni superar esta recomendación.
- **Riesgo:** contradicción entre dos documentos de análisis vigentes; la reformulación de G5 se presentaría como simple ajuste técnico cuando en realidad revierte una recomendación aprobada.
- **Corrección:** incluir el análisis R1 entre las fuentes; documentar explícitamente la superación de su recomendación como decisión del propietario, no como consecuencia automática del protocolo.

### AUD-AI-REV-R1-03 — MEDIUM — Independencia no demostrable

- **Referencia:** protocolo §5 (líneas 79–86) y §8 (línea 133).
- **Evidencia:** «cuando sea viable» sin criterios; sin prohibición de resúmenes derivados del generador; sin sesión limpia ni manifiesto sellado; sin control de linajes compartidos; sin inventario de herramientas/contexto.
- **Riesgo:** la IA de terceros puede repetir conclusiones de OpenCode con apariencia de independencia; falsa atribución de independencia.
- **Corrección:** definir viabilidad (proveedor/modelo distintos y sin linaje compartido conocido); exigir sesión nueva, manifiesto de fuentes con hash, registro íntegro de prompts/contexto y herramientas; mismo proveedor ⇒ `INCONCLUSIVE` por defecto; prohibir resúmenes del generador como entrada.

### AUD-AI-REV-R1-04 — MEDIUM — Reproducibilidad indefinida

- **Referencia:** protocolo §7-F (línea 118), §9.11 (línea 155), §8 (líneas 132–135).
- **Evidencia:** se exigen «resultados reproducibles» y «repetibilidad» sin definir configuración fija, número de ejecuciones ni criterio de concordancia para un modelo estocástico.
- **Riesgo:** `ACCEPTED` podría emitirse sobre un resultado que no puede repetirse; falso positivo de robustez.
- **Corrección:** ejecutar hash/JCS/comparaciones con herramientas deterministas; fijar y registrar configuración; repetir la parte no determinista al menos dos veces con concordancia; divergencia ⇒ `INCONCLUSIVE`.

### AUD-AI-REV-R1-05 — MEDIUM — Criterio `ACCEPTED_WITH_FINDINGS` ambiguo

- **Referencia:** protocolo §8 (línea 133).
- **Evidencia:** «no bloqueantes», «aceptables» y «resolución documentada» sin definición ni escala de severidad; no se dice quién decide la aceptabilidad.
- **Riesgo:** hallazgos materiales podrían degradarse a «no bloqueantes» por decisión de la propia IA revisora.
- **Corrección:** definir severidades `BLOCKER/HIGH/MEDIUM/LOW/INFO`; cualquier hallazgo `BLOCKER/HIGH` o limitación de independencia/reproducibilidad ⇒ `INCONCLUSIVE` o `REJECTED`; la aceptabilidad la decide el auditor y el propietario, nunca la IA.

### AUD-AI-REV-R1-06 — MEDIUM — Evidencia no vinculable

- **Referencia:** protocolo §6 (línea 105), §9 (líneas 143–161), §11 (línea 185).
- **Evidencia:** no se exige registro por ruta/metadato, reconstrucción hashable inmutable, citación normativa por hallazgo ni formato de registro de discrepancias; §11 exige 139 casos individuales que §9 no obliga a conservar.
- **Riesgo:** conclusiones sin trazabilidad objetiva; auditoría posterior imposible de reproducir.
- **Corrección:** añadir registro mínimo de 139 × 9 resultados, artefacto de reconstrucción con hash, tabla de discrepancias con ID/severidad/resolución y referencia normativa por conclusión.

### AUD-AI-REV-R1-07 — LOW — Independencia de la auditoría posterior no garantizada

- **Referencia:** protocolo §11 (líneas 178–191).
- **Evidencia:** no exige rol de auditor distinto ni revisión a ciegas; no separa pruebas deterministas de juicio humano.
- **Riesgo:** auditoría circular por reutilización de la misma IA o del mismo contexto.
- **Corrección:** exigir rol funcional distinto, evaluación a ciegas del dictamen ajeno, herramientas deterministas para hashes/JCS/cobertura y verificación humana de identidad, versión, fecha y decisión.

### AUD-AI-REV-R1-08 — LOW — Alcance omite ART-02

- **Referencia:** protocolo §2 y §6 (líneas 96–103).
- **Evidencia:** ART-02 no aparece aunque G6 exige los siete artefactos.
- **Riesgo:** revisión presentada como cobertura del conjunto Oracle con un artefacto omitido.
- **Corrección:** incorporar ART-02 al alcance o documentar la exclusión con justificación normativa aprobada.

---

## 11. Estado Git y cierre

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni unstaged. `git diff --check`: exit 0. Sin commits ni push. No se ejecutaron G5/G6, no se creó ART-04, no se modificaron artefactos, decisiones, autorizaciones, producción, schemas, dependencias ni Parquet. Único archivo creado: este informe.

```text
PROTOCOLO: PENDING_INDEPENDENT_AUDIT
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La aceptación de este protocolo **no** equivale a la aprobación de la modalidad ni a la aceptación de revisión concreta alguna.

**Fin de R13-AUDIT-ORACLE-ART-04-AI-INDEPENDENT-REVIEW-PROTOCOL-R1.**
