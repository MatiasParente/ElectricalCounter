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
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivymd.uix.textfield import MDTextField
from kivy.uix.label import Label
import random
from plyer import notification
from datetime import datetime, timedelta
import subprocess
import os

client = mqtt.Client()
Kwh = []
Precio_Plan = []
ConsumoM =[]
notificaciones1 = 0
num_notificacion = 0

class LoginScreen(Screen):
    pass

class Ui(Screen):
    pass

class RegisterScreen(Screen):
    pass


class Controles(Screen):
    pass

class Graficas(Screen):
    pass

class Usuario(Screen):
    pass



class Consejos(Screen):

    def __init__(self, **kwargs):
        super(Consejos, self).__init__(**kwargs)
        main_app = App.get_running_app()
        self.conexion = main_app.Conexion_mysql()

    def obtener_consejos(self, username):
        main_app = App.get_running_app()
        self.check_energy_consumption(username)

    

   
            
    

class Notificaciones(Screen):
    pass

class Servicios(Screen):
    pass

class MainApp(MDApp):
    
    selected_ute_option = ""  # Variable para almacenar la opción seleccionada
    dialog = None
    plan_ute_mapping = {
        "Opción 1": 1,
        "Opción 2": 2,
        "Opción 3": 3,
    }

    def build(self, *args):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')
        #Window.size = (720 , 1190)
        self.client = mqtt.Client()
        self.ConsumoD = 0 
        self.ConsumoM = [] 
        self.notificaciones1 = 0
        self.num_notificacion = 0
        Clock.schedule_once(self.actualizar_variable, 0) 

        
   
       
        sm = ScreenManager()
        
            
            # Agrega tus pantallas al ScreenManager
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(Ui(name='Screen_Menu'))
        sm.add_widget(Controles(name='screen1'))
        sm.add_widget(Graficas(name='screen2'))
        sm.add_widget(Usuario(name='screen3'))
        sm.add_widget(Consejos(name='screen4'))
        sm.add_widget(Notificaciones(name='screen5'))
        sm.add_widget(Servicios(name='screen6'))
 



        
            
        return Ui()
        
    
    def on_enter(self):
        self.obtener_consejos()

    def get_current_kwh_value(self, username):
        main_app = App.get_running_app()
        connection = main_app.Conexion_mysql()
        if connection is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return 0.0

        try:
            cursor = connection.cursor()

            # Consulta SQL para obtener el valor de kWh específico para el usuario
            select_query = "SELECT Kwh FROM Dato WHERE UsuarioDispo = (SELECT CodigoUsuario FROM Usuario WHERE NombreUsuario = %s)"
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()

            if result:
                current_kwh = result[0]
                print(f"Valor actual de kWh para {username}: {current_kwh}")
                return current_kwh
            else:
                return 0.0

        except Exception as e:
            print("Error al obtener el valor de kWh:", e)
            return 0.0
        finally:
            cursor.close()

    def get_number_of_people(self, username):
        main_app = App.get_running_app()
        connection = main_app.Conexion_mysql()

        if connection is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return 1  # Valor predeterminado si la conexión falla

        try:
            cursor = connection.cursor()

            # Consulta SQL para obtener la cantidad de personas específica para el usuario
            select_query = "SELECT Personas FROM Usuario WHERE NombreUsuario = %s"
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()

            if result:
                total_personas = result[0]
                print(f"Total de personas para {username}: {total_personas}")
                return total_personas
            else:
                return 1  # Valor predeterminado si no se encuentra ningún resultado

        except Exception as e:
            print("Error al obtener el número de personas:", e)
            return 1  # Valor predeterminado en caso de error
        finally:
            cursor.close()


    def check_energy_consumption(self, username):
        print("Función check_energy_consumption se está ejecutando")
        # Obtén la fecha y hora actual
        current_time = datetime.now()

        # Formatea la fecha y hora para mostrar solo el día, la hora y los minutos
        formatted_time = current_time.strftime("%m-%d %H:%M")
        self.num_notificacion = self.num_notificacion + 1
        kwh = self.get_current_kwh_value(username)
        personas = self.get_number_of_people(username)

        # Accede directamente a los widgets MDLabel
        consejos_label = self.root.get_screen('screen4').ids.consejos_label
        consejos_label2 = self.root.get_screen('screen4').ids.consejos_label2

        consejos = [
            'Las bombillas LED consumen significativamente menos energía que las bombillas incandescentes y duran mucho más tiempo.',
            'Muchos dispositivos continúan consumiendo energía cuando están en stand by. Utiliza la función "Controles" de la aplicación para cortar la corriente a los dispositivos de tu hogar a distancia.',
            'Utiliza la aplicación para ver los datos de consumo eléctrico en tu hogar para realizar un seguimiento de tu consumo y hacer ajustes según sea necesario.'
        ]

        if kwh >= personas:
            print("El consumo de energía es elevado. ¡Debes tomar medidas!")
            mensaje = "El consumo de energía es elevado. ¡Debes tomar medidas!."
            mensaje2 = random.choice(consejos)
            notification.notify(
                    title="Notificación de consejos",
                    message="El consumo de energía es elevado. ¡Debes tomar medidas!"
                    )
            if self.notificaciones1 == 0:
                self.root.get_screen('screen5').ids.Notificacion22.text = " "
                self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Nofificación de consejos"
                self.root.get_screen('screen5').ids.Notificacion11.text = f"El consumo de energía es elevado. ¡Debes tomar medidas!, notificacion realizada el {formatted_time}"
                self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                self.notificaciones1 = 1
            elif self.notificaciones1 == 1:
                self.root.get_screen('screen5').ids.Notificacion2.text = f"    {self.num_notificacion}. Nofificación de consejos"
                self.root.get_screen('screen5').ids.Notificacion22.text = f"El consumo de energía es elevado. ¡Debes tomar medidas!, notificacion realizada el {formatted_time}"
                self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                self.notificaciones1 = 2
            elif self.notificaciones1 == 2:
                self.root.get_screen('screen5').ids.Notificacion3.text = f"    {self.num_notificacion}. Nofificación de consejos"
                self.root.get_screen('screen5').ids.Notificacion33.text = f"El consumo de energía es elevado. ¡Debes tomar medidas!, notificacion realizada el {formatted_time}"
                self.notificaciones1 = 3
            else:
                self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Nofificación de consejos"
                self.root.get_screen('screen5').ids.Notificacion11.text = f"El consumo de energía es elevado. ¡Debes tomar medidas!, notificacion realizada el {formatted_time}"
                self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                self.notificaciones1 = 1
        else:
            mensaje = "El consumo de energía es normal."
            mensaje2 = ""

        consejos_label.text = mensaje
        consejos_label2.text = mensaje2

        print(mensaje)
    
    def Conexion_mysql(self):
        connection = None
        try:
            connection = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                db='Proyecto4'
            )
            print("Conexión exitosa a MySQL")
            return connection
        except Exception as e:
            print("Error al conectar a MySQL:", e)
            return None
        
#=========================================================================================================
#Login Registrar

    def login(self):
        username = self.root.get_screen('login').ids.user.text
        password = self.root.get_screen('login').ids.password.text
        connection = self.Conexion_mysql()
        try:
            cursor = connection.cursor()

            # Consulta SQL para verificar si el usuario y la contraseña coinciden
            select_query = "SELECT * FROM Usuario WHERE NombreUsuario = %s AND Contrasenia = %s"
            cursor.execute(select_query, (username, password))
            user_data = cursor.fetchone()  # Obtener el primer resultado

            if user_data:
                # Usuario y contraseña válidos, permitir el acceso
                print(f"Bienvenido, {username}!")
                self.check_energy_consumption(username)  # Pasar el 'username' como argumento
                self.current_username = username
                self.root.current = 'Screen_Menu'

            else:
                # Usuario o contraseña incorrectos, mostrar un mensaje de error
                self.show_message("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos")

            # Cerrar la conexión
            cursor.close()
            connection.close()

        except Exception as e:
            print("Error de inicio de sesión:", str(e))
            self.show_message("Error", "Ocurrió un error al iniciar sesión")

    def show_ute_menu(self, button):
        menu_items = [{"viewclass": "OneLineListItem", "text": "Opción 1"}, {"viewclass": "OneLineListItem", "text": "Opción 2"}, {"viewclass": "OneLineListItem", "text": "Opción 3"}]

        self.ute_menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=4,
        )

        # Enlazar la función de selección de opción al evento on_release del DropDownItem
        for item in menu_items:
            item["on_release"] = lambda x=item: self.ute_option_selected(x["text"])

        self.ute_menu.open()

    def ute_option_selected(self, option):
        # Almacenar la opción seleccionada y actualizar el texto del MDDropDownItem
        self.selected_ute_option = option
        self.root.current_screen.ids.ute_dropdown.text = option

    def register(self):
        # Recopila la información de registro aquí y realiza las acciones necesarias
        name = self.root.get_screen('register').ids.register_user.text
        email = self.root.get_screen('register').ids.register_email.text
        password = self.root.get_screen('register').ids.register_password.text
        personas = self.root.get_screen('register').ids.register_personas.text
        # Plan de UTE: self.selected_ute_option

        print(f"Nombre: {name}, Email: {email}, Password: {password}, Plan de UTE: {self.selected_ute_option}, Personas: {personas}")

  
        selected_option = self.selected_ute_option  # Obtiene la opción seleccionada del menú

        # Obtén el valor correspondiente a la opción seleccionada
        plan_ute = self.plan_ute_mapping.get(selected_option, None)

        if plan_ute is None:
            self.show_message("Error", "Opción de UTE no válida.")
            return

        # Realizar la inserción en la base de datos
        connection = self.Conexion_mysql()
        try:
            cursor = connection.cursor()

            # Insertar el nuevo usuario en la tabla Usuario
            insert_query = "INSERT INTO Usuario (Contrasenia, Correo, NombreUsuario, PlanUteID, Personas) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (password, email, name, plan_ute, personas))
            connection.commit()

            # Cerrar la conexión
            cursor.close()
            connection.close()

            # Mostrar un mensaje de éxito
            self.show_message("Registro exitoso", "El usuario ha sido registrado exitosamente.")

        except Exception as e:
            print("Error al registrar el usuario:", str(e))
            self.show_message("Error", "Ocurrió un error al registrar el usuario.")


    def show_message(self, title, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ]
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()
        self.dialog = None
        
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
            self.check_energy_consumption(self.current_username)
    
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
# Paginas graficas 
    def button_action_Graficas(self, button_id):
       if button_id == 1:
            script_path = os.path.join(os.path.dirname(__file__), "graficoBarras.py")
            subprocess.Popen(["python", script_path])
    
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

# Pagina Dispositivos

    
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
        self.num_notificacion = self.num_notificacion + 1
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
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
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
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El dispostivo no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El dispostivo no esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"     {self.num_notificacion}. Conexión con el dispositivo"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El dispostivo esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1

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
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El servidor esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1
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
                elif self.notificaciones1 == 1:
                    self.root.get_screen('screen5').ids.Notificacion2.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion22.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion222.text = "_______________________________________________________"
                    self.notificaciones1 = 2
                elif self.notificaciones1 == 2:
                    self.root.get_screen('screen5').ids.Notificacion3.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion33.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.notificaciones1 = 3
                else:
                    self.root.get_screen('screen5').ids.Notificacion1.text = f"    {self.num_notificacion}. Conexión con el servidor"
                    self.root.get_screen('screen5').ids.Notificacion11.text = f"El servidor no esta conectado, prueba realizada el {formatted_time}"
                    self.root.get_screen('screen5').ids.Notificacion111.text = "_______________________________________________________"
                    self.notificaciones1 = 1

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


#====================================================================================

#Pagina Notificaciones
     
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
        self.num_notificacion = 0  
  



   
if __name__ == "__main__":
    MainApp().run()


