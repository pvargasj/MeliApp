#!usr/bin/python
#-*-coding: utf-8-*-

from kivy.app import App
#kivy.require('1.10.0')
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import Button	
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock

from kivy.garden.zbarcam import ZBarCam

import os.path
import sqlite3

estudiante=''
ruta= ""


def retornaEstudiantes(rt):
	"""Función global que retorna una lista con los estudiantes de una base de datos, recibiendo como parámetro su ruta rt.
	
	Busca en la tabla info de la base de datos, que es creada por la aplicación al inicializarla, todos los nombres de los estudiantes que se han creado en este laboratorio, es decir, que tienen una tabla en la base de datos. Genera una lista únicamente con los nombres de los estudiantes como strings y los retorna.
	"""
	conn=sqlite3.connect(rt)
	c=conn.cursor()
	c.execute("SELECT * FROM {}".format('info'))
	lista=c.fetchall()
	estudiantes=[]
	for estudiante in range(1, len(lista)):
		estudiantes.append(lista[estudiante][2])
	return estudiantes
	

def retornaNumLabo(rt):
	"""Función global que retorna el número del siguiente laboratorio a crear (si ya existen n laboratorios, retorna n+1), para una base de datos con ruta rt.

	Dicho número se encuentra almacenado en la primera fila de la tabla info, que se creó cuando se inicializó la base de datos. Se extrae el dato y se retorna como un entero.
	"""
	conn=sqlite3.connect(rt)
	c=conn.cursor()
	c.execute("SELECT * FROM {}".format('info'))
	lista=c.fetchall()
	
	return int(lista[0][1])
		
def imprimirTabla(rt, nombre):
	"""Función global que retorna una lista con títulos y cadenas de notas, correspondientes a las calificaciones de los laboratorios para un estudiante.

	Toma como parámetros la ruta a la base de datos y el nombre del estudiante a buscar. Obtiene la información de la tabla del estudiante y genera strings con formato adecuado a partir de ella, para retornarlas en la lista. 
	"""
	conn=sqlite3.connect(rt)
	c=conn.cursor()
	c.execute("SELECT * FROM {}".format(nombre))
	lista=c.fetchall()
	laboratorio=' '	
	for i in lista:
		laboratorio+=(str(i[0])+'    ')
	asistencia=' '
	for i in lista:
		asistencia+=(str(i[1])+'    ')
	prereporte=' '
	for i in lista:
		prereporte+=(str(i[2])+'    ')
	quiz=' '
	for i in lista:
		quiz+=(str(i[3])+'    ')
	cotidiano=' '
	for i in lista:
		cotidiano+=(str(i[4])+'    ')
	reporte=' '
	for i in lista:
		reporte+=(str(i[5])+'    ')
	return ['Número de laboratorio', laboratorio, 'Asistencia', asistencia, 'Prereporte', prereporte, 'Quiz', quiz, 'Cotidiano', cotidiano, 'Reporte', reporte]


class InitScreen(Screen):
	"""Pantalla de inicio donde se selecciona el tipo de ingreso: Estudiante o profesor.
	
	Tiene dos botones, uno para cada ingreso, que lo redireccionan a otras pantallas de acuerdo con la selección.
	"""
	def switchEstudiante(self):
		"""Una función que inicializa el widget de la cámara en la pantalla de selección de estudiante al ingresar a ella.
	
		Esta función es ejecutada por el botón, cambia la pantalla y llama la función addCam() de la clase MyApp, que abre el widget de la cámara en la nueva pantalla.
		"""
		App.get_running_app().addCam('VerNotasEstudiante')
		self.parent.current='VerNotasEstudiante'


class VerNotasEstudiante(Screen):
	"""Pantalla para indicar el estudiante y laboratorio desde el ingreso de estudiante.

	Atributos:
		popup, popupA:	popups a desplegar en caso de un error en el ingreso de datos.
	
	Una pantalla con un ingreso para el estudiante mediante un código QR y un ingreso de entrada de texto para el laboratorio. Redirige a las calificaciones de dicho estudiante en dicho laboratorio. El laboratorio es el nombre del usuario del profesor.
	"""
			
	global estudiante
	global ruta
	popup = Popup(title='Ingresar estudiante',
	content=Label(text='Estudiante no encontrado!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupA = Popup(title='Ingresar estudiante',
	content=Label(text='Curso no encontrado!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def actualizarEntrada(self):
		"""Toma el estudiante y la ruta ingresados y, en caso de que sean válidos, hace el ingreso a la pantalla de calificaciones.

		Revisa si la ruta existe, y si contiene al estudiante. En caso de que alguna de estas condiciones no se cumpla, muestra un popup explicando el error. Si los datos son válidos, los asigna a las variables globales estudiante y ruta, para que luego sean tomadas como referencia por otras clases, y hace el ingreso a la pantalla de calificaciones, utilizando la función refresh() de la clase MyApp para actualizar el objeto RecycleView que contiene la lista de notas, a la selección actual.
		"""
		global estudiante	
		global ruta
		entradaEstudiante=", ".join([str(symbol.data) for symbol in App.get_running_app().zbarcam.symbols])
		nrut='./'+self.ids.entradaCurso.text+'.sqlite'
		if os.path.isfile(nrut):
			if entradaEstudiante in retornaEstudiantes(nrut):
				estudiante= entradaEstudiante
				ruta=nrut
				App.get_running_app().refresh()
				self.parent.current = 'DisplayNotasEstudiante'
			else:
				self.popup.open()
		else:
			self.popupA.open()

	def back(self):
		"""Función que retorna el programa a la pantalla de inicio.

		Es ejecutada por el botón Atrás. Remueve el widget de la cámara de la pantalla con la función rmCam() de MyApp, para que sea accesible posteriormente en otras pantallas, y cambia la pantalla.
		"""
		App.get_running_app().rmCam('VerNotasEstudiante')
		self.parent.current='InitScreen'


class DisplayNotasEstudiante(Screen):
	"""Pantalla que muestra las notas con el ingreso de estudiante.
	
	Una pantalla con un objeto RecycleView que despliega las notas seleccionadas, y un botón Atrás.
	"""

	def resetEstudiante(self):
		"""Función que reasigna la variable global estudiante a un string vacío.

		Esta función es ejecutada por el botón Atrás, para reiniciar dicha variable y que no haya problemas con sus futuras reasignaciones.
		"""
		global estudiante
		estudiante=''

	def update(self, dt):
		"""Función que actualiza el RecycleView.
	
		Toma las variables globales estudiante y ruta, y las usa junto con la función global imprimirTabla() para generar los datos a desplegar en el RecycleView. Esta función se llama desde la función refresh() de MyApp.
		""" 
		global estudiante
		global ruta
		self.ids.displaydatose.data=[{'text': x} for x in imprimirTabla(ruta, estudiante)]


class RV(RecycleView):
	"""Clase para manejar el display de notas.

	Esta clase se instancia en cada pantalla donde se muestren las notas de un estudiante.
	"""
	global estudiante
	global ruta
	def __init__(self, **kwargs):
		"""El constructor de la clase.

		Inicializa el RecycleView con su atributo data como un diccionario con un único string vacío, cuya llave el el string 'text'. Éste es el formato utilizado para asignar información a dicho display.
		"""
		super(RV, self).__init__(**kwargs)
		self.data=[{'text': ''}]
		

class IngresaProfe(Screen):
	"""Pantalla para ingresar como profesor o crear nuevo usuario.

	Posee tres botones, Nuevo usuario, usuario existente, y Atrás.
	"""
	pass


class NuevoProfe(Screen):
	"""Pantalla para agregar nuevo profesor a la base de datos.
	
	Atributos:
		popup, popupA:	popups a desplegar en caso de errores.
		__rutalogin:	atributo privado con la ruta de la base de datos donde se guardan los usuarios, contraseñas y rutas a las bases de datos de cada laboratorio.
	
	Una pantalla con dos entradas de texto, una para el usuario y una para la contraseña (que puede ser vacía), un botón Ingresar y un botón de Atrás.

	"""
	__rutalogin= "./login.sqlite"
	popup = Popup(title='Crear usuario',
	content=Label(text='Usuario ya existe!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupA = Popup(title='Crear usuario',
	content=Label(text='Debe introducir un usuario!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def __retornaProfes(self):
		"""Función privada que retorna una lista de los usuarios, contraseñas y rutas existentes.

		Accesa la base de datos en __rutalogin, extrae la tabla, la convierte en una matriz de strings y la retorna.
		"""
		conn=sqlite3.connect(self.__rutalogin)
		c=conn.cursor()
		c.execute("SELECT * FROM {}".format('login'))
		lista=c.fetchall()
		profes=[]
		contrasenas=[]
		rutas=[]
		for profe in range(len(lista)):
			profes.append(lista[profe][0])
			contrasenas.append(lista[profe][1])
			rutas.append(lista[profe][2])
		return [profes, contrasenas, rutas]


	def __initInfo(self, rt):
		"""Inicializa la tabla info en la base de datos de un usuario, que contendrá el número del siguiente laboratorio a crear y la lista de estudiantes.
		"""
		conn=sqlite3.connect(rt)
		c=conn.cursor()
		c.execute('''CREATE TABLE {}
        	(GUIA TEXT PRIMARY KEY  NOT NULL,
        	 NUMLABO 		INTEGER ,
        	 ESTUDIANTES              TEXT  );'''.format('info'))
		conn.commit()
		
		c.execute("INSERT INTO {} (GUIA, NUMLABO) VALUES ({}, {})".format('info','\'numlabo\'', 1))
		conn.commit()
		conn.close()

	def __addProfe(self, usuario, contrasena):
		"""Agrega un nuevo usuario al sistema.

		Agrega el usuario, la contraseña, y la ruta a una base de datos con el nombre del usuario, a una nueva fila de la tabla en login.
		"""
		usr='\''+usuario+'\''
		pwd='\''+contrasena+'\''
		rut='./'+usuario+'.sqlite'
		rt='\''+'./'+usuario+'.sqlite'+'\''
		conn=sqlite3.connect(self.__rutalogin)
		c=conn.cursor()
		c.execute("INSERT INTO {} (USUARIO, CONTRASENA, RUTA) VALUES ({}, {}, {})".format('login',usr, pwd, rt))
		conn.commit()
		conn.close()
		self.__initInfo(rut)

	def __initLogin(self):
		"""Inicializa la base de datos login, con los datos de los usuarios.
		"""
		conn=sqlite3.connect(self.__rutalogin)
		c=conn.cursor()
		c.execute('''CREATE TABLE {}
        	(USUARIO TEXT PRIMARY KEY  NOT NULL,
        	 CONTRASENA               TEXT,
        	 RUTA                     TEXT  NOT NULL);'''.format('login'))
		conn.commit()
		conn.close()

	def nuevo(self):
		"""La función ejecutada por el botón Ingresar para agregar el nuevo usuario.

		Si la base de datos login aún no existe, la crea. Si el usuario es vacío o ya existe, abre un popup explicando el error. En caso de recibir información válida, agrega los datos del usuario a la tabla login e inicializa su base de datos con la tabla info.
		"""
		if not(os.path.isfile(self.__rutalogin)):
			self.__initLogin()

		if self.ids.usuario.text == "":
			self.popupA.open()

		elif self.ids.usuario.text in self.__retornaProfes()[0]:
			self.popup.open()
		else:
			self.__addProfe(self.ids.usuario.text, self.ids.contrasena.text)
			self.parent.current = 'IngresaProfe'
		

class LoginProfe(Screen):
	"""Pantalla para hacer ingreso de profesor.

	Atributos:
		popup, popupA:	popups a desplegar en caso de errores.
		__rutalogin:	atributo privado con la ruta de la base de datos donde se guardan los usuarios, contraseñas y rutas a las bases de datos de cada laboratorio.

	Una pantalla con dos entradas de texto, una para el usuario y una para la contraseña (que puede ser vacía), un botón Ingresar y un botón de Atrás.
	"""

	__rutalogin= "./login.sqlite"
	global ruta
	popup = Popup(title='Ingresar',
	content=Label(text='Datos inválidos!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupA = Popup(title='Ingresar',
	content=Label(text='Aún no existen usuarios!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def __retornaProfes(self):
		"""Función privada que retorna una lista de los usuarios, contraseñas y rutas existentes.

		Accesa la base de datos en __rutalogin, extrae la tabla, la convierte en una matriz de strings y la retorna.
		"""
		conn=sqlite3.connect(self.__rutalogin)
		c=conn.cursor()
		c.execute("SELECT * FROM {}".format('login'))
		lista=c.fetchall()
		profes=[]
		contrasenas=[]
		rutas=[]
		for profe in range(len(lista)):
			profes.append(lista[profe][0])
			contrasenas.append(lista[profe][1])
			rutas.append(lista[profe][2])
		return [profes, contrasenas, rutas]

	def ingresar(self):
		"""Realiza el ingreso en caso de que el usuario sea válido.

		Genera la matriz con los datos de los profesores, y si encuentra un usuacio que coincida con el ingresado, y su contraseña es la indicada, realiza el ingreso a la siguiente pantalla y asigna la variable global ruta a la ruta de la base de datos de dicho usuario.
		"""
		global ruta
		if not(os.path.isfile(self.__rutalogin)):
			self.popupA.open()
			return
		profes=self.__retornaProfes()
		for i in range(len(profes[0])):
			if self.ids.usuario.text==profes[0][i] and self.ids.contrasena.text==profes[1][i]:
				ruta=profes[2][i]
				self.parent.current = 'DisplayProfe'
				return
		self.popup.open()
		return 


class DisplayProfe(Screen):
	"""Pantalla con las opciones del profesor para manejar los laboratorios.

	Contiene los botones Crear laboratorio, Agregar estudiante, Calificar, Ver notas, y Atrás.
	"""
	popup = Popup(title='Crear laboratorio',
	content=Label(text='Laboratorio creado!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def profeCreaLabo(self):
		"""Crea un nuevo laboratorio.

		Actualiza el dato del siguiente laboratorio en la tabla info, y para todos los estudiantes registrados en dicha tabla, inicializa una nueva fila en sus respectivas tablas, con todas las calificaciones por defecto en 0.
		"""
		global ruta
		numlabo= retornaNumLabo(ruta)
		estudiantes= retornaEstudiantes(ruta)
		conn=sqlite3.connect(ruta)
		c= conn.cursor()
		for estudiante in estudiantes:
			c.execute("INSERT INTO {} (LABORATORIO, ASISTENCIA, PREREPORTE, QUIZ, COTIDIANO, REPORTE) VALUES ({}, {}, {}, {}, {}, {})".format(estudiante, numlabo, 0, 0, 0, 0, 0))
		numlabo+=1
		c.execute("UPDATE {} SET NUMLABO = {} WHERE GUIA = {}".format('info',numlabo , '\'numlabo\''))
		conn.commit()
		conn.close()
		self.popup.open()

	def switchEstudiante(self):
		"""Una función que inicializa el widget de la cámara en la pantalla de selección de estudiante para calificar al ingresar a ella.
	
		Esta función es ejecutada por el botón, cambia la pantalla y llama la función addCam() de la clase MyApp, que abre el widget de la cámara en la nueva pantalla.
		"""
		App.get_running_app().addCam('InputEstudiante')
		self.parent.current='InputEstudiante'

	def switchEstudianteA(self):
		"""Una función que inicializa el widget de la cámara en la pantalla de selección de estudiante para ver notas al ingresar a ella.
	
		Esta función es ejecutada por el botón, cambia la pantalla y llama la función addCam() de la clase MyApp, que abre el widget de la cámara en la nueva pantalla.
		"""
		App.get_running_app().addCam('VerNotasProfe')
		self.parent.current='VerNotasProfe'


class AgregaEstudiante(Screen):
	"""Pantalla para ingresar id de nuevo estudiante.

	Posee una entrada de texto para ingresar el id del nuevo estudiante, un botón Ingresar y un botón Atrás.
	"""

	popupA = Popup(title='Agregar estudiante',
	content=Label(text='Debe introducir un nombre!'),
	size_hint=(None, None), size=(400, 400))

	popup = Popup(title='Agregar estudiante',
	content=Label(text='Estudiante ya existe, modifique el nombre.'),
	size_hint=(None, None), size=(400, 400))

	def initTabla(self, nombre):
		"""Inicializa una nueva tabla para un estudiante.
	
		Toma la ruta indicada en la variable global ruta, y crea en ella una nueva tabla con el nombre recibido como parámetro, con las columnas adecuadas para las calificaciones. También agrega el nombre del estudiante a la tabla info.
		"""
		nuevo='\''+nombre+'\''
		conn=sqlite3.connect(ruta)
		c=conn.cursor()
		c.execute('''CREATE TABLE {}
        	(LABORATORIO INTEGER PRIMARY KEY  NOT NULL,
         	ASISTENCIA              BLOB  NOT NULL,
         	PREREPORTE              REAL  NOT NULL,
         	QUIZ        		 REAL  NOT NULL,
	 	COTIDIANO		 REAL  NOT NULL,
         	REPORTE         	 REAL  NOT NULL);'''.format(nombre))
		conn.commit()
		c.execute("INSERT INTO {} (GUIA, ESTUDIANTES) VALUES ({}, {})".format('info',nuevo, nuevo))
		conn.commit()
		conn.close()

	def agregarEstudiante(self):
		"""Función ejecutada por el botón Ingresar para agregar el estudiante.

		Si el estudiante ya existe o el texto ingresado es vacío, retorna error. En caso contrario, procede a agregar el estudiante a la base de datos, a partir del laboratorio en el que se encuentran actualmente.
		"""
		if self.ids.nuevoEstudiante.text == "":
			self.popupA.open()
			return		
		elif self.ids.nuevoEstudiante.text in retornaEstudiantes(ruta):
			self.popup.open()
			return
		else:
			self.initTabla(self.ids.nuevoEstudiante.text)
			self.parent.current = 'DisplayProfe'
			return


class InputEstudiante(Screen):
	"""Pantalla para ingresar estudiante a calificar.

	Posee una entrada de cámara mediante código QR, y botones Ingresar y Atrás.
	"""

	global estudiante
	popup = Popup(title='Ingresar estudiante',
	content=Label(text='Estudiante no encontrado!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def actualizarEntrada(self):
		"""Realiza el ingreso a la pantalla de calificar para un estudiante.

		Lee el dato del código QR y , en caso de encontrar un estudiante válido, asigna su id a la variable global estudiante y realiza el ingreso a la pantalla Rubros. En caso contrario, muestra un popup indicando el error.
		"""
		global estudiante
		global ruta
		entradaEstudiante=", ".join([str(symbol.data) for symbol in App.get_running_app().zbarcam.symbols])
		if entradaEstudiante in retornaEstudiantes(ruta):
			estudiante=entradaEstudiante
			self.parent.current = 'Rubros'
		else:
			self.popup.open()

	def back(self):
		"""Función que retorna a la pantalla principal del profesor.

		Es ejecutada por el botón Atrás. Cierra el widget de la cámara para que sea accesible posteriormente por otras pantallas, y cambia la pantalla.
		"""
		App.get_running_app().rmCam('InputEstudiante')
		self.parent.current='DisplayProfe'


class Rubros(Screen):
	"""Pantalla para seleccionar rubro a calificar.

	Posee un botón por rubro a calificar, y un botón Atrás.
	"""
	global estudiante
	global rubro	
	def resetEstudiante(self):
		"""Función que reinicia la variable global estudiante.

		Se ejecuta por el botón Atrás, para devolver la variable global a un string vacío.
		"""
		global estudiante
		estudiante=''


class CalificarA(Screen):
	"""Pantalla para calificar asistencia.

	Contiene dos entradas de texto, una para el número de laboratorio y una para el valor de la asistencia, además de un botón Ingresar y un botón Atrás.
	"""

	global estudiante

	def __asignarA(self, nombre, n, a):
		"""Función privada para asignar la asistencia al estudiante.

		Se conecta a la base de datos en la variable global ruta, y asigna el valor recibido como parámetro, al nombre y número de laboratorio recibidos también como parámetros.
		"""
		conn=sqlite3.connect(ruta)
		c=conn.cursor()
		c.execute("UPDATE {} SET ASISTENCIA = {} WHERE LABORATORIO = {}".format(nombre, a, n))
		conn.commit()
		conn.close()
		return

	popupA = Popup(title='Calificar',
	content=Label(text='Asistencia inválida!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupB = Popup(title='Calificar',
	content=Label(text='Número de laboratorio inválido!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupC = Popup(title='Calificar',
	content=Label(text='No se ingresó un número!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def asignarRubro(self):
		"""Función ejecutada por el botón Ingresar para realizar la calificación.

		En caso de que los datos ingresados sean válidos, ejecuta la función __asignarA(). En caso contrario, abre un popup indicando el error.
		"""
		global estudiante
		global ruta
		if not(self.ids.nota.text.isdigit()) or not(self.ids.labo.text.isdigit()):
			self.popupC.open()
		elif int(self.ids.nota.text)!=0 and int(self.ids.nota.text)!=1:
			self.popupA.open()
		elif int(self.ids.labo.text)<1 or int(self.ids.labo.text)>=retornaNumLabo(ruta):
			self.popupB.open()
		else:
			self.__asignarA(estudiante, self.ids.labo.text, self.ids.nota.text)
			self.parent.current = 'Rubros'


class CalificarP(Screen):
	"""Pantalla para calificar prereporte.

	Contiene dos entradas de texto, una para el número de laboratorio y una para el valor de la asistencia, además de un botón Ingresar y un botón Atrás.
	"""

	global estudiante

	def __asignarP(self, nombre, n, p):
		"""Función privada para asignar la nota del prereporte al estudiante.

		Se conecta a la base de datos en la variable global ruta, y asigna el valor recibido como parámetro, al nombre y número de laboratorio recibidos también como parámetros.
		"""
		conn=sqlite3.connect(ruta)
		c=conn.cursor()
		c.execute("UPDATE {} SET PREREPORTE = {} WHERE LABORATORIO = {}".format(nombre, p, n))
		conn.commit()
		conn.close()
		return

	popupA = Popup(title='Calificar',
	content=Label(text='Nota inválida!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupB = Popup(title='Calificar',
	content=Label(text='Número de laboratorio inválido!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupC = Popup(title='Calificar',
	content=Label(text='No se ingresó un número!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def asignarRubro(self):
		"""Función ejecutada por el botón Ingresar para realizar la calificación.

		En caso de que los datos ingresados sean válidos, ejecuta la función __asignarP(). En caso contrario, abre un popup indicando el error.
		"""
		global estudiante
		global ruta
		if not(self.ids.nota.text.isdigit()) or not(self.ids.labo.text.isdigit()):
			self.popupC.open()
		elif int(self.ids.nota.text)<0 or int(self.ids.nota.text)>100:
			self.popupA.open()
		elif int(self.ids.labo.text)<1 or int(self.ids.labo.text)>=retornaNumLabo(ruta):
			self.popupB.open()
		else:
			self.__asignarP(estudiante, self.ids.labo.text, self.ids.nota.text)
			self.parent.current = 'Rubros'


class CalificarQ(Screen):
	"""Pantalla para calificar quiz.

	Contiene dos entradas de texto, una para el número de laboratorio y una para el valor de la asistencia, además de un botón Ingresar y un botón Atrás.
	"""

	global estudiante

	def __asignarQ(self, nombre, n, q):
		"""Función privada para asignar la nota del quiz al estudiante.

		Se conecta a la base de datos en la variable global ruta, y asigna el valor recibido como parámetro, al nombre y número de laboratorio recibidos también como parámetros.
		"""
		conn=sqlite3.connect(ruta)
		c=conn.cursor()
		c.execute("UPDATE {} SET QUIZ = {} WHERE LABORATORIO = {}".format(nombre, q, n))
		conn.commit()
		conn.close()
		return

	popupA = Popup(title='Calificar',
	content=Label(text='Nota inválida!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupB = Popup(title='Calificar',
	content=Label(text='Número de laboratorio inválido!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupC = Popup(title='Calificar',
	content=Label(text='No se ingresó un número!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def asignarRubro(self):
		"""Función ejecutada por el botón Ingresar para realizar la calificación.

		En caso de que los datos ingresados sean válidos, ejecuta la función __asignarQ(). En caso contrario, abre un popup indicando el error.
		"""
		global estudiante
		global ruta
		if not(self.ids.nota.text.isdigit()) or not(self.ids.labo.text.isdigit()):
			self.popupC.open()
		elif int(self.ids.nota.text)<0 or int(self.ids.nota.text)>100:
			self.popupA.open()
		elif int(self.ids.labo.text)<1 or int(self.ids.labo.text)>=retornaNumLabo(ruta):
			self.popupB.open()
		else:
			self.__asignarQ(estudiante, self.ids.labo.text, self.ids.nota.text)
			self.parent.current = 'Rubros'


class CalificarC(Screen):
	"""Pantalla para calificar trabajo en laboratorio.

	Contiene dos entradas de texto, una para el número de laboratorio y una para el valor de la asistencia, además de un botón Ingresar y un botón Atrás.
	"""

	global estudiante

	def __asignarC(self, nombre, n, cot):
		"""Función privada para asignar la nota del trabajo en laboratorio al estudiante.

		Se conecta a la base de datos en la variable global ruta, y asigna el valor recibido como parámetro, al nombre y número de laboratorio recibidos también como parámetros.
		"""
		conn=sqlite3.connect(ruta)
		c=conn.cursor()
		c.execute("UPDATE {} SET COTIDIANO = {} WHERE LABORATORIO = {}".format(nombre, cot, n))
		conn.commit()
		conn.close()
		return

	popupA = Popup(title='Calificar',
	content=Label(text='Nota inválida!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupB = Popup(title='Calificar',
	content=Label(text='Número de laboratorio inválido!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupC = Popup(title='Calificar',
	content=Label(text='No se ingresó un número!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def asignarRubro(self):
		"""Función ejecutada por el botón Ingresar para realizar la calificación.

		En caso de que los datos ingresados sean válidos, ejecuta la función __asignarC(). En caso contrario, abre un popup indicando el error.
		"""
		global estudiante
		global ruta
		if not(self.ids.nota.text.isdigit()) or not(self.ids.labo.text.isdigit()):
			self.popupC.open()
		elif int(self.ids.nota.text)<0 or int(self.ids.nota.text)>100:
			self.popupA.open()
		elif int(self.ids.labo.text)<1 or int(self.ids.labo.text)>=retornaNumLabo(ruta):
			self.popupB.open()
		else:
			self.__asignarC(estudiante, self.ids.labo.text, self.ids.nota.text)
			self.parent.current = 'Rubros'


class CalificarR(Screen):
	"""Pantalla para calificar reporte.

	Contiene dos entradas de texto, una para el número de laboratorio y una para el valor de la asistencia, además de un botón Ingresar y un botón Atrás.
	"""

	global estudiante

	def __asignarR(self, nombre, n, r):
		"""Función privada para asignar la nota del reporte al estudiante.

		Se conecta a la base de datos en la variable global ruta, y asigna el valor recibido como parámetro, al nombre y número de laboratorio recibidos también como parámetros.
		"""
		conn=sqlite3.connect(ruta)
		c=conn.cursor()
		c.execute("UPDATE {} SET REPORTE = {} WHERE LABORATORIO = {}".format(nombre, r, n))
		conn.commit()
		conn.close()
		return

	popupA = Popup(title='Calificar',
	content=Label(text='Nota inválida!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupB = Popup(title='Calificar',
	content=Label(text='Número de laboratorio inválido!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	popupC = Popup(title='Calificar',
	content=Label(text='No se ingresó un número!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def asignarRubro(self):
		"""Función ejecutada por el botón Ingresar para realizar la calificación.

		En caso de que los datos ingresados sean válidos, ejecuta la función __asignarR(). En caso contrario, abre un popup indicando el error.
		"""
		global estudiante
		global ruta
		if not(self.ids.nota.text.isdigit()) or not(self.ids.labo.text.isdigit()):
			self.popupC.open()
		elif int(self.ids.nota.text)<0 or int(self.ids.nota.text)>100:
			self.popupA.open()
		elif int(self.ids.labo.text)<1 or int(self.ids.labo.text)>=retornaNumLabo(ruta):
			self.popupB.open()
		else:
			self.__asignarR(estudiante, self.ids.labo.text, self.ids.nota.text)
			self.parent.current = 'Rubros'


class VerNotasProfe(Screen):
	"""Pantalla para indicar el estudiante desde el ingreso de profesor.

	Posee una entrada de cámara para el código QR, un botón Ingresar y un botón Atrás.
	"""

	global estudiante
	popup = Popup(title='Ingresar estudiante',
	content=Label(text='Estudiante no encontrado!'),
	size_hint=(0.8, 0.4), pos_hint={'right':0.9, 'top':0.9})

	def actualizarEntrada(self):
		"""Realiza el ingreso a la pantalla para ver las notas de un estudiante.

		Lee el dato del código QR y , en caso de encontrar un estudiante válido, asigna su id a la variable global estudiante y realiza el ingreso a la pantalla DisplayNotasProfe. En caso contrario, muestra un popup indicando el error.
		"""
		global estudiante
		global ruta
		entradaProfe=", ".join([str(symbol.data) for symbol in App.get_running_app().zbarcam.symbols])
		if entradaProfe in retornaEstudiantes(ruta):
			estudiante=entradaProfe
			App.get_running_app().refresh()
			self.parent.current = 'DisplayNotasProfe'
		else:
			self.popup.open()
	def back(self):
		"""Función que retorna a la pantalla principal del profesor.

		Es ejecutada por el botón Atrás. Cierra el widget de la cámara para que sea accesible posteriormente por otras pantallas, y cambia la pantalla.
		"""
		App.get_running_app().rmCam('VerNotasProfe')
		self.parent.current='DisplayProfe'


class DisplayNotasProfe(Screen):
	"""Pantalla que muestra las notas con el ingreso de profesor.
	
	Contiene una instancia del RecycleView para mostrar las notas, y un botón Atrás.
	"""

	def resetEstudiante(self):
		"""Función que reasigna la variable global estudiante a un string vacío.

		Esta función es ejecutada por el botón Atrás, para reiniciar dicha variable y que no haya problemas con sus futuras reasignaciones.
		"""
		global estudiante
		estudiante=''

	def update(self, dt):
		"""Función que actualiza el RecycleView.
	
		Toma las variables globales estudiante y ruta, y las usa junto con la función global imprimirTabla() para generar los datos a desplegar en el RecycleView. Esta función se llama desde la función refresh() de MyApp.
		""" 
		global estudiante
		global ruta
		self.ids.displaydatosp.data=[{'text': x} for x in imprimirTabla(ruta, estudiante)]



class MyApp(App):
	"""Aplicación, con el ScreenManager para la administración de todas las pantallas.

	Atributos:
		zbarcam:	una instancia de ZBarCam que corresponde al widget que muestra la cámara y lee los códigos QR.
	"""

	zbarcam=ZBarCam(pos_hint={"right":1, "top":0.9},
            		size_hint=(1, 0.5),
            		code_types='qrcode')

	def build(self):
		"""Función que construye las pantallas de la aplicación.

		Esta función es llamda al iniciar la aplicación. Crea un ScreenManager y le agrega todas las pantallas, y llama el archivo .kv con el módulo Builder para complementar los atributos de las pantalla definidos en dicho archivo.
		"""
		self.title= 'Notas de Laboratorio'
		Builder.load_file('main.kv')
		self.sm=ScreenManager()
		self.sm.add_widget(InitScreen(name="InitScreen"))
		self.sm.add_widget(LoginProfe(name="LoginProfe"))
		self.sm.add_widget(IngresaProfe(name="IngresaProfe"))
		self.sm.add_widget(NuevoProfe(name="NuevoProfe"))
		self.sm.add_widget(DisplayProfe(name="DisplayProfe"))
		self.sm.add_widget(VerNotasProfe(name="VerNotasProfe"))
		self.sm.add_widget(DisplayNotasProfe(name="DisplayNotasProfe"))
		self.sm.add_widget(VerNotasEstudiante(name="VerNotasEstudiante"))
		self.sm.add_widget(DisplayNotasEstudiante(name="DisplayNotasEstudiante"))
		self.sm.add_widget(InputEstudiante(name="InputEstudiante"))
		self.sm.add_widget(Rubros(name="Rubros"))
		self.sm.add_widget(CalificarA(name="CalificarA"))
		self.sm.add_widget(CalificarP(name="CalificarP"))
		self.sm.add_widget(CalificarQ(name="CalificarQ"))
		self.sm.add_widget(CalificarC(name="CalificarC"))
		self.sm.add_widget(CalificarR(name="CalificarR"))
		self.sm.add_widget(AgregaEstudiante(name="AgregaEstudiante"))
		return self.sm

	def refresh(self):
		"""Función encargada de actualizar los datos mostrados en el RecycleView.

		Utiliza variables y triggers asignados con el módulo Clock para definir intérvalos de actualización por tiempos definidos, llamados por los botones de la aplicación cuando se realiza un cambio en el display.
		"""
		refreshP = Clock.schedule_interval(self.sm.get_screen('DisplayNotasProfe').update, 0.1)
		refreshE = Clock.schedule_interval(self.sm.get_screen('DisplayNotasEstudiante').update, 0.1)
		trigP = Clock.create_trigger(self.sm.get_screen('DisplayNotasProfe').update, 0.2)
		trigE = Clock.create_trigger(self.sm.get_screen('DisplayNotasEstudiante').update, 0.2)
		trigP()
		trigE()
		refreshP.cancel()
		refreshE.cancel()

	def addCam(self, pantalla):
		"""Función que agrega el widget zbarcam de MyApp a una pantalla.
		"""
		self.sm.get_screen(pantalla).add_widget(self.zbarcam)

	def rmCam(self, pantalla):
		"""Función que elimina el widget zbarcam de MyApp de una pantalla.
		"""
		self.sm.get_screen(pantalla).remove_widget(self.zbarcam)
			

if __name__ == '__main__':
	MyApp().run()
