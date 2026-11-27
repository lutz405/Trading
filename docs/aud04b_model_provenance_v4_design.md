# AUD-04B.1 — Especificación propuesta de provenance 4.0.0

**Estado:** propuesta documental para revisión humana; no implementada ni aprobada.

**Base de revisión:** commit **8498af4f45dfbed8fc0cdeda27565a3d1e3b4830** de **lutz405/Trading**.

**Contrato anterior:** **docs/aud04b_model_provenance_v3_design.md**, preservado como contrato histórico 3.0.0.
**Alcance:** especificar la transición, los datos de procedencia, sus hashes y límites de validación. Este documento no cambia el JSON Schema, código, tests, fixtures o artefactos.

> Las etiquetas REQUISITO EXISTENTE, ACLARACIÓN, CAMBIO PROPUESTO y PENDIENTE DE APROBACIÓN indican el origen y estado de cada regla. Ningún cambio propuesto queda aprobado por aparecer en este documento.
>
> Los fragmentos JSON y ejemplos numéricos de este documento son ilustrativos; no son fixtures ejecutables ni evidencia de implementación.

## 1. Propósito y límites

Este documento propone un contrato independiente para manifiestos con **schema_version = "4.0.0"**. Está basado en AUD-04B.1 y en la resolución R13-DESIGN-R3.2. Su propósito es precisar las reglas que tendrían que aplicarse en una futura implementación y auditoría.

Esta propuesta no autoriza:

- Deserializar modelos, cargar modelos para inferencia ni ejecutar inferencia.
- Entrenar, recalibrar o evaluar modelos.
- Promover, aprobar o revocar un modelo de forma efectiva.
- Crear loaders, registry, writer, integración de pipeline o conectividad con exchanges.
- Iniciar R13-IMPLEMENTATION ni S2.

S1, aun implementada conforme a esta propuesta, solo podría validar estructura, relaciones y hashes declarados. No sería un mecanismo de confianza criptográfica ni de autorización.

## 2. Clasificación y jerarquía

| Etiqueta | Significado |
|---|---|
| **REQUISITO EXISTENTE** | Regla ya expresada en AUD-04B.1. No significa que esté implementada o que haya pasado pruebas. |
| **ACLARACIÓN** | Interpretación precisa que conserva la intención existente sin afirmar que el código actual la cumpla. |
| **CAMBIO PROPUESTO** | Regla nueva o modificación incompatible que requiere aprobación explícita antes de incorporarse a un contrato aprobado. |
| **PENDIENTE DE APROBACIÓN** | Decisión cuyo catálogo, política o aceptación final todavía debe resolver una autoridad humana. |

En caso de discrepancia, los documentos de diseño no alteran silenciosamente el comportamiento de un manifiesto 3.0.0. La versión declarada determina el contrato aplicable.

## 3. Versionado y compatibilidad

### 3.1 Contrato 3.0.0 congelado

**REQUISITO EXISTENTE.** AUD-04B.1 define el manifiesto 3.0.0, sus campos y su política de canonicalización.

**ACLARACIÓN.** 3.0.0 se conserva como contrato histórico. No se cambian retroactivamente sus reglas, no se añaden campos obligatorios, no se recalculan sus fingerprints con reglas 4.0.0 y no se convierte automáticamente un manifiesto.

La lectura compatible de un manifiesto 3.0.0 solo significa que un lector futuro puede comprobarlo conforme a las reglas históricas de 3.0.0. No certifica que dicho manifiesto satisfaga el contrato propuesto de 4.0.0.

### 3.2 Contrato 4.0.0 y selección de validador

**CAMBIO PROPUESTO.** Usar un contrato y esquema independientes con **schema_version = "4.0.0"**. Se recomienda un incremento mayor porque los límites fuente, condiciones de calibration, reglas de evidencia y relaciones de fingerprint cambian la validez del manifiesto.

La selección futura será explícita:

| schema_version | Esquema y reglas |
|---|---|
| 3.0.0 | Validador congelado 3.0.0 |
| 4.0.0 | Validador 4.0.0 |
| Ausente, desconocida o no admitida | Rechazo; sin fallback |

El wrapper público **validate_manifest** conservará su nombre y retorno **list[str]**, y seleccionará el validador por **schema_version**. Esto es un contrato de compatibilidad futuro; no afirma que el dispatch exista hoy.

No se permite:

- Aceptar un 3.0.0 usando reglas 4.0.0.
- Añadir campos 4.0.0 a un manifiesto 3.0.0.
- Cambiar la versión de un manifiesto existente sin reconstruir el objeto y todos sus hashes.
- Aplicar valores por defecto implícitos para “actualizar” un manifiesto.

Las fixtures históricas deben permanecer como casos 3.0.0. Las futuras fixtures 4.0.0 deben identificarse con esa versión y no sustituir a las históricas.

### 3.3 Diferencias incompatibles propuestas

| Área | 3.0.0 histórico | 4.0.0 propuesto |
|---|---|---|
| Posición fuente | El diseño la menciona como posible información auxiliar; el esquema no la declara. | Límites fuente obligatorios en cada partición y posición por fila en la preimagen de índice. |
| Purga | El diseño compara filas entre particiones con el horizonte, sin definir todos los casos. | Separación explícita entre gap de filas filtradas y gap de posiciones fuente. |
| Calibración | El diseño admite calibration igual a validation o anterior. | Solo calibration compartida exactamente con validation en S1. |
| Evento | Hay reglas de cadena, pero la evidencia no tiene schema cerrado y hashes son opcionales en validate_event. | Payload, evidencia y sidecar con campos y relaciones definidos. |
| Fingerprint | El diseño describe una intención, sin allowlist completa. | Allowlist explícita por rutas 4.0.0. |

## 4. Contrato del manifiesto 4.0.0

**CAMBIO PROPUESTO.** El manifiesto mantiene las áreas del contrato v3: identidad, productor, datos, target, features, training, validation, calibration, artifacts, metrics y extensions. Su esquema futuro debe ser JSON Schema 2020-12, con objetos núcleo cerrados. El esquema histórico de referencia es `src/tradingai/schemas/manifest_v3.json`. Los cambios siguientes son parte de esta propuesta y todavía no existen en ese JSON Schema del commit base.

Para propiedades de 3.0.0 no cambiadas expresamente en este documento, 4.0.0 conserva el tipo, nulabilidad, restricciones y obligatoriedad de `manifest_v3.json`. El esquema 4.0.0 debe seguir rechazando propiedades desconocidas en objetos núcleo. Las diferencias de esquema aquí propuestas son: `schema_version` constante `4.0.0`; incorporación obligatoria de `source_position_start` y `source_position_end` a cada partición; `shared_with` ausente en train, validation y test, y obligatorio e igual a `validation` solo para calibration; validación de que, con `calibration.mode = in_pipeline`, `base_model_id = model_id` y los hashes base correspondan a los artefactos del mismo manifiesto, y que con `external_run` identifique el modelo base distinto cuyos hashes se declaran; restricciones reforzadas de clases, eventos y sidecars; y campos de entorno añadidos/requeridos según §9.3. `base_model_id` y ambos hashes base siguen siendo obligatorios y con formato válido en ambos modos. Cualquier otra diferencia debe añadirse explícitamente antes de aprobar el contrato.

### 4.1 Posiciones fuente y particiones

Para cada una de **train**, **validation**, **calibration** y **test**, 4.0.0 requiere:

| Campo | Tipo propuesto | Significado |
|---|---|---|
| row_start, row_end | Enteros | Intervalo semiabierto en las filas filtradas del dataset. |
| source_position_start, source_position_end | Enteros | Intervalo semiabierto en las filas de la serie OHLCV original. |
| n_rows | Entero | Número de filas conservadas: row_end - row_start. |
| time_start, time_end | Timestamp | Primer y último instante de la partición. |
| class_counts | Array de enteros | Conteos alineados con target.class_order. |
| index_sha256 | SHA-256 | Digest de la secuencia de identidad de las filas. |

**CAMBIO PROPUESTO.** source_position es el ordinal entero de la fila de la serie OHLCV original, antes de descartar filas por features o etiquetas. No es el ordinal de la serie filtrada ni una etiqueta arbitraria del índice de pandas. Filtrar filas no renumera sus posiciones fuente. horizon_bars mide pasos de ese ordinal, es decir, filas de la serie fuente original.

Los límites de cada partición son semiabiertos:

    P = [row_start, row_end)
    S = [source_position_start, source_position_end)

El límite final es exclusivo. Para una partición no vacía, si la secuencia de filas conservadas tiene posiciones fuente `s_0, …, s_(n-1)`, se exige `source_position_start = s_0` y `source_position_end = s_(n-1) + 1`. Las filas filtradas dentro de los límites pueden hacer que el ancho del intervalo fuente sea mayor que n_rows.

**Invariantes de la secuencia:** las posiciones `s_i` son enteros no negativos, estrictamente crecientes (`s_(i+1) > s_i`) y, por ello, únicas. No se renumeran tras filtrar filas. Calibration compartida debe usar exactamente la misma secuencia de posiciones que validation.

### 4.2 Gaps, purga y embargo

Para dos particiones consecutivas A y B:

    gap_rows(A,B)   = B.row_start - A.row_end
    gap_source(A,B) = B.source_position_start - A.source_position_end

gap_rows mide filas conservadas del dataset. gap_source mide posiciones de la serie original entre los límites de las particiones. Los dos valores no son intercambiables.

rows_between_partitions es el mínimo de gap_rows sobre las fronteras reales. Se recalcula desde los límites y no sustituye gap_source.

Sea H = target.horizon_bars y E = validation.purge.embargo_rows. Para que la comparación sea dimensionalmente válida, **CAMBIO PROPUESTO:** en 4.0.0 E cuenta posiciones de la serie fuente original, igual que H; el nombre histórico `embargo_rows` se conserva solo por continuidad del campo y su descripción normativa deberá decir “barras de fuente”. No representa filas del dataset filtrado.

**ACLARACIÓN propuesta.** La etiqueta de la última posición fuente p de A puede depender de datos hasta p + H. Para evitar que alcance la primera fila de B, gap_source(A,B) debe ser al menos H.

**CAMBIO PROPUESTO.** embargo_rows es una segunda cota mínima sobre el mismo hueco de posiciones fuente, no una reserva adicional posterior a la purga. La condición normativa propuesta en cada frontera es:

    gap_source(A,B) >= max(H, E)

Así no se suma dos veces una misma región excluida. Si el propósito fuera reservar E posiciones adicionales después de la purga, se necesitaría otro campo y otra fórmula; esa alternativa no se adopta en esta propuesta. Si se decide que embargo_rows debe conservar el significado de filas filtradas, esta fórmula no se puede aplicar: el contrato tendrá que definir una restricción separada sobre gap_rows o añadir un campo de embargo en posiciones fuente antes de aprobar 4.0.0.

Una frontera con gap negativo es un solapamiento y se rechaza. Un indicador declarado no puede reemplazar el cálculo. Para aceptar una partición como purgada, todas sus fronteras cronológicas deben satisfacer la fórmula.

#### Ejemplo con filas descartadas

Si train conserva posiciones fuente 0, 1, 3, 4, 6, sus filas filtradas pueden ocupar [0,5) y su rango fuente [0,7). Si validation conserva posiciones 10, 11, 12, sus filas filtradas pueden ocupar [5,8) y su rango fuente [10,13).

    gap_rows   = 5 - 5  = 0
    gap_source = 10 - 7 = 3

Con H=3 y E=2, la frontera satisface la fórmula propuesta. El gap de cero filas filtradas coexiste con tres posiciones fuente de separación porque las coordenadas cuentan universos distintos. Con H=4, la misma frontera no estaría purgada.

### 4.3 Qué puede verificar S1

**ACLARACIÓN.** Con límites y hashes declarados, S1 puede comprobar tipos, límites semiabiertos, que `source_position_start < source_position_end`, orden entre rangos declarados, aritmética de conteos, fórmula de gap basada en límites declarados, relaciones entre hashes declarados y el formato de los digests. Si recibe también la secuencia por fila, puede comprobar sobre esa entrada que las posiciones sean enteros no negativos, estrictamente crecientes y únicas, y que los límites declarados coincidan con el primer valor y el último más uno.

El manifiesto S1 solo contiene límites y `index_sha256`, no la secuencia de posiciones por fila. Por ello, a partir del manifiesto y su digest únicamente, S1 no puede demostrar monotonía, unicidad ni igualdad efectiva entre los límites declarados y los extremos de la secuencia; tampoco demuestra que posiciones, timestamps, etiquetas o conteos correspondan al dataset original. Para esa verificación efectiva, un verificador posterior debe obtener los bytes del dataset identificado por `dataset_sha256`, reconstruir el orden de las filas fuente y aplicar las reglas de filtrado. Debe comprobar las invariantes de la secuencia y recalcular posiciones, índices, límites y digest. Un digest bien formado no demuestra por sí solo que su preimagen sea correcta.

## 5. Identidad de índices y datos temporales

### 5.1 Preimagen de index_sha256

**CAMBIO PROPUESTO.** Para cada fila etiquetada, la entrada ordenada es:

    [row, source_position, timestamp_utc, label]

- row es el ordinal global de la fila en el dataset filtrado y etiquetado.
- source_position es el ordinal de la fila en la serie OHLCV original.
- En la secuencia de cada partición, source_position es estrictamente creciente y único. El primer valor debe igualar source_position_start y el último valor más uno debe igualar source_position_end.
- timestamp_utc es el instante normalizado según §5.2.
- label es una clase permitida de target.classes.

La secuencia conserva el orden de filas; no se ordena para producir el digest. Se serializa como JCS RFC 8785, UTF-8 sin BOM y sin salto de línea final. index_sha256 es SHA-256 de esos bytes.

### 5.2 Timestamps

**ACLARACIÓN y CAMBIO PROPUESTO.**

1. Aceptar timestamps RFC 3339 con Z o desplazamiento numérico explícito.
2. Rechazar timestamp sin zona, offset desconocido -00:00, segundos intercalares y precisión superior a nueve cifras decimales.
3. Validar calendario, fecha y offset antes de normalizar.
4. Convertir el instante a UTC con precisión de nanosegundos, sin truncamiento ni redondeo.
5. Antes de JCS, representar cada instante como YYYY-MM-DDTHH:MM:SS.fffffffffZ, con exactamente nueve cifras fraccionarias.
6. Rechazar instantes duplicados y secuencias no estrictamente crecientes para el mismo símbolo y timeframe. No ordenar ni reparar entradas.

El esquema v3 y el parser actual no establecen esta normalización completa; es una regla propuesta para 4.0.0.

### 5.3 Tipos de clases y etiquetas

**CAMBIO PROPUESTO.**

- target.classes y target.class_order son arrays no vacíos de enteros JSON, sin duplicados.
- class_order debe ser una permutación exacta de classes.
- label debe ser un miembro de classes del mismo tipo y valor numérico.
- Booleanos, null, strings, números fraccionarios, NaN e infinitos se rechazan. Un string numérico como "1" no se convierte a 1.
- JSON Schema define integer por valor numérico integral. Un valor numérico como 1.0 se trata como entero solo mediante una normalización explícita y limitada a valores finitos, sin fracción y dentro del rango seguro de JCS. Después de la normalización, 1 y 1.0 son el mismo valor y cuentan como duplicados. No se normalizan booleanos.

## 6. Calibración compartida

**CAMBIO PROPUESTO.** S1/4.0.0 admite únicamente calibración compartida con validation:

- calibration.fit_partition es exactamente "validation".
- validation.partitions.calibration.shared_with es exactamente "validation" y se requiere.
- Calibration y validation coinciden en límites de filas, límites fuente, n_rows, timestamps normalizados, conteos por clase e index_sha256.
- Calibration no introduce una partición ni frontera temporal separada.
- Solo se validan las fronteras train→validation y validation→test.
- validation.partitions.calibration se conserva; partition_manifest_sha256 cubre las cuatro particiones declaradas.
- La proyección de run_fingerprint contiene calibration y su relación shared_with.

Calibration independiente queda fuera de este contrato hasta que tenga representación, fit_partition y controles de purga completos. No se acepta shared_with = null en S1/4.0.0.

### 6.1 calibration_input_sha256

**CAMBIO PROPUESTO.** Su preimagen identifica exactamente las entradas entregadas al calibrador: índice, orden de clases, etiquetas y matrices de probabilidad RF/XGB, con las filas en el orden de calibration/validation y columnas en class_order.

Para evitar diferencias de dtype o endianess, cada probabilidad se convierte al patrón IEEE-754 binary64 big-endian y se representa como 16 caracteres hexadecimales minúsculos. Se rechazan valores no finitos o fuera de [0,1]; el cero negativo se normaliza a positivo. `y` tiene exactamente una etiqueta por fila; cada matriz de probabilidades tiene el mismo número de filas que `y` y una columna por elemento de `class_order`, en ese orden. La preimagen JCS tiene esta forma ilustrativa:

    {
      "schema": "tradingai.calibration-input.v1",
      "index_sha256": "<64 hex>",
      "class_order": [0, 1, 2],
      "y": [0],
      "proba_rf_f64be": [["3fe0000000000000", "3fd0000000000000", "3fd0000000000000"]],
      "proba_xgb_f64be": [["3fe0000000000000", "3fd0000000000000", "3fd0000000000000"]]
    }

calibration_input_sha256 es SHA-256 de los bytes JCS UTF-8 sin BOM ni salto final. No forma parte de run_fingerprint: es un digest derivado de entradas efectivas, cuya integridad se comprueba por separado.

## 7. Lifecycle, eventos y evidence

### 7.1 Transiciones

**REQUISITO EXISTENTE.** Génesis sealed, avance sealed → validated → approved, depreciación después de aprobación y revocación como estado que prohíbe el uso.

**CAMBIO PROPUESTO.** La tabla completa propuesta para 4.0.0 es:

| Estado anterior | Estado nuevo |
|---|---|
| Génesis | sealed |
| sealed | validated |
| validated | approved |
| approved | deprecated |
| sealed | revoked |
| validated | revoked |
| approved | revoked |
| deprecated | revoked |
| sealed | rejected |
| validated | rejected |

rejected y revoked son terminales. Se prohíben transiciones no listadas, estados repetidos y cualquier re-aprobación de un estado terminal. deprecated → revoked, sealed/validated → rejected son cambios propuestos; no se afirman como reglas existentes de AUD-04B.1.

event es el estado nuevo; la transición se deriva del evento previo aceptado del mismo modelo y el evento actual. Los timestamps no reordenan la secuencia.

### 7.2 Campos de evento

El payload canónico tiene exactamente nueve campos:

    sequence_number
    event_id
    model_id
    event
    at
    actor
    evidence
    manifest_sha256
    previous_event_sha256

El evento almacenado añade event_sha256, para diez campos en total.

Todos son obligatorios. sequence_number empieza en 1 y aumenta de uno en uno por modelo. El primer estado es sealed, con previous_event_sha256 igual a 64 ceros. Los eventos mantienen orden físico de inserción; no se ordenan, reparan ni reconstruyen automáticamente. manifest_sha256 permanece estable para ese modelo. event_id es globalmente único. Campos desconocidos se rechazan.

**CAMBIO PROPUESTO — tipos y formatos.** sequence_number es un entero entre 1 y 9007199254740991; event_id cumple `^evt_[0-7][0-9A-HJKMNP-TV-Z]{25}$`; model_id cumple `^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$`; event es uno de los seis estados de §7.1; at usa las reglas RFC 3339, zona explícita y normalización UTC sin pérdida de precisión de §5.2, con representación normalizada exacta `YYYY-MM-DDTHH:MM:SS.fffffffffZ`; actor es una cadena ASCII no vacía de hasta 128 caracteres con patrón `^[A-Za-z0-9][A-Za-z0-9._:@-]{0,127}$`; evidence sigue §7.3; manifest_sha256, previous_event_sha256 y event_sha256 son 64 caracteres hexadecimales minúsculos. En el primer evento previous_event_sha256 es exactamente 64 ceros; en los siguientes debe ser el event_sha256 del evento inmediatamente anterior en el orden físico para ese model_id.

**PENDIENTE DE APROBACIÓN.** El tipo del actor queda fijado como string, pero falta decidir el namespace/patrón que distingue identidades humanas y de servicio. No se debe inferir identidad o autoridad desde el texto actor.

### 7.3 Evidence cerrada por evento

**CAMBIO PROPUESTO.** Cada objeto evidence es cerrado; el evento sealed usa null.

| Evento | Campos de evidence |
|---|---|
| sealed | null |
| validated | report_sha256 (SHA-256 hex minúsculo), signature_sidecar_id (`sig_` más ULID 128-bit válido) |
| approved | approval_ref (string UTF-8 de 1–256 caracteres, sin controles, espacios externos ni solo espacios), signature_sidecar_id (`sig_` más ULID 128-bit válido) |
| deprecated | reason_code (string `^[a-z][a-z0-9_]{0,63}$`), replacement_model_id (model ID válido) |
| revoked | reason_code (string `^[a-z][a-z0-9_]{0,63}$`), incident_ref (string UTF-8 de 1–256 caracteres, sin controles, espacios externos ni solo espacios) |
| rejected | reason_code (string `^[a-z][a-z0-9_]{0,63}$`), report_sha256 (SHA-256 hex minúsculo), signature_sidecar_id (`sig_` más ULID 128-bit válido) |

Todos los campos de cada fila son obligatorios; no se permiten campos extra. Los hashes son SHA-256 hex minúsculos. signature_sidecar_id cumple `^sig_[0-7][0-9A-HJKMNP-TV-Z]{25}$`. replacement_model_id cumple el patrón de model ID y debe ser distinto del model ID del evento. La evidencia de depreciación declara un sustituto; la existencia y aprobación efectiva de ese sustituto se comprueba externamente.

approval_ref e incident_ref son referencias externas opacas, no rutas ni prueba de confianza. Los informes de validación/rechazo contienen al menos model_id, manifest_sha256, las métricas correspondientes y la afirmación de evaluación de test una sola vez. Su contenido y firma se verifican externamente.

**PENDIENTE DE APROBACIÓN.** El patrón sintáctico de reason_code queda propuesto, pero no se define un catálogo de valores. El contrato aprobado deberá decidir entre un catálogo versionado o códigos libres bajo ese patrón. No se debe inventar un enum durante la implementación. approval_ref e incident_ref son identificadores externos opacos: S1 solo aplica las restricciones de string anteriores, no resuelve su destino ni los interpreta como prueba.

## 8. Firmas Ed25519 y sidecar

### 8.1 Bytes firmados

**CAMBIO PROPUESTO.** La firma cubre los mismos bytes JCS que originan event_sha256: el payload de nueve campos, incluido evidence y excluido event_sha256.

    event_sha256 = SHA-256(JCS-UTF8(payload de nueve campos))
    signature = Ed25519(private_key, esos mismos bytes)

Los bytes no llevan BOM ni salto de línea final. El evento se almacena con la política de línea definida para el JSONL, fuera de la preimagen.

AUD-04B.1 §8.6 actualmente describe una firma que incluye event_sha256. Debe corregirse para coincidir con esta propuesta. La firma de nueve campos no crea circularidad: el hash se calcula primero sobre el payload; el sidecar externo contiene el digest derivado.

### 8.2 Sidecar

El objeto lateral exacto es:

    {
      "format_version": 1,
      "sidecar_id": "sig_<ULID>",
      "event_id": "evt_<ULID>",
      "event_sha256": "<64 hex>",
      "key_id": "<id>",
      "algorithm": "Ed25519",
      "signature_b64": "<Base64>"
    }

La referencia signature_sidecar_id se incorpora a evidence antes de canonicalizar el evento. No se incorpora un hash del sidecar al evento.

Reglas propuestas:

- format_version es el entero 1; otras versiones se rechazan si no están soportadas.
- algorithm es exactamente Ed25519.
- sidecar_id es globalmente único.
- (event_id, key_id) es globalmente único entre todas las versiones.
- event_id y event_sha256 deben coincidir con el evento referido.
- key_id es una cadena opaca de 1 a 128 caracteres ASCII del conjunto [A-Za-z0-9._:-]. La identidad, rol y confianza de esa clave se resuelven fuera de S1.
- signature_b64 es Base64 estándar RFC 4648 canónico, sin espacios; al decodificar y volver a codificar debe producir exactamente la cadena original y el resultado decodificado tiene exactamente 64 bytes.
- El objeto no admite campos desconocidos.
- Sidecar ausente, duplicado o mal asociado invalida estructuralmente la referencia.

S1 puede comprobar forma, unicidad y asociación si recibe el sidecar como entrada. No verifica la firma, rol, confianza o revocación de la clave ni un anclaje externo. Un sidecar asociado no autoriza inferencia.

## 9. run_fingerprint

### 9.1 Canonicalización común

**REQUISITO EXISTENTE.** RFC 8785 JCS es la canonicalización única. Se usa UTF-8 sin BOM, claves ordenadas por unidades UTF-16, arrays en su orden original y separadores sin espacios.

**ACLARACIÓN y CAMBIO PROPUESTO.** Números finitos están permitidos donde el esquema declare number, conforme a RFC 8785. NaN e infinitos se rechazan. Los campos que el esquema declara como strings decimales permanecen strings. Todo valor entero JSON debe satisfacer `abs(n) <= 9007199254740991` (2^53−1); los enteros fuera del rango seguro se rechazan.

La ausencia de una propiedad opcional se conserva como ausencia; un null explícito solo se conserva en propiedades anulables. No se rellenan defaults.

### 9.2 Allowlist propuesta

La proyección se construye mediante esta allowlist, no copiando el manifiesto completo.

| Rutas exactas | Regla |
|---|---|
| schema_version | Incluir. |
| model_id, created_at, sealed_at, status_at_seal, run_fingerprint | Excluir: identidad de salida, timestamps, estado de sello o resultado del propio cálculo. |
| git.source_bundle_sha256 | Incluir. |
| git.commit, git.dirty, git.branch, git.tag | Excluir: localizador/meta; dirty=false se valida como condición de admisión. |
| producer.name, producer.version, producer.python, producer.config_sha256 | Incluir. |
| producer.command | Excluir: texto de invocación sin normalización entre shells. Toda opción conductual debe reflejarse en configuración efectiva o campos tipados. |
| data.symbol, data.timeframe, data.provider, data.provider_version, data.dataset_sha256, data.raw_rows, data.feature_rows, data.labeled_rows, data.time_range.start, data.time_range.end, data.time_range.timezone, data.missing_data_policy, data.gap_policy, data.ohlcv_schema_version, data.alignment | Incluir. Los timestamps se normalizan; conteos se contrastan con datos disponibles. |
| data.snapshot_uri | Excluir: ubicación; el hash del contenido identifica los datos. |
| target.name, target.horizon_bars, target.vol_mult, target.classes, target.class_order, target.rule_sha256, target.nan_policy | Incluir. |
| features.ordered, features.count, features.definition_sha256, features.matrix_sha256, features.pipeline_version, features.code_sha256, features.parameters.lookback_max, features.parameters.lookback_min, features.parameters.lookback_step, features.parameters.lookback_total, features.nan_policy | Incluir propiedades presentes; ausencia se conserva. |
| training.task, training.models.rf.library, training.models.rf.version, training.models.rf.params.n_estimators, training.models.rf.params.max_depth, training.models.rf.params.class_weight, training.models.rf.params.random_state, training.models.rf.params.n_jobs, training.models.xgb.library, training.models.xgb.version, training.models.xgb.params.n_estimators, training.models.xgb.params.max_depth, training.models.xgb.params.learning_rate, training.models.xgb.params.subsample, training.models.xgb.params.colsample_bytree, training.models.xgb.params.random_state, training.models.xgb.params.tree_method, training.models.xgb.params.device, training.models.xgb.params.objective, training.models.xgb.params.num_class, training.models.xgb.params.eval_metric, training.models.xgb.params.n_jobs, training.ensemble.method, training.ensemble.weights.rf, training.ensemble.weights.xgb, training.seed | Incluir propiedades presentes; null permitido se conserva como null. |
| training.environment.python, training.environment.numpy, training.environment.pandas, training.environment.scikit_learn, training.environment.xgboost, training.environment.joblib, training.environment.os, training.environment.arch, training.environment.cuda_version, training.environment.cudnn_version | Incluir. Las rutas numpy, pandas, scikit_learn, xgboost, joblib, os y arch son adiciones requeridas propuestas para 4.0.0. CUDA/cuDNN pueden ser null si no aplican. |
| training.hardware.device, training.hardware.gpu_model, training.hardware.cuda_version, training.hardware.cpu_count, training.hardware.ram_gb, training.determinism.bitwise_reproducible, training.determinism.n_jobs, training.determinism.omp_num_threads, training.determinism.xgb_tree_method, training.determinism.xgb_deterministic_histogram, training.determinism.gpu_deterministic | Incluir. Los campos GPU/CUDA anulables conservan null explícito. |
| validation.split_method, y para cada partición train, validation, calibration, test: row_start, row_end, source_position_start, source_position_end, n_rows, time_start, time_end, class_counts, index_sha256, shared_with cuando exista | Incluir. Timestamps normalizados; propiedades opcionales conservan presencia. En calibration, shared_with es requerido y vale validation. |
| validation.purge.rows_between_partitions, validation.purge.label_horizon_bars, validation.purge.embargo_rows | Incluir. |
| validation.purge.label_purge_satisfied, validation.leakage_checks.disjoint, validation.leakage_checks.purge_satisfied, validation.leakage_checks.labels_within_partition | Excluir: resultados derivados; todos deben validarse como true. |
| validation.partition_manifest_sha256 | Excluir: digest derivado de las cuatro particiones. |
| validation.evaluation.metric_spec_version, validation.evaluation.primary_metric, validation.evaluation.test_evaluated_once, validation.evaluation.evaluation_code_sha256, validation.evaluation.evaluated_at | Excluir: describen el protocolo o resultado de evaluación y no la intención de entrenamiento; evaluated_at también es temporal. test_evaluated_once debe ser true para admitir el manifiesto. Si una futura regla de entrenamiento o calibración depende de una de estas propiedades, debe convertirse en una ruta tipada incluida, con cambio de contrato explícito. |
| calibration.mode, calibration.method, calibration.fit_partition, calibration.classes, calibration.class_order, calibration.n_calibrators | Incluir. |
| calibration.base_model_id, calibration.base_artifact_sha256.rf, calibration.base_artifact_sha256.xgb | Incluir solo con mode=external_run. Excluir con in_pipeline, donde referencian el propio modelo y sus outputs. |
| calibration.calibration_input_sha256, calibration.artifact_sha256 | Excluir: digest de entradas efectivas derivadas y artefacto de salida; comprobar por separado. |
| artifacts[] y sus propiedades role, path, sha256, bytes, media_type, format, serializer | Excluir: outputs. Se valida exactamente un artefacto por rol. |
| metrics.path, metrics.sha256, metrics.schema_version | Excluir: resultados evaluativos. |
| extensions | Excluir del fingerprint; siempre queda en los bytes cubiertos por manifest.sha256. En la primera revisión de 4.0.0 se propone exigir `{}` hasta que exista un contrato verificable de namespaces y schemas de extensión. |

La preimagen es un objeto JSON nuevo que conserva la estructura y nombres de las rutas permitidas, y contiene exactamente esas rutas; no copia el manifiesto entero. Todos los campos raíz del esquema 4.0.0 son obligatorios. Los campos anidados opcionales se incluyen únicamente cuando aparecen. Las propiedades anulables conservan null si está presente. En calibration in_pipeline, base_model_id debe seguir validándose contra model_id, aunque se excluya del fingerprint.

### 9.3 Entorno y extensiones

El diseño §5.5 promete versiones de Python, numpy, pandas, scikit-learn, xgboost, joblib, sistema operativo y arquitectura. El esquema v3 solo permite Python, CUDA y cuDNN en training.environment, y Python es opcional allí. **CAMBIO PROPUESTO:** 4.0.0 exige python, numpy, pandas, scikit_learn, xgboost, joblib, os y arch como strings no vacíos en training.environment. Todos forman parte de la proyección. cuda_version y cudnn_version pueden seguir ausentes o ser null cuando no apliquen; si aparecen, se incluyen preservando la distinción entre ausencia y null.

**CAMBIO PROPUESTO.** La intención futura es que extensions contenga metadata estable, versionada, no sensible y no conductual. Cada namespace usaría una clave namespaced y un objeto cuyo schema_version identifica un schema registrado. Los valores de extensión no se usarían como configuración efectiva; cualquier extensión que altere el entrenamiento tendría que elevarse a un campo tipado o formar parte de producer.config_sha256.

El esquema genérico no puede demostrar que un objeto de extensión no contenga secretos, rutas temporales o valores volátiles. Por eso, para la primera versión de 4.0.0 se recomienda normativamente exigir extensions = {}. Permitir namespaces no vacíos queda pendiente hasta definir schemas registrados, límites de tamaño y validación de sensibilidad/estabilidad. Las extensiones 3.0.0 conservan sin cambios su contrato histórico.

### 9.4 Relaciones de hashes y ciclos

    index_sha256
      = SHA-256(JCS([row, source_position, timestamp_utc, label]...))

    partition_preimage = {
      "train": validation.partitions.train,
      "validation": validation.partitions.validation,
      "calibration": validation.partitions.calibration,
      "test": validation.partitions.test
    }
    partition_manifest_sha256
      = SHA-256(JCS(partition_preimage))

En partition_preimage cada valor es el objeto completo de la partición según el esquema 4.0.0, incluidos todos sus campos declarados, index_sha256 y shared_with cuando corresponda. No se omiten campos por ser redundantes. JCS ordena las propiedades de los objetos; el orden de arrays, incluido class_counts, se conserva.

    calibration_input_sha256
      = SHA-256(JCS de la preimagen calibration-input.v1)

    run_fingerprint
      = SHA-256(JCS de la allowlist de intención 4.0.0)

    manifest.sha256
      = SHA-256 de los bytes almacenados del manifiesto según la política 4.0.0

    event_sha256
      = SHA-256(JCS(payload canónico de nueve campos del evento))

run_fingerprint contiene directamente las propiedades permitidas de las particiones e index_sha256; no incluye partition_manifest_sha256. calibration_input_sha256 no entra en el fingerprint porque identifica entradas efectivas derivadas. Los digests de outputs y el fingerprint mismo tampoco se incluyen. Ninguna preimagen incluye el digest que produce. No hay dependencias circulares.

Para manifest.sha256, el archivo se almacena como bytes JCS más exactamente un LF final; el hash del archivo incluye ese LF. Para index, particiones, fingerprint y eventos, JCS no añade LF y los bytes hasheados no lo incluyen.

### 9.5 Vector reducido conservado

Este vector solo verifica el hash JCS de un objeto reducido. No contiene todas las rutas del manifiesto ni demuestra que la selección de la allowlist sea correcta.

    {"calibration_intent":{"fit_partition":"validation","method":"sigmoid","mode":"in_pipeline"},"data":{"dataset_sha256":"b"},"features":{"ordered":["close","volume"]},"git":{"source_bundle_sha256":"a"},"schema_version":"3.0.0","target":{"horizon_bars":1},"training":{"seed":42},"validation_intent":{"split_method":"chronological_holdout"}}

SHA-256 esperado:

    ed01f9cea45b644c561b6eb0346c7450b7836abb35f4ece1ede5b265e3722157

Las rutas validation_intent y calibration_intent pertenecen al vector reducido y no son rutas del manifiesto real. El vector no es una fixture 4.0.0 ni evidencia de implementación.

## 10. API y límites de S1

**REQUISITO EXISTENTE.** Los validadores públicos actuales devuelven list[str].

**ACLARACIÓN propuesta.** Mantener nombres y retornos públicos; se puede diseñar un núcleo tipado interno con adaptadores, pero este documento no afirma que exista. Los wrappers deben preservar mensajes exactos usados por consumidores existentes hasta que una migración se apruebe.

Separar:

1. Validez de JSON/schema y relaciones declaradas.
2. Transición estructural permitida.
3. Evidencia declarada y asociada.
4. Firma y anclaje criptográficamente verificados.
5. Autorización efectiva.

S1 solo cubre los primeros tres niveles hasta donde sus entradas permitan. No verifica firmas o claves, no inspecciona datos reales si no se le entregan, no deserializa artefactos y no concede autorización de inferencia.

## 11. Criterios de aceptación futuros

Los siguientes son criterios para una futura implementación; no son pruebas ejecutadas.

| ID | Criterio futuro |
|---|---|
| V4-U01 | Un manifiesto 3.0.0 se valida solo con reglas 3.0.0; uno 4.0.0 solo con reglas 4.0.0; versión desconocida se rechaza. |
| V4-U02 | Gaps de filas y fuente se calculan por separado, incluyendo el ejemplo con filas descartadas. |
| V4-U03 | La purga se comprueba en todas las fronteras reales con max(H,E). |
| V4-U04 | Para calibration compartida coinciden límites, tiempos normalizados, conteos e índice; no aparece una frontera calibration independiente. |
| V4-U05 | Timestamps duplicados/desordenados, más de nueve decimales y zona desconocida se rechazan; UTC se normaliza sin redondeo. |
| V4-U06 | Clases duplicadas, booleanos, strings y etiquetas fuera de classes se rechazan; integral numérico se normaliza conforme a la regla documentada. |
| V4-U07 | Transiciones fuera de la tabla, estados repetidos y salidas de rejected/revoked se rechazan. |
| V4-U08 | Evidence con campos desconocidos o tipos incorrectos se rechaza. |
| V4-U09 | Sidecars ausentes, duplicados o vinculados a otro evento se rechazan; la validación estructural no declara firma verificada. |
| V4-U10 | Cambiar cada ruta incluida altera el fingerprint; cambiar rutas excluidas no; ausencia se distingue de null. |
| V4-U11 | Se recalculan index_sha256, partition_manifest_sha256, calibration_input_sha256 y event_sha256 desde sus preimágenes independientes. |
| V4-U12 | Los wrappers públicos mantienen list[str] y sus mensajes históricos. |
| V4-U13 | En la primera versión 4.0.0, extensions={} se acepta y cualquier namespace no vacío se rechaza; el cambio no altera el fingerprint. |
| V4-U14 | Con una secuencia por fila disponible, posiciones fuente negativas, repetidas o no crecientes se rechazan, y los límites declarados deben coincidir con el primer valor y el último más uno. Sin esa secuencia, S1 valida solo estructura y aritmética de los límites; no afirma haber verificado sus valores reales. |
| V4-U15 | Un verificador posterior reconstruye las posiciones desde el dataset original, aplica las reglas de filtrado y recalcula secuencia, límites e index_sha256; no forma parte de la validación S1 basada solo en manifiesto. |

## 12. Trazabilidad R13-DESIGN-R3.2

| ID | Decisión | Origen R3.2 | Sección anterior | Sección 4.0.0 | Cambio requerido | Futura prueba de aceptación | Clase / estado |
|---|---|---|---|---|---|---|---|
| V4-D01 | 3.0.0 congelado y dispatch por versión | R3.2-02 | §5.1, §14 | §§2–3 | Validador/schema separado por versión | V4-U01 | CAMBIO PROPUESTO; pendiente |
| V4-D02 | Ordinal fuente antes del filtrado, secuencia estricta y límites derivados de sus extremos | R3.2-01 | §5.6 | §§4.1, 4.3, 5.1 | Añadir límites; definir unicidad/monotonía y distinguir verificación estructural de reconstrucción de datos | V4-U02/U14/U15 | CAMBIO PROPUESTO; pendiente |
| V4-D03 | Gap de filas distinto de gap fuente | R3.2-01 | §5.6 | §4.2 | Calcular ambos; definir rows_between | V4-U02 | ACLARACIÓN y CAMBIO PROPUESTO |
| V4-D04 | Purga gap_source >= max(H,E) | R3.2-01 | §5.6 | §4.2 | Aclarar que H/E son cotas del mismo hueco | V4-U03 | CAMBIO PROPUESTO; pendiente |
| V4-D05 | Calibración solo compartida con validation | R3.2-03 | §§5.6–5.7 | §6 | Restringir shared_with y fit_partition | V4-U04 | CAMBIO PROPUESTO; pendiente |
| V4-D06 | Tipos/timestamps de índice | R3.2-01/03/06 | §§5.6, 5.11 | §5 | Normalización ns/UTC y clases únicas | V4-U05/U06 | ACLARACIÓN y CAMBIO PROPUESTO |
| V4-D07 | Estados rejected/revoked terminales | R3.2-04 | §§4.2, 8.3 | §7.1 | Añadir transiciones propuestas | V4-U07 | CAMBIO PROPUESTO; pendiente |
| V4-D08 | Evidence cerrada por evento | R3.2-04 | §§7.8.2, 8.6 | §§7.2–7.3 | Definir schema de evento/evidence | V4-U08 | CAMBIO PROPUESTO; catálogo reason_code pendiente |
| V4-D09 | Firma de payload de nueve campos | R3.2-05 | §§5.11, 7.8.2, 8.6 | §8 | Corregir contradicción de §8.6 | V4-U09 | CAMBIO PROPUESTO; pendiente |
| V4-D10 | Sidecar asociado sin hash circular | R3.2-05 | §7.8 | §8 | Añadir sidecar ID, unicidad y validación estructural | V4-U09 | CAMBIO PROPUESTO; pendiente |
| V4-D11 | Allowlist exacta de fingerprint | R3.2-06 | §5.11/U11 | §9 | Definir campos y exclusiones 4.0.0 | V4-U10 | CAMBIO PROPUESTO; pendiente |
| V4-D12 | Añadir entorno prometido por el diseño | R3.2-06 | §5.5 | §9.2 | Incorporar versiones faltantes al esquema futuro | V4-U10 | CAMBIO PROPUESTO; pendiente |
| V4-D13 | Extensions vacías al inicio; namespaces versionados en una ampliación futura | R3.2-06 | §5.1/§5.11 | §9.3 | Exigir extensions={} en 4.0 inicial; excluir del fingerprint | V4-U13 | CAMBIO PROPUESTO; pendiente |
| V4-D14 | Preservar wrappers list[str] | R3.2-06, R3.2-07 | interfaces S1 | §10 | Dispatch/versionado bajo API compatible | V4-U12 | ACLARACIÓN |
| V4-D15 | S1 no verifica datos reales ni autoriza inferencia | R3.2-01/04/05 | §§6, 8.3 | §§1, 4.3, 8, 10 | Separar niveles de validación | V4-U02/U09 | REQUISITO EXISTENTE y ACLARACIÓN |

## 13. Decisiones pendientes de aprobación

Las siguientes decisiones están documentadas como propuestas y no se consideran aprobadas:

1. Adoptar 4.0.0 como versión mayor y mantener dispatch dual.
2. Adoptar source_position como ordinal de la serie OHLCV original.
3. Aprobar la semántica de embargo_rows como cota sobre el mismo gap y la fórmula max(H,E).
4. Limitar S1 a calibration compartida con validation.
5. Añadir las transiciones a rejected y deprecated → revoked.
6. Adoptar evidence y sidecar Ed25519 según esta propuesta, incluidos los nueve campos firmados.
7. Aprobar allowlist, reglas de environment y extensions={} para 4.0.0 inicial; definir el contrato de namespaces antes de permitir extensiones no vacías.
8. Resolver el catálogo de reason_code.

Una aprobación de este documento requerirá decisión humana explícita. Hasta entonces, el contrato permanece en estado de propuesta.

## 14. Seguridad y alcance preservados

Permanecen intactos el alcance de S2–S7, la prohibición de deserializar durante S1, las restricciones de cuarentena, la separación entre diseño/implementación/auditoría, la prohibición de autorizar inferencia desde S1 y la protección de datasets, modelos y Parquet.

Este documento no añade loaders, writer, registry, integración de entrenamiento, backtesting, PaperBroker, RiskManager, inferencia ni ejecución real. No aprueba S1, no autoriza R13-IMPLEMENTATION y no inicia S2.
