from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import paho.mqtt.client as mqtt
from kivy.core.window import Window 
from kivy.uix.label import Label
import MySQLdb
from pythonping import ping
from kivy.uix.popup import Popup
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from plyer import notification
from datetime import datetime


client = mqtt.Client()
Kwh = []
Precio_Plan = []
ConsumoM =[]
notificaciones1 = 0
num_notificacion = 1

class Ui(Screen):
    pass

class Controles(Screen):
    pass

class Graficas(Screen):
    pass

class Usuario(Screen):
    pass

class Consejos(Screen):
    pass

class Notificaciones(Screen):
    pass

class Servicios(Screen):
    pass

class MainApp(MDApp):
    

    def build(self, *args):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')
        #Window.size = (720 , 1190)
        self.client = mqtt.Client()
        self.ConsumoD = 0 
        self.ConsumoM = [] 
        Clock.schedule_once(self.actualizar_variable, 0) 
        self.notificaciones1 = 0
        self.num_notificacion = 1
        
       
        sm = ScreenManager()
        
            
            # Agrega tus pantallas al ScreenManager
        sm.add_widget(Ui(name='Screen_Menu'))
        sm.add_widget(Controles(name='screen1'))
        sm.add_widget(Graficas(name='screen2'))
        sm.add_widget(Usuario(name='screen3'))
        sm.add_widget(Consejos(name='screen4'))
        sm.add_widget(Notificaciones(name='screen5'))
        sm.add_widget(Servicios(name='screen6'))
 



        
            
        return sm
        
    
    
    def Conexion_mysql(self):
        connection = None
        try:
            connection = MySQLdb.connect(
                host='192.168.175.52',
                user='aplicacion',
                password='Qwerty123#',
                db='Proyecto'
            )
            print("Conexión exitosa a MySQL")
            return connection
        except Exception as e:
            print("Error al conectar a MySQL:", e)
            return None
        
#=========================================================================================================
        
#==========================================================================================================
#Menu
        
    def Select_Datos_Consumo(self):
        connection = self.Conexion_mysql()
        Kwh, Precio_Plan = [], []
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Dato.Kwh, Plan_UTE.PrecioP FROM Dato, Plan_UTE where UsuarioDispo = '3';")
                resultados = cursor.fetchall()
                for fila in resultados:
                    Kwh.append(fila[-1])
                    Precio_Plan.append(fila[1])
                    print(Kwh)
                    print(Precio_Plan)
            except Exception as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                cursor.close()
                connection.close()
        return Kwh, Precio_Plan


    def actualizar_variable(self, *args):
        
        try:
            Kwh, Precio_Plan = self.Select_Datos_Consumo()
            self.ConsumoD += sum(Kwh)
            PrecioD = Kwh[-1] * Precio_Plan[-1]
            self.ConsumoM.append(sum(Kwh))  # Modifica esta línea
            

            self.root.get_screen('Screen_Menu').ids.Consumo_dia.text = f"Consumo Kwh/Día: {self.ConsumoD}"
            self.root.get_screen('Screen_Menu').ids.Precio_dia.text = f"Precio Kwh/Día: {PrecioD}"
            self.root.get_screen('Screen_Menu').ids.Consumo_mes.text = f"Consumo Kwh/Mes: {sum(self.ConsumoM)}"
            self.root.get_screen('Screen_Menu').ids.Precio_mes.text = f"Precio Kwh/Mes: {sum(self.ConsumoM) * Precio_Plan[-1]}"
        except Exception as e:
                print("Error al ejecutar la consulta:", e)

    def on_start(self):
        Clock.schedule_interval(self.actualizar_variable, 3600)

    def on_start_Mes(self):
        Clock.schedule_interval(self.actualizar_consumoM, 86400)

    def actualizar_consumoM(self, *args):
        self.ConsumoM += sum(self.ConsumoD)
    
    def on_start_Limpiar_consumoM(self):
        Clock.schedule_interval(self.Limpiar_consumoM, 2,592,000)
        
    def on_start_Limpiar_consumoD(self):
        Clock.schedule_interval(self.Limpiar_consumoD, 86400)
        
    def Limpiar_consumoM(self, *args):
        self.ConsumoM = []  # Limpiar la lista, no asignar una nueva
        print("Consumo Mensual limpiado")

    def Limpiar_consumoD(self, *args):
        self.ConsumoD = 0  # Limpiar el valor, no asignar una nueva lista
        print("Consumo Diario limpiado")
    
    
    def button_action_Controles(self, button_id):
        if button_id == 1:
            self.root.current = 'screen1'
    
   
            
    def button_action_Consejos(self, button_id):
        if button_id == 1:
            self.root.current = 'screen4'
    
    def button_action_Notificaciones(self, button_id):
        if button_id == 1:
            self.root.current = 'screen5'
    
    def button_action_Servicios(self, button_id):
        if button_id == 1:
            self.root.current = 'screen6'
            
    def button_action_Regresar(self, button_id):
        if button_id == 1:
            self.root.current = 'Screen_Menu'
        
#=====================================================================================
# Pagina Graficas

    def actualizar_grafica(self,data):
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        precios_uruguayos = [1, 2, 3, 2.5, 1.8]  # Precio en pesos uruguayos
        watts = [100, 150, 120, 180, 200]  # Consumo en watts

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
        plt.suptitle('Gráfica del Dispositivo', fontsize=32, y=0.98)
        ax1.bar(dias_semana, precios_uruguayos, color='blue')
        ax1.set_title('Precio en Pesos Uruguayos por Día de la Semana')
        ax1.set_xlabel('Día de la Semana')
        ax1.set_ylabel('Precio (en pesos uruguayos)')

        ax2.bar(dias_semana, watts, color='green')
        ax2.set_title('Consumo en Watts por Día de la Semana')
        ax2.set_xlabel('Día de la Semana')
        ax2.set_ylabel('Consumo (en watts)')

        manager = plt.get_current_fig_manager()
        manager.toolbar.pack_forget()

        plt.tight_layout()
        plt.show()

    
    def button_action_Graficas(self, button_id):
        if button_id == 1:
            self.actualizar_grafica(data=1)
            
#===================================================
    
    def clear_notifications(self):
        self.root.get_screen('screen5').ids.Notificacion1.text = " "
        self.root.get_screen('screen5').ids.Notificacion11.text = " "
        self.root.get_screen('screen5').ids.Notificacion111.text = " "
        self.root.get_screen('screen5').ids.Notificacion2.text = " "
        self.root.get_screen('screen5').ids.Notificacion22.text = "Usted no tiene notificaciones"
        self.root.get_screen('screen5').ids.Notificacion222.text = " "
        self.root.get_screen('screen5').ids.Notificacion3.text = " "
        self.root.get_screen('screen5').ids.Notificacion33.text = " "
        self.notificaciones1 = 0     
        self.num_notificacion = 1  

        
    
#==================================================================================== 

# Pagina Controles

    def publish_mqtt_message(self, message):
        self.client.connect("192.168.175.52", 1883, 1)
        self.client.publish("controlar_reles", message)
        
    
    def switch_changed_1(self, active):
        try:
            if active:
                print("Switch 1 encendido")
                self.publish_mqtt_message("1**")
            else:
                print("Switch 1 apagado")
                self.publish_mqtt_message("0**")
        except Exception as e:
            print("Error al publicar:", e)


    def switch_changed_2(self, active):
        try:
            if active:
                print("Switch 2 encendido")
                self.publish_mqtt_message("*1*")
            else:
                print("Switch 2 apagado")
                self.publish_mqtt_message("*0*")
        except Exception as e:
            print("Error al publicar:", e)

    def switch_changed_3(self, active):
        try:
            if active:
                print("Switch 3 encendido")
                self.publish_mqtt_message("**1")
            else:
                print("Switch 3 apagado")
                self.publish_mqtt_message("**0")
        except Exception as e:
            print("Error al publicar:", e)
            
    def start(self):
        self.client.loop_start()

#====================================================================================

# Pagina Dispocitibos

    
    def show_data_popup(self, data):
        scroll_view = MDScrollView()
        content = Label(text=data)  
        content.bind(size=content.setter('text_size'))  
        scroll_view.add_widget(content)

        popup = Popup(title="Datos de la consulta SELECT", content=scroll_view, size_hint=(None, None), size=(720, 1000))
        popup.open()
         
    def show_message(self, title, text):
        from kivymd.toast import toast
        toast(text)

    def button_action(self, button_id):
        # Obtén la fecha y hora actual
        current_time = datetime.now()

        # Formatea la fecha y hora para mostrar solo el día, la hora y los minutos
        formatted_time = current_time.strftime("%m-%d %H:%M")
        if button_id == 1:
            # Realizar ping al 192.168.169.74
            response = ping('192.168.175.74', count=2)
            if response.success():
                self.show_message("Ping exitoso", "El dispositivo responde.")
                notification.notify(
                    title="Conexión con el dispositivo",
                    message="El dispositivo esta conectado"
                    )
                if self.notificaciones1 == 0:
                    self.root.get_screen('screen5').ids.Notificacion22.text = " "
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                    self.num_notificacion = self.num_notificacion + 1
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1
            else:
                self.show_message("Ping fallido", "El dispositivo no responde.")
                notification.notify(
                    title="Conexión con el dispositivo",
                    message="El dispositivo no esta conectado"
                    )
                if self.notificaciones1 == 0:
                    self.root.get_screen('screen5').ids.Notificacion22.text = " "
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El dispostivo no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El dispostivo no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El dispostivo no esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                    self.num_notificacion = self.num_notificacion + 1
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1

        elif button_id == 2:
            # Realizar ping al 192.168.169.2
            response = ping('192.168.175.52', count=2)
            if response.success():
                self.show_message("Ping exitoso", "El servidor responde.")
                notification.notify(
                    title="Conexión con el servidor",
                    message="El servidor esta conectado"
                    )
                if self.notificaciones1 == 0:
                    self.root.get_screen('screen5').ids.Notificacion22.text = " "
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                    self.num_notificacion = self.num_notificacion + 1
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1
            else:
                self.show_message("Ping fallido", "El servidor no responde.")
                notification.notify(
                    title="Conexión con el servidor",
                    message="El servidor no esta conectado"
                    )
                if self.notificaciones1 == 0:
                    self.root.get_screen('screen5').ids.Notificacion22.text = " "
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                    self.num_notificacion = self.num_notificacion + 1
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                    self.num_notificacion = self.num_notificacion + 1
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
                    self.num_notificacion = self.num_notificacion + 1

        elif button_id == 3:
            print("Botón 'Datos Generales' presionado")
            # Intenta conectar a MySQL
            connection = self.Conexion_mysql()
            if connection is not None:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT Kwh ,Fecha ,Reles1, Reles2, Reles3 FROM Dato where UsuarioDispo = '3';")
                    # Obtener todos los resultados de la consulta
                    resultados = cursor.fetchall()
                    # Crear una cadena de texto con los resultados
                    data_text = ""
                    for fila in resultados:
                        data_text += str(fila) + "\n"
                    # Llamar a la función para mostrar la ventana emergente con los datos
                    self.show_data_popup(data_text)
                except Exception as e:
                    print("Error al ejecutar la consulta:", e)
                finally:
                    # Cerrar el cursor
                    cursor.close()
                    # Cerrar la conexión
                    connection.close()






#====================================================================================
#Pagina Usuario

    def button_action_datosUsuario(self, button_id):
        if button_id == 1:
            self.Select_Datos_Usuarios()
            NombreU, CorreoU, DispoU, NombrePU = self.Select_Datos_Usuarios()
            self.actualizar_variable_Usuario(NombreU, CorreoU, DispoU, NombrePU)
            self.root.current = 'screen3'

    def Select_Datos_Usuarios(self):
        NombreU=[]
        CorreoU=[]
        DispoU=[]
        NombrePU=[]
        connection = self.Conexion_mysql()
        if connection is not None:
            print("Conexión a MySQL establecida correctamente.")
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Usuario.NombreUsuario, Usuario.Correo, Dato.UsuarioDispo, Plan_UTE.NombreP FROM Dato INNER JOIN Usuario ON Dato.NumDatoDispo = Usuario.CodigoUsuario INNER JOIN Plan_UTE ON Dato.NumDatoDispo = Plan_UTE.codigoP WHERE Plan_UTE.CodigoP = 3;")
                resultados = cursor.fetchall()
                for fila in resultados:
                    NombreU.append(fila[0])
                    CorreoU.append(fila[1])
                    DispoU.append(fila[2])
                    NombrePU.append(fila[3])
                    


            except Exception as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                cursor.close()
                connection.close()
                print("NombreU:", NombreU)
                print("CorreoU:", CorreoU)
                print("DispoU:", DispoU)
                print("NombrePU:", NombrePU)
        return NombreU, CorreoU, DispoU, NombrePU,


    def actualizar_variable_Usuario(self,  NombreU, CorreoU, DispoU, NombrePU):
        if NombreU and CorreoU and DispoU and NombrePU:

            self.root.get_screen('screen3').ids.Usuario.text = f"  Usuario : {NombreU[-1]}"
            self.root.get_screen('screen3').ids.Plan_UTE.text = f"      Plan de UTE : {NombrePU[-1]}"
            self.root.get_screen('screen3').ids.CorreoE.text = f"      Correo electronico : {CorreoU[-1]}"
            self.root.get_screen('screen3').ids.NuemeroD.text = f"      Numero de dispocitivo :{DispoU[-1]}"


if __name__ == "__main__":
    MainApp().run()


