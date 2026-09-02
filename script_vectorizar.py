import os
import zipfile
import vtracer

def procesar_vectorizacion(carpeta_origen, carpeta_destino, zip_salida):
    os.makedirs(carpeta_destino, exist_ok=True)
    archivos_svg = []

    if not os.path.exists(carpeta_origen):
        print(f"La carpeta {carpeta_origen} no existe.")
        return

    archivos = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not archivos:
        print(f"No hay imágenes en {carpeta_origen}.")
        return

    print(f"Iniciando vectorización de {len(archivos)} imágenes...")

    for nombre_archivo in archivos:
        ruta_img = os.path.join(carpeta_origen, nombre_archivo)
        nombre_base = os.path.splitext(nombre_archivo)[0]
        ruta_svg = os.path.join(carpeta_destino, f"{nombre_base}.svg")

        print(f"-> Vectorizando: {nombre_archivo}")

        vtracer.convert_image_to_svg_py(
            ruta_img,
            ruta_svg,
            colormode='color',
            hierarchical='stacked',
            filter_speckle=4,
            color_precision=6
        )
        archivos_svg.append(ruta_svg)

    with zipfile.ZipFile(zip_salida, 'w') as zipf:
        for svg in archivos_svg:
            zipf.write(svg, os.path.basename(svg))

    print(f"¡Completado! Archivo ZIP creado en: {zip_salida}")

if __name__ == "__main__":
    procesar_vectorizacion("input_normal", "output_normal", "output_normal/vectores_normales.zip")
