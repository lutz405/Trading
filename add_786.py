import json, re
from pathlib import Path

root = Path(r"C:\Users\USER\Documents\GitHub\Trading")
doc = root / "docs" / "aud04b_model_provenance_v3_design.md"
t = doc.read_text(encoding="utf-8")

# Find where to insert §7.8.6 - look for §7.8.5 end and §7.8.7 start
idx_785 = t.find("### 7.8.5")
idx_787 = t.find("### 7.8.7")

print("7.8.5 at:", idx_785)
print("7.8.7 at:", idx_787)

# Find where to insert 7.8.6 - between 7.8.5 and 7.8.7
if idx_785 >= 0 and idx_787 >= 0:
    section_785_end = t.find("\n### ", idx_785+1)
    if section_785_end < 0:
        section_785_end = t.find("\n---", idx_785+1)
    if section_785_end > idx_785:
        # Insert 7.8.6 between 7.8.5 and 7.8.7
        seven86_content = '''\n### 7.8.6 Anclaje externo del ltimo hash conocido

Una cadena de hashes local no puede detectar por s misma la eliminacin de su propia cola. Este es un limite fundamental de cualquier esquema de integridad baso en hashes puramente local.

Definir un mecanismo de anclaje externo que permita comprobar ltimo hash conocido:

- Cada vez que se agrega un nuevo evento al lifecycle.jsonl, su event_sha256 debe anclarse (registrarse) en un almacn de confianza externo. Las opciones incluyen:
  - Una transaccin en un Git firmado del repositorio cannico (el commit que contiene el lifecycle.jsonl actualizado).
  - Un ltulo Merkle root en un servicio de tiempo distribuido (ej., AWS Quantum Ledger Database, o servicios equivalentes).
  - Un hash grabado en un almacn WORM (Write Once Read Many) de alta disponibilidad.
  - Una firma digital del ltimo evento ms reciente por una clave fuera del control del pipeline (clave privada fuera del repositorio, en un HSM o keychain del sistema operativo).

- El propio lifecycle.jsonl no puede ser la fuente de anclaje externo (evita el ciclo circular).

- Si el anclaje externo no est disponible en un momento dado, el loader debe operar en modo *integrity-only*:
  - No deserializar runs con estado approved o validated para inferencia o evaluacin.
  - Permitir slo audit purpose con verificacin de hashes de artefactos y manifiesto.
  - Registrar el evento con codigo E_ANCHOR_UNAVAILABLE.

- El anclaje externo debe actualizarse cada vez que se agrega un nuevo evento al registro. La frecuencia de actualizacin y el mnodo especfico son decisiones de poltica operativa, pero la regla fundamental es: ningn nuevo evento debe agregarse al registro sin que su event_sha256 sea anclado externamente (o el sistema opere en modo conservativo integrity-only hasta que el anclaje se restablezca).

**Regla transversal**: la ausencia de anclaje externo o cadena rota obliga al loader a modo *integrity-only* y deniega approved/inference sin firma verificable y anclaje de confianza.'''

# Insert the content
new_t = t[:section_785_end] + seven86_content + t[idx_787:]

# Verify JSON blocks still parse
blocks = __import__('re').findall(r'```json\n(.*?)```', new_t, __import__('re').S)
print("JSON blocks after insert:", len(blocks))
for i, b in enumerate(blocks, 1):
    try:
        json.loads(b)
        print("Block", i, "OK")
    except:
        print("Block", i, "FAIL")

# Write the new document
with open(doc, 'w', encoding='utf-8', newline='') as f:
    f.write(new_t)
print("\nInserted 7.8.6, new doc size:", len(new_t))