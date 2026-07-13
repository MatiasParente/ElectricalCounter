from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
import os
import mysql.connector
from kivy.uix.screenmanager import ScreenManager



KV = '''
ScreenManager:

    LoginScreen:
    RegisterScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: [20, 0]

        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'  # Centro verticalmente
            MDIcon:
                icon: 'account'
                icon_color: 0, 0, 0, 0
                halign: 'center'
                font_size: 250

        MDCard:
            size_hint: None, None
            size: 220, 400  # Ajustar la altura de la tarjeta
            pos_hint: {"center_x": 0.5}
            elevation: 0
            GridLayout:
                cols: 1
                spacing: 10
                padding: [20, 20]

                MDTextField:
                    id: user
                    icon_left: "account-check"
                    hint_text: "Username"
                    foreground_color: 1, 0, 1, 1
                    size_hint_x: None
                    width: 180
                    font_size: 20
                    pos_hint: {"center_x": 0.5}

                MDTextField:
                    id: password
                    icon_left: "key-variant"
                    hint_text: "Password"
                    foreground_color: 1, 0, 1, 1
                    size_hint_x: None
                    width: 180
                    font_size: 20
                    pos_hint: {"center_x": 0.5}
                    password: True  # Mostrar la contraseña con viñetas

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint_x: None
                    width: 180
                    pos_hint: {"center_x": 0.5}
                    size_hint_y: None
                    height: self.minimum_height

                    MDRaisedButton:
                        text: "Registrarse"
                        font_size: 15
                        on_release: root.manager.current = 'register'

                    MDRaisedButton:
                        text: "Ingresar"  # Nuevo botón "Ingresar"
                        font_size: 15
                        on_release: app.login()  # Llamar a la función login en la aplicación

<RegisterScreen>:
    name: 'register'
    BoxLayout:
        orientation: 'vertical'
        padding: [20, 0]

        AnchorLayout:
            anchor_x: 'center'
            anchor_y: 'center'  # Centro verticalmente
            MDIcon:
                icon: 'account-plus'
                icon_color: 0, 0, 0, 0
                halign: 'center'
                font_size: 250

        MDCard:
            size_hint: None, None
            size: 220, 400 
            pos_hint: {"center_x": 0.5}
            elevation: 0
            GridLayout:
                cols: 1
                spacing: 10
                padding: [20, 20]

                MDTextField:
                    id: register_user
                    icon_left: "account-check"
                    hint_text: "Username"
                    foreground_color: 1, 0, 1, 1
                    size_hint_x: None
                    width: 180
                    font_size: 20
                    pos_hint: {"center_x": 0.5}

                MDTextField:
                    id: register_email
                    icon_left: "email"
                    hint_text: "Email"
                    foreground_color: 1, 0, 1, 1
                    size_hint_x: None
                    width: 180
                    font_size: 20
                    pos_hint: {"center_x": 0.5}

                MDTextField:
                    id: register_password
                    icon_left: "key-variant"
                    hint_text: "Password"
                    foreground_color: 1, 0, 1, 1
                    size_hint_x: None
                    width: 180
                    font_size: 20
                    pos_hint: {"center_x": 0.5}
                    password: True  

                MDDropDownItem:
                    id: ute_dropdown
                    pos_hint: {"center_x": 0.5}
                    width: 180
                    dropdown_cls: "MyDropdown"
                    text: "Plan de UTE"
                    on_release: app.show_ute_menu(self)

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint_x: None
                    width: 180
                    pos_hint: {"center_x": 0.5}
                    size_hint_y: None
                    height: self.minimum_height

                    MDRaisedButton:
                        text: "Registrarse"
                        font_size: 15
                        on_release: app.register()

                    MDRaisedButton:
                        text: "Volver"
                        font_size: 15
                        on_release: root.manager.current = 'login'
'''

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class LoginApp(MDApp):
    selected_ute_option = ""  # Variable para almacenar la opción seleccionada
    dialog = None
    plan_ute_mapping = {
        "Opción 1": 1,
        "Opción 2": 2,
        "Opción 3": 3,
    }

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.accent_palette = 'Green'
        return Builder.load_string(KV)

    def login(self):
        username = self.root.current_screen.ids.user.text
        password = self.root.current_screen.ids.password.text

        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                database="ec"
            )
            cursor = conn.cursor()

            # Consulta SQL para verificar si el usuario y la contraseña coinciden
            select_query = "SELECT * FROM Usuario WHERE Usuario = %s AND Contrasenia = %s"
            cursor.execute(select_query, (username, password))
            user_data = cursor.fetchone()  # Obtener el primer resultado

            if user_data:
                # Usuario y contraseña válidos, permitir el acceso
                print(f"Bienvenido, {username}!")
                
             

            else:
                # Usuario o contraseña incorrectos, mostrar un mensaje de error
                self.show_message("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")

            # Cerrar la conexión
            cursor.close()
            conn.close()

        except Exception as e:
            print("Error de inicio de sesión:", str(e))
            self.show_message("Error", "Ocurrió un error al iniciar sesión.")

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
        # Plan de UTE: self.selected_ute_option

        print(f"Nombre: {name}, Email: {email}, Password: {password}, Plan de UTE: {self.selected_ute_option}")

  
        selected_option = self.selected_ute_option  # Obtiene la opción seleccionada del menú

        # Obtén el valor correspondiente a la opción seleccionada
        plan_ute = self.plan_ute_mapping.get(selected_option, None)

        if plan_ute is None:
            self.show_message("Error", "Opción de UTE no válida.")
            return

        # Realizar la inserción en la base de datos
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                database="ec"
            )
            cursor = conn.cursor()

            # Insertar el nuevo usuario en la tabla Usuario
            insert_query = "INSERT INTO Usuario (Contrasenia, Correo, Usuario, numP) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (password, email, name, plan_ute))
            conn.commit()

            # Cerrar la conexión
            cursor.close()
            conn.close()

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

if __name__ == "__main__":
    LoginApp().run()

