#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from pathlib import Path

def camel_to_snake(name):
    """Convierte CamelCase a snake_case"""
    # Inserta guiones bajos antes de mayúsculas
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def process_key(key):
    """
    Procesa una key del Objects.es-ES.json
    QiBean_Name -> objects.qi_bean.name 
    QiBean_Description -> objects.qi_bean.desc
    """
    if key.endswith('_Name'):
        base = key[:-5]  # Quita "_Name"
        snake_base = camel_to_snake(base)
        return f"objects.{snake_base}.name"
    elif key.endswith('_Description'):
        base = key[:-12]  # Quita "_Description"
        snake_base = camel_to_snake(base)
        return f"objects.{snake_base}.desc"
    elif key.endswith('_Flavored_Name'):
        base = key[:-14]  # Quita "_Flavored_Name"
        snake_base = camel_to_snake(base)
        return f"objects.{snake_base}.flavored_name"
    elif key.endswith('_CollectionsTabName'):
        base = key[:-19]  # Quita "_CollectionsTabName"
        snake_base = camel_to_snake(base)
        return f"objects.{snake_base}.collection_name"
    elif key.endswith('_CollectionsTabDescription'):
        base = key[:-26]  # Quita "_CollectionsTabDescription"
        snake_base = camel_to_snake(base)
        return f"objects.{snake_base}.collection_desc"
    elif key.endswith('_Flavored_Name'):
        base = key[:-14]
        snake_base = camel_to_snake(base)
        return f"objects.{snake_base}.flavored_name"
    else:
        # Para keys sin sufijo (ej: "CactusSeedsOutside")
        snake_base = camel_to_snake(key)
        return f"objects.{snake_base}"

def main():
    # Rutas de los archivos
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    objects_file = Path("d:/Documents/xnbcli-windows-x64/output/Objects.es-ES.json")
    content_file = root_dir / "content.json"
    i18n_file = root_dir / "i18n" / "es.json"
    
    print(f"Leyendo {objects_file}...")
    with open(objects_file, 'r', encoding='utf-8') as f:
        objects_data = json.load(f)
    
    print(f"Leyendo {content_file}...")
    with open(content_file, 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    print(f"Leyendo {i18n_file}...")
    with open(i18n_file, 'r', encoding='utf-8') as f:
        i18n_data = json.load(f)
    
    # Procesar las keys del content de Objects.es-ES.json
    objects_content = objects_data.get("content", {})
    
    # Contador de cambios
    content_changes = 0
    i18n_changes = 0
    i18n_preserved = 0
    
    # Actualizar content.json
    entries = content_data["Changes"][0]["Entries"]
    
    for key, value in objects_content.items():
        i18n_key = process_key(key)
        i18n_ref = f"{{{{i18n:{i18n_key}}}}}"
        
        # Actualizar content.json si la key no existe o es diferente
        if key not in entries or entries[key] != i18n_ref:
            entries[key] = i18n_ref
            content_changes += 1
            print(f"  content.json: {key} -> {i18n_ref}")
        
        # Actualizar i18n/es.json
        if i18n_key not in i18n_data:
            i18n_data[i18n_key] = value
            i18n_changes += 1
            print(f"  i18n/es.json: {i18n_key} = {value}")
        else:
            i18n_preserved += 1
            print(f"  i18n/es.json: {i18n_key} (preservado)")
    
    # Guardar archivos
    print(f"\nGuardando {content_file}...")
    with open(content_file, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=4)
    
    print(f"Guardando {i18n_file}...")
    with open(i18n_file, 'w', encoding='utf-8') as f:
        json.dump(i18n_data, f, ensure_ascii=False, indent=4, sort_keys=True)
    
    print(f"\n=== Resumen ===")
    print(f"Content.json actualizado: {content_changes} entries")
    print(f"i18n/es.json nuevas entries: {i18n_changes}")
    print(f"i18n/es.json preservadas: {i18n_preserved}")
    print(f"Total procesadas: {len(objects_content)} keys")

if __name__ == "__main__":
    main()
