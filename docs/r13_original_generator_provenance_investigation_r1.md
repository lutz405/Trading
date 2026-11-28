# R13 — INVESTIGACIÓN DE PROCEDENCIA DEL GENERADOR ORIGINAL — R1

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Alcance:** exclusivamente procedencia técnica del generador reportado como `opencode / hy4-flash-free`. **No** es una nueva auditoría normativa y **no** modifica R5.

**RESULTADO: `PROVENANCE_UNVERIFIABLE`.**

---

## 1. Inventario de fuentes consultadas

| # | Fuente | Naturaleza | SHA-256 / valor |
|---|---|---|---|
| 1 | Catálogo de modelos del entorno OpenCode (`models`, consulta local de solo lectura) | Configuración local de la plataforma | Ver §2.1 |
| 2 | Declaración de identidad del entorno de ejecución (encabezado del sistema) | Declaración de plataforma | `opencode` / `Hy4 flash Free` / `hy4-flash-free` |
| 3 | `docs/r13_oracle_artifacts_r5_external_audit_handoff_r1.md` | Documento histórico | `8af6fbddb39bbfdee81e1d70c3f042beab14dcfc894cee9356f7e69b035105df` |
| 4 | `docs/r13_oracle_artifacts_r5_external_independent_audit_r1.md` | Informe de auditoría externa previa | `771011ea61d7c01f9e2cd0783e5cb39fd183bf6a90c0c43c5dece85e7cf8ad86` |
| 5 | `docs/r13_oracle_artifacts_r4_independent_audit_r1.md` | Informe de auditoría previa | `94152ea9b8a53a5f66f6f051983fbad048e57210b7c218a4a5dc32744c51308a` |
| 6 | `docs/audit_report_r13_oracle_art_04_antigravity_external.md` | Informe de auditoría previa | `65218a58167708ed8b959bac89337f1c070bf0a556759bd6ceb6d66e64aa866f` |
| 7 | `docs/r13_oracle_art_04_antigravity_independent_reconstruction.md` | Reconstrucción independiente previa | `de71137f80418b223068ccb5066418883aeaf6ce8a957317992160cf8f425949` |
| 8 | `docs/r13_antigravity_findings_resolution_analysis_r1.md` | Análisis histórico | `27a578d88e0d6c0fd185256488ea920baf8d8377fe9fb7a5cf95ca268f9942e7` |
| 9 | `docs/r13_reconstruccion_normativa_independiente_kilo.md` | Reconstrucción previa | `50f93e8bdaaad976373aa771fc1ba02189c578ef2113aa5682ac0da9345247b7` |
| 10 | `audit_report_r13_oracle_art_04_kilo_external.md` | Informe externo previo | `492a9a1469d59942ab600e3413ba51f34c7177324fe7f46174e20e9203889098` |
| 11 | `audit_report_r13_oracle_art_04.md` | Informe previo | `8a99b4f04b12737bd306020fae40974ea27ec645ff07fb9abe0b558f0d0be022` |

No se accedió a credenciales, secretos, tokens ni datos privados; no se realizaron solicitudes externas con credenciales; no se modificaron configuraciones.

---

## 2. Evidencia primaria obtenida

### 2.1 Catálogo local de modelos (fuente primaria de configuración)

Consulta de solo lectura al catálogo de modelos del entorno:

| Dato del catálogo | Valor |
|---|---|
| `provider.id` | `opencode` |
| `provider.name` | `Personal / OpenCode` |
| `model.id` | `opencode/hy4-flash-free` |
| `model.name` | `Hy4 flash Free` |
| `variants` | `none`, `high` |
| `cost` | `input 0`, `output 0`, `cache 0` |
| `status` | `active` |
| `released` | `1794787200000` (marca temporal de catálogo, **no** checkpoint) |

El catálogo incluye además proveedores distintos con sus propios modelos: `openai` (48 modelos) y `ollama` (6 modelos), y un total de 127 modelos. Por tanto, `opencode` aparece como **un identificador de proveedor/configuración dentro de la plataforma**, separado de `openai` y `ollama` en el catálogo. Ello **no** identifica al proveedor real que suministra los pesos o el endpoint.

### 2.2 Declaración del entorno

El encabezado del sistema declara: nombre `Hy4 flash Free`, `Provider ID: opencode`, `Model ID: hy4-flash-free`. Concuerda con el catálogo de §2.1 en el identificador de plataforma y modelo.

### 2.3 Evidencia histórica

Los informes de §1 (filas 3–11) registran de forma reiterada la identidad `opencode / Hy4 Flash Free` y coinciden en que el **proveedor real subyacente no está acreditado**. El informe externo R5 (fuente 4) declara explícitamente: *«El proveedor real de `hy4-flash-free` no está acreditado (podría ser una API Anthropic u OpenAI reempaquetada)»*, y califica la separación como `PROBABLE_BUT_NOT_FULLY_ACREDITABLE` con versión y parámetros `NO_DISPONIBLE`.

---

## 3. Respuesta a las seis preguntas

1. **¿Qué proveedor real suministró el modelo?** **Desconocido.** No existe atestación de proveedor real, ni en el catálogo local, ni en metadatos de solicitud/respuesta, ni en el repositorio.
2. **¿Qué identifica `hy4-flash-free`?** En el catálogo local aparece como una **entrada de modelo** con variantes y costo, bajo el proveedor de plataforma `opencode`. Si es un modelo subyacente, un alias, un endpoint enrutado o una configuración personalizada es **INDETERMINADO** (`INFERRED` como posibilidad, no verificado).
3. **¿Documentación contemporánea que identifique el modelo subyacente?** **No disponible.** Solo consta la entrada del catálogo y la declaración del entorno.
4. **¿Versión, checkpoint o linaje verificables?** **No.** El campo `released` es metadato de catálogo; no hay checkpoint, hash de pesos ni datos de entrenamiento auditables.
5. **¿Puede acreditarse un proveedor concreto?** **No.** Puede acreditarse únicamente la identidad **a nivel de plataforma** (`opencode` / `hy4-flash-free`).
6. **¿Qué se prueba y qué permanece inferencia?** Ver matriz de §4.

---

## 4. Matriz de afirmaciones y nivel probatorio

| Afirmación | Nivel | Evidencia |
|---|---|---|
| El catálogo local contiene `opencode/hy4-flash-free`, nombre `Hy4 flash Free`, variantes `none`/`high`, estado `active`, costo 0 | **`VERIFIED`** | Salida directa del catálogo de modelos (§2.1) |
| El proveedor del catálogo se identifica como `opencode` / `Personal / OpenCode`, distinto de `openai` y `ollama` en el catálogo | **`VERIFIED`** | Salida directa del catálogo (§2.1) |
| El entorno declara al agente como `opencode` / `hy4-flash-free` | **`CORROBORATED`** | Declaración del sistema + catálogo local concordantes (solo nivel plataforma) |
| Informes históricos registran al generador como `OpenCode / Hy4 Flash Free` | **`CORROBORATED`** | Fuentes 3–11; todas remiten a la misma declaración de plataforma |
| El proveedor real (empresa/servicio) que suministró pesos o endpoint | **`UNKNOWN`** | Sin atestación ni metadatos de red disponibles |
| `hy4-flash-free` es alias/endpoint/router de otro modelo | **`INFERRED`** | Posibilidad planteada en informes previos; sin evidencia |
| `Hy4` equivale a `Hydrogen 4` y por tanto a la misma familia que `Gemini 4 Hydrogen` | **`INFERRED`** | Hipótesis de nombre; **no** se acepta como prueba (prohibida la inferencia por nombre comercial) |
| Versión/checkpoint exacto del generador | **`UNKNOWN`** | `NO_DISPONIBLE`; el campo `released` no es checkpoint |
| Linaje de entrenamiento verificable | **`UNKNOWN`** | No auditable de forma cruzada |
| Metadatos de solicitud/respuesta con cabeceras de proveedor conservados en el repositorio | **`UNKNOWN`** | No localizados en las fuentes examinadas |
| La auditoría externa previa declaró separación `PARTIAL`, no totalmente acreditable | **`REPORTED`** | Fuente 4, §1.2 |
| No se accedieron credenciales ni se hicieron solicitudes externas con credenciales | **`VERIFIED`** | Procedimiento seguido en esta investigación |

---

## 5. Limitaciones

- El catálogo local acredita **identidad de plataforma**, no procedencia de pesos ni endpoint real.
- Una plataforma o interfaz distinta **no** prueba proveedor distinto (DEC-OWNER-AI-04 y mandato de no presunción).
- Una declaración de plataforma **no** prueba linaje subyacente.
- No hay checkpoint, hash de pesos, cabeceras de proveedor ni documentación oficial contemporánea del modelo subyacente disponible en el workspace.
- No se realizó búsqueda externa con credenciales ni se consultaron fuentes privadas.

---

## 6. Conclusión sobre DEC-OWNER-AI-04

**`PROVENANCE_UNVERIFIABLE`.** La evidencia sostiene únicamente la identidad a nivel de plataforma (`opencode / hy4-flash-free`); falta toda evidencia primaria sobre el proveedor real, versión/checkpoint y linaje. En consecuencia:

- **No puede afirmarse** que DEC-OWNER-AI-04 esté satisfecho.
- **No puede acreditarse** que un auditor use proveedor distinto del generador original, aunque use otra plataforma o nombre comercial.
- La independencia requerida permanece **`INCONCLUSIVE`**; EXT-01 y EXT-02 **no** se declaran cerrados.
- Para superar esta limitación haría falta una atestación verificable del proveedor real del generador (identificador de endpoint, facturación o documentación oficial del servicio) **y** la del auditor, con versión/checkpoint y parámetros registrados.

---

## 7. Estados y cierre

```text
INVESTIGATION_RESULT: PROVENANCE_UNVERIFIABLE
DEC_OWNER_AI_04_STATUS: NOT_SATISFIED
EXT_01: NOT_CLOSED
EXT_02: NOT_CLOSED
R5: NOT_APPROVED / NOT_AUDITED
ORACLE-ART-04: NOT_CREATED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
```

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff; `git diff --check` exit 0. Sin commits ni push. Único archivo creado: este informe. No se modificaron R5, predecesores, informes, producción, tests, schemas, dependencias ni Parquet; no se creó ART-04 ni se ejecutaron G5/G6.

**Fin de R13-ORIGINAL-GENERATOR-PROVENANCE-INVESTIGATION-R1.**
