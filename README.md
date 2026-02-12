# Generador de `dist` para Stardew Valley Español Latino Revisitado

Este script crea un paquete listo para distribuir en `dist/[CP] StardewValleyEspañolLatinoRevisitado`.

Resumen
- Combina recursivamente todos los archivos JSON en `src/data/` en un único objeto JSON y lo guarda en `i18n/es.json` dentro del paquete.
- Copia `manifest.json` y `content.json` a la raíz del paquete.

Comportamiento
- Merge: fusiona objetos JSON en un solo objeto; si hay conflicto de clave entre archivos, se imprime una advertencia y el valor del último archivo procesado sobrescribe al anterior.
- Ignora archivos JSON cuya raíz no sea un objeto (se avisa).
- Por defecto sobrescribe la carpeta de salida si ya existe.

Ubicación del script
- `src/scripts/generate_dist.py`

Requisitos
- Python 3.8+ (probado en Windows)

Uso
Desde la raíz del repositorio ejecutar:

PowerShell / CMD:

python src\scripts\generate_dist.py

Opciones útiles:
- `--package-name "[CP] StardewValleyEspañolLatinoRevisitado"` : cambiar el nombre de la carpeta dentro de `dist`.
- `--no-overwrite` : no sobrescribir la carpeta del paquete si ya existe.
- `--repo-root <ruta>` : usar una raíz de repo distinta (opcional).

Salida esperada
- `dist/[CP] StardewValleyEspañolLatinoRevisitado/manifest.json`
- `dist/[CP] StardewValleyEspañolLatinoRevisitado/content.json`
- `dist/[CP] StardewValleyEspañolLatinoRevisitado/i18n/es.json`

Notas
- El script imprimirá advertencias sobre conflictos de clave y archivos inválidos.
- Si quieres que haga commit automático o cambios adicionales, dímelo y lo agrego.
