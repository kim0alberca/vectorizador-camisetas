import os
import zipfile
from rembg import remove
import vtracer

CARPERTA_ENTRADA = "input_camisetas"
CARPETA_INTERMEDIA = "temp_artes_planos"
CARPETA_SALIDA = "output_camisetas"
ZIP_FINAL = "output_camisetas/artes_camisetas_vectorizados.zip"

os.makedirs(CARPETA_INTERMEDIA, exist_ok=True)
os.makedirs(CARPETA_SALIDA, exist_ok=True)

archivos = [f for f in os.listdir(CARPERTA_ENTRADA) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

if not archivos:
    print("No se encontraron imágenes en input_camisetas.")
else:
    print(f"Procesando {len(archivos)} fotos de camisetas...")
    archivos_svg = []

    for nombre in archivos:
        ruta_entrada = os.path.join(CARPERTA_ENTRADA, nombre)
        nombre_base = os.path.splitext(nombre)[0]
        ruta_plano_png = os.path.join(CARPETA_INTERMEDIA, f"{nombre_base}_plano.png")
        ruta_final_svg = os.path.join(CARPETA_SALIDA, f"{nombre_base}_arte.svg")

        print(f"-> Extrayendo arte de prenda: {nombre}")

        # 1. Remover silueta de camiseta, fondo y pliegues exteriores
        with open(ruta_entrada, 'rb') as input_file:
            input_bytes = input_file.read()
            output_bytes = remove(input_bytes)
            
        with open(ruta_plano_png, 'wb') as output_file:
            output_file.write(output_bytes)

        print(f"-> Vectorizando arte extraído a SVG: {nombre_base}")

        # 2. Vectorizar el arte plano resultante
        vtracer.convert_image_to_svg_py(
            ruta_plano_png,
            ruta_final_svg,
            colormode='color',
            hierarchical='stacked',
            filter_speckle=4,
            color_precision=6
        )
        archivos_svg.append(ruta_final_svg)

    # 3. Comprimir todos los artes SVG en un paquete ZIP
    with zipfile.ZipFile(ZIP_FINAL, 'w') as zipf:
        for svg in archivos_svg:
            zipf.write(svg, os.path.basename(svg))

    print(f"¡Proceso completado! Archivo guardado en: {ZIP_FINAL}")
