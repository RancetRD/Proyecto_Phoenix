def crear_empresa(lista_empresas):
    print("Bienvenido, Registro a nueva empresa")
    id_empresa = len(lista_empresas)+1#GENERA UN ID UNICO

    nombre = input("Nombre de la empresa-->").upper().strip()
    rnc = input("RNC(9 u 11 Digitos)-->")
    
    while not rnc.isdigit() or len (rnc) not in [9,11]:
        print("Error el RNC debe solo debe ser numeros de 9 o 11 digitos ")
        rnc = input("Introduce un RNC valido").strip()

    print("Persona Fisica o Juridica")
    print("1-Persona fisica")
    print("2-Persona Juridica")
    opciones = input("Seleccione la opcion 1/2")
    regimen ="FISICA" if opciones =="1" else "JURIDICA"     

    nueva_empresa = {
        "id":id_empresa,
        "nombre":nombre,
        "rnc":rnc,
        "regimen":regimen,
        "compras":[],#AQUI PARA EL 606
        "ventas":[],# AQUI PARA EL 607
        "ncf_secuencia": 1#PARA FACTURAS DE VENTAS
    }      
    return nueva_empresa    
    
def campo_texto(mensaje):#FUNCION REUTILIZABLE , PARA CUALQUIER VALOR EN TEXTO
    while True:
     valor_texto = input(mensaje).strip().upper()
     if not valor_texto:
        print("Campo vacio!, debe introducir un valor valido ")
        continue
     return valor_texto

def campo_float(mensaje):#FUNCION REUTILIZABLE, PARA CUALQUIER VALOR EN NUMEROS
   while True:
      try:
         valor_float = float(input(mensaje))
         if valor_float < 0:
            print("El valor no puede ser negativo")
            continue
         return valor_float
      except ValueError:
         print("Debe introducir un monto valido por ejm 150.75")

import datetime

def campo_fecha(mensaje):#FUNCION REUTILIZABLE, PARA CUALQUIER FECHA 
    while True:
        campo_fecha = input(mensaje)
        try:
           datetime.datetime.strptime(campo_fecha,"%d/%m/%Y")
           return campo_fecha
        except ValueError:
           print("Formato invalido")

def campo_ncf(mensaje):
   while True:
      ncf = campo_texto(mensaje)
      largo = len(ncf)
      if largo == 11 or largo == 13:#VALIDAMOS QUE TENGA EXACTAMENTE 11 O 13 CARACTERES PARA EVITAR ERROR DE TYPING
        return ncf
      else:
         print("Debe introducir un minimo de 11 caracteres y un limite de 13")

#---------------FUNCION BASE DE REGISTRO DE FACTURAS-------------------
def registrar_gasto(facturas):# ESTA SER LA FUNCION BASE DE LAS FACTURAS
   print("REGISTROS GASTOS 606")
   while True:
        ncf = campo_ncf("NCF-->").upper()
        if any (f["ncf"]== ncf for f in facturas):
         print("NCF duplicado, vuelva introcuir el ncf",ncf)
         continue
        break
   proveedor = campo_texto("PROVEEDOR-->").strip()
   rnc = campo_texto("RNC/CEDULA-->")
   fecha = campo_fecha("FECHA-->")
   monto_neto = campo_float("MONTO NETO-->")
   while True:
            
        itbs = campo_float("ITBS-->")    
        if itbs > monto_neto:
            print("EL itbs no puede ser mayor al monto neto")
            continue
        break

   total = monto_neto + itbs 

   factura = {#AQUI CREAMOS LA LISTA , DE TODO LO QUE TENGA QUE VER CON FACTURA Y DE LA FORMA QUE LA VISUALIZAREMOS
         "proveedor":proveedor,
         "rnc":rnc,
         "ncf":ncf,
         "fecha":fecha,
         "monto_neto":monto_neto,
         "itbs":itbs,
         "total":total
           }
   facturas.append(factura)
   print(f"\n✅ Registro exitoso.")
   print(f"Su número de factura registrado es el #{len(facturas)}") #AQUI VALIDAMOS TOTAL DE FACTURAS
   print(f"Proovedor{proveedor}--,Factura {ncf} --registrada. Total:-- {total},")#AQUI SE VALIDA EL TOTAL DE LA FACTURA CON LOS DATOS MAS IMPORTANTE
    
   return facturas
    
def configurar_empresa():#CON ESTA FUNCION VAMOS A DECIDIR SI EL CLIENTE NECESITA SU DECLARACION FISCA ORDINARIO O RST
   nombre = campo_texto("Introduca el nombre").strip()
   rnc = campo_texto("Introduce el RNC")
   
   print("Selecciona el regimen fiscal")
   print("1-RST")
   print("2-Ordinaria")

   while True:
    opcion_configuracion = campo_texto("Eliga la opcion 1 o 2-->").strip()
    if opcion_configuracion not in("1","2"):# NOS ASEGURAMOS DE CUALQUIER ERROR CON ESTA LINEA DE ESPACIO U OPCION DIFERENTE
      print("Opcion invalida,debe introducir 1 o 2")
      continue
   
    if opcion_configuracion =="1":
      regimen = "RST"
    elif opcion_configuracion =="2":
       regimen = "ordinario"
    print(f">>Configuracion guardada: {regimen}")
    break
   #DEVOLVEMOS LOS DATOS CON RETURN
   return nombre, rnc, regimen
#AQUI SE VA ALMACENAR TODOS LOS DATOS QUE TIENE UNA FACTURA
def guardar_factura_bodega(facturas, ncf, proveedor, rnc, fecha, monto_neto, itbs, isc=0, cdt=0, ley_10=0):
    total = monto_neto + itbs + isc + cdt + ley_10
    
    factura = {
        "ncf": ncf,           # Empezamos con el NCF como llave principal
        "proveedor": proveedor,
        "rnc": rnc,
        "fecha": fecha,
        "monto_neto": monto_neto,
        "itbs": itbs,
        "isc": isc,
        "cdt": cdt,
        "ley_10": ley_10,
        "total": total     
    }
    facturas.append(factura)
    print(f"\n Registro exitoso. Total: {total}")
    return facturas

#FUNCION ESPECIALMENTE PARA LOS GASTOS DE RESTAURANTE
def registrar_telecom(facturas):
   ncf = campo_ncf("NCF-->").upper()
   proveedor = campo_texto("Proveedor").strip()
   rnc = campo_texto("RNC-->").strip()
   fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
   monto_neto = campo_float("Monto neto-->")
   itbs = monto_neto * 0.18
   isc = monto_neto * 0.10
   cdt = monto_neto * 0.02
   return guardar_factura_bodega(facturas,ncf,proveedor,rnc,fecha,monto_neto,itbs,isc,cdt)

#FUNCION PARA TIPO GASTO FACTURA RESTAURANTE
def registrar_restaurante(facturas):

   ncf = campo_ncf("NCF-->").upper()
   proveedor = campo_texto("Proveedor").strip()
   rnc = campo_texto("RNC-->").strip()
   fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
   monto_neto = campo_float("Monto neto-->")
   itbs = monto_neto * 0.18
   ley_10 = monto_neto * 0.10

   return guardar_factura_bodega(facturas,ncf,proveedor,rnc,fecha,monto_neto,itbs,0,0,ley_10)

def menu_registro(facturas):#AQUI ES DONDE REGISTRAREMOS EL TIPO DE FACTURA , SEGUN LOS QUE NOS CONVENGAN
   
   while True:
      print("Bienvenido al programa Phoenix")
      print("Seleccione la opcion del tipo de factura que desea registrar")
      print("1-Registrar gastos")
      print("2-Registrar Telecom")
      print("3-Registrar restaurante")
      print("4-Salir del menu")
      opciones = campo_texto("Introduce la opcion que desees registrar").strip()
      if opciones not in ("1","2","3","4"):
         print("Opcion invalida,debe digitar un numero")
         continue
      if opciones =="1":
         registrar_gasto(facturas)
      elif opciones =="2":
         registrar_telecom(facturas)
      elif opciones =="3":
         registrar_restaurante(facturas)
      elif opciones =="4":
         print("Saliendo del sistema")
         break
      else:
         print("Opcion no valida")
      


    