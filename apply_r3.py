import json, re
from pathlib import Path

root = Path(r"C:\Users\USER\Documents\GitHub\Trading")
doc = root / "docs" / "aud04b_model_provenance_v3_design.md"
t = doc.read_text(encoding="utf-8")

# Read the current document and replace §8.3
old_marker = "### 8.3 Política de estado por propósito"
old_start = t.find(old_marker)
if old_start < 0:
    print("§8.3 not found")
    exit(1)

# Find the end of §8.3 (next ## section)
old_end = t.find("## 9", old_start)
if old_end < 0:
    old_end = len(t)

print("§8.3 old length:", old_end - old_start)

# The new §8.3 content
new_section = '''### 8.3 Política de estado por propósito

La deserialización solo está permitida cuando la cadena de ciclo de vida y la autenticidad del manifiesto son verificables. La política por propósito es la siguiente:

| Estado efectivo | `inference` | `evaluation` | `audit` (solo metadata) |
|---|:---:|:---:|:---:|
| `sealed` | **No recomendado** para inferencia producción. Solo para auditoría/evaluación controlada si no hay firma válida. | **No** para evaluación formal. Puede usarse con verificación de integridad manual. | **Sí** — solo metadata, sin deserializar el payload. |
| `validated` | **No** para inferencia. Solo con autorización del verificador que emitió el informe firmado y anclaje externo válido. | **Sí** — con informe de re-evaluación firmado, cadena de ciclo de vida verificada y `manifest.sig` verificado. | **Sí** — metadata + verificación de integridad. |
| `approved` | **No** sin firma Ed25519 válida y cadena de eventos verificada. | **No** sin cadena de ciclo de vida verificada y anclaje externo. | **Sí** — solo con firma Ed25519 válida en `manifest.sig`, evento `approved` firmado en el registro, cadena verificada y estado vigente (sin caducidad). |
| `deprecated` | **No**. Requiere run sustituto `approved`. | **No**. Usar run sustituto. | **Sí** — metadata, sin deserializar. |
| `revoked` | **No**. Prohibido su uso incluso si los hashes son correctos. | **No**. Prohibido. | **Solo forense** — con autorización administrativa. |
| `rejected` | **No**. | **No**. | **No**. |
| Ausente o desconocido | **No**. | **No**. | **No**. |

#### Límites y advertencias adicionales

- **Firma no disponible:** Si no hay clave Ed25519 privada para verificar `manifest.sig` y los eventos `approved` en el registro, el sistema debe limitarse a modo *integrity-only*: los hashes de artefactos y el manifiesto pueden verificarse, pero **nunca** se permite la deserialización para `inference` o `evaluation` con fines de confianza. Solo `audit` purpose con inspección de metadatos está permitido.

- **Registro manipulado o sin anclaje externo:** Si el `lifecycle.jsonl` no puede verificarse (cadena rota, eventos faltantes, sin firma Ed25519 en eventos `approved`, o sin anclaje externo confiable), el loader debe:
  1. **No deserializar** ningún run con estado `approved` o `validated` para inferencia o evaluación.
  2. Permitir inspección de solo metadata (`audit`) de runs `sealed` si los hashes de artefactos y el manifiesto son válidos.
  3. Registrar el fallo con código de error `E_CHAIN_UNAVAILABLE` y continuar en modo *integrity-only*.

- **Confusión de firma con seguridad del pickle:** Una firma Ed25519 válida autentica el origen del run, pero **no** garantiza que el contenido del pickle sea seguro. La firma forma parte de un plan de migración futura a un formato de inferencia más seguro (ONNX o equivalente). Mantener el aislamiento del proceso de carga (mínimos privilegios, sandbox, límites de memoria/tiempo) sigue siendo obligatorio independientemente de la firma.

- **Corrida entre verificación y deserialización (TOCTOU):** El loader debe usar el buffer único verificado en los pasos 7-9 (hashes, estado, coherencia) y **nunca** volver a abrir la ruta del archivo para `joblib.load`. La deserialización debe ocurrir exclusivamente sobre los bytes ya leídos y cuya integridad fue comprobada.

- **Carga de runs `sealed` sin firma:** Un run `sealed` (sin evento `approved` en el registro) puede cargarse con propósito `audit` para inspección de metadatos y verificación de hashes, pero **no** para inferencia ni evaluación formal. Si se necesita inferencia, el run debe promocionarse a `validated` o `approved` mediante los flujos correspondientes.

#### Tabla de decisión rápida para el loader

| Acción | Estado `sealed` | Estado `validated` | Estado `approved` | Sin cadena verificable |
|---|---|---|---|---|
| Deserializar para `inference` | **No** (solo audit) | **No** (solo con autorización del verificador y anclaje externo) | **No** (sin firma verificada y anclaje) | **No** |
| Deserializar para `evaluation` | **No** (solo audit con integridad) | **Sí** (con informe firmado, cadena verificada y anclaje) | **Sí** (con firma válida y cadena verificada) | **No** |
| Cargar metadata (`audit`) | **Sí** (hashes OK) | **Sí** (hashes OK) | **Sí** (hashes + firma OK) | **No** (cadena rota) |
| Firmar aprobación pendiente | N/A | N/A | Requiere clave Ed25519 + evento en registro | N/A |

**Regla transversal:** la ausencia de firma verificada o anclaje externo obliga al loader a modo *integrity-only* y deniega `approved`/`inference` sin autenticación completa.
'''

# Replace
new_doc = t[:old_start] + new_section + t[old_end:]

# Write back
with open(doc, 'w', encoding='utf-8', newline='') as f:
    f.write(new_doc)
print('§8.3 replaced successfully, new doc size:', len(new_doc))
"