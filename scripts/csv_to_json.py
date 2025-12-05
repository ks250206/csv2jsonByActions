#!/usr/bin/env python
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

# CSV は data/ 以下だけを対象
DATA_ROOT = Path("data")
# 変換結果 JSON は output/ 以下に保存
OUTPUT_ROOT = Path("output")


def csv_to_json(csv_path: Path, output_root: Path = OUTPUT_ROOT) -> Path:
    """
    1つの CSV ファイルを JSON (配列形式) に変換し、
    リポジトリ内の output/ 配下に同じパス構造で保存する。

    例:
      data/sample.csv          -> output/data/sample.json
      data/users/list.csv      -> output/data/users/list.json

    CSV は 1 行目をヘッダ行として DictReader で読み取る前提。
    """
    if not csv_path.exists():
        print(f"[WARN] CSV not found, skip: {csv_path}", file=sys.stderr)
        return (output_root / csv_path).with_suffix(".json")

    rows: list[dict[str, Any]] = []

    # UTF-8 前提。必要なら encoding は環境に合わせて変更
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))

    # output/ 以下に元のパス構造ごと JSON を配置
    json_path = (output_root / csv_path).with_suffix(".json")
    json_path.parent.mkdir(parents=True, exist_ok=True)

    # ensure_ascii=False で日本語などもそのまま出力
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Converted: {csv_path} -> {json_path}")
    return json_path


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "Usage: python scripts/csv_to_json.py <csv1> [<csv2> ...]",
            file=sys.stderr,
        )
        return 1

    csv_files = [Path(arg) for arg in argv[1:]]

    for csv_path in csv_files:
        # .csv 以外はスキップ
        if csv_path.suffix.lower() != ".csv":
            print(f"[WARN] Not a CSV, skip: {csv_path}", file=sys.stderr)
            continue

        # data/ 以下以外の CSV は対象外にする
        try:
            # Python 3.9+ の is_relative_to を利用
            if not csv_path.resolve().is_relative_to(DATA_ROOT.resolve()):
                print(f"[WARN] CSV is not under 'data/', skip: {csv_path}", file=sys.stderr)
                continue
        except AttributeError:
            # もし古い Python を使う場合のフォールバック（Actions では 3.12 なので通らない）
            if DATA_ROOT.resolve() not in csv_path.resolve().parents:
                print(f"[WARN] CSV is not under 'data/', skip: {csv_path}", file=sys.stderr)
                continue

        csv_to_json(csv_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

