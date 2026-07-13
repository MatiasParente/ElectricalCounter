#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>
#include <PZEM004Tv30.h>
#include <SoftwareSerial.h>
#include <ESP8266Ping.h>

#if !defined(PZEM_RX_PIN) && !defined(PZEM_TX_PIN)
#define PZEM_RX_PIN 5 // D1 //se conecta al pin TX del modulo
#define PZEM_TX_PIN 4 // D2 //se conecta al pin RX del modulo
#endif
 

SoftwareSerial pzemSWSerial(PZEM_RX_PIN, PZEM_TX_PIN);
PZEM004Tv30 pzem(pzemSWSerial);

IPAddress staticIP(192, 168,144, 75); // Configura la dirección IP estática deseada
IPAddress gateway(192, 168, 144, 243);   // Reemplaza con la dirección de tu gateway/router
IPAddress subnet(255, 255, 255, 0);

const char* ssid = "Vigo";
const char* password = "55784877";
const char* mqttServer = "192.168.144.52";
const int mqttPort = 1883;                     
const char* mqttUser = "Dispositivo";
const char* mqttPassword = "12345";
const char* mqttTopic = "controlar_reles";
unsigned long tiempoAnterior = 0;
unsigned long TiempoActual;
const char* dispo = "1";
const unsigned long intervalo = 3600000;  // 1 hora en milisegundos
float KwhAcumulado = 0.0;

unsigned long tiempoAnterior2 = 0; 
const unsigned long intervalo2 = 1000;
unsigned long TiempoActual2;


IPAddress server_addr(192,168,144,52); 
char user[] = "dispo";               
char password_db[] = "Qwerty123#";   
char db[] = "Proyecto";  

WiFiClient espClient;
WiFiClient Client1;
PubSubClient client(espClient);
MySQL_Connection conn((Client *)&Client1);

int estadoBoton1 = LOW;
int estadoBoton2 = LOW;
int estadoBoton3 = 0;

bool estadoRele1 = false;
bool estadoRele2 = false;
bool estadoRele3 = false;


float Kwh;
float Amperios;
float Voltios;
float Potencia_actual;


const int relay1Pin = 0;  //D3    OUPUT
const int relay2Pin = 2;  //D4    OUPUT
const int relay3Pin = 14;  //D5   OUPUT

const int pinBoton1 = 13; //D7   INPUT
const int pinBoton2 = 12;//D6   INPUT
const int pinBoton3 = A0; //ADC0 INPUT





void setup() {
  Serial.begin(115200); //baudios (ciclos)
  WiFi.begin(ssid, password);
   WiFi.config(staticIP, gateway, subnet);


  pinMode(relay1Pin, OUTPUT);
  pinMode(relay2Pin, OUTPUT);
  pinMode(relay3Pin, OUTPUT);
  
  pinMode(pinBoton1, INPUT_PULLUP);
  pinMode(pinBoton2, INPUT_PULLUP);
  pinMode(pinBoton3, INPUT);
  
 estadoRele1 = false;
 estadoRele2 = false;
 estadoRele3 = false;

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  Serial.println("Connecting to database...");

  if (conn.connect(server_addr, 3306, user, password_db, db)) {
    Serial.println("Connected to database server.");
  } else {
    Serial.println("Connection failed.");
    while (1);
  }

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback); //siempre lo mantiene conectado al servicio mqtt
  
  while (!client.connected()) {
    Serial.println("Conectando al servidor MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword)) {
      Serial.println("Conectado al servidor MQTT");
      client.subscribe(mqttTopic);
    } else  {
      Serial.print("Error al conectar al servidor MQTT - Estado: ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  
  

}

void loop() {
  if (!client.connected()) {
    reconnect_MQTT();
  }
 if (!conn.connected()) {
    reconnect_Mysql();
  }
  publishRelayStates();
 client.loop(); //premite que callback funcione en cada ciclo

 TiempoActual = millis();
 if (TiempoActual - tiempoAnterior >= intervalo ) {
 evnioMysql();
  
}

Botones();

 TiempoActual2 = millis();

if (TiempoActual2 - tiempoAnterior2 >= intervalo2 ) {

    
Voltios = pzem.voltage();
Amperios = pzem.current();
   
 Potencia_actual += pzem.power();
  KwhAcumulado += (Potencia_actual * 0.001);
  Kwh = KwhAcumulado;

 tiempoAnterior2 = TiempoActual2;

}
  
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Comando recibido en el topic: ");
  Serial.println(topic);

  Serial.print("Mensaje: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

   if (strcmp(topic, mqttTopic) == 0) {
    if ((char)payload[0] == '1') {
      digitalWrite(relay1Pin, HIGH);  
      Serial.println("Relay 1 Encendido");
      estadoRele1 = true;

    } else if ((char)payload[0] == '0') {
      digitalWrite(relay1Pin, LOW);   
      Serial.println("Relay 1 Apagado");
       estadoRele1 = false;

    } 
     if ((char)payload[1] == '1') {
      digitalWrite(relay2Pin, HIGH);  
      Serial.println("Relay 2 Encendido");
       estadoRele2 = true;

    } else if ((char)payload[1] == '0') {
      digitalWrite(relay2Pin, LOW);   
      Serial.println("Relay 2 Apagado");
       estadoRele2 = false;

    } 
     if ((char)payload[2] == '1') {
      digitalWrite(relay3Pin, HIGH); 
      Serial.println("Relay 3 Encendido");
       estadoRele3 = true;

    } else if ((char)payload[2] == '0') {
      digitalWrite(relay3Pin, LOW);   
      Serial.println("Relay 3 Apagado");
       estadoRele3 = false;

    }
  }
}
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  void Botones(){
 // Lee el estado de los botones
  estadoBoton1 = digitalRead(pinBoton1);
  estadoBoton2 = digitalRead(pinBoton2);
  estadoBoton3 = digitalRead(pinBoton3);
  int lecturaBoton3 = analogRead(pinBoton3); 
  Serial.println(lecturaBoton3);

  // Si se presiona un botón, cambia el estado del relé correspondiente
  if (estadoBoton1 == LOW) {
    
    while (!digitalRead(pinBoton1)) {
      delay(100);
    }
    estadoRele1 = !estadoRele1;

    digitalWrite(relay1Pin, !digitalRead(relay1Pin));
    delay(50);  // Debounce

    
  }
  if (estadoBoton2 == LOW) {
     while (!digitalRead(pinBoton2)) {
      delay(100);
    }
     estadoRele2 = !estadoRele2;
    digitalWrite(relay2Pin, !digitalRead(relay2Pin));
    delay(50);  // Debounce

    
  }
 //Utiliza el valor analógico del botón 3 para determinar si se debe cambiar el estado del relé 3
if (lecturaBoton3 > 10) {
  delay(10);
  estadoRele3 = !estadoRele3;
  digitalWrite(relay3Pin, !digitalRead(relay3Pin));
  delay(50);  // Debounce
  }

  }

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  


void reconnect_MQTT() {
  while (!client.connected()) {
    Serial.println("Intentando reconexión MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword)) {
      Serial.println("Reconectado al servidor MQTT");
      client.subscribe(mqttTopic);
    } else {
      Serial.print("Error al reconectar al servidor MQTT - Estado: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  delay(100);
}

void reconnect_Mysql() {
 while (!conn.connected()) {
    Serial.println("Intentando reconexión Mysql...");
    if (conn.connect(server_addr, 3306, user, password_db, db)) {
    Serial.println("Connected to database server.");
    } else {
    Serial.println("Connection failed.");
    }
  }
  delay(100);

}
/////////////////////////////////////////////////////////////////////////////////////////////////////////

void publishRelayStates() {
  // Obtener el estado actual de los relés
  String relayStateMessage = String(estadoRele1) + String(estadoRele2) + String(estadoRele3);

  // Publicar el estado de los relés en el topic "estado_relés"
  client.publish("estado_reles", relayStateMessage.c_str());

  delay(500);
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

void evnioMysql() {




   if (Voltios >= 0.0) {
 
  } else {
    Voltios = 0;
  }

  if (Amperios >= 0.0) {
 
  } else {
    Amperios = 0;
  }
 if (Kwh >= 0.0) {
 
  } else {
    Kwh = 0;
  }



    char INSERT_SQL[200];
sprintf(INSERT_SQL,"INSERT INTO Dato (Kwh, Amperio, Voltio, Fecha, Reles1, Reles2, Reles3, UsuarioDispo) VALUES (%f, %.2f, %.2f, NOW(), %d, %d, %d, '%s')", Kwh, Amperios, Voltios, estadoRele1, estadoRele2, estadoRele3, dispo);   
 Serial.println("Executing INSERT...");
    MySQL_Cursor *cur_mem1 = new MySQL_Cursor(&conn);
    cur_mem1->execute(INSERT_SQL);
    delete cur_mem1;
    Serial.println("INSERT executed.");

    tiempoAnterior = TiempoActual;
    KwhAcumulado = 0.0;


}

///////////////////////////////////////////////////////////////////////////

