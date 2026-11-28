"""ORACLE-ART-02 — verificador independiente del oracle normativo v4 R5.

Ubicación aprobada por D6: área de pruebas/CI. No importa módulos de
producción, no añade dependencias y no se ejecuta en el camino productivo.
Este archivo es un artefacto materializado en G4; su verificación independiente
pertenece a G5.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import rfc8785  # dependencia ya declarada; no se añade ninguna nueva

VERSION = "ORACLE_NORMATIVE_V4_R5"
DECLARED_INPUTS = (
    Path(__file__).resolve().parents[1]
    / "docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json",
)
EXPECTED_CHECKSUM = "7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b"


def load_transcription() -> dict:
    """Leer la transcripción canonicalizada declarada como única entrada."""
    return json.loads(DECLARED_INPUTS[0].read_text(encoding="utf-8"))


def canonical_bytes(obj: dict) -> bytes:
    """Canonicalización JCS; única primitiva permitida."""
    return rfc8785.dumps(obj)


def expected_checksum() -> str:
    """SHA-256 de la transcripción canonicalizada."""
    return hashlib.sha256(canonical_bytes(load_transcription())).hexdigest()


def verify() -> list[str]:
    """Comparar versión, entradas y checksum; falla cerrado sin fallback."""
    errors: list[str] = []
    obj = load_transcription()
    if obj.get("version") != VERSION:
        errors.append("ORACLE_VERSION_MISMATCH")
    if not obj.get("entries"):
        errors.append("ORACLE_INCOMPLETE")
    if expected_checksum() != EXPECTED_CHECKSUM:
        errors.append("ORACLE_CHECKSUM_MISMATCH")
    return sorted(set(errors))
