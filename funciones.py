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
        "cotizaciones":[],#AQUI SE GUARDARAN TODAS LAS COTIZACIONES
        "proformas":[],#AQUI SE GUARDARAN TODAS LAS PROFORMAS
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

#ESTE CAMPO ES EXCLUSIVAMENTE PARA REGLAS DE NCF, QUE TENGA UN RANGO MINIMO DE CARACTERES A UN RANGO MAXIMO DE CARACTERES 
def campo_ncf(mensaje):
   while True:
      ncf = campo_texto(mensaje)
      largo = len(ncf)
      if largo == 11 or largo == 13:#VALIDAMOS QUE TENGA EXACTAMENTE 11 O 13 CARACTERES PARA EVITAR ERROR DE TYPING
        return ncf
      else:
         print("Debe introducir un minimo de 11 caracteres y un limite de 13")

#ESTE CAMPO ES EXCLUSIVO PARA ENCAPSULAR REGLAR CONTABLES DE ISC , SE LE DA UN MARGEN DE ERROR DE 3 PESOS , POR POSIBLES REDONDEOS 
def campo_isc(mensaje,monto_neto):
   while True:
     valor_isc = campo_float((mensaje))
     if valor_isc < 0:
        print("No se aceptan numeros negativos")
        continue
     if valor_isc > (monto_neto * 0.10) +3:
      print("El monto de ISC, no puede ser mayor al 10%,pero tiene un margen de error de 3 pesos")
      continue    
     return valor_isc

#ESTE CAMPO ES EXCLUSIVO PARA ENCAPSULAR REGLAR CONTABLES DE CDT , SE LE DA UN MARGEN DE ERROR DE 3 PESOS , POR POSIBLES REDONDEOS 
def campo_cdt(mensaje,monto_neto):
   while True:
      valor_cdt = campo_float((mensaje))
      if valor_cdt < 0:
         print("No se aceptan numeros ngeativos")
         continue
      if valor_cdt > (monto_neto *0.02)+3:
         print("El monto de CDT, no puede ser mayor al 2%,pero tiene un margen de error de 3 pesos")
         continue
      return valor_cdt

def campo_10_ley(mensaje,monto_neto):
   while True:
      propina_10_ley = campo_float(mensaje)
      if propina_10_ley < 0:
         print("Monto,invalido , no puede introducir numeros negativos")
         continue
      if propina_10_ley > (monto_neto * 0.10)+3:
         print("El monto de la propina legal no puede ser mayor al 10% , tiene un margen derror de 3 pesos")
         continue
      return propina_10_ley
   

#---------------FUNCION BASE DE REGISTRO DE FACTURAS-------------------
def registrar_gasto(empresa):# ESTA SER LA FUNCION BASE DE LAS FACTURAS
   print("REGISTROS GASTOS 606")
   while True:
        ncf = campo_ncf("NCF-->").upper()
        if any (f["ncf"]== ncf for f in empresa["compras"]):
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
   isc = 0
   cdt = 0
   ley_10 = 0

   
   concepto = campo_texto("Concepto del gasto-->").strip()
   comentario = input("Comentario (Opcional)-->").strip().upper()

   empresa = guardar_factura_bodega(empresa, ncf, proveedor, rnc, fecha, monto_neto, itbs, isc, cdt, ley_10, concepto, comentario)
   
   ultima_factura = empresa["compras"][-1]
   print(f"\n✅ Registro exitoso.")
   print(f"Su numero de facturo registrado es el #{len(empresa['compras'])}" )
   print(f"Resumen: {ultima_factura['proveedor']} | NCF: {ultima_factura['ncf']} | Total: {ultima_factura['total']}")
   return empresa
  
    
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
def guardar_factura_bodega(empresa, ncf, proveedor, rnc, fecha, monto_neto, itbs, isc=0, cdt=0, ley_10=0,concepto="",comentario="0",destino="compras"):
    destinos_validos = ["compras", "ventas", "cotizaciones", "proformas", "recibos_decaja"]
    
    if destino not in destinos_validos:
        print(f" ERROR: El destino '{destino}' no existe en la estructura.")
        return empresa
    conteo = len(empresa["compras"]) + len(empresa["ventas"])
    id_fijo = f"PHX-{conteo + 1:04d}"
    
    total = monto_neto + itbs + isc + cdt + ley_10
   
    factura = {
       "id_transaccion":id_fijo,
        "ncf": ncf,           # Empezamos con el NCF como llave principal
        "proveedor": proveedor,
        "rnc": rnc,
        "fecha": fecha,
        "monto_neto": monto_neto,
        "itbs": itbs,
        "isc": isc,
        "cdt": cdt,
        "ley_10": ley_10,
        "total": total,
        "concepto":concepto,
        "comentario":comentario,  
        "historial_pagos":[],
        "monto_acumulado": 0.0,
        "estado_pago":"PENDIENTE",
        "tipo_documento":destino
    }
    
    empresa[destino].append(factura)
    print(f"\n Guardado en Bodega con ID: {id_fijo}")
    print(f"\n Registro exitoso. Total: {total}")
    return empresa

#FUNCION REUTILIZABLE DE COTIZACION
def registrar_cotizacion(empresa):
   print("REGISTRO DE COTIZACIONES")
   
   proveedor = campo_texto("Proveedor-->").strip()
   rnc = campo_texto("RNC o Cedula")
   fecha = campo_texto ("Fecha (dd/mm/aaaa)-->")
   monto_neto = campo_float("Introduce el monto de la cotizacion")
   itbs = monto_neto * 0.18
   concepto = campo_texto("Introduce un concepto si desea")
   comentario = input("Introduce un comentario si desea")
   

   empresa = guardar_factura_bodega(
      empresa,
      ncf ="N/A",
      proveedor = proveedor,
      rnc = rnc,
      fecha = fecha,
      monto_neto = monto_neto,
      itbs = itbs,
      isc = 0,
      cdt = 0,
      ley_10 = 0,
      concepto = concepto,
      comentario = comentario,
      destino ="cotizaciones"

   )
   ultima_cotizacion = empresa["cotizaciones"][-1]
   print(f"\n Registro exitoso. Su ID generado es: {ultima_cotizacion['id_transaccion']}")
   return empresa

#FUNCION RETULIZABLE DE BUSQEUDA DE FACTURAS
def buscar_facturas(empresa,ncf):
    ncf_buscar = ncf.strip().upper()
    for  factura in empresa["compras"]:
      if factura ["ncf"]== ncf_buscar:
       print("Factura encontrada")
       return factura
      
    print("NCF no encontrado")
    return None


          

#FUNCION ESPECIALMENTE PARA LOS GASTOS DE RESTAURANTE
def registrar_telecom(empresa):
   print("Registros de telecomunicaciones")

   ncf = campo_ncf("NCF-->").upper()
   proveedor = campo_texto("Proveedor-->").strip()
   rnc = campo_texto("RNC-->").strip()
   fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
   monto_neto = campo_float("Monto neto-->")
   itbs = campo_float("ITBS")
   isc = campo_isc("ISC-->",monto_neto)
   cdt = campo_cdt("CDT-->",monto_neto)
   ley_10 = 0
   concepto = campo_texto("Concepto del gasto-->").strip()
   comentario = input("Comentario (Opcional)-->").strip().upper()

   return guardar_factura_bodega(empresa,ncf,proveedor,rnc,fecha,monto_neto,itbs,isc,cdt,ley_10,concepto, comentario)

#FUNCION PARA TIPO GASTO FACTURA RESTAURANTE
def registrar_restaurante(empresa):

   ncf = campo_ncf("NCF-->").upper()
   proveedor = campo_texto("Proveedor").strip()
   rnc = campo_texto("RNC-->").strip()
   fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
   monto_neto = campo_float("Monto neto-->")
   itbs = monto_neto * 0.18
   ley_10 = monto_neto * 0.10
   concepto = campo_texto("Concepto del gasto-->").strip()
   comentario = input("Comentario (Opcional)-->").strip().upper()


   return guardar_factura_bodega(empresa, ncf, proveedor, rnc, fecha, monto_neto, itbs, 0, 0, ley_10, concepto, comentario)


#LINEA DONDE VAMOS IMPORTAR EL DICCIONARIO DONDE ESTA EL ARCHIVO MODELO
from modelos import  crear_contenedor_vacio


def iniciar_nueva_operacion(proveedor,monto_total,moneda,tipo_documento):
  operacion = crear_contenedor_vacio()
  operacion["informacion"]["proveedor"] = proveedor
  operacion["informacion"]["fecha"] = "2026-04-11"
  operacion["informacion"]["comentario"]= "Registro inicial"

  operacion["montos"]["total_moneda_original"] = monto_total
  operacion ["montos"]["moneda"]= moneda
  operacion ["montos"]["saldo_pendiente"]= monto_total
  
  operacion ["tipo_documento"]= tipo_documento
  return operacion

   


def menu_registro(empresa):#AQUI ES DONDE REGISTRAREMOS EL TIPO DE FACTURA , SEGUN LOS QUE NOS CONVENGAN
   
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
         registrar_gasto(empresa)
      elif opciones =="2":
         registrar_telecom(empresa)
      elif opciones =="3":
         registrar_restaurante(empresa)
      elif opciones =="4":
         print("Saliendo del sistema")
         break
      else:
         print("Opcion no valida")
      


    