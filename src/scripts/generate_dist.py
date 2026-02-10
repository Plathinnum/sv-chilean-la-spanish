#!/usr/bin/env python3
"""Genera la carpeta `dist/[CP] StardewValleyEspañolLatinoRevisitado`.

Combina todos los JSON bajo `src/data/` en un único objeto y guarda
en `i18n/es.json`. Copia `manifest.json` y `content.json` a la raíz
del paquete dentro de `dist`.

Comportamiento por defecto:
- Recursivo: busca en subcarpetas de `src/data/`.
- Fusiona objetos JSON en un solo objeto (las claves encontradas luego
  sobrescriben las previas). Cuando ocurre un conflicto de valor se
  muestra una advertencia indicando las rutas y archivos implicados.
- Si existe la carpeta de salida se borra y se vuelve a crear (sobrescribir).
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Dict


def recursive_merge(dest: Dict[str, Any], src: Dict[str, Any], origins: Dict[str, str], file: str, path: str = "") -> None:
    for key, val in src.items():
        key_path = f"{path}.{key}" if path else key
        if key in dest:
            if isinstance(dest[key], dict) and isinstance(val, dict):
                recursive_merge(dest[key], val, origins, file, key_path)
            else:
                if dest[key] != val:
                    prev_file = origins.get(key_path, "(desconocido)")
                    print(f"Advertencia: conflicto en '{key_path}': valor de '{prev_file}' será sobrescrito por '{file}'")
                dest[key] = val
                origins[key_path] = file
        else:
            dest[key] = val
            origins[key_path] = file


def gather_json_files(data_dir: Path) -> list[Path]:
    return sorted(p for p in data_dir.rglob("*.json") if p.is_file())


def load_and_merge(data_dir: Path) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    origins: Dict[str, str] = {}
    files = gather_json_files(data_dir)
    if not files:
        print(f"No se encontraron archivos JSON en {data_dir}")
        return merged
    for p in files:
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error leyendo {p}: {e}")
            continue
        if not isinstance(data, dict):
            print(f"Advertencia: el archivo {p} no contiene un objeto JSON en la raíz; será ignorado.")
            continue
        recursive_merge(merged, data, origins, str(p))
    return merged


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def build_dist(repo_root: Path, package_name: str, overwrite: bool = True) -> None:
    data_dir = repo_root / "src" / "data"
    if not data_dir.exists():
        raise FileNotFoundError(f"No existe el directorio de datos: {data_dir}")

    merged = load_and_merge(data_dir)

    dist_root = repo_root / "dist"
    package_dir = dist_root / package_name
    if package_dir.exists():
        if overwrite:
            shutil.rmtree(package_dir)
        else:
            raise FileExistsError(f"La carpeta {package_dir} ya existe (use --overwrite para reemplazar)")
    package_dir.mkdir(parents=True, exist_ok=True)

    # Copiar manifest.json y content.json desde repo root
    for fname in ("manifest.json", "content.json"):
        src = repo_root / fname
        dst = package_dir / fname
        try:
            copy_file(src, dst)
        except FileNotFoundError:
            print(f"Advertencia: no se encontró {src}; se continúa sin copiar.")

    # Escribir i18n/es.json
    i18n_dir = package_dir / "i18n"
    i18n_dir.mkdir(parents=True, exist_ok=True)
    out_file = i18n_dir / "es.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"Creado paquete: {package_dir}")
    print(f"- i18n/es.json ({len(merged)} entradas raíz)")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Genera la carpeta dist del ContentPack y combina JSONs en i18n/es.json")
    parser.add_argument("--package-name", default="[CP] StardewValleyEspañolLatinoRevisitado", help="Nombre de la carpeta del paquete dentro de dist")
    parser.add_argument("--repo-root", type=Path, default=repo_root, help="Raíz del repositorio (opcional)")
    parser.add_argument("--no-overwrite", dest="overwrite", action="store_false", help="No sobrescribir carpeta existente en dist")
    args = parser.parse_args()

    try:
        build_dist(args.repo_root, args.package_name, overwrite=args.overwrite)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
