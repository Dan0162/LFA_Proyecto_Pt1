from Validar import validador
from gramatica import Parsed

def eliminar_espacios(linea):
    # Reemplazar espacios simples
    linea = linea.replace(' ', '')

    return linea



parseo = Parsed()

def main ():

    secciones = ["S","T","A","E"]

    seccion_SETS = False
    seccion_TOKENS = False
    seccion_ACTIONS = False
    seccion_ERROR = False
    validacion = ""
    i = 1

    llave_abierta = False  # Para verificar si la llave de apertura { ya fue encontrada
    f_reservadas = False  # Para verificar si RESERVADAS() ya fue encontrada
    f_activa = False #Verifica si se encuentra una funcion activa para

    filepath = 'prueba4-1.txt'

    with open(filepath, 'r') as archivo:
        # Lee el archivo línea por línea
        for numero_fila, linea in enumerate(archivo, start=1):

            linea = linea.replace('\n','')


            if not linea:
                i += 1
                continue

            if numero_fila ==  i:  # Si estamos en la primera línea

                linea = eliminar_espacios(linea)

                if linea == 'SETS':
                    seccion_SETS = True  # Activa seccion_SETS si la línea es 'SETS'
                    secciones[0] = True

                    continue

                elif linea == 'TOKENS':
                    seccion_TOKENS = True
                    secciones[1] = True
                    continue

                else:
                    if linea.startswith('S') | linea.startswith('s'):
                        columna_error = len(linea)
                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'SETS'")
                        break
                    else:
                        columna_error = len(linea)
                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'TOKENS'")
                        break


            if linea == linea.lstrip():

                if linea == 'TOKENS':
                    seccion_SETS = False
                    seccion_TOKENS = True
                    secciones[1] = True
                    continue

                elif linea.startswith('t') or linea.startswith('T'):
                    print(f"Error de formato en la linea {numero_fila}, se esperaba la palabra 'TOKENS'")
                    break


                elif linea == 'ACTIONS':
                    seccion_TOKENS = False
                    seccion_ACTIONS = True
                    secciones[2] = True
                    continue

                    if secciones[1] == False:
                        print(f"Error de formato en la linea {numero_fila}, se esperaba la palabra 'TOKENS'")
                        break

                elif linea.startswith('a') or linea.startswith('A'):
                    print(f"Error de formato en la linea {numero_fila}, se esperaba la palabra 'ACTIONS'")
                    break

                elif 'ERROR' in linea:
                    seccion_ACTIONS = False
                    seccion_ERROR = True
                    secciones[3] = True

                    if secciones[2] == False:
                        print(f"Error de formato en la linea {numero_fila}, se esperaba la palabra 'ACTIONS'")
                        break

                    elif f_reservadas == False:
                        print(f"Error de formato en la linea {numero_fila}, se esperaba la funcion 'RESERVADAS()' en ACTIONS")
                        break

                elif linea.startswith('e') or linea.startswith('E'):
                    print(f"Error de formato en la linea {numero_fila}, se esperaba la palabra 'ERROR'")
                    break

                else:
                    if seccion_ACTIONS == True:

                        if linea == 'RESERVADAS()':
                            f_reservadas = True
                            f_activa = True
                            continue

                        # Verifica apertura de llave
                        elif '{' in linea:
                            if llave_abierta:
                                print(f"Error en la línea {numero_fila}: ya hay una llave de apertura '{'{'}' sin cerrar")
                                break
                            llave_abierta = True
                            continue

                        # Verifica cierre de llave
                        elif '}' in linea:
                            if not llave_abierta:
                                print(f"Error en la línea {numero_fila}: se encontró una llave de cierre {'}'} sin una llave de apertura '{'{'}'")
                                break
                            llave_abierta = False  # Cerrar función actual
                            f_activa = False
                            continue

                        else:

                            if f_activa:
                                columna_error = 2
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba una llave de apertura '{'{'}'")

                            if '(' not in linea:
                                columna_error = len(linea) - 1
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un parentesis abierto '('")

                            partes = linea.split('(')

                            if len(partes) != 2:
                                columna_error = linea.rfind('(')
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo parentesis abierto '('")
                                break

                            identificador = partes[0].strip()
                            cierre = partes[1].strip()

                            if not identificador.isalpha() & identificador.isupper():
                                columna_error = len(identificador)
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un identificador con letras mayusculas '('")
                                break

                            if not cierre == ')':
                                columna_error = len(linea)
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un parentesis de cierre ')'")
                                break

                            f_activa = True

                    else:
                        print(f"Error de formato en la linea {numero_fila}, se esperaba un titulo de una seccion como 'TOKENS' o 'ACTIONS")


            linea = eliminar_espacios(linea)

            if seccion_SETS:

                validacion = parseo.validar_SET(linea, numero_fila)

                if validacion != "Formato valido":

                    print(validacion)
                    break;
                else:
                    continue

            if seccion_TOKENS:

                if not linea:
                  i += 1
                  continue

                validacion = parseo.validar_TOKENS(linea, numero_fila)

                if validacion != "Formato valido":

                    print(validacion)
                    break;
                else:
                    continue

            if seccion_ACTIONS:

                if not linea:
                    i += 1
                    continue

                validacion = parseo.validar_ACTIONS(linea, numero_fila)

                if validacion != "Formato valido":

                    print(validacion)
                    break;
                else:
                    continue

            if seccion_ERROR:
                if not linea:
                    i += 1
                    continue

                validacion = parseo.validar_ERROR(linea,numero_fila)

                if validacion != "Formato valido":

                    print(validacion)
                    break;
                else:
                    continue
        else:
            print ("Formato correcto")























if __name__ == "__main__":
    main()