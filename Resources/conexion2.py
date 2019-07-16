#!/usr/bin/env python
#-*- coding: utf-8 -*-
import MySQLdb


def Consulta(query=''): 
    # Abrir conexion.
    
    conexion = MySQLdb.connect(host="faraday.eie.ucr.ac.cr",user="recetario",passwd="eR9P4vGAC9l5h37X",db="recetario")
    cursor = conexion.cursor()         # Crear un cursor 
    cursor.execute(query)              # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()       # Traer los resultados de un select 
    else: 
        conexion.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()                 # Cerrar el cursor 
    conexion.close()               # Cerrar la conexión 

  
    return data


def AgregarCategoria(nombreCategoria, descripcion):
    #nombreCategoria = input("Nombre de la categoria: ")
    #descripcion = input("Ingrese una descripcion de la categoria: ")
    query = "INSERT INTO Categorias (nombreCategoria, Descripcion) VALUES ('%s','%s')" %(nombreCategoria,descripcion)
    Consulta(query)



def AgregarPlato(Nombre, CategoriaSelec, Ingredientes, Porciones, Preparacion):
    #Nombre = input("Nombre del plato: ")
    #CategoriaSelec = input("A cual categoría pertenece el plato: ")
    query = "SELECT codigoCategoria FROM Categorias WHERE nombreCategoria = '%s'" %CategoriaSelec
    idCategoria = ProcesarNumero(Consulta(query))
    #Ingredientes = input("Escriba los ingredientes del plato: ")
    #Porciones = input("Ingrese la cantidad de porciones: ")

    #Preparacion =input("Escriba los pasos para la preparacion del plato: ")

    query = "INSERT INTO Plato (Nombre, idCategoria, Ingredientes, Porciones, Preparacion) VALUES ('%s','%d','%s','%d','%s')" %(Nombre,idCategoria,Ingredientes,int(Porciones),Preparacion)
    Consulta(query)



def AgregarUsuario(nombreUsuario,clave,email):
    
    query = "INSERT INTO Usuario (nombreUsuario, email, clave) VALUES ('%s','%s','%s')" %(nombreUsuario,email,clave)
    Consulta(query)


def verificarUsuario(nombreUsuario):
    
    Usuarios = getUsuarios()
        
    if nombreUsuario in Usuarios:
        return True
    else:
        return False


def BorrarPlato(platoBorrar):
    
    query = "DELETE FROM Plato WHERE Nombre = '%s'" % platoBorrar 
    Consulta(query)


def verificarPlato(Categoria,platoBorrar):

    Platos = getPlatos(Categoria)
        
    if platoBorrar in Platos:
        return True   

    else:
        return False


def BorrarUsuario(usuarioBorrar):
  
    query = "DELETE FROM Usuario WHERE nombreUsuario = '%s'" % usuarioBorrar 
    Consulta(query)
    


def ProcesarDatos(Datos):

    Vector = ["" for x in range(len(Datos))]
    for i in range(len(Datos)):
        Vec = Datos[i]
        Vec = str(Vec)
        Vec = Vec.replace('(','')
        Vec = Vec.replace("'",'')
        #Vec = Vec.replace('.','')
        Vec = Vec.replace(')','')
        Vec = Vec.replace(',','')
        Vector[i] = Vec
    return Vector


def ProcesarNumero(Datos):
    
    Datos = str(Datos)
    Datos = Datos.replace('(','')
    Datos = Datos.replace("'",'')
    Datos = Datos.replace('L','')
    Datos = Datos.replace(')','')
    Datos = Datos.replace(',','')
    Datos = int(Datos)
    return Datos





def getPlatos(Categoria):
    query = "SELECT codigoCategoria FROM Categorias WHERE nombreCategoria = '%s'" %Categoria 
    idCategoria = ProcesarNumero(Consulta(query))
    query = "SELECT Nombre FROM Plato WHERE idCategoria = '%i'" %idCategoria
    PlatosVector = Consulta(query)

    return ProcesarDatos(PlatosVector)

def getCategorias():
    query = "SELECT nombreCategoria FROM Categorias"
    CategoriasVector = Consulta(query)

    return ProcesarDatos(CategoriasVector)


def getUsuarios():
    query = "SELECT nombreUsuario FROM Usuario"
    
    return ProcesarDatos(Consulta(query))


def getClave(Usuario):
    query = "SELECT clave FROM Usuario WHERE nombreUsuario = '%s'" %Usuario
    
    return ProcesarDatos(Consulta(query))


def getPorciones(nombrePlato):
    query = "SELECT Porciones FROM Plato WHERE Nombre = '%s'" %nombrePlato

    return ProcesarNumero(Consulta(query))

def getIngredientes(nombrePlato):
    query = "SELECT Ingredientes FROM Plato WHERE Nombre = '%s'" %nombrePlato

    return ProcesarDatos(Consulta(query))

def getPreparacion(nombrePlato):
    query = "SELECT Preparacion FROM Plato WHERE Nombre = '%s'" %nombrePlato

    return ProcesarDatos(Consulta(query))


print(getIngredientes('Camarones a la parrilla'))
print('\n')
print(getPreparacion('Camarones a la parrilla'))
