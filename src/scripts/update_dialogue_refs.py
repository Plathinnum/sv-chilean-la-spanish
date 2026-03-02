import json
import argparse
from pathlib import Path

def main():
	parser = argparse.ArgumentParser(description="Actualiza content.json y archivo de diálogos según rango de líneas.")
	parser.add_argument("--dialogue", required=True, help="Ruta al archivo de diálogos (ej: dialogues_alex.json)")
	parser.add_argument("--start", type=int, required=True, help="Línea de inicio (1-indexed)")
	parser.add_argument("--end", type=int, required=True, help="Línea de fin (inclusive, 1-indexed)")
	args = parser.parse_args()

	content_path = Path("content.json")
	dialogue_path = Path(args.dialogue)
	
	# Extraer nombre del personaje del archivo de diálogos (ej: dialogues_emily.json -> emily)
	character_name = dialogue_path.stem.replace('dialogues_', '')

	# Leer content.json como texto para procesar líneas y reemplazar in-place
	with open(content_path, 'r', encoding='utf-8') as f:
		content_lines = f.readlines()

	# Leer archivo de diálogos
	with open(dialogue_path, 'r', encoding='utf-8') as f:
		dialogue_data = json.load(f)


	for idx in range(args.start-1, args.end):
		line = content_lines[idx]
		parts = line.strip().split(':', 1)
		if len(parts) != 2:
			continue
		key = parts[0].strip().strip('"')
		value = parts[1].strip().strip('",')
		dialogue_key = f"characters.dialogue.{character_name}.{key.lower()}"
		content_value = f"{{{{i18n:{dialogue_key}}}}}"

		# Saltar si el value de content.json ya está en formato requerido
		if content_value in line:
			continue

		# Actualizar línea en content.json
		# Si es la última línea del rango, no agregar coma
		if idx == args.end - 1:
			new_line = f'    "{key}": "{content_value}"\n'
		else:
			new_line = f'    "{key}": "{content_value}",\n'
		content_lines[idx] = new_line

		# Eliminar la key antigua si existe (por ejemplo, AcceptGift_(O)Book_Defense)
		if key in dialogue_data:
			del dialogue_data[key]
		# Actualizar archivo de diálogos (reemplazar siempre el value)
		dialogue_data[dialogue_key] = value

	# Guardar cambios en content.json (sobrescribe solo el texto)
	with open(content_path, 'w', encoding='utf-8') as f:
		f.writelines(content_lines)

	# Guardar cambios en archivo de diálogos
	with open(dialogue_path, 'w', encoding='utf-8') as f:
		json.dump(dialogue_data, f, ensure_ascii=False, indent=4, sort_keys=True)

	print(f"Actualización completa. Modificadas líneas {args.start}-{args.end}.")

if __name__ == "__main__":
	main()