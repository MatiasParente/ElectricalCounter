# Electrical Counter

## Ganador del 1.er Premio Nacional en las Olimpíadas de Programación 2022 (Uruguay)
### Categoría Placas Programables

Proyecto final de graduación del Bachillerato Tecnológico EMT en Informática del Instituto Tecnológico Superior de Paysandú (ANEP).

Electrical Counter es un sistema IoT orientado a la monitorización, análisis y reducción del consumo eléctrico innecesario en hogares y pequeñas empresas.

---

# Vista del Proyecto

## Dispositivo IoT ensamblado

<img src="./Fotos del proyecto/Dispositivo ensamblado.png" width="600">

## Equipo de desarrollo

<img src="./Fotos del proyecto/Equipo.png" width="600">

---

# Estructura del repositorio

ElectricalCounter/

│

├── Base de datos/

│ └── Diagramas de base de datos utilizada

│

├── Cisco Packet Tracer empresa ficticia Electrical Counter/

│ ├── Archivo .pkt de la empresa ficticia

│ └── Documento de calculo de subredes

│

├── Dispositivo/

│ ├── Codigo del dispositivo

│ └── Diagrama del dispositivo

│

├── Documentación/

│ └── Documentación del proyecto

│

├── Electrical Counter (APP)/

│ └── Todo lo necesario para ejecutar la app

│

├── Fotos del proyecto/

│ └── Imagenes de la app, dispositivo y equipo

│

├── Servidor (Configuración)/

│ ├── Scripts del servidor

│ └── Explicación del servidor

│

└── Versiones anteriores/

  └── Archivos antiguos para ver el avance del proyecto realizado durante 2 años de bachillerato

---

# Objetivo

El objetivo del proyecto es desarrollar un sistema IoT capaz de monitorear y controlar el consumo eléctrico, permitiendo identificar desperdicios energéticos y optimizar el uso de la energía en hogares y pequeñas empresas.

---

# Descripción

Electrical Counter nace con el objetivo de combatir la problemática de la **energía parásita**, causada por dispositivos electrónicos que continúan consumiendo electricidad mientras permanecen conectados en modo standby.

El sistema permite:

- Medir variables eléctricas en tiempo real.
- Registrar históricos de consumo.
- Calcular costos aproximados según tarifas eléctricas.
- Controlar dispositivos remotamente.
- Analizar patrones de consumo.
- Detectar posibles desperdicios energéticos.

La solución integra hardware, comunicación IoT, servidor, base de datos y una aplicación multiplataforma.

---

# Arquitectura del Sistema

El proyecto está dividido en tres componentes principales:

```text

┌──────────────────────┐
│  Dispositivo IoT     │
│  ESP8266 + Sensores  │
│  + Relés             │
└──────────┬───────────┘
           │MQTT
           │
           ▼
┌──────────────────────┐
│ Servidor Ubuntu      │
│ MySQL                │
│ Mosquitto Broker     │
└──────────┬───────────┘
           │MySQLdb
           │
           ▼
┌──────────────────────┐
│ Aplicación Kivy      │
│ Python               │
└──────────────────────┘
```


---

# Hardware / Dispositivo IoT

El dispositivo físico es el encargado de recolectar información eléctrica y ejecutar acciones de control.

## Componentes utilizados

| Componente | Función |
|------------|---------|
| ESP8266 NodeMCU v3 | Microcontrolador principal con conexión WiFi |
| PZEM-004T v3.0 | Medición de voltaje, corriente, potencia y consumo energético |
| Módulo de 4 relés 5V | Control físico de dispositivos eléctricos |
| TXS0108E | Conversión de niveles lógicos entre 5V y 3.3V |

<img src="./Fotos del proyecto/dispositivo.png" width="600">

---

# Servidor e Infraestructura

El servidor centraliza la comunicación entre dispositivos, almacenamiento y procesamiento de información.

## Tecnologías utilizadas

- Ubuntu Server 22.04 LTS
- MySQL
- Mosquitto MQTT Broker
- Bash
- Cron

## Responsabilidades

- Recepción de mediciones enviadas por el dispositivo.
- Persistencia histórica de datos.
- Gestión de usuarios.
- Automatización de backups.
- Comunicación mediante protocolo MQTT.

---

# Aplicación Cliente

Aplicación multiplataforma desarrollada utilizando:

- Python 3.11
- Framework Kivy
- Biblioteca MySQLdb

Permite al usuario consultar información energética y controlar dispositivos conectados.

---

# Funcionalidades Principales

## Monitorización del consumo

Registro de:

- Voltaje (V)
- Corriente (A)
- Potencia eléctrica
- Energía consumida (kWh)

<img src="./Fotos del proyecto/pagin Graficas.png" width="600">

---

## Control remoto

Permite activar o desactivar dispositivos conectados mediante relés utilizando comunicación MQTT.

<img src="./Fotos del proyecto/pagina controles.png" width="600">

---

## Visualización de información

La aplicación muestra:

- Históricos de consumo.
- Gráficas estadísticas.
- Costos aproximados.
- Información energética relevante.

<img src="./Fotos del proyecto/pagina Inicio.png" width="600">

---

# Modelo de Base de Datos

El sistema utiliza una base de datos relacional compuesta principalmente por:

## Usuario

Almacena:

- Credenciales protegidas.
- Configuración del hogar.
- Información del plan eléctrico.

## Dato

Registra:

- Mediciones eléctricas.
- Fecha y hora.
- Valores obtenidos por el dispositivo IoT.

## Plan_UTE

Gestiona:

- Tarifas eléctricas.
- Cálculo aproximado del costo energético.

---

# Tecnologías utilizadas

## Hardware

- ESP8266
- PZEM-004T v3.0
- Relés 5V
- TXS0108E

## Comunicación

- MQTT
- Mosquitto Broker

## Backend / Infraestructura

- Ubuntu Server
- MySQL
- Bash
- Cron

## Aplicación

- Python 3.11
- Kivy
- MySQLdb

---

# Aprendizajes adquiridos

Durante el desarrollo del proyecto se trabajó con:

- Diseño de sistemas IoT completos.
- Comunicación entre dispositivos mediante MQTT.
- Integración hardware-software.
- Administración de servidores Linux.
- Diseño de bases de datos relacionales.
- Desarrollo de aplicaciones multiplataforma.
- Automatización de procesos.

---

# Reconocimiento

**1.er Premio Nacional - Olimpíadas de Programación 2022**

Categoría: **Placas Programables**

Uruguay

---

# Autores

Proyecto desarrollado por el equipo:

## SegundoBeJota - 3.º BB (2023)

- Santiago Szwec
- Cristian Vigo
- Lucio Romero
- Matías Parente

---

# Agradecimientos

Agradecimientos especiales a:

- Juan Pablo Villanueva por facilitar materiales físicos.
- Nancy López y Bruno Rodríguez por el acompañamiento durante el desarrollo del proyecto.

---

# Consideraciones legales

El desarrollo contempla principios de protección de datos personales establecidos en la Ley N.º 18.331 de la República Oriental del Uruguay.
