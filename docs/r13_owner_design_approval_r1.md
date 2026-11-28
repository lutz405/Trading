# R13-OWNER-DESIGN-APPROVAL-R1 — Registro de aprobación del propietario del diseño de Fase C

**Proyecto:** `TradingAI_BTC`.
**Fecha de la decisión:** 2026-11-27.
**Naturaleza del documento:** registro documental de una decisión del propietario. No implementa Fase C, no autoriza su implementación y no sustituye la autorización técnica separada.

---

## 1. Base de aprobación

| Dato | Valor |
|---|---|
| Diseño aprobado | `R13-PHASE-C-DESIGN-R9` (`docs/r13_phase_c_design_r9.md`) |
| SHA-256 del diseño | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` |
| Hash Git del diseño | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| HEAD de referencia | `259ca6ee11878f114cdcab4cef500074b3bc1a48` |
| Rama | `main`, `origin/main` alineada |
| Auditoría independiente | `R13-AUDIT-PHASE-C-DESIGN-R9 — ACCEPTED` |
| AUD-R8-01 | `RESOLVED` |
| AUD-R8-02 | `OPEN` |

La aprobación se otorgó después de recibir el dictamen independiente `ACCEPTED` sobre la versión del diseño identificada por los hashes anteriores.

---

## 2. Decisión del propietario

```text
OWNER_DESIGN_APPROVAL: APPROVED
```

Alcance de la aprobación:

- Se aprueba **el diseño documental R9** en su versión identificada en §1.
- Se aceptan su estructura normativa, decisiones registradas, allowlist de 139 rutas, patrones P1–P5, invariantes I1–I12, algoritmo de preimagen y criterios CP-C-01…CP-C-18.
- Se reconoce el dictamen favorable de la auditoría independiente `R13-AUDIT-PHASE-C-DESIGN-R9 — ACCEPTED`.
- Se acepta expresamente que los siete artefactos materiales del oracle siguen pendientes (AUD-R8-02 `OPEN`) y que esta circunstancia no forma parte de la aprobación del diseño.

La aprobación se refiere únicamente al documento de diseño. No modifica, interpreta ni reabre las decisiones DEC-01 a DEC-09 ni las decisiones Q-01, Q-02, Q-03 y Q-05.

---

## 3. Límites explícitos

La aprobación **NO** significa:

- Autorización para implementar Fase C.
- Autorización para modificar código, tests, schemas o dependencias.
- Autorización para generar fingerprints productivos.
- Aprobación anticipada de resultados de CP-C.
- Autorización de Fases D, E, F, G o S2.
- Autorización de trading real.

Se mantienen los estados siguientes:

```text
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED_PENDING_TECHNICAL_AUTHORIZATION_AND_ORACLE_ARTIFACTS
```

Ningún criterio CP-C se declara PASS por este registro. La aprobación del diseño no equivale a la ejecución ni a la aceptación de pruebas de implementación.

---

## 4. Prerrequisitos pendientes

Antes de solicitar la autorización técnica de implementación:

1. Materializar los siete artefactos del oracle especificados en R9 §5.8.5:
   - transcripción normativa completa e independiente;
   - identificador de versión;
   - SHA-256 reproducible de la transcripción canonicalizada;
   - registro de revisión humana;
   - evidencia de comparación de las 139 rutas;
   - evidencia de comparación de los nueve metadatos;
   - evidencia de detección de la mutación intencional de `external_run_only`.
2. Verificar la integridad y el checksum de la transcripción.
3. Realizar y documentar la revisión humana independiente; el checksum no la sustituye.
4. Comprobar las 139 rutas, los nueve metadatos y la mutación `external_run_only`.
5. Someter la evidencia a auditoría independiente.
6. Obtener la autorización técnica expresa del propietario en una decisión separada y explícita.

Este registro **no** afirma que estos requisitos estén cumplidos. No se inventa evidencia, transcripción, checksum ni revisión.

---

## 5. Restricciones de ejecución aplicadas

- Trabajo exclusivamente documental.
- No se modificó R9 ni ningún documento histórico R1–R8.
- No se implementó código ni helper de Fase C.
- No se ejecutaron pruebas de software ni benchmarks.
- No se modificaron schemas, dependencias, fixtures, modelos ni datasets.
- No se accedió a los Parquet protegidos.
- No se crearon commits ni push.
- No se modificó el índice Git.

---

## 6. Verificación final

| Comprobación | Resultado |
|---|---|
| HEAD | `259ca6ee11878f114cdcab4cef500074b3bc1a48` |
| Rama / remoto | `main`, `origin/main` alineados |
| R1–R9 | intactos; hashes idénticos a los registrados |
| Único archivo creado | `docs/r13_owner_design_approval_r1.md` |
| staged / diff | ninguno |
| `git diff --check` | sin errores |

---

## 7. Conclusión

Queda registrada la aprobación expresa del propietario del diseño documental `R13-PHASE-C-DESIGN-R9`. La autorización técnica de implementación **no** está concedida. Fase C permanece `BLOCKED_PENDING_TECHNICAL_AUTHORIZATION_AND_ORACLE_ARTIFACTS`; las fases D, E, F, G y S2 permanecen sin autorización.

**Fin de R13-OWNER-DESIGN-APPROVAL-R1.**
