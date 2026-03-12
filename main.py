

print("Proyecto Phoenix activo")

import funciones
mis_empresas = []
empresa_status_loggin = None
while True:
    print("Seleccione la opcion que desee-->")
    print("1-Crear empresa")
    print("2-Buscar ID empresarial")
    print("3-Salir del sistema")
    if empresa_status_loggin == None:
     print("Ninguna empresa activa")
    else:
       print("Trabajando con ",empresa_status_loggin["nombre"])
       
    opciones_empresas = input("Introduce la opcion que desee-->").strip()
    if opciones_empresas not in ("1","2","3"):
     print("Invalido debe seleccionar de la opcion 1 al 3")
     continue

    if opciones_empresas =="1":
        print("Puede empezar a crear su empresa")
        nueva = funciones.crear_empresa(mis_empresas)
        mis_empresas.append(nueva)
    elif opciones_empresas =="2":
       id_buscado = int(input("Que ID buscas?"))
       for empresa in mis_empresas:
          if empresa["id"]== id_buscado:
             empresa_status_loggin = empresa
             break
    elif opciones_empresas =="3":
        print("Salir")
        break

from funciones import*#CON ESTO IMPORTAMOS TODAS LAS FUNCIONES.PY


print("Proyecto funcionandooooooooooo")
       




    


print("Proyecto Phoenix activo")
