#!/usr/bin/python3

# Realizar las validaciones solicitadas sobre al archivo de ventas
def validar(nomArchivoVentas):
    import csv
    class RegistroExcede(Exception):
        pass

    class MiError(Exception):
        pass
    totalCampos = 5 
    try:
        with open(nomArchivoVentas, 'r', encoding='latin-1') as documento:
            archivoVentas=csv.reader(documento)
            posRegistro = 1
            for linea in archivoVentas:
                if posRegistro == 1:
                    x=0
                    posPrecio=0
                    posCantidad=0
                    for x in range(totalCampos):
                        nomCampo = linea[x].strip(' ')
                        nomCampo = nomCampo.upper()
                        if nomCampo == 'PRECIO':
                            posPrecio = x
                        elif nomCampo =='CANTIDAD':
                            posCantidad = x
                        elif nomCampo =='CODIGO':
                            posCodigo = x
                        else:
                            pass

                if len (linea) != totalCampos:
                    raise RegistroExcede()
                else:
                    i=0
                    for i in range(totalCampos):
                        if posRegistro > 1:
                            if i == posCodigo:
                                valCodigo = linea[i].strip(' ')
                                if valCodigo == '':
                                    tipoErrorCodigo = 'vacio'
                                    raise ValueError()
                                else:
                                    if len(valCodigo) > 6:
                                        tipoErrorCodigo = 'tamano'
                                        raise ValueError()
                                    elif valCodigo[0:3].isalpha() == False:
                                        tipoErrorCodigo = 'texto'
                                        raise ValueError()
                                    elif valCodigo[3:].isdigit() == False:
                                        tipoErrorCodigo = 'numero'
                                        raise ValueError()
                            elif i == posCantidad:
                                valCantidad=int(linea[i].strip(' '))
                            elif i == posPrecio:
                                valPrecio = linea[i].strip(' ')
                                if valPrecio.isdigit() == True:
                                    raise ValueError()
                                else:
                                    f=float(valPrecio)                            
                            else:
                                pass
           
                posRegistro = posRegistro + 1
            print('Archivo de ventas correcto!!')                 
    except FileNotFoundError:
        print('No existe archivo de ventas')
    except PermissionError:
        print('No tiene permisos para abrir el archivo de ventas')
    except RegistroExcede:
        mensaje='El registro {} contiene una cantidad inválida de campos {}'.format(posRegistro, linea)
        print(mensaje)
        with open('Error.log','w') as error_file:
            error_file.write(mensaje)
    except ValueError:
        if i == posCantidad:
            print('El registro {} tiene un valor incorrecto en CANTIDAD: {}'.format(posRegistro-1,linea[i].strip(' ')))
        elif i == posPrecio:
            print('El registro {} tiene un valor incorrecto en PRECIO: {}'.format(posRegistro-1, linea[i].strip(' ')))
        else:
            if tipoErrorCodigo == 'vacio':
                print('El registro {} tiene el campo CODIGO vacío'.format(posRegistro-1))
            else:
                print('El registro {} tiene un valor incorrecto en CODIGO: {}. Debe contener 3 caracteres alfabeticos seguido de 3 números'.format(posRegistro-1, valCodigo))