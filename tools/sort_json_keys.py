#!/usr/bin/env python3
"""Sort JSON object keys recursively and write output.

Usage:
  python tools/sort_json_keys.py i18n/es.json --inplace --backup
"""
import argparse
import json
import shutil
from pathlib import Path


def sort_obj(o):
    if isinstance(o, dict):
        return {k: sort_obj(o[k]) for k in sorted(o.keys(), key=str)}
    if isinstance(o, list):
        return [sort_obj(v) for v in o]
    return o


def main():
    p = argparse.ArgumentParser(description="Sort JSON keys recursively")
    p.add_argument("paths", nargs="+", help="JSON file(s) to sort")
    p.add_argument("--inplace", action="store_true", help="Overwrite input file(s)")
    p.add_argument("--backup", action="store_true", help="Save a .bak copy when using --inplace")
    args = p.parse_args()

    for path_str in args.paths:
        path = Path(path_str)
        if not path.exists():
            print(f"File not found: {path}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Failed to parse {path}: {e}")
            continue

        sorted_data = sort_obj(data)
        output = json.dumps(sorted_data, ensure_ascii=False, indent=4)

        if args.inplace:
            if args.backup:
                bak = path.with_suffix(path.suffix + ".bak")
                shutil.copyfile(path, bak)
            path.write_text(output + "\n", encoding="utf-8")
            print(f"Wrote: {path}")
        else:
            print(output)


if __name__ == "__main__":
    main()
