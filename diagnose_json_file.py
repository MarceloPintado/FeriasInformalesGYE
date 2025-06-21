# Script para diagnosticar el archivo JSON
import os
import json

def diagnose_json_file(filename):
    """
    Diagnostica problemas en el archivo JSON
    """
    print(f"DIAGNOSTICANDO ARCHIVO: {filename}")
    print("=" * 50)
    
    # 1. Verificar que el archivo existe
    if not os.path.exists(filename):
        print(f"ERROR: El archivo {filename} no existe")
        return
    
    # 2. Verificar tamaño del archivo
    file_size = os.path.getsize(filename)
    print(f"TAMAÑO DEL ARCHIVO: {file_size:,} bytes")
    
    if file_size == 0:
        print("ERROR: El archivo está vacío")
        return
    
    # 3. Leer los primeros bytes en crudo
    print("\nPRIMEROS 20 BYTES EN HEXADECIMAL:")
    with open(filename, 'rb') as f:
        first_bytes = f.read(20)
        hex_bytes = ' '.join(f'{b:02x}' for b in first_bytes)
        print(f"   {hex_bytes}")
    
    # 4. Intentar diferentes codificaciones
    encodings_to_try = ['utf-16', 'utf-16-le', 'utf-16-be', 'utf-8', 'latin1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            print(f"\nPROBANDO CODIFICACION: {encoding}")
            with open(filename, 'r', encoding=encoding) as f:
                # Leer solo los primeros 200 caracteres para inspección
                content_preview = f.read(200)
                print(f"   Primeros 200 caracteres:")
                print(f"   '{content_preview}'")
                
                # Volver al inicio y leer todo
                f.seek(0)
                full_content = f.read()
                
                # Intentar parsear como JSON
                try:
                    json_data = json.loads(full_content)
                    print(f"   EXITO: JSON válido con {len(json_data)} elementos")
                    
                    # Guardar con UTF-8
                    output_file = f"{os.path.splitext(filename)[0]}_fixed.json"
                    with open(output_file, 'w', encoding='utf-8', ensure_ascii=False) as out_f:
                        json.dump(json_data, out_f, indent=2, ensure_ascii=False)
                    
                    print(f"   EXITO: Archivo corregido guardado como: {output_file}")
                    return output_file
                    
                except json.JSONDecodeError as json_err:
                    print(f"   ERROR: No es JSON válido: {str(json_err)[:100]}...")
                    
                    # Si el contenido parece JSON pero tiene errores, mostrar más detalles
                    if full_content.strip().startswith(('[', '{')):
                        print(f"   NOTA: El archivo parece JSON pero tiene errores de sintaxis")
                        print(f"   NOTA: Longitud del contenido: {len(full_content)} caracteres")
                
        except UnicodeDecodeError as e:
            print(f"   ERROR: Error de codificación: {e}")
        except Exception as e:
            print(f"   ERROR: Error inesperado: {e}")
    
    print(f"\nERROR: No se pudo leer el archivo con ninguna codificación estándar")
    
    # 5. Verificar si el archivo podría estar comprimido o corrupto
    print("\nVERIFICACIONES ADICIONALES:")
    with open(filename, 'rb') as f:
        first_4_bytes = f.read(4)
        
    # Verificar firmas de archivos comunes
    if first_4_bytes[:2] == b'\x1f\x8b':
        print("   NOTA: El archivo parece estar comprimido con GZIP")
    elif first_4_bytes[:2] == b'PK':
        print("   NOTA: El archivo parece ser un ZIP")
    elif first_4_bytes == b'\x00\x00\x00\x00':
        print("   NOTA: El archivo contiene muchos bytes nulos - posible corrupción")
    else:
        print(f"   INFO: Primeros 4 bytes: {first_4_bytes}")

def try_fix_json_manually(filename):
    """
    Intenta reparar manualmente problemas comunes de JSON
    """
    print(f"\nINTENTANDO REPARACION MANUAL DE: {filename}")
    
    try:
        # Probar UTF-16 primero (basado en los bytes que vimos)
        with open(filename, 'r', encoding='utf-16') as f:
            content = f.read()
        
        print(f"   CONTENIDO LEIDO (primeros 500 chars):")
        print(f"   '{content[:500]}'")
        
        # Limpiar el contenido
        content = content.strip()
        
        # Verificar si hay caracteres de control o BOM
        if content.startswith('\ufeff'):
            content = content[1:]  # Remover BOM
            print("   INFO: BOM removido")
        
        # Intentar parsear
        try:
            json_data = json.loads(content)
            output_file = f"{os.path.splitext(filename)[0]}_manual_fix.json"
            with open(output_file, 'w', encoding='utf-8', ensure_ascii=False) as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"   EXITO: Archivo reparado guardado como: {output_file}")
            return output_file
        except json.JSONDecodeError as e:
            print(f"   ERROR: Error JSON después de limpieza: {e}")
            print(f"   NOTA: Error en línea {e.lineno}, columna {e.colno}")
            
    except Exception as e:
        print(f"   ERROR: Error durante reparación manual: {e}")
    
    return None

if __name__ == "__main__":
    filename = "backup_ferias_completo.json"
    
    # Primero diagnosticar
    fixed_file = diagnose_json_file(filename)
    
    # Si no se pudo arreglar automáticamente, intentar reparación manual
    if not fixed_file:
        fixed_file = try_fix_json_manually(filename)
    
    if fixed_file:
        print(f"\nEXITO: ¡Archivo corregido exitosamente!")
        print(f"Usa: python manage.py loaddata {fixed_file}")
    else:
        print(f"\nERROR: No se pudo corregir el archivo automáticamente.")
        print(f"NOTA: El archivo podría estar muy corrupto o no ser un JSON válido.")