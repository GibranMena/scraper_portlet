import json
import re
import os

def extract_patterns_and_append_to_json(text, json_file_path):
    # Define the regex pattern to extract details
    pattern = re.compile(r"""
        LICITACION\sPUBLICA\s(\d+/\d+)\n
        Estado:\n(\w+)\n
        Código\sSIGAF:\n(\#)\n
        Publicación:\n(\d{2}/\d{2}/\d{4})\n
        Cierre:\n(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s(?:AM|PM))\n
        Última\sActualización:\n(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s(?:AM|PM))\n
        Alcaldía\sManagua\s\(
        Alcaldía\sManagua
        \)\s-\sUnidad\sde\sAdquisición\sMANAGUA\n
        ([^\n]+)\n
        (.+?)\nMás\sDatos
    """, re.VERBOSE | re.DOTALL)

    matches = pattern.findall(text)
    
    # Structure the extracted data
    extracted_data = []
    for match in matches:
        extracted_data.append({
            "licitacion": match[0],
            "estado": match[1],
            "codigo_sigaf": match[2],
            "publicacion": match[3],
            "cierre": match[4],
            "ultima_actualizacion": match[5],
            "unidad_adquisicion": "Alcaldía Managua - Unidad de Adquisición MANAGUA",
            "servicios": match[6],
            "programa": match[7]
        })

    # Check if the JSON file exists, and load or initialize data
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append the new data to the existing JSON data
    existing_data.extend(extracted_data)

    # Save the updated JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

# Sample text input
text = ('Procedimiento Detalles Acciones\nLICITACION PUBLICA\n241/2022\nEstado:\nEjecución\nCódigo SIGAF:\n#\n'
        'Publicación:\n21/07/2022\nCierre:\n22/08/2022 10:00:00 AM\nÚltima Actualización:\n03/10/2022 10:58:35 AM\n'
        'Alcaldía Managua (Alcaldía Managua) - Unidad de Adquisición MANAGUA\n'
        'Servicios de construcción de edificaciones residenciales (72110000)\n'
        'PROGRAMA BISMARCK MARTINEZ VIVIENDA SOCIAL (COMPONENTE: OBRAS COMPLEMENTARIAS PLANTA DE TRATAMIENTO '
        'URBANIZACIÓN FLOR DE PINO)\nMás Datos\nLICITACION PUBLICA\n215/2022\nEstado:\nEjecución\nCódigo SIGAF:\n#\n'
        'Publicación:\n13/06/2022\nCierre:\n13/07/2022 10:00:00 AM\nÚltima Actualización:\n21/11/2022 08:42:52 AM\n'
        'Alcaldía Managua (Alcaldía Managua) - Unidad de Adquisición MANAGUA\nEstructuras y edificios permanentes '
        '(95120000)\nPROGRAMA BISMARCK MARTINEZ, VIVIENDA SOCIAL (COMPONENTE: CONSTRUCCION DE 1,728 VIVIENDAS)\n'
        'Más Datos\nLICITACION PUBLICA\n193/2022\nEstado:\nEjecución\nCódigo SIGAF:\n#\nPublicación:\n19/05/2022\n'
        'Cierre:\n20/06/2022 11:00:00 AM\nÚltima Actualización:\n17/08/2022 08:54:39 AM\nAlcaldía Managua (Alcaldía '
        'Managua) - Unidad de Adquisición MANAGUA\nServicios de construcción de edificaciones residenciales '
        '(72110000)\nPROGRAMA BISMARCK MARTINEZ VIVIENDA SOCIAL, COMPONENTE: CONSTRUCCIÓN DE TERRAZAS Y SISTEMA '
        'HIDROSANITARIO DE 46 LOTES ADICIONALES EN URBANIZACIÓN FLOR DE PINO\nMás Datos')

# Path to the JSON file
json_file_path = 'scraped_dat.json'

# Execute the function
extract_patterns_and_append_to_json(text, json_file_path)
