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
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class Consejos(Screen):
    def __init__(self, **kwargs):
        super(Consejos, self).__init__(**kwargs)
        self.current_kwh_value = 0  # Inicializa con un valor predeterminado

        # Configura el temporizador para verificar el consumo cada 60 segundos
        Clock.schedule_interval(self.check_energy_consumption, 60)

    def get_current_kwh_value(self):
        try:
            # Establece la conexión a tu base de datos MySQL
            connection = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                db='Proyecto'
            )

            if connection:
                cursor = connection.cursor()

                # Ejecuta una consulta SQL para obtener el valor actual de kWh
                cursor.execute("SELECT valor_kwh FROM tu_tabla ORDER BY fecha DESC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    # Si se obtiene un resultado, toma el valor de kWh
                    current_kwh = result[0]
                    return current_kwh
                else:
                    # No se encontraron resultados, puedes devolver un valor predeterminado
                    return 0.0

        except Exception as e:
            print("Error al obtener el valor de kWh:", e)
            return 0.0
        finally:
            cursor.close()
            connection.close()

        return 0.0  # En caso de error

    def check_energy_consumption(self, dt):
        # Obtener el valor actual de kWh
        self.current_kwh_value = self.get_current_kwh_value()

        # Verificar el consumo de energía y mostrar consejos
        if self.current_kwh_value > 100:
            message = "El consumo de energía es elevado. ¡Debes tomar medidas!"
        else:
            message = "El consumo de energía es normal."

        self.show_message("Consumo de Energía", message)

    def show_message(self, title, text):
        # Implementa la lógica real para mostrar un mensaje
        # Puedes utilizar widgets como MDDialog para mostrar el mensaje en la aplicación.
        pass