import re

class validador:
 # Definir un diccionario con los patrones de expresiones regulares para cada sección.
    def dividir_secciones(self, contenido):
        secciones = {}
        patrones = {
            'SETS': r'SETS\s+(.*?)(?=\bTOKENS\b|\bACTIONS\b|\bERROR\b|$)',
            'TOKENS': r'TOKENS\s+(.*?)(?=\bACTIONS\b|\bERROR\b|$)',
            'ACTIONS': r'ACTIONS\s+(.*?)(?=\bERROR\b|$)',
            'ERROR': r'ERROR\s*=\s*(\d+)\s*'
        }
# Iterar sobre cada sección y su patrón asociado.
        for seccion, patron in patrones.items():
 # Buscar el patrón en el contenido 
            match = re.search(patron, contenido, re.DOTALL)
# Si coincide, se extrae el texto y se limpia de espacios en blanco.
            if match:
                secciones[seccion] = match.group(1).strip()

        return secciones

    @staticmethod
    def validar_sets(contenido_sets):
        # Expresión regular para validar cada SET
        patron_set = re.compile(r'^TOKEN\s+\d+\s*=\s*([\'".\w\s\(\)\|\+\*\?]+)$', re.MULTILINE)
        sets = contenido_sets.splitlines()
        if not any(line.strip() for line in sets):
            print("No se encontraron SETS.")
            return

        for linea in sets:
            if linea.strip():
                match = patron_set.match(linea.strip())
                if match:
                    identificador, definicion = match.groups()
                    print(f"SET encontrado: {identificador} = {definicion}")
                else:
                    print(f"Error en el formato del SET: {linea.strip()}")

        # Asegurarse de que hay al menos un SET
        if not any(patron_set.match(linea.strip()) for linea in sets):
            print("Debe haber al menos un SET en la sección SETS.")

    @staticmethod
    def validar_tokens(contenido_tokens):
        # Expresión regular para validar cada TOKEN
        patron_token = re.compile(r'^TOKEN\s+\d+\s*=\s*([\'".\w\s\(\)\|\+\*\?]+)$', re.MULTILINE)
        tokens = contenido_tokens.splitlines()
        if not any(linea.strip() for linea in tokens):
            print("No se encontraron TOKENS.")
            return

        for linea in tokens:
            if linea.strip():
                match = patron_token.match(linea.strip())
                if match:
                    token = match.group(0)
                    print(f"TOKEN encontrado: {token}")
                else:
                    print(f"Error en el formato del TOKEN: {linea.strip()}")

        # Asegurarse de que hay al menos un TOKEN
        if not any(patron_token.match(linea.strip()) for linea in tokens):
            print("Debe haber al menos un TOKEN en la sección TOKENS.")

        @staticmethod
        def validar_actions(contenido_actions):
            # Expresión regular para validar funciones en ACTIONS
            patron_funcion = re.compile(r'^\w+\s*\(\)\s*\{((?:\d+\s*=\s*\'[^\']+\')*)\}$', re.DOTALL | re.MULTILINE)
            funciones = contenido_actions.splitlines()
            if not any(linea.strip() for linea in funciones):
                print("No se encontraron ACTIONS.")
                return

            for linea in funciones:
                if linea.strip():
                    match = patron_funcion.match(linea.strip())
                    if match:
                        funciones = match.group(1)
                        print(f"FUNCIONES encontradas: {funciones}")
                    else:
                        print(f"Error en el formato de ACTIONS: {linea.strip()}")

            # Asegurarse de que la función RESERVADAS() está presente
            if not re.search(r'RESERVADAS\s*\(\)\s*\{', contenido_actions):
                print("Debe existir la función RESERVADAS() en la sección ACTIONS.")


        @staticmethod
        def validar_error(contenido_error):
            # Expresión regular para validar ERROR
            patron_error = re.compile(r'^ERROR\s*=\s*(\d+)$', re.MULTILINE)
            errores = contenido_error.splitlines()
            if not any(linea.strip() for linea in errores):
            #Si no encuentra ERROR lanza mensaje
                print("No se encontraron errores.")
                return

            for linea in errores:
                if linea.strip():
                    match = patron_error.match(linea.strip())
                    if match:
                        error = match.group(1)
            #Si encuentra algun ERROR imprime mensaje
                        print(f"ERROR encontrado: {error}")
                    else:
            #Si el formato está mal
                        print(f"Error en el formato de ERROR: {linea.strip()}")

            # Asegurarse de que hay al menos un ERROR
            if not any(patron_error.match(linea.strip()) for linea in errores):
                print("Debe haber al menos un ERROR en la sección ERROR.")

