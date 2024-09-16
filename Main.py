from Validar import validador

def leer_archivos(filepath):
    try:
        with open(filepath, 'r') as archivo:
            contenido = archivo.read().strip()

        # Crear una instancia de la clase validador
        val = validador()
        secciones = val.dividir_secciones(contenido)

        if 'SETS' in secciones:
            print("Sección SETS encontrada:")
            val.validar_sets(secciones['SETS'])
        else:
            print("No se encontró la sección SETS.")

        if 'TOKENS' in secciones:
            print("\nSección TOKENS encontrada:")
            val.validar_tokens(secciones['TOKENS'])
        else:
            raise ValueError("No se encontró la sección TOKENS.")
        
        if 'ACTIONS' in secciones:
            print("\nSección ACTIONS encontrada:")
            val.validar_actions(secciones['ACTIONS'])
        else:
            raise ValueError("No se encontró la sección ACTIONS.")
        
        if 'ERROR' in secciones:
            print("\nSección ERROR encontrada:")
            val.validar_error(secciones['ERROR'])
        else:
            raise ValueError("No se encontró la sección ERROR.")
    
    except FileNotFoundError:
        print(f"El archivo no fue encontrado.")
    except Exception as e:
        print(f"Error procesando el archivo: {e}")

def main():
    ruta_archivo = input("Por favor, ingrese la ruta del archivo: ")
    leer_archivos(ruta_archivo)

if __name__ == "__main__":
    main()
