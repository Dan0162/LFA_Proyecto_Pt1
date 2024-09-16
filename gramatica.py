
class Parsed:

    def validar_SET(self, linea, numero_fila):
        # Paso 1: Verificar el formato general (identificador seguido de '=')
        linea = linea.strip()  # Eliminar espacios en blanco al final de la línea

        if '=' not in linea:
            columna_error = linea.find('=') if '=' in linea else len(linea)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

        # Dividir la cadena en la parte antes y después del '='
        partes = linea.split('=')
        if len(partes) != 2:
            return f"Error de formato en la fila {numero_fila}: se esperaba un solo signo '=' "

        identificador = partes[0].strip()  # Quitar espacios en blanco alrededor del identificador
        contenido = partes[1].strip()      # Quitar espacios en blanco alrededor del contenido

        # Verificación del identificador
        if not all(c.isalnum() or c == '_' for c in identificador):
            columna_error = linea.find(identificador)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba que el identificador solo contuviera letras"

        # Paso 2: Validar el identificador
        if not identificador.isupper():
            columna_error = linea.find(identificador)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba que el identificador solo contuviera letras mayúsculas"

        # Paso 3: Validar el contenido
        contenido = contenido.strip()

        if not contenido:
            columna_error = linea.find('=')
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error + 1}: se esperaba una definición después de '='"

        if len(contenido) < 3:
            columna_error = linea.find(contenido)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una definición completa"

        if contenido[len(contenido) - 1] == '+':
            columna_error = len(linea) - 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba otro símbolo terminal para concatenar"

        # Paso 4: Procesar el contenido

        # Dividir por el operador de concatenación '+' si existe
        partes = contenido.split('+')

        for parte in partes:
            parte = parte.strip()

            # Validar si es un rango ('A'..'Z') o ('CHR(x)..CHR(y)')
            if '..' in parte:
                limites = parte.split('..')

                inicio, fin = limites[0].strip(), limites[1].strip()

                if inicio == '' or fin == '':
                    columna_error = linea.find(parte)
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un intervalo cerrado como 'A'..'Z'"

                # Validar que los rangos sean correctos
                elif inicio.startswith("'") and inicio.endswith("'") and fin.startswith("'") and fin.endswith("'"):
                    if len(inicio) != 3 or len(fin) != 3:
                        columna_error = linea.find(inicio if len(inicio) != 3 else fin)
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un carácter dentro de las comillas"


                # Verificar si es una llamada a CHR()
                elif inicio.startswith("CHR(") and inicio.endswith(")"):

                    # Validar que ambos contengan paréntesis de apertura y cierre correctamente
                    if fin.startswith("CHR(") and not fin.endswith(")"):
                        columna_error = len(linea)
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: falta un paréntesis de cierre en CHR()"

                    elif not fin.startswith("CHR("):
                        columna_error = linea.find(fin if not fin.startsswith("CHR(") else fin)
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba la funcion CHR()"

                    else:

                        try:
                            # Intentar convertir el contenido entre los paréntesis a números
                            int(inicio[4:-1])  # Validar que haya un número dentro de CHR()
                            int(fin[4:-1])
                        except ValueError:
                            columna_error = linea.find(inicio if not inicio[4:-1].isdigit() else fin)
                            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un número dentro de los parámetros de la función CHR()"

                # En caso de que no tenga el paréntesis de cierre
                elif inicio.startswith("CHR(") and not inicio.endswith(")"):
                    columna_error = linea.find(inicio)
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: falta un paréntesis de cierre en CHR()"

                else:
                    columna_error = linea.find(parte)
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un intervalo válido"

            # Si es un carácter suelto ('_'), debe estar entre comillas
            elif parte.startswith("'") and parte.endswith("'"):
                if len(parte) < 3:
                    columna_error = linea.find(parte)
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un carácter dentro de las comillas"
                if len(parte) > 3:
                    columna_error = linea.find(parte)
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo carácter encerrado entre comillas"

            # Procesar casos adicionales
            elif not parte.startswith("'") and parte.endswith("'") or parte.startswith("'") and not parte.endswith("'"):
                columna_error = linea.find(parte)
                return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de apertura/cierre"

            else:
                columna_error = linea.find(parte)
                return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un intervalo válido separado por '..'"


        return "Formato valido"



    def validar_ERROR(self, linea, numero_fila):
        # Paso 1: Verificar el formato general (identificador seguido de '=')
        linea = linea.strip()  # Eliminar espacios en blanco al principio y al final de la línea

        if '=' not in linea:
            columna_error = len(linea)  # Si no hay '=', asumimos que el error está al final de la línea
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

        # Dividir la cadena en la parte antes y después del '='
        partes = linea.split('=')
        if len(partes) != 2:
            columna_error = linea.find('=') if '=' in linea else len(linea)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo signo '='"

        identificador = partes[0].strip()  # Quitar espacios en blanco alrededor del identificador
        contenido = partes[1].strip()      # Quitar espacios en blanco alrededor del contenido

        # Validar el identificador
        if not identificador.isalpha() or not identificador.endswith('ERROR'):
            columna_error = linea.find(identificador)  # Localizar dónde está el identificador
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: El identificador debe contener solo letras y terminar con 'ERROR'"

        # Validar la parte después del '='
        if not contenido.isdigit():
            columna_error = linea.find(contenido)  # Localizar dónde está el contenido después del '='
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: La parte después del '=' debe contener solo números"

        return "Formato valido"



    def validar_TOKENS(self, linea, numero_fila):
        # Paso 1: Verificar el formato general (identificador seguido de '=')

        # Se recorre la línea para encontrar el primer '=' que no esté entre comillas simples
        dentro_comillas = False
        posicion_igual = -1  # Guardará la posición del primer '=' encontrado fuera de comillas

        for idx, char in enumerate(linea):
            if char == "'":  # Cambiamos el estado si encontramos una comilla simple
                dentro_comillas = not dentro_comillas
            elif char == '=' and not dentro_comillas:
                posicion_igual = idx
                break  # Nos detenemos al encontrar el primer '=' fuera de comillas

        if posicion_igual == -1:
            columna_error = len(linea)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

        # Dividir la cadena en la parte antes y después del '='
        identificador = linea[:posicion_igual].strip()
        contenido = linea[posicion_igual + 1:].strip()


        # Paso 2: Validar el identificador del Token (debe empezar con "TOKEN")
        if not identificador.startswith("TOKEN"):
            columna_error = linea.find(identificador)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba que el identificador iniciara con la palabra 'TOKEN'"

        # Validar que el número del token siga a "TOKEN"
        token_num = identificador[5:].strip()  # Tomar la parte después de "TOKEN"
        if not token_num.isdigit():
            columna_error = linea.find(token_num)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un número después de 'TOKEN'"

        k = len(identificador) + 4


       # Paso 3: Validar el contenido
        i = 0
        stack = []  # Pila para validar paréntesis y llaves

        while i < len(contenido):
            # Verificar si el carácter actual es una comilla simple
            if contenido[i] == "'":
                # Asegurarse de que haya un carácter encerrado entre comillas simples
                if i + 2 >= len(contenido):
                    columna_error = len(contenido) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba un carácter entre comillas"

                elif contenido[i + 2] != "'":
                    columna_error = k + i + 2
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba una comilla de cierre"

                # Verificar que haya exactamente un carácter entre las comillas simples
                if len(contenido[i + 1]) != 1:
                    columna_error = k + i + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Solo se permite un carácter entre comillas simples"

                # Mover el índice al siguiente posible token
                i += 3  # Saltar el grupo "'X'"
            else:
                # Validar caracteres no terminales (como LETRA, DIGITO, etc.)
                j = i
                while j < len(contenido) and contenido[j].isalpha():
                    j += 1
                token = contenido[i:j]

                if token.isupper() or contenido[j] in {'+', '*', '?', '|', '(', ')', '{', '}'}:
                    i = j  # Mover el índice más allá del identificador
                else:
                    columna_error = k + i + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba un simbolo no terminal o un simbolo de expresion regular"

            # Validar los operadores de expresiones regulares o concatenación
            if i < len(contenido) and contenido[i] in {'+', '*', '?', '|', '(', ')', '{', '}'}:
                if contenido[i] in {'(', '{'}:
                    stack.append(contenido[i])  # Agregar paréntesis o llave de apertura a la pila
                elif contenido[i] == ')':
                    if not stack or stack[-1] != '(':
                        columna_error = k + i + 1
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Paréntesis de cierre inesperado"
                    stack.pop()  # Quitar el paréntesis de apertura correspondiente
                elif contenido[i] == '}':
                    if not stack or stack[-1] != '{':
                        columna_error = k + i + 1
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Llave de cierre inesperada"
                    stack.pop()  # Quitar la llave de apertura correspondiente

                i += 1  # Saltar el operador de expresión regular


        # Verificar que no hayan quedado paréntesis o llaves sin cerrar
        if stack:
            columna_error = len(linea)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Falta cerrar {'paréntesis' if stack[-1] == '(' else 'llave'}"

        return "Formato valido"

    def validar_ACTIONS(self, linea, numero_fila):
        # Paso 1: Verificar el formato general (identificador seguido de '=')

        linea = linea.strip()  # Eliminar espacios en blanco al principio y al final de la línea

        if '=' not in linea:
            columna_error = len(linea)  # Si no hay '=', se asume que el error está al final de la línea
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

         # Dividir la cadena en la parte antes y después del '='
        partes = linea.split('=')

        if len(partes) != 2:
            columna_error = linea.rfind('=') if '=' in linea else len(linea)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo signo '='"

        identificador = partes[0].strip()  # Quitar espacios en blanco alrededor del identificador
        contenido = partes[1].strip()      # Quitar espacios en blanco alrededor del contenido

        #Paso 2: Verificar que el identificador sea un numero
        if not identificador.isdigit():
            columna_error = len(identificador)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un numero"

        #Paso 3: Verificar que la definicion este en un formato correcto

        if contenido.startswith("'") and not contenido.endswith("'"):
            columna_error = len(linea)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de cierre"

        elif not contenido.startswith("'") and contenido.endswith("'"):
            columna_error = linea.find('=')
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de apertura"

        if contenido.startswith("'") and contenido.endswith("'"):
            # Extraer el contenido entre las comillas
            contenido_interno = contenido[1:-1]  # Remover las comillas simples

            # Verificar que el contenido interno sean solo letras mayúsculas
            if not contenido_interno.isalpha() or not contenido_interno.isupper():
                columna_error = linea.find(contenido_interno) + 1
                return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba solo letras mayúsculas"

        return "Formato valido"










