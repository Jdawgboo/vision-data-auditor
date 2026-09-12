"""Audit image dataset manifests without a vision framework dependency."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class AuditReport:
    missing_files: tuple[str, ...]
    duplicate_groups: dict[str, tuple[str, ...]]
    class_counts: dict[str, int]
    imbalance_ratio: float


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(rows: Sequence[Mapping[str, Any]], root: Path = Path(".")) -> AuditReport:
    missing: list[str] = []
    hashes: dict[str, list[str]] = defaultdict(list)
    labels: Counter[str] = Counter()
    for row in rows:
        relative = str(row["path"])
        label = str(row["label"])
        labels[label] += 1
        location = root / relative
        if not location.is_file():
            missing.append(relative)
            continue
        hashes[_digest(location)].append(relative)
    duplicates = {digest: tuple(paths) for digest, paths in hashes.items() if len(paths) > 1}
    counts = dict(sorted(labels.items()))
    ratio = max(counts.values()) / min(counts.values()) if counts and min(counts.values()) else 0.0
    return AuditReport(tuple(sorted(missing)), duplicates, counts, ratio)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit image dataset manifest JSON")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    report = audit(json.loads(args.manifest.read_text()), args.root)
    print(json.dumps({"missing_files": report.missing_files, "duplicate_groups": report.duplicate_groups, "class_counts": report.class_counts, "imbalance_ratio": report.imbalance_ratio}, indent=2))
    if report.missing_files or report.duplicate_groups:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
