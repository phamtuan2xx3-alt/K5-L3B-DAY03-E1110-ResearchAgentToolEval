"""Download two public Ollama models into the project's isolated model store.

No Ollama server is needed during download. Manifests are published only after
every blob passes SHA256 validation; ollama list can then discover the models.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import time

import requests

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / ".local-models" / "models"
MODELS = [("qwen2.5", "3b"), ("llama3.2", "1b")]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_blob(entry: tuple[str, dict]) -> None:
    name, blob = entry
    digest = blob["digest"]
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("Unexpected registry digest")
    target = STORE / "blobs" / digest.replace(":", "-")
    expected = digest.split(":", 1)[1]
    if target.exists() and target.stat().st_size == blob["size"] and sha256(target) == expected:
        print(f"Already verified: {name} {digest[:19]}", flush=True)
        return
    part = target.with_suffix(".part")
    url = f"https://registry.ollama.ai/v2/library/{name}/blobs/{digest}"
    for attempt in range(3):
        try:
            offset = part.stat().st_size if part.exists() else 0
            response = requests.get(url, headers={"Range": f"bytes={offset}-"} if offset else {}, stream=True, timeout=(30, 180))
            if offset and (response.status_code != 206 or not response.headers.get("Content-Range", "").startswith(f"bytes {offset}-")):
                response.close()
                offset = 0
                response = requests.get(url, stream=True, timeout=(30, 180))
            response.raise_for_status()
            total = offset
            next_report = total + 64 * 1024 * 1024
            with response, part.open("ab" if offset else "wb") as stream:
                for chunk in response.iter_content(chunk_size=4 * 1024 * 1024):
                    if not chunk:
                        continue
                    stream.write(chunk)
                    total += len(chunk)
                    if total >= next_report:
                        print(f"{name}: {total / 1024**2:.0f}/{blob['size'] / 1024**2:.0f} MiB", flush=True)
                        next_report = total + 64 * 1024 * 1024
            if part.stat().st_size != blob["size"] or sha256(part) != expected:
                part.write_bytes(b"")
                raise ValueError(f"Size/SHA256 mismatch for {name}")
            part.replace(target)
            print(f"Verified: {name} {digest[:19]} ({blob['size'] / 1024**2:.1f} MiB)", flush=True)
            return
        except (requests.RequestException, OSError, ValueError) as exc:
            print(f"{name}: download attempt {attempt + 1}/3 failed ({type(exc).__name__})", flush=True)
            if attempt == 2:
                raise
            time.sleep(10)


def main() -> None:
    (STORE / "blobs").mkdir(parents=True, exist_ok=True)
    (STORE.parent / ".e1110-managed").write_text(str(ROOT), encoding="utf-8")
    manifests = []
    blobs = {}
    for name, tag in MODELS:
        response = requests.get(f"https://registry.ollama.ai/v2/library/{name}/manifests/{tag}", timeout=30)
        response.raise_for_status()
        manifest = response.json()
        manifests.append((name, tag, manifest))
        for blob in [manifest["config"], *manifest["layers"]]:
            blobs.setdefault(blob["digest"], (name, blob))
    print(f"Downloading {len(blobs)} blobs for qwen2.5:3b and llama3.2:1b into {STORE}", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(download_blob, blobs.values()))
    for name, tag, manifest in manifests:
        path = STORE / "manifests" / "registry.ollama.ai" / "library" / name / tag
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest), encoding="utf-8")
    (STORE.parent / "weights-ready.json").write_text(json.dumps({"models": [f"{n}:{t}" for n, t in MODELS], "verified_sha256": True}, indent=2), encoding="utf-8")
    print("DONE: both models downloaded and SHA256 verified.", flush=True)


if __name__ == "__main__":
    main()
