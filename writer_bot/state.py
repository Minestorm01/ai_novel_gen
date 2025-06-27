"""Centralised story-state and entity registry helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List

META = Path("book/meta")
META.mkdir(parents=True, exist_ok=True)

REGISTRY_PATH = META / "entity_registry.yaml"
SCENE_PATH = META / "scene_state.json"
HASH_PATH = META / "seen_hashes.txt"


# ───────────────────────── helper loads ─────────────────────────
def load_registry() -> Dict[str, object]:
    import yaml
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))


def load_scene() -> Dict[str, object]:
    if SCENE_PATH.exists():
        return json.loads(SCENE_PATH.read_text("utf-8"))
    return {}


def save_scene(state: Dict[str, object]) -> None:
    SCENE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), "utf-8")


# ───────────────────────── deduplication ────────────────────────
def is_duplicate(text: str) -> bool:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if not HASH_PATH.exists():
        HASH_PATH.write_text(digest + "\n")
        return False

    seen: List[str] = HASH_PATH.read_text("utf-8").splitlines()
    if digest in seen:
        return True
    HASH_PATH.write_text("\n".join(seen + [digest]), "utf-8")
    return False
