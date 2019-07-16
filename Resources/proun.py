import crypt
import conexion2
import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial

salt = 'abcdefg'
arr = conexion2.getCategorias()



class pant1(ScreenManager):
    transition = FadeTransition()
    	
	
class LoginScreen(Screen):

#    def __init__(self, **kwargs):
 #       super(LoginScreen, self).__init__(**kwargs)

    def login22(self):
        
        tuser = self.ids.texto1.text
        tpass = self.ids.texto2.text
        
        if tuser != '' and tpass != '':

            if (conexion2.verificarUsuario(tuser)):
                
                tcpass = crypt.crypt(tpass, salt)
                gpass = conexion2.getClave(tuser)  #solicitar contrasena del user desde la base de datos
               
                if tcpass == gpass[0]:
                    print('acceso concedido')
        
                    self.changer()

                else:
                    Error=DatosErrorPop()
                    Error.open()
                    return False  

            else:
                Error=DatosErrorPop()
                Error.open()
                return False
        else:
            Lleno=TodoLlenoPop()
            Lleno.open()  
            return False

    def changer(self):
        self.manager.current = 'screen3'


class AccountScreen(Screen):
        
    def createe(self):
        nuser = self.ids.texto1.text
        npass = self.ids.texto2.text
        ncpass = self.ids.texto3.text
        email = self.ids.texto4.text
        existencia = conexion2.verificarUsuario(nuser)

        if(existencia == False):

            if (nuser != '' and npass != '' and ncpass != '' and email != '' ):
                if npass == ncpass:
                    nupass = crypt.crypt(npass, salt)
                    print(nupass)
                    conexion2.AgregarUsuario(nuser, nupass, email) #Agrega el usuario a la base de datos
                    Login=LoginPopup()
                    Login.open()
                    return 0
			
                else:
                    print('intente de nuevo')
                    Fclave=FalloClavePop()
                    Fclave.open()
                    return 1
            
            else:
                Lleno=TodoLlenoPop()
                Lleno.open()
        else:
            pops=SimplePopup()
            pops.open()        

#categoriaSelec = 'Carnes'
categoriaSelec = ''
#nombrePlato ='Camarones a la Parrilla'
nombrePlato ='Pollo'

class CateScreen(Screen):

    def __init__(self,**kwargs):
        super(CateScreen, self).__init__(**kwargs)
        self.add_widget(Conbox())


class ReceScreen(Screen):

    def __init__(self,catsel,**kwargs):
        super(ReceScreen, self).__init__(**kwargs)
        self.add_widget(Conju(catsel))


class Conbox(BoxLayout):

    def __init__(self,**kwargs):
        super(Conbox, self).__init__(**kwargs)
        self.add_widget(Wid_btns(arr))

class Conju(BoxLayout):
    def __init__(self,catsel,**kwargs):
        super(Conju, self).__init__(**kwargs)
        self.add_widget(Wirese(conexion2.getPlatos(catsel)))


class Wirese(BoxLayout):

    def __init__(self,arr):
        super(Wirese,self).__init__()
        btnn = Button(text="+",background_color=[1,1,.1,0.4], font_size= 0.16*self.height)
        argg = btnn.text
        btnn.bind(on_press = lambda btn: imppt()) #CAMBIAR A LA PANTALLA DE MOSTRAR RECETA
        self.add_widget(btnn)
        
        for i in arr:
            self.add_btn(i)


    def add_btn(self,arr,*arg):

        btnn = Button(text=arr,background_color=[1,1,1,0.4], font_size= 0.16*self.height)
        argg = btnn.text
        btnn.bind(on_press = lambda btn: imppr(argg)) #CAMBIAR A LA PANTALLA DE MOSTRAR RECETA
        self.add_widget(btnn)



class Wid_btns(BoxLayout):
	
	def __init__(self,arr):
		super(Wid_btns,self).__init__()
		for i in arr:
			self.add_btn(i)


	def add_btn(self,arr,*arg):

		btnn = Button(text=arr, background_color=[1,1,.1,0.4])
		argg = btnn.text
		btnn.bind(on_press = lambda btn:imppc(argg)) #CAMBIAR A LA PANTALLA RECESCREEN
		self.add_widget(btnn)
        

class Box01(Screen):


    def readText(self):
        nombre = self.ids.texto1.text
        ingredientes = self.ids.texto2.text
        procedimiento = self.ids.texto3.text
        porciones = self.ids.texto4.text
		
        if nombre != '' and ingredientes != '' and procedimiento != '' and porciones != '':
            conexion2.AgregarPlato(nombre, categoriaSelec,ingredientes,porciones,procedimiento)
            Login=LoginPopup()
            Login.open()
           
        else:
            Lleno=TodoLlenoPop()
            Lleno.open()  
            return False

class Box02(Screen):
	
	nombrePlato2 = "Pollo"
	tm1 = nombrePlato2
	tm2 = str(conexion2.getIngredientes(nombrePlato2))
	tm3 = str(conexion2.getPreparacion(nombrePlato2))
	tm4 = "5"
	#tm4 = conexion2.getPorciones(nombrePlato2)
	#nombrePlato2 = "Pollo"
	#tm1 = nombrePlato2
	#tm2 = conexion2.ProcesarDatos(conexion2.getIngredientes(nombrePlato2))
	#tm3 = conexion2.ProcesarDatos(conexion2.getPreparacion(nombrePlato2))
	#tm4 = conexion2.ProcesarDatos(conexion2.getPorciones(nombrePlato2))


	def writeText(self):
		nombrePlato2 = "Pollo"
		self.ids.textoM1.text = nombrePlato2
		self.ids.textoM2.text = conexion2.ProcesarDatos(getIngredientes(nombrePlato2))
		self.ids.textoM3.text = conexion2.ProcesarDatos(getPreparacion(nombrePlato2))
		self.ids.textoM4.text = conexion2.ProcesarDatos(getPorciones(nombrePlato2))




#FUNCION QUE CAMBIA DE PANTALLA

def imppc(argg, *arg):
    #categoriaSelec = argg
    #sm.current ='screen2'
    nascr = ''
    cont = 0
    for i in arr:
        if argg == i:
            nascr = 'screen2' + str(cont)
        cont = cont + 1
    sm.current = nascr
    return argg

def imppr(argg, *arg):
    nombrePlato = argg
    sm.current ='screen6'
    print(argg)
    
def imppt(*arg):
    sm.current ='screen5'


sm = ScreenManager()
	
class proun(App):
	
    title = "Recetario"
    def build(self):
        screen1 = LoginScreen(name='screen1')
        screen3 = CateScreen(name='screen3')
        screen4 = AccountScreen(name='screen4')
        screen5 = Box01(name='screen5') #Agregar
        screen6 = Box02(name='screen6') #Mostrar
        sm.add_widget(screen1)
        cont = 0
        arr22 = conexion2.getCategorias()
        for i in arr22:
            catsel = i
            nascr = 'screen2' + str(cont)
            rescreen = ReceScreen(catsel, name = nascr)
            cont = cont + 1
            sm.add_widget(rescreen)
        sm.add_widget(screen3)
        sm.add_widget(screen4)
        sm.add_widget(screen5)
        sm.add_widget(screen6)
        return sm
	


#### MENSAJES POPUP:

# Se imprime un mensaje si se creo bien la cuenta.
class LoginPopup(Popup):
    pass				
				                   
class LoginButton(Button):
    
    def Login(self):
        Login=LoginPopup()
        Login.open()

# Se imprime un mensaje de que el usuario existe.
class SimplePopup(Popup):
    pass				
				                   
class SimpleButton(Button):
    text = "Popup"
    def popup(self):
        pops=SimplePopup()
        pops.open()


# Se imprime un mensaje de que las claves no concuerdan.
class FalloClavePop(Popup):
    pass

class FalloClaveButton(Button):
    text = "Fire Popup !"
    def FalloClave(self):
        Fclave=FalloClavePop()
        Fclave.open()


# Se imprime un mensaje de que todos los espacios deben estar llenos.
class TodoLlenoPop(Popup):
    pass

class TodoLlenoButton(Button):
    text = "Fire !"
    def TodoLleno(self):
        Lleno=TodoLlenoPop()
        Lleno.open()

# Se imprime un mensaje cuando el usuario o la clave son incorrectos.
class DatosErrorPop(Popup):
    pass

class DatosErrorButton(Button):
    text = "Fi !"
    def DatosError(self):
        Error=DatosErrorPop()
        Error.open()



if __name__ == "__main__":
	proun().run()




