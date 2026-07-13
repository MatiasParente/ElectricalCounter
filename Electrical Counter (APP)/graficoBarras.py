# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:       graficoBarras.py

from PyQt5.QtChart import (QChart, QChartView, QBarCategoryAxis, QBarSeries, QBarSet,
                           QValueAxis, QAbstractBarSeries)
import MySQLdb
from datetime import datetime, timedelta
from PyQt5.QtGui import QFont, QIcon, QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt, QMargins, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QSizePolicy,
                             QGridLayout, QLabel, QColorDialog, QComboBox, QCheckBox,
                             QPushButton, QFileDialog, QMessageBox)
from plyer import notification
import main
import argparse 
notificaciones1 = 0
num_notificacion = 0
# ===================== CLASE graficoBarras ========================

class graficoBarras(QWidget):
    def __init__(self, parent=None):
        super(graficoBarras, self).__init__(parent)
        self.notificaciones1 = 0
        self.num_notificacion = 0
        self.initUI()

        

    def Conexion_mysql(self):
        connection = None
        try:
            connection = MySQLdb.connect(
                host='192.168.17.53',
                user='aplicacion',
                password ='Qwerty123#',
                db='Proyecto'
            )
            print("Conexión exitosa a MySQL")
            return connection
        except Exception as e:
            print("Error al conectar a MySQL:", e)
            return None

    def Select_Datos_Consumo(self, nombre_usuario):
        connection = self.Conexion_mysql()
        print(nombre_usuario)
        
        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()
    
    # Calcula la fecha de inicio de la semana actual (lunes)
        inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())
    
    # Calcula la fecha de final de la semana actual (domingo)
        final_semana = inicio_semana + timedelta(days=6)
    
        print("Fecha de inicio de la semana:", inicio_semana)
        print("Fecha de final de la semana:", final_semana)
        
        Kwh = [0, 0, 0, 0, 0, 0, 0]  # Inicializamos una lista con 7 ceros para cada día de la semana
        if connection is not None:
            try:
                cursor = connection.cursor()
                select_query = (
                "SELECT DATE(fecha), SUM(Kwh) FROM Dato "
                "WHERE UsuarioDispo = (SELECT CodigoUsuario FROM Usuario WHERE NombreUsuario = %s LIMIT 1) "
                "AND DATE(fecha) BETWEEN %s AND %s "  # Filtra por la semana actual
                "GROUP BY DATE(fecha);"
                )
                cursor.execute(select_query, (nombre_usuario, inicio_semana, final_semana))
                resultados = cursor.fetchall()
                for fila in resultados:
                    fecha = fila[0]  # Obtenemos la fecha
                    kwh_diario = fila[1]  # Obtenemos la suma de Kwh para esa fecha

                    # Obtén el número de día de la semana (0 = lunes, 1 = martes, ..., 6 = domingo)
                    dia_semana = fecha.weekday()

                    # Asigna el valor de la suma de Kwh al día correspondiente
                    Kwh[dia_semana] = kwh_diario

                    print("Datos de consumo obtenidos:", Kwh)
                
            except Exception as e:
                print("Error al ejecutar la consulta:", e)
                self.mostrar_notificacion()
            finally:
                cursor.close()
                connection.close()
        return Kwh

    def actualizar_variable(self, username):
        Kwh = self.Select_Datos_Consumo(username)
        return Kwh

    def initUI(self):

        buttonGuardar = QPushButton("Guardar gráfico")
        buttonRegresar = QPushButton("Regresar")

        self.vistaGrafico = QChartView(self.crearGraficoBarras())
        self.vistaGrafico.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.vistaGrafico.setRenderHint(QPainter.Antialiasing, True)

        disenioConfiguracion = QVBoxLayout()

        disenioConfiguracion.setSpacing(4)
        disenioConfiguracion.addStretch()
        disenioConfiguracion.addWidget(buttonGuardar)
        disenioConfiguracion.addWidget(buttonRegresar)
        baseDisenio = QGridLayout()
        baseDisenio.addLayout(disenioConfiguracion, 0, 0, 0, 1)
        baseDisenio.addWidget(self.vistaGrafico, 0, 1, 0, 4)
        baseDisenio.setSpacing(10)
        baseDisenio.setContentsMargins(10, 10, 10, 10)

        self.setLayout(baseDisenio)

        buttonGuardar.clicked.connect(self.Guardar)
        buttonRegresar.clicked.connect(self.Regresar)

    def crearGraficoBarras(self,*args):
        parser = argparse.ArgumentParser()
        parser.add_argument("--usuario", type=str, help="Nombre de usuario")
        args = parser.parse_args()

        if args.usuario:
            usuario = args.usuario
            print(f"Nombre de usuario recibido: {usuario}")

        Kwh = self.actualizar_variable(usuario)  # Utiliza el valor de usuario definido
  


        # Días de la semana
        paises = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Lista para almacenar los valores de Kwh
        valores = []

        colores = [Qt.blue, Qt.red, Qt.darkYellow, Qt.gray, Qt.black, Qt.darkCyan, Qt.darkMagenta]

         # Obtén el día actual de la semana (0 = lunes, 1 = martes, ..., 6 = domingo)
        #dia_actual = datetime.now().weekday()

        # Asegúrate de que Kwh tenga 7 elementos correspondientes a cada día de la semana
        if len(Kwh) != len(paises):
            raise ValueError("La lista Kwh no tiene datos para cada día de la semana.")
            

    # Reorganiza las listas paises y valores para comenzar desde el día actual
        #paises = paises[dia_actual:] + paises[:dia_actual]
        #Kwh = Kwh[dia_actual:] + Kwh[:dia_actual]

        print("Valores de la gráfica:", Kwh)  # Agregar esta línea para verificar los valores de la gráfica

        grafico = QChart()
        grafico.setMargins(QMargins(30, 30, 30, 30))
        grafico.setTheme(QChart.ChartThemeLight)
        grafico.setTitle("Consumo de energía por día de la semana")
        grafico.setAnimationOptions(QChart.SeriesAnimations)

        for i in range(len(paises)):
            series = QBarSeries()

            barSet = QBarSet(paises[i])
            barSet.setColor(colores[i])
            barSet.setLabelColor(Qt.yellow)
            barSet.append(Kwh[i])  # Agrega el valor correspondiente del día
            series.append(barSet)
            series.setLabelsVisible(True)
            series.setLabelsAngle(-90)
            series.setLabelsFormat("@value ")
            series.setLabelsPosition(QAbstractBarSeries.LabelsCenter)

            grafico.addSeries(series)

        axisX = QBarCategoryAxis()
        axisX.append(paises)

        grafico.createDefaultAxes()
        grafico.setAxisX(axisX, None)

        grafico.legend().setVisible(True)
        grafico.legend().setAlignment(Qt.AlignBottom)

        return grafico

    def mostrar_notificacion(self):
        
        notification.notify(
        title="Error en la conexion",
        message="Problema con la conexion en la Base de datos, intentelo otra vez"
        )
                
    def Regresar(self):
        ventana.close()
        
    def Guardar(self):
        nombre, extension = QFileDialog.getSaveFileName(self, "Guardar como",
                                                        "Gráfico de barras",
                                                        "JPG (*.jpg);;PNG (*.png)",
                                                        options=QFileDialog.Options())
                
        if nombre:
            guardar = QPixmap(self.vistaGrafico.grab())
            guardar.save(nombre, quality = 100)

            if guardar:
                QMessageBox.information(self, "Guardar gráfico", "Gráfico guardado con éxito.",
                                        QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Guardar gráfico", "Error al guardar el gráfico.",
                                     QMessageBox.Ok)
                

# ==================================================================           

if __name__ == "__main__":
    import sys

    aplicacion = QApplication(sys.argv)

    traductor = QTranslator(aplicacion)
    lugar = QLocale.system().name()
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    traductor.load("qtbase_%s" % lugar, path)
    aplicacion.installTranslator(traductor)

    fuente = QFont()
    fuente.setPointSize(10)
    aplicacion.setFont(fuente)

    ventana = QMainWindow()
    ventana.setWindowIcon(QIcon("LogoDefinitivo.jpg"))
    ventana.setWindowTitle("Grafica del dispositivo")
    ventana.setMinimumSize(900, 550)
        
    widget = graficoBarras()
    
    layoutPrincipal = QVBoxLayout()
    layoutPrincipal.addWidget(widget)
    
    centralWidget = QWidget()
    centralWidget.setLayout(layoutPrincipal)
    ventana.setCentralWidget(centralWidget)
    
    ventana.show()
    
    sys.exit(aplicacion.exec_())
