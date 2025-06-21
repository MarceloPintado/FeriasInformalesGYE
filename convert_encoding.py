# Script para convertir el archivo JSON de UTF-16 a UTF-8
import json
import os

def convert_json_utf16_to_utf8(input_file, output_file=None):
    """
    Convierte un archivo JSON de UTF-16 a UTF-8
    """
    if output_file is None:
        # Crear nombre del archivo de salida
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_utf8{ext}"
    
    try:
        # Leer el archivo con codificación UTF-16
        print(f"Leyendo archivo: {input_file}")
        with open(input_file, 'r', encoding='utf-16') as f:
            content = f.read()
        
        # Verificar que sea JSON válido
        try:
            json_data = json.loads(content)
            print(f"JSON válido con {len(json_data)} elementos")
        except json.JSONDecodeError as e:
            print(f"Error: El contenido no es JSON válido: {e}")
            return False
        
        # Escribir el archivo con codificación UTF-8
        print(f"Escribiendo archivo: {output_file}")
        with open(output_file, 'w', encoding='utf-8', ensure_ascii=False) as f:
            f.write(content)
        
        print(f"Conversión exitosa!")
        print(f"Archivo original: {input_file}")
        print(f"Archivo convertido: {output_file}")
        
        # Verificar el tamaño de los archivos
        original_size = os.path.getsize(input_file)
        converted_size = os.path.getsize(output_file)
        print(f"Tamaño original: {original_size:,} bytes")
        print(f"Tamaño convertido: {converted_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error durante la conversión: {e}")
        return False

if __name__ == "__main__":
    # Convertir el archivo
    input_file = "backup_ferias_completo.json"
    success = convert_json_utf16_to_utf8(input_file)
    
    if success:
        print("\n ¡Conversión completada!")
        print("Ahora puedes usar:")
        print("python manage.py loaddata backup_ferias_completo_utf8.json")
    else:
        print("\n La conversión falló. Revisa los errores arriba.")