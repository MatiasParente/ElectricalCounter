from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import paho.mqtt.client as mqtt
from kivy.core.window import Window 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import MySQLdb
from pythonping import ping
from kivy.uix.popup import Popup
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from plyer import notification
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
from datetime import datetime
import matplotlib.pyplot as plt

client = mqtt.Client()

plt.style.use('ggplot')
x_data = []
y_data = []

figure = pyplot.figure()
line, = pyplot.plot_date(x_data, y_data, '-')


class Ui(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')
        Window.size = (720, 1190)
        self.client = mqtt.Client()
        return Ui()

    def Graficas(frame):
        x_data.append(datetime.now())
        y_data.append(randrange(0, 100))
        line.set_data(x_data, y_data)
        figure.gca().relim()
        figure.gca().autoscale_view()
        return line,

    animacion3 = FuncAnimation(figure, Graficas, interval=3000)
    pyplot.show()
        
       
   

    def button_action2(self, button_id):
        if button_id == 1:
            
            self.Graficas()

    
    
    
    
    
    
    
    
#==================================================================================== 

# Pagina Controles

    def publish_mqtt_message(self, message):
        self.client.connect("192.168.169.2", 1883, 1)
        self.client.publish("controlar_reles", message)
        
    
    def switch_changed_1(self, active):
        if active:
            print("Switch 1 encendido")
            self.publish_mqtt_message("1**")
            notification.notify(
            title="Switch 1",
            message="Switch 1 encendido"
            )
        else:
            print("Switch 1 apagado")
            self.publish_mqtt_message("0**")
            notification.notify(
            title="Switch 1",
            message="Switch 1 apagado"
            )

    def switch_changed_2(self, active):
        if active:
            print("Switch 2 encendido")
            self.publish_mqtt_message("*1*")
            notification.notify(
            title="Switch 2",
            message="Switch 2 encendido"
            )
        else:
            print("Switch 2 apagado")
            self.publish_mqtt_message("*0*")
            notification.notify(
            title="Switch 2",
            message="Switch 2 apagado"
            )
    def switch_changed_3(self, active):
        if active:
            print("Switch 3 encendido")
            self.publish_mqtt_message("**1")
            notification.notify(
            title="Switch 3",
            message="Switch 3 encendido"
            )
        else:
            print("Switch 3 apagado")
            self.publish_mqtt_message("**0")
            notification.notify(
            title="Switch 3",
            message="Switch 3 apagado"
            )

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
        if button_id == 1:
            # Realizar ping al 192.168.169.74
            response = ping('192.168.169.74', count=2)
            if response.success():
                self.show_message("Ping exitoso", "El dispositivo responde.")
                notification.notify(
                title="Conexion con el dispositivo",
                message="El dispositivo esta conectado"
                )
            else:
                self.show_message("Ping fallido", "El dispositivo no responde.")
                notification.notify(
                title="Conexion con el dispositivo",
                message="El dispositivo no esta conectado"
                )

        elif button_id == 2:
            # Realizar ping al 192.168.169.2
            response = ping('192.168.169.2', count=2)
            if response.success():
                self.show_message("Ping exitoso", "El servidor responde.")
                notification.notify(
                title="Conexion con el servidor",
                message="El servidor esta conectado"
                )
            else:
                self.show_message("Ping fallido", "El servidor no responde.")
                notification.notify(
                title="Conexion con el servidor",
                message="El servidor no esta conectado"
                )

        elif button_id == 3:
            print("Botón 'Datos Generales' presionado")
            # Intenta conectar a MySQL
            connection = None
            try:
                connection = None
                connection = MySQLdb.connect(
                    host='192.168.169.52',
                    user='aplicacion',
                    password='Qwerty123#',
                    db='Proyecto'
                )
                print("Conexión exitosa a MySQL")
                # Crear un cursor para interactuar con la base de datos
                cursor = connection.cursor()
                # Ejecutar una consulta SELECT
                cursor.execute("SELECT * FROM Dato")
                # Obtener todos los resultados de la consulta
                resultados = cursor.fetchall()
                # Crear una cadena de texto con los resultados
                data_text = ""
                for fila in resultados:
                    data_text += str(fila) + "\n"
                    # Llamar a la función para mostrar la ventana emergente con los datos
                self.show_data_popup(data_text)
                    
            except Exception as e:
                print("Error al conectar a MySQL:", e)
            finally:
                if connection is not None:
                    # Cerrar el cursor y la conexión si se estableció correctamente
                    cursor.close()
                    connection.close()
            
#====================================================================================
if __name__ == "__main__":
    MainApp().run()
